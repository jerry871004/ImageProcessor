import math
import cv2
import os
import numpy as np
import xml.etree.ElementTree as ET

img_dir = r"C:\Users\wei\Desktop\test\img"
xml_dir = r"C:\Users\wei\Desktop\test\xml"
result = r".\result"
angle = [0,-90,-180,-270]

def write_xml(path,file_name,n_xmin,n_ymin,n_xmax,n_ymax,angle_str):
    tree = ET.parse(path)
    root = tree.getroot()
    for i,bndbox in enumerate(root.iter("bndbox")):
        # print(i,bndbox.find("xmin").text)
        bndbox.find("xmin").text = str(n_xmin[i])
        bndbox.find("ymin").text = str(n_ymin[i])
        bndbox.find("xmax").text = str(n_xmax[i])
        bndbox.find("ymax").text = str(n_ymax[i])
    tree.write(os.path.join(result +'/'+angle_str+file_name.split('.')[0]+'.xml'))

def rotate_point(x,y,n_center,center,angle):
    n_xmin = []
    n_ymin = []
    n_xmax = []
    n_ymax = []
    tmp_angle = (angle*math.pi)/180
    tmp_x = [[0]*4 for i in range(len(x))]
    tmp_y = [[0]*4 for i in range(len(y))]
    # print(tmp_x)
    for i in range(len(x)):
        (tmp_x1,tmp_y1) = (x[i][0]-center[0],y[i][0]-center[1])
        (tmp_x2,tmp_y2) = (x[i][1]-center[0],y[i][1]-center[1])
        (tmp_x3,tmp_y3) = (x[i][2]-center[0],y[i][2]-center[1])
        (tmp_x4,tmp_y4) = (x[i][3]-center[0],y[i][3]-center[1])
        tmp_x[i][0] = int(tmp_x1*math.cos(tmp_angle)+tmp_y1*math.sin(tmp_angle)+n_center[0]) if int(tmp_x1*math.cos(tmp_angle)+tmp_y1*math.sin(tmp_angle)+n_center[0])>0 else 1
        tmp_y[i][0] = int(math.fabs(n_center[1]-tmp_x1*math.sin(tmp_angle)+tmp_y1*math.cos(tmp_angle))) if int(math.fabs(n_center[1]-tmp_x1*math.sin(tmp_angle)+tmp_y1*math.cos(tmp_angle)))>0 else 1
        tmp_x[i][1] = int(tmp_x2*math.cos(tmp_angle)+tmp_y2*math.sin(tmp_angle)+n_center[0]) if int(tmp_x2*math.cos(tmp_angle)+tmp_y2*math.sin(tmp_angle)+n_center[0])>0 else 1
        tmp_y[i][1] = int(math.fabs(n_center[1]-tmp_x2*math.sin(tmp_angle)+tmp_y2*math.cos(tmp_angle))) if int(math.fabs(n_center[1]-tmp_x2*math.sin(tmp_angle)+tmp_y2*math.cos(tmp_angle)))>0 else 1
        tmp_x[i][2] = int(tmp_x3*math.cos(tmp_angle)+tmp_y3*math.sin(tmp_angle)+n_center[0]) if int(tmp_x3*math.cos(tmp_angle)+tmp_y3*math.sin(tmp_angle)+n_center[0])>0 else 1
        tmp_y[i][2] = int(math.fabs(n_center[1]-tmp_x3*math.sin(tmp_angle)+tmp_y3*math.cos(tmp_angle))) if int(math.fabs(n_center[1]-tmp_x3*math.sin(tmp_angle)+tmp_y3*math.cos(tmp_angle)))>0 else 1
        tmp_x[i][3] = int(tmp_x4*math.cos(tmp_angle)+tmp_y4*math.sin(tmp_angle)+n_center[0]) if int(tmp_x4*math.cos(tmp_angle)+tmp_y4*math.sin(tmp_angle)+n_center[0])>0 else 1
        tmp_y[i][3] = int(math.fabs(n_center[1]-tmp_x4*math.sin(tmp_angle)+tmp_y4*math.cos(tmp_angle))) if int(math.fabs(n_center[1]-tmp_x4*math.sin(tmp_angle)+tmp_y4*math.cos(tmp_angle)))>0 else 1
    for i in range(len(x)):
        n_xmin.append(str(min(tmp_x[i])))
        n_ymin.append(str(min(tmp_y[i])))
        n_xmax.append(str(max(tmp_x[i])))
        n_ymax.append(str(max(tmp_y[i])))
    return n_xmin,n_ymin,n_xmax,n_ymax
    
def read_xml(xml_data):
    tree = ET.parse(xml_data)
    root = tree.getroot()

    xmin = []
    ymin = []
    xmax = []
    ymax = []

    for bndbox in root.iter("bndbox"):
        xmin.append(int(bndbox.find("xmin").text))
        ymin.append(int(bndbox.find("ymin").text))
        xmax.append(int(bndbox.find("xmax").text))
        ymax.append(int(bndbox.find("ymax").text))

    x = [[] for i in range(len(xmin))]
    y = [[] for i in range(len(xmin))]
    # print(len(xmin))
    for i in range(len(xmin)):
        x[i].append(xmin[i])
        y[i].append(ymin[i])
        x[i].append(xmax[i])
        y[i].append(ymin[i])
        x[i].append(xmax[i])
        y[i].append(ymax[i])
        x[i].append(xmin[i])
        y[i].append(ymax[i])
        # print(x)
        # print(y)
        # print("---------------")
    return x,y

def rotate_img(img,image_name,angle,angle_str):
    h = img.shape[0]
    w = img.shape[1]
    center = (w//2,h//2)
    M = cv2.getRotationMatrix2D((center[0], center[1]),angle, 1.0)
    nw = int((h * np.abs(M[0, 1])) + (w * np.abs(M[0, 0])))
    nh = int((h * np.abs(M[0, 0])) + (w * np.abs(M[0, 1])))
    M[0, 2] += (nw - w) / 2
    M[1, 2] += (nh - h) / 2
    rotate_img = cv2.warpAffine(img, M, (nw, nh))
    cv2.imwrite(os.path.join(result,angle_str+image_name),rotate_img)
    n_center = (nw//2,nh//2)
    return n_center,center

if __name__ == "__main__":
    if not os.path.exists(result):
        os.makedirs(result)
    for image_name in os.listdir(img_dir):
        img_path = img_dir+'/'+image_name
        x,y = read_xml(xml_dir +'/'+ image_name.split('.')[0]+'.xml')
        img = cv2.imread(img_path)
        # cv2.imshow('img',img)
        # cv2.waitKey(0)

        for i in range(len(angle)):
            angle_str = str(angle[i]).strip('-').zfill(3)
            n_center,center = rotate_img(img,image_name,angle[i],angle_str)
            # print(n_center,center)
            print(angle[i])
            n_xmin,n_ymin,n_xmax,n_ymax = rotate_point(x,y,n_center,center,angle[i])
            print(x,y)
            print('----------------------------------------')
            write_xml(xml_dir +'/'+ image_name.split('.')[0]+'.xml',image_name,n_xmin,n_ymin,n_xmax,n_ymax,angle_str)