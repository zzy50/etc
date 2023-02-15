import pandas as pd
import numpy as np
from tqdm import tqdm

import os
import cv2


INPUT_ROOT = '2302-00'
OUTPUT_ROOT = INPUT_ROOT + "_output"
if not os.path.exists(OUTPUT_ROOT):
    os.makedirs(OUTPUT_ROOT)

CROP_UPPER_LINE = 150
CROP_LOWER_LINE = CROP_UPPER_LINE + 608

input_list = os.listdir(INPUT_ROOT)


for input_name in input_list:
    input_path = os.path.join(INPUT_ROOT, input_name)
    output_path = os.path.join(OUTPUT_ROOT, input_name)
    
    cap = cv2.VideoCapture(input_path)
    
    # codec
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    # frame size, fps
    # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = 1080
    height = 608
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    pbar = tqdm(total=frame_count, unit="frame", desc=input_name)
    while True:
        hasFrame, frame = cap.read()
        if not hasFrame:
            break

        frame_rotate = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame_cropped = frame_rotate[CROP_UPPER_LINE:CROP_LOWER_LINE, :, :]

        # cv2.imshow(input_name, frame_cropped)
        writer.write(frame_cropped)
        pbar.update(1)
            
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

    if cap.isOpened():
        writer.release()
        cap.release()
        # cv2.destroyAllWindows()

    else:
        raise Exception(f"영상을 확인해주세요!! >>> {input_path}")
        