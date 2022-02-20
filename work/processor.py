import requests
import uuid
import time
import os, os.path
from datetime import datetime

from extract import unsharp, thresh, gray, scale, blur, process_text, extract_text
import download

class VideoProcessor:
    def __init__(self):
        prefix = os.environ.get('PREFIX', 'proc')
        self.runner_id = prefix + '-' + str(uuid.uuid4())[:8]
        self.url = os.environ.get('SERVER', 'http://localhost:5000')

    def get_task(self):
        while True:
            try:
                r = requests.get(self.url + '/api/videotasks', params={'runner': self.runner_id})
                if len(r.content) == 0:
                    return None
                return r.json()
            except:
                time.sleep(10)
    
    def process_task(self, task):
        if task['type'] == 'INFO_REQUEST':
            self.info_request(task)
        elif task['type'] == 'GET_TEXT':
            self.get_text(task)
        pass
    
    def info_request(self, task):
        frames, fps = download.info(task['videoId'])
        while True:
            try:
                requests.post(self.url + '/api/videotasks/info', json={
                    'taskId': task['id'],
                    'runner': self.runner_id,
                    'frames': frames,
                    'fps': fps
                })
            except:
                time.sleep(10)

    def get_text(self, task):
        texts = []
        frames, fps = download.info(task['videoId'])
        frame = task['frame']
        count = task['count']
        skip = task['frameSkip']
        
        for i in range(frame, frame+count*skip, skip):
            print(task['videoId'], i)
            image = download.get_frame_num(task['videoId'], i)
            if image is None:
                break
            text = process_text(extract_text(unsharp(scale(6, gray(image)))))
            if text:
                texts.append({'frame': i, 'text': text, 't': int(i / fps)})

        while True:
            try:
                requests.post(self.url + '/api/videotasks/texts', json={
                    'taskId': task['id'],
                    'runner': self.runner_id,
                    'texts': texts
                })
                break;
            except:
                time.sleep(10)
                
    def cleanup(self):
        for root, dirs, files in os.walk('download'):
            for file in files:
                path = os.path.join(root, file)
                atime = time.ctime(os.stat(path).st_atime)
                diff = datetime.now() - datetime.strptime(atime, "%a %b %d %H:%M:%S %Y")
                days = diff.total_seconds()/60/60/24
                if days > 2:
                    os.remove(path)

    def run(self):
        while True:
            try:
                task = self.get_task()
                if task is not None:
                    self.process_task(task)
                else:
                    self.cleanup()
                    time.sleep(10)
            except Exception as e:
                print(e)
                time.sleep(10)


if __name__ == '__main__':
    VideoProcessor().run()
