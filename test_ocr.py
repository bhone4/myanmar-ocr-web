import easyocr
import cv2
from PIL import Image
import numpy as np

print('Loading Myanmar OCR...(1-2 minutes)')

reader = easyocr.Reader(['my','en'],gpu=False) #Myanmar + Englich
print('OCR Ready!')

def extract_text_from_image(image_path):
    """Extract Myanmar text from image"""
    img = cv2.imread(image_path) #Read image
    img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #Convert to RGB
    print('Reading text...')
    result = reader.readtext(img_rgb)
    print('Extracted Text:')
    print('-'*50)

    extract_text = []
    for detection in result:
        text = detection[1]
        confidence = detection[2]
        print(f'{text} (Confidence: {confidence:.2f})')

    print('-'*50)
    return extract_text

if __name__ == "__main__":
    print('Myanmar OCR Test Program')
    print('-'*50)

    #Test with an image
    image_path = input('Enter image path (or drag image here):').strip('"')
    if image_path:
        texts = extract_text_from_image(image_path)

        with open('output.txt','w',encoding='utf-8') as f:
            f.write(''.join(texts))

            print('Text saved to output.txt')
    else:
        print('No image provided')        
        

