import requests
import uuid
import time
import os, os.path

from extract import unsharp, thresh, gray, scale, blur, process_text, extract_text
import download

class VideoProcessor:
    def __init__(self):
        prefix = os.environ.get('PREFIX', 'proc')
        self.runner_id = prefix + '-' + str(uuid.uuid4())[:8]
        self.url = os.environ.get('SERVER', 'http://localhost:5000')

    def get_task(self):
        r = requests.get(self.url + '/api/videotasks', params={'runner': self.runner_id})
        if len(r.content) == 0:
            return None
        return r.json()
    
    def process_task(self, task):
        if task['type'] == 'INFO_REQUEST':
            self.info_request(task)
        elif task['type'] == 'GET_TEXT':
            self.get_text(task)
        pass
    
    def info_request(self, task):
        frames, fps = download.info(task['videoId'])
        requests.post(self.url + '/api/videotasks/info', json={
            'taskId': task['id'],
            'runner': self.runner_id,
            'frames': frames,
            'fps': fps
        })

    def get_text(self, task):
        texts = []
        frames, fps = download.info(task['videoId'])
        frame = task['frame']
        count = task['count']
        skip = task['frameSkip']
        
        for i in range(frame, frame+count*skip, skip):
            print(task['videoId'], i)
            image = download.get_frame_num(task['videoId'], i)
            text = process_text(extract_text(unsharp(scale(6, gray(image)))))
            if text.strip():
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
                os.remove(os.path.join(root, file))
        pass

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
                time.sleep(10)


if __name__ == '__main__':
    VideoProcessor().run()
