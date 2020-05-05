import time
import cv2
import re
import os
import os.path
import pytube
import traceback

from matching import find_match
from extract import preprocess_image, extract_text
from mongodb import client

__version__ = '1.1'


strings = client.Translate.Strings
videos = client.Translate.Videos

reg = re.compile('[^A-Za-z0-9!?\.\-,'' ]+')


def process_text(txt):
    lines = txt.split('\n')
    lines = [reg.sub('', l) for l in lines]
    txt = ' '.join(lines)
    return txt


class VideoProcessor:
    def __init__(self, video):
        self.game = video['Game']
        self.video_id = video['VideoId']
        self.mongoRec = video
        self.frame_dir = os.environ.get('FRAMES_DIR', './frames') + '/' + self.video_id
        self.download_dir = os.environ.get('DOWNLOAD_DIR', './download')
        self.file = None

    def apply_matching(self, match, seconds):
        res = strings.find_one({
            'Res': match['resource'],
            'Index': match['line'],
            'Game': self.game
        })
        if res is None:
            print('No game res %s %d' % (match['resource'], match['line']))
            return False

        if 'Videos' not in res or res['Videos'] is None or len(res['Videos']) == 0:  # У ресурса еще нет ни одного видео
            strings.update_one({'_id': res['_id']}, {'$set': {'Videos': [self.video_rec(match, seconds)]}})
            return True

        res_videos = res['Videos']
        for v in res_videos:
            if v['video_id'] == self.video_id and v['score'] >= match['score']:
                print('Video exists')
                return False
            if match['score'] < v['score'] / 2:  # Пропускаем плохие соответствия
                print('Score small')
                return False

        min_score = match['score'] / 2
        res_videos = [v for v in res_videos if v['score'] > min_score]  # Отфильтровываем худшие совпадения
        res_videos = [v for v in res_videos if v['video_id'] != self.video_id]  # Отфильтровываем повторения
        res_videos.append(self.video_rec(match, seconds))
        res_videos.sort(key=lambda v: v['score'], reverse=True)
        res_videos = res_videos[:4]  # Ограничиваем размер массива

        strings.update_one({'_id': res['_id']}, {'$set': {'Videos': res_videos}})

        return True

    def video_rec(self, match, seconds):
        return {
            'video_id': self.video_id,
            'time': seconds,
            'score': match['score'],
            'txt': match['rec'],
            'url': 'https://www.youtube.com/watch?v=' + self.video_id + '&t=' + str(seconds)
        }

    def process_image(self, image, seconds):
        im = preprocess_image(image)
        text = extract_text(im)
        text = process_text(text)

        print(seconds)
        print(text)
        matches = find_match(text)
        if matches is not None:
            for m in matches:
                self.apply_matching(m, seconds)

        print()
        print("inv")
        img_inv = cv2.bitwise_not(im)
        inv_text = extract_text(img_inv)
        inv_text = process_text(inv_text)
        print(inv_text)
        matches = find_match(inv_text)
        if matches is not None:
            for m in matches:
                self.apply_matching(m, seconds)

        self.save_frame(seconds, image)

    def process_video(self):
        os.makedirs(self.frame_dir, exist_ok=True)

        if 'File' in self.mongoRec and os.path.isfile(self.mongoRec['File']):
            self.file = self.mongoRec['File']
        else:
            self.file = self.download_video()
            videos.update_one({'_id': self.mongoRec['_id']}, {'$set': {'File': self.file}})

        vidcap = cv2.VideoCapture(self.file)
        if 'Completed' in self.mongoRec:
            if self.mongoRec['Completed'] is None:
                count = 0
            else:
                count = self.mongoRec['Completed'] + 1
        else:
            count = 0

        fps = vidcap.get(cv2.CAP_PROP_FPS)
        total_frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
        total = int(total_frames // fps)
        videos.update_one({'_id': self.mongoRec['_id']}, {'$set': {'Total': total}})

        while True:
            vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))

            success, image = vidcap.read()
            if not success:
                break

            self.process_image(image, count)

            if (count % 60) == 0:
                videos.update_one({'_id': self.mongoRec['_id']}, {'$set': {'Completed': count}})

            count += 1

        print('%s completed' % self.video_id)
        videos.update_one({'_id': self.mongoRec['_id']}, {'$set': {'Finished': True, 'InProcess': False}})

    def download_video(self):
        print("Downloading...")
        video_url = 'https://www.youtube.com/watch?v=' + self.video_id
        youtube = pytube.YouTube(video_url)
        v = youtube.streams.first()
        path = v.download(self.download_dir)
        print("Downloaded to %s" % path)
        return path

    def save_frame(self, seconds, image):
        path = "%s/%d.png" % (self.frame_dir, seconds)
        print('saving frame to %s' % path)
        cv2.imwrite(path, image)
        pass


if __name__ == '__main__':
    print("Video processing v.%s" % __version__)
    while True:
        video = videos.find_one_and_update({'InProcess': False, 'Finished': False}, {'$set': {'InProcess': True}})
        if video is None:
            print('Wait 5 min')
            time.sleep(5*60)  # Раз в 5 минут проверяем новые запросы
            continue

        try:
            processor = VideoProcessor(video)
            processor.process_video()
        except Exception as err:
            print(traceback.format_exc())
            videos.update_one({'_id': video['_id']}, {'$set': {'Err': traceback.format_exc()}})
        finally:
            videos.update_one({'_id': video['_id']}, {'$set': {'InProcess': False}})
