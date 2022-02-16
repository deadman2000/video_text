import cv2
import pytesseract
import numpy as np


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


def preprocess_image(im):
    im = unsharp(im)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)  # В оттенки серого
    h, w = im.shape
    scale = 1920 // w
    im = cv2.resize(im, None, fx=scale, fy=scale)
    # im = cv2.medianBlur(im, 3)
    return im


def extract_text(im):
    # data = pytesseract.image_to_data(im, config='--psm 4', output_type=pytesseract.Output.DICT)
    # count = len(data['text'])
    # for i in range(count):
    #     v = dict()
    #     for k in data.keys():
    #         v[k] = data[k][i]
    #     print(v)

    return pytesseract.image_to_string(im, config='--psm 4')
