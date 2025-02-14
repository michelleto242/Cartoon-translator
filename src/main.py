print("HELLO") 
from MT.interactive.py import translator 
from OCR.detector.py import detect_text_from_byte
from PargraphGenerating.insert_text import remover, inpainting
from PargraphGenerating.combine_images import PreProcessByteImages
from crawler import byteImgDownload
import os 
import numpy as np
import cv2
import matplotlib.pylab as plt

def main(url):
    cwd = os.getcwd()
    ckpt_path = os.path.join(cwd, 'MT/ckpt/checkpoint77.pt')
    vocab_path = os.path.join(cwd, 'MT/wiki.ko.model')
    data_path = os.path.join(cwd, 'MT/')
    font_path = os.path.join(cwd, 'PargraphGenerating/font/KOMIKHI_.ttf')
    
    byteImgs = byteImgDownload(url)
    print("Crawling complete!")
    combinedByteImg = byteImgs
    json_files = [detect_text_from_byte(img) for img in byteImgs]
    print("OCR complete")
    images = [cv2.imdecode(np.frombuffer(img, dtype=np.uint8), -1) for img in byteImgs]
    images = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in images]

    # remove text and insert translated text
    Contents, Paragraphs = remover(images, json_files, discriminative_power = 0.55, autotune=True)
    # remove text
    translated = translator(Paragraphs, ckpt_path, vocab_path, data_path)
    # Generate text inserted image in list
    
    images = inpainting(Contents, translated, font_path)
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    for i, img in enumerate(images):
        img.original_image.save('tmp/{}.jpg'.format(i))


if __name__ == "__main__":
    import sys 
    url = sys.argv[1]
    main(url)
    print("END")
