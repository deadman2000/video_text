import cv2
import pytesseract

import download
from matching import find_match
from extract import unsharp_mask


def estimate(video_id, frame, unsharp, gray, target_width, tesseract_conf, resource, line, invert):
    im = download.get_frame(video_id, frame)

    if invert:
        im = cv2.bitwise_not(im)

    if unsharp:
        im = unsharp_mask(im)

    if gray:
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    if target_width is not None:
        h = im.shape[0]
        w = im.shape[1]
        scale = target_width // w
        im = cv2.resize(im, None, fx=scale, fy=scale)

    txt = pytesseract.image_to_string(im, config=tesseract_conf)

    matches = find_match(txt)
    if matches is None:
        return 0

    for m in matches:
        if m['resource'] == resource and m['line'] == line:
            return m['score']
    return 0
