import os
import cv2
import numpy as np
import ast
from datetime import datetime
from tqdm import tqdm
from os.path import join as opj

now = datetime.now().strftime("%Y%m%d_%H%M%S")

SPOT_NAME = "6생활권 미르3 2번카메라"
INPUT_ROOT = "C:/Users/ZZY/Desktop/영상/2023/세종시_교차로"
OUTPUT_ROOT = "video_with_line"
LINE_ROOT = "line_info"

if not os.path.exists(OUTPUT_ROOT):
    os.makedirs(OUTPUT_ROOT)

spot_path = opj(INPUT_ROOT, SPOT_NAME)
input_path = opj(spot_path, os.listdir(spot_path)[0]) # 맨 앞 영상 하나만 읽어옴
output_path = opj(OUTPUT_ROOT, f"{SPOT_NAME}_output_{now}.mp4")
line_path = opj(LINE_ROOT, "6생활권 미르3 2번카메라.txt")

with open(line_path, "r") as f:
    read_line_info = f.readline()
    line_list = ast.literal_eval(read_line_info)
    line_array = np.array(line_list)
    print(line_array.shape)


cap = cv2.VideoCapture(input_path)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
cv2.VideoWriter
writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
pbar = tqdm(total=frame_count, unit="frame", desc=input_path)

blue_color = (255, 0, 0)
green_color = (0, 255, 0)
red_color = (0, 0, 255)

while True:
    hasFrame, frame = cap.read()
    if not hasFrame:
        break

    for i, line in enumerate(line_array):
        text_coord_x = max(line[0][0], line[1][0]) - (max(line[0][0], line[1][0]) - min(line[0][0], line[1][0]))//2
        text_coord_y = max(line[0][1], line[1][1]) - (max(line[0][1], line[1][1]) - min(line[0][1], line[1][1]))//2
        cv2.putText(frame, str(i), (text_coord_x,text_coord_y), 2, 1, color=blue_color, thickness=2)
        frame = cv2.line(frame, line[0], line[1], color=green_color, thickness=1)

    writer.write(frame)
    pbar.update(1)

# if cap.isOpened():
writer.release()
cap.release()
    
