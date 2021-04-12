from PIL import Image, ImageDraw, ImageFont
import os
import cv2
import numpy as np
from skimage import measure
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import randint, uniform
from string import ascii_uppercase, ascii_lowercase, digits

os.system("mkdir -p data")

all_char = digits+ascii_uppercase
myfonts = [
    ImageFont.truetype(font="./font/"+i, size=80)
    for i in os.listdir("./font/")
]

f_ind = 1
for char in all_char:
    print(char)
    for ind in range(1000):
        out = Image.new("RGB", (100, 100), (255, 255, 255))
        font = myfonts[randint(0, len(myfonts)-1)]
        d = ImageDraw.Draw(out)
        d.text((20, 0), char, font=font, fill=(0, 0, 0))
        out = out.rotate(uniform(-5, 5))
        out.save("_.png")

        image = cv2.imread("_.png")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

        cnts, new = cv2.findContours(
            thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
        new_image = cv2.drawContours(image, cnts, -1, (0, 255, 0), 1)
        captcha = np.invert(thresh)
        labelled_captcha = measure.label(captcha)

        character_dimensions = (
            0.1*captcha.shape[0], 0.99*captcha.shape[0],
            0.1*captcha.shape[1], 0.99*captcha.shape[1]
        )
        min_height, max_height, min_width, max_width = character_dimensions
        snip = None

        for regions in regionprops(labelled_captcha):
            y0, x0, y1, x1 = regions.bbox
            region_height = y1 - y0
            region_width = x1 - x0

            if region_height > min_height and region_height < max_height and region_width > min_width and region_width < max_width:
                snip = captcha[y0:y1, x0:x1]

        x_p, y_p = 5, 5
        img = cv2.copyMakeBorder(snip, x_p, x_p, y_p, y_p, cv2.BORDER_CONSTANT)
        img = cv2.resize(img, (50, 50))

        os.system(str("mkdir -p ./data/"+"Sample"+str(f_ind).zfill(3)))
        cv2.imwrite("./data/"+"Sample"+str(f_ind).zfill(3)+"/"+char+"_"+str(ind)+".png", img)
    f_ind+=1