import os
import cv2

# 이미지 화질 낮출때 사용하는 코드

INPUT_ROOT = "input"
OUTPUT_ROOT = "output"
DOWNSCALE_RATE = 0.166 # 영상 축소 비율 (1이면 원본 크기, 0.5면 가로 세로가 각각 반으로 줄어듦)
INPUT_FILE_LIST = [
    "benchmark_sample.png"
    ]

for INPUT_FILE in INPUT_FILE_LIST:
    file, ext = os.path.splitext(INPUT_FILE)
    OUTPUT_FILE = f"{file}_resize{DOWNSCALE_RATE}{ext}"

    input_path = os.path.join(INPUT_ROOT, INPUT_FILE)
    output_path = os.path.join(OUTPUT_ROOT, OUTPUT_FILE)

    if os.path.isfile(input_path):
        img_raw = cv2.imread(input_path)
    else:
        raise Exception(f"{input_path}는 파일이 아닙니다!")

    img_size = img_raw.shape
    RESIZE = tuple(map(lambda x: int(x*DOWNSCALE_RATE), (img_size[1], img_size[0])))
    RESIZE = (320, 180)

    img_resized = cv2.resize(img_raw, dsize=(RESIZE), interpolation=cv2.INTER_AREA)
    cv2.imwrite(output_path, img_resized)
    print(f"Saved!! >>> {output_path}")
