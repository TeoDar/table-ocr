import os
from io import BytesIO
from hashlib import md5

import numpy as np
from PIL import Image

from pdf2image import convert_from_bytes

supported_filetypes = ('pdf', 'png')


def extraction_images(file: bytes, filename: str) -> list:
    """Возвращает массив пикселей полученной страницы"""
    # Провера типа файла
    filetype: str = filename[-3:].lower()
    if filetype not in supported_filetypes:
        return None
    elif filetype == 'png':
        return [np.array(Image.open(BytesIO(file)))]
    else:
        images = []
        pages = convert_from_bytes(file, poppler_path='D:/Program Files/poppler-0.68.0/bin')
        for page in pages:
            images.append(np.array(page))
        return images


def save_images_from_bytes(path: str, images: list):
    # Проверка на существование папки для сохранения
    os.makedirs(os.path.dirname(path), exist_ok=True)
    imgs_md5 = []
    for img in images:
        img_md5 = md5(img).hexdigest()
        imgs_md5.append(img_md5)
        file_path = f'{path}{img_md5}.png'
        img = Image.fromarray(img)
        img.save(file_path, bits=1, optimize=True)
        print(f'[IMAGE SAVED]   {file_path}')
    return imgs_md5


def test():
    test_path = 'C:/PROJECTS/ocr/Other/KAH/'
    if not os.path.exists(f'{test_path}'): os.makedirs(f'{test_path}')
    test_file = '21-4504-021.pdf'
    with open(test_path + test_file, 'rb') as png:
        images = extraction_images(file=png.read(), filename=test_file)
        save_images_from_bytes('C:/PROJECTS/ocr/App/', images)


if __name__ == "__main__":
    test()