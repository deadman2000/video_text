import os
from yt_dlp import YoutubeDL
import cv2

video_dir = 'download'


def download_video(video_id):
    path = video_dir + '/' + video_id + '.mp4'
    if os.path.isfile(path):
        return path
    
    ydl_opts = {
        'format': 'mp4',
        'restrictfilenames': True,
        'outtmpl': '%(id)s.%(ext)s',
        'paths': {'home': video_dir},
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download('https://www.youtube.com/watch?v=%s' % video_id)

    return path


def get_frame(video_id, time):
    path = download_video(video_id)
    vidcap = cv2.VideoCapture(path)
    vidcap.set(cv2.CAP_PROP_POS_MSEC, (time * 1000))
    success, image = vidcap.read()
    if not success:
        return None
    return image


def info(video_id):
    path = download_video(video_id)
    vidcap = cv2.VideoCapture(path)
    return (int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)), vidcap.get(cv2.CAP_PROP_FPS))


def get_frame_num(video_id, frame):
    path = download_video(video_id)
    vidcap = cv2.VideoCapture(path)
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame)
    success, image = vidcap.read()
    if not success:
        return None
    return image
