import cv2
import pytesseract
import numpy as np
import re


def unsharp(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    """Return a sharpened version of the image, using an unsharp mask."""
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened

def thresh(image):
    return cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)[1]

def gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def scale(factor, image):
    return cv2.resize(image, None, fx=factor, fy=factor, interpolation=cv2.INTER_CUBIC) # INTER_CUBIC INTER_LINEAR INTER_NEAREST

def blur(image):
    return cv2.medianBlur(image, 3)

def extract_text(image):
    return pytesseract.image_to_string(image)

reg = re.compile('[^A-Za-z0-9!?\.\-,'' ]+')

def process_text(txt):
    lines = txt.split('\n')
    lines = [reg.sub('', l.replace('|', 'I')).strip() for l in lines]
    txt = ' '.join(lines)
    return txt.strip()

def image_filter(im, ps):
    for p in ps.split(':'):
        if len(p) == 0: continue
        if p.startswith('h_'):
            target_height = int(p[2:])
            h = im.shape[0]
            w = im.shape[1]
            scale = target_height / h
            im = cv2.resize(im, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        elif p.startswith('*'):
            scale = int(p[1:])
            im = cv2.resize(im, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        elif p == 'gray':
            im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        elif p == 'unsharp':
            im = unsharp(im)
        elif p == 'thresh':
            im = cv2.threshold(im, 150, 255, cv2.THRESH_BINARY)[1]
        elif p == 'blur':
            im = cv2.medianBlur(im, 3)
    return im

def estimate(im, ps):
    return process_text(extract_text(image_filter(im, ps)))
