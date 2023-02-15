from cgitb import text
import cv2 
from glob import glob 
import os 
import shutil 
import numpy as np 

path = "truck_m/"
#save_path = "C:/Users/CITYEYELAB/Downloads/390301660. 충남아산염치백암 1번카메라_(차종조사)/분류/"
save_path = "C:/Users/JJY/Desktop/4301_07_차종분류/4301_07_최종분류/"


car_type = ['truck_s_a', "truck_s_b", "truck_m_3W", "truck_m_4W", "truck_m_5W", "truck_4W_ST", "truck_4W_FT", "truck_5W_ST", "truck_5W_FT", "truck_6W_ST"]

imgs = glob(os.path.join(path, "*.jpg"))
window_name = "qwe"


# cv2.imshow("asd", text_img)
for img_path in imgs:
    text_img = np.zeros((1080,1920,3), dtype=np.uint8)
    s1 = f"{car_type}"
    s2 = f"      0 {' ' * len(car_type[0])}    1{' ' * len(car_type[1])}    2{' ' * len(car_type[2])}    3{' ' * len(car_type[3])}    4 {' ' * len(car_type[4])}   5 {' ' * len(car_type[5])}   6{' ' * len(car_type[6])}   7 {' ' * len(car_type[7])}   8 {' ' * len(car_type[8])}  9"
    s3 = f"{len(os.listdir(path))}"
    cv2.putText(text_img, s1,(200,450),1,1,(255,255,255),1)
    cv2.putText(text_img, s2,(200,430),1,1,(255,255,255),1)
    cv2.putText(text_img, s3,(400,230),1,3,(255,255,255),1)
    img = cv2.imread(img_path)
    img_name = os.path.basename(img_path)
    h,w,c =  img.shape
    text_img[500:500+h, 500:500+w, :] = img
    cv2.imshow(window_name,text_img)
    cv2.moveWindow(window_name,0,0)
    key = cv2.waitKey(0)
    for i in range(len(car_type)):
        if key == ord(str(i)):
            shutil.move(img_path, os.path.join(save_path, car_type[i], img_name))
        else:
            pass