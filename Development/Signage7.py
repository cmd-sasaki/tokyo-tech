from tkinter import *
from PIL import Image, ImageTk

import testadc

root = Tk()
root.title('Raspberry Pi Seminar')
root.attributes('-fullscreen', True)

canvas = Canvas(root)
canvas.pack(anchor=NW, fill=BOTH, expand=YES)

imgArray = ['DayTime/1.png', 'DayTime/2.png']
imgArrayNight = ['NightTime/1.png', 'NightTime/2.png']
imgIndex = 0


def update_image():
    global photo, imgIndex

    canvas.update()

    if len(imgArray) <= imgIndex:
        imgIndex = 0

    gpioval = adc.readSensor()

    if gpioval > 3000:
        img = Image.open(imgArray[imgIndex])
    else:
        img = Image.open(imgArrayNight[imgIndex])

    img_w, img_h = img.size

    win_w = root.winfo_width()
    win_h = root.winfo_height()

    ratio = win_w / img_w

    img = img.resize((win_w, int(img_h * ratio)))

    photo = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, image=photo, anchor=NW)

    imgIndex = imgIndex + 1

    root.after(1000, update_image)

try:
    adc = testadc.TestReadAdc()
    adc.open()

    update_image()

except KeyboardInterrupt:
    print('keyinterrupt')
    adc.close()
