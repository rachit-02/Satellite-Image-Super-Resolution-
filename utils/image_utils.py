import cv2
import os


def generate_lr_image(hr_img, scale):
    """
    Downsample HR image to LR using bicubic interpolation
    """
    h, w = hr_img.shape[:2]
    lr_img = cv2.resize(hr_img, (w // scale, h // scale), interpolation=cv2.INTER_CUBIC)
    return lr_img


def save_image(path, image):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cv2.imwrite(path, image)