import os

import PIL
from PIL import Image
from flask import current_app

from app import avatars


def create_thumbnail(image):
    file_name, ext = os.path.splitext(image)
    base_width = 30
    img = Image.open(avatars.path(image))
    new_file_name = file_name + '_t' + ext
    if img.size[0] > 30:
        # 计算缩小百分比
        percent = (base_width / img.size[0])
        # 缩小后的高度
        height = int(img.size[1] * percent)
        img = img.resize((base_width, height), PIL.Image.ANTIALIAS)
    img.save(os.path.join(
        current_app.config['UPLOADED_AVATARS_DEST'], new_file_name
    ))
    return new_file_name
