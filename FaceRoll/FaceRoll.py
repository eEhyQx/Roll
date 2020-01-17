# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import time
import json
import cv2
import os
import numpy as np
import random

key='Find in readme.md'
secret='Find in readme.md'

def saveFace(key,secret,img_path,temp_path='./temp.jpg'):
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    key = "DPHaK7dG2sab8F3SW9aSrt2gP21-JSyk"
    secret = "wRN-HPj4sbExcfmg0a8n9dPWcB2juJjE"
    orginal_img=cv2.imread(img_path)
    cv2.imwrite(temp_path,cv2.resize(orginal_img,None,fx=0.5,fy=0.5,interpolation=cv2.INTER_CUBIC))
    filepath = temp_path

    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(key)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(secret)
    data.append('--%s' % boundary)
    fr = open(filepath, 'rb')
    data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    data.append(fr.read())
    fr.close()
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_landmark')
    data.append('1')
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
    data.append(
        "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus")
    data.append('--%s--\r\n' % boundary)

    for i, d in enumerate(data):
        if isinstance(d, str):
            data[i] = d.encode('utf-8')

    http_body = b'\r\n'.join(data)

    # build http request
    req = urllib.request.Request(url=http_url, data=http_body)

    # header
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)

    try:
        # post data to server
        resp = urllib.request.urlopen(req, timeout=5)
        # get response
        qrcont = resp.read()
        # if you want to load as json, you should decode first,
        # for example: json.loads(qrount.decode('utf-8'))
        #print(qrcont.decode('utf-8'))
        qrcont=json.loads(qrcont.decode('utf-8'))
        face_num=len(qrcont['faces'])
        faces_dict=[]
        for i in range(face_num):
            face_rectangle=qrcont['faces'][i]['face_rectangle']
            crap=orginal_img[face_rectangle['top']*2:(face_rectangle['top']+face_rectangle['height'])*2-1,face_rectangle['left']*2:(face_rectangle['left']+face_rectangle['width'])*2-1]
            faces_dict.append(crap)
            #print('added a face at:'+str(qrcont['faces'][i]['face_rectangle']))
        os.remove(temp_path)
        return face_num,faces_dict
    except urllib.error.HTTPError as e:
        print(e.read().decode('utf-8'))

def getImgs(key,secret,dir_path):
    faces_dict=[]
    for root, dirs, files in os.walk(dir_path):
        f=[ dir_path+i for i in files if i[-3:]=='jpg' or i[-3:]=='JPG' or i[-3:]=='png' or i[-3:]=='PNG']
    print("totally has "+str(len(f))+" pics.")
    total_num=0
    print('let me see...')
    for i in f:
        tmp=saveFace(key,secret,i)
        faces_dict.extend(tmp[1])
        total_num+=tmp[0]
    print('totally has '+str(total_num)+' faces.')
    return total_num,faces_dict


temp=getImgs(key,secret,'./samples/')
for i in range(temp[0]):
    temp[1][i]=cv2.resize(temp[1][i],(500,500))
while 1:
    i=random.randint(0,temp[0]-1)
    try:
        cv2.imshow('face',temp[1][i])
        cv2.moveWindow('face',600,200)
    except:
        pass
    if cv2.waitKey(10) == ord('s'):
        break

cv2.waitKey(0)
cv2.destroyAllWindows()
