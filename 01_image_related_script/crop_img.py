import cv2
from glob import glob
import os
from tqdm import tqdm

train_img = glob("data/train/0*.jpg")
train_txt = glob("data/train/0*.txt")
test_img = glob("data/test/0*.jpg")
test_txt = glob("data/test/0*.txt")
# print(len(train_img))
# print(len(train_txt))
# print(len(test_img))
# print(len(test_txt))


# label(txt)이 없는 jpg 총 10개 확인
# train sym list: ['00242528', '00206958', '00222014', '00260176', '00257088', '00217048', '00211419', '00206647']
# test sym list: ['00278252', '00288925']

# def get_sym(img_list, txt_list, print_text):
#     img_stem = []
#     for img in img_list:
#         spl = img.split(".")
#         img_stem.append(spl[0][-8:])
#     txt_stem = []
#     for txt in txt_list:
#         spl = txt.split(".")
#         txt_stem.append(spl[0][-8:])
#     sym = set(img_stem) ^ set(txt_stem)
#     print(print_text, sym)
# get_sym(train_img, train_txt, "train sym list:")
# get_sym(test_img, test_txt, "test sym list:")


def get_inter(img_list: list, txt_list: list):

    img_stem = []
    for img in img_list:
        spl = img.split(".")
        img_stem.append(spl[0][-8:])
    txt_stem = []
    for txt in txt_list:
        spl = txt.split(".")
        txt_stem.append(spl[0][-8:])
    sym = set(img_stem) & set(txt_stem)
    sym = sorted(sym)
    return sym


def crop_img(img_set: list, txt_set: list, mode_set: list):

    for img_list, txt_list, mode in zip(img_set, txt_set, mode_set):
        print(f"{mode} file cropping start....")
        sym = get_inter(img_list, txt_list)
        for stem in tqdm(sym):
            img = cv2.imread(f"data/{mode}/{stem}.jpg")
            img_h, img_w, img_c =  img.shape
            with open(f"data/{mode}/{stem}.txt", "r", encoding="utf-8") as f:
                count = 0
                for line in f.readlines():
                    count += 1
                    spl = line.split(" ")
                    cls = spl[0]
                    if stem == "00206810" and cls == "1":
                        print(*spl)
                    x, y, w, h = list(map(float, spl[1:]))

                    cen_x = int(x * img_w)
                    cen_y = int(y * img_h)

                    w = int(w * img_w)
                    h = int(h * img_h)

                    x_min = cen_x - w//2
                    y_min = cen_y - h//2
                    if x_min < 0: x_min = 1
                    if y_min < 0: y_min = 1

                    cropped = img[y_min:y_min+h, x_min:x_min+w]
                    if cropped is None:
                        continue
                    save_name = f"data_crop/{mode}/{cls}/{stem}_{str(count).zfill(3)}.jpg"
                    cv2.imwrite(save_name, cropped)


MODE_LIST = ["train", "test"]
IMG_LIST = [train_img, test_img]
TXT_LIST = [train_txt, test_txt]
crop_img(IMG_LIST, TXT_LIST, MODE_LIST)
# MODE_LIST = ["test"]
# IMG_LIST = [test_img]
# TXT_LIST = [test_txt]
# crop_img(IMG_LIST, TXT_LIST, MODE_LIST)


# cropped = img[y_min:y_min+h, x_min:x_min+w]
# img = cv2.rectangle(img, (x_min, y_min), (x_min+w, y_min+h), color = green_color, thickness = thickness)
# cv2.imshow("cropped", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()