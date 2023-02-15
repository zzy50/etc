import os
import cv2
from tqdm import tqdm

# 동영상 화질 낮출때 사용하는 코드

INPUT_ROOT = "input"
OUTPUT_ROOT = "output"
DOWNSCALE_RATE = 0.25 # 영상 축소 비율 (1이면 원본 크기, 0.5면 가로 세로가 각각 반으로 줄어듦)
INPUT_FILE_LIST = [
    "origin_video.mp4"
    ]

for INPUT_FILE in INPUT_FILE_LIST:
    file, ext = os.path.splitext(INPUT_FILE)
    OUTPUT_FILE = f"{file}_resize{DOWNSCALE_RATE}{ext}"

    input_path = os.path.join(INPUT_ROOT, INPUT_FILE)
    output_path = os.path.join(OUTPUT_ROOT, OUTPUT_FILE)

    if os.path.isfile(input_path):
        cap = cv2.VideoCapture(input_path)#, cv2.IMREAD_UNCHANGED)
    else:
        raise Exception(f"{input_path}는 파일이 아닙니다!")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (frame_width, frame_height)
    RESIZE = tuple(map(lambda x: int(x*DOWNSCALE_RATE), frame_size))

    wait_key_time = int(1000/fps)

    print(f"fps: {fps}")
    print(f"frame count: {frame_count}")
    print(f"frame size: {frame_size}")
    print(f"resize: {RESIZE}")

    codec = cv2.VideoWriter_fourcc(*'mp4v')
    resize_writer = cv2.VideoWriter(output_path, codec, fps, RESIZE)

    pbar = tqdm(total=frame_count, unit='frame', desc='Resize')
    while True:
        hasFrame, frame = cap.read() # hasFrame: 다음 프레임이 존재하는지 여부
        if not hasFrame:
            break

        frame_resized = cv2.resize(frame, dsize=(RESIZE), interpolation=cv2.INTER_AREA)

        # frame_origin = ToPILImage()(np.uint8(frame))
        # frame_resize = ToPILImage()(np.uint8(frame_resized))
        # crop_origin = transforms.FiveCrop(size=frame_origin.width // 5 - 9)(frame_origin)
        # crop_origin = [np.asarray(transforms.Pad(padding=(10, 5, 0, 0))(img)) for img in crop_origin]
        # frame_origin = transforms.Pad(padding=(5, 0, 0, 5))(frame_origin)
        # co_img = transforms.Resize(size=(frame_size), interpolation=InterpolationMode.BICUBIC)(ToPILImage()(frame_resize))
        # frmae_concat = cv2.hconcat(frame, frame_resized)
        # cv2.imshow("frame", frame_resized)
        # key = cv2.waitKey(wait_key_time) # 단위: msec
        # if key == 27:
        #     break
        resize_writer.write(frame_resized)
        pbar.update(1)

    if cap.isOpened():
        resize_writer.release()
        cap.release()

    cv2.destroyAllWindows()