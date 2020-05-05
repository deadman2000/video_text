import os
import pytube
import cv2

video_dir = './download'


def download_video(video_id):
    file_name = video_id + '.mp4'
    path = video_dir + '/' + file_name
    if os.path.isfile(path):
        return path

    video_url = 'https://www.youtube.com/watch?v=%s' % video_id
    print('Downloading %s' % video_url)
    youtube = pytube.YouTube(video_url)
    video = youtube.streams.first()
    return video.download(video_dir, video_id)


def get_frame(video_id, time):
    path = download_video(video_id)
    vidcap = cv2.VideoCapture(path)
    vidcap.set(cv2.CAP_PROP_POS_MSEC, (time * 1000))
    success, image = vidcap.read()
    if not success:
        return None
    return image

if __name__ == '__main__':
    print(download_video('4edj5UJvfIc'))
