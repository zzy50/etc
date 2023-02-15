import os
import cv2
import numpy as np
from tqdm import tqdm
from torchvision import transforms
from torchvision.transforms import ToTensor, ToPILImage, InterpolationMode

# SR된 영상을 원본 영상과 붙혀서 최종 결과영상을 만들 때 사용하는 코드




# file, ext = os.path.splitext(INPUT_FILE)
# OUTPUT_FILE = f"{file}_final{ext}"


# class Reader(object):
#     def __init__(self, input_path) -> None:
#         self.input_path = input_path
#         cap_org = cv2.VideoCapture(input_path)
#         fps = cap_org.get(cv2.CAP_PROP_FPS)
#         frame_count = cap_org.get(cv2.CAP_PROP_FRAME_COUNT)
#         frame_width = int(cap_org.get(cv2.CAP_PROP_FRAME_WIDTH))
#         frame_height = int(cap_org.get(cv2.CAP_PROP_FRAME_HEIGHT))
#         frame_size = (frame_width, frame_height)
#         wait_key_time = int(1000/fps)

#         print(f"fps: {fps}")
#         print(f"frame count: {frame_count}")
#         print(f"frame size: {frame_size}")

#         codec = cv2.VideoWriter_fourcc(*'mp4v')
#         resize_writer = cv2.VideoWriter(output_path, codec, fps, frame_size)
#     def VideoCapture(self):
#         self.cap = cv2.VideoCapture(self.input_path)
#         return self.cap


def main(num: int) -> None:

    INPUT_FILE_ORG = f"project{num}_resize0.25.mp4"
    INPUT_FILE_SR = f"project{num}_resize0.25_sr.mp4"
    OUTPUT_FILE = f"project{num}_final_221106.mp4"


    INPUT_ROOT = "test"
    OUTPUT_ROOT = "output/final"
    if not os.path.exists(OUTPUT_ROOT):
        os.makedirs(OUTPUT_ROOT)

    UPSCALE_FACTOR = 4
    input_path_org = os.path.join(INPUT_ROOT, INPUT_FILE_ORG)
    input_path_sr = os.path.join(INPUT_ROOT, INPUT_FILE_SR)
    output_path = os.path.join(OUTPUT_ROOT, OUTPUT_FILE)

    cap_org = cv2.VideoCapture(input_path_org)
    cap_sr = cv2.VideoCapture(input_path_sr)

    fps_org = cap_org.get(cv2.CAP_PROP_FPS)
    frame_count_org = cap_org.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_width_org = int(cap_org.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height_org = int(cap_org.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size_org = (frame_width_org, frame_height_org)

    fps_sr = cap_sr.get(cv2.CAP_PROP_FPS)
    frame_count_sr = cap_sr.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_width_sr = int(cap_sr.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height_sr = int(cap_sr.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size_sr = (frame_width_sr, frame_height_sr)
    
    final_width = int(frame_width_org * UPSCALE_FACTOR * 2 + 10)
    final_height = int(frame_height_org) * UPSCALE_FACTOR + 10 + int(final_width / int(10 * int(int(frame_width_org * UPSCALE_FACTOR) // 5 + 1)) * int(int(frame_width_org * UPSCALE_FACTOR) // 5 - 9))
    final_video_size = (final_width, final_height)


    video_writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps_org, final_video_size)
    wait_key_time = int(1000/fps_sr)

    print(f"[ video_org ] fps: {fps_org}")
    print(f"[ video_org ] frame count: {frame_count_org}")
    print(f"[ video_org ] frame size: {frame_size_org}")
    print()
    print(f"[ video_sr ] fps: {fps_sr}")
    print(f"[ video_sr ] frame count: {frame_count_sr}")
    print(f"[ video_sr ] frame size: {frame_size_sr}")


    # while True:
    for _ in tqdm(range(int(frame_count_sr))):
        hasFrame1, frame_org = cap_org.read() # hasFrame: 다음 프레임이 존재하는지 여부
        hasFrame2, frame_sr = cap_sr.read()
        if not hasFrame1:
            print("영상1 끝!")
            break
        if not hasFrame2:
            print("영상2 끝!")
            break

        # frame_org = ToPILImage()(np.uint8(frame_org))
        # crop_org = transforms.FiveCrop(size=frame_org.width // 5 - 9)(frame_org)
        # crop_org = [np.asarray(transforms.Pad(padding=(10, 5, 0, 0))(img)) for img in crop_org]
        # frame_org = transforms.Pad(padding=(5, 0, 0, 5))(frame_org)

        # SR 이미지
        frame_sr = ToPILImage()(np.uint8(frame_sr))
        crop_sr = transforms.FiveCrop(size=frame_sr.width // 5 - 9)(frame_sr)
        crop_sr = [np.asarray(transforms.Pad(padding=(10, 5, 0, 0))(img)) for img in crop_sr]
        frame_sr = transforms.Pad(padding=(5, 0, 0, 5))(frame_sr)

        # 원본 이미지를 SR 이미지 사이즈만큼 업스케일
        frame_org_upscaled = transforms.Resize(size=(frame_size_sr[1], frame_size_sr[0]), interpolation=InterpolationMode.BICUBIC)(ToPILImage()(np.uint8(frame_org)))
        crop_org_upscaled = transforms.FiveCrop(size=frame_org_upscaled.width // 5 - 9)(frame_org_upscaled)
        crop_org_upscaled = [np.asarray(transforms.Pad(padding=(0, 5, 10, 0))(img)) for img in crop_org_upscaled]
        frame_org_upscaled = transforms.Pad(padding=(0, 0, 5, 5))(frame_org_upscaled)


        # concatenate all the pictures to one single picture
        top_image = np.concatenate((np.asarray(frame_org_upscaled), np.asarray(frame_sr)), axis=1)
        bottom_image = np.concatenate(crop_org_upscaled + crop_sr, axis=1)
        bottom_image = np.asarray(
            transforms.Resize(size=(int(top_image.shape[1] / bottom_image.shape[1] * bottom_image.shape[0]), top_image.shape[1]))(ToPILImage()(bottom_image))
            )
        final_image = np.concatenate((top_image, bottom_image))

        # cv2.imshow("frame", final_image)
        # key = cv2.waitKey(wait_key_time) # 단위: msec
        # if key == 27:
        #     break
        
        video_writer.write(final_image)


    if cap_org.isOpened():
        video_writer.release()
        cap_org.release()

    cv2.destroyAllWindows()
    print(f"Saved!!! >>> {output_path}")



if __name__ == "__main__":
    for num in range(1, 9):
        if num == 4:
            continue
        main(num)