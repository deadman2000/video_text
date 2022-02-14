import os
from yt_dlp import YoutubeDL
import cv2

video_dir = 'download'


def download_video(video_id):
    ydl_opts = {
        'format': 'mp4',
        'restrictfilenames': True,
        'outtmpl': '%(id)s.%(ext)s',
        'paths': {'home': video_dir},
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download('https://www.youtube.com/watch?v=%s' % video_id)

    file_name = video_id + '.mp4'
    path = video_dir + '/' + file_name
    return path


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
