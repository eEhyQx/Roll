import cv2
from  random import randint

def roll(img_path):
    img=cv2.imread(img_path)
    h,w=img.shape[0],img.shape[1]

    luckyman=randint(270,h)
    cv2.line(img,(0,luckyman),(w,luckyman),(0,255,0),10)
    top=luckyman-100 if luckyman-100>270 else 270
    bottom=luckyman+100 if luckyman+100<h-83 else h-83
    img=img[top:bottom][:]

    cv2.imshow('img',img)
    cv2.waitKey(0)

#T-Shirt 1
roll('TShirt.jpg')
#T-Shirt 2
roll('TShirt.jpg')
#For Free!!!
roll('ForFree.jpg')

