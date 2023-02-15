'''
Metrics for unferwater image quality evaluation.

Author: Xuelei Chen 
Email: chenxuelei@hotmail.com

Usage:
python evaluate.py RESULT_PATH frame_org_PATH
'''
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from skimage.metrics import mean_squared_error as compare_mse
from skimage.metrics import peak_signal_noise_ratio as compare_psnr
from skimage.metrics import structural_similarity as compare_ssim
from skimage import io, color, filters

import math
import os
import cv2
from tqdm import tqdm
from torchvision import transforms
from torchvision.transforms import ToTensor, ToPILImage, InterpolationMode

import warnings
warnings.filterwarnings(action='ignore')



class MinMaxScaler3D(MinMaxScaler):
    def fit_transform(self, X, y=None):
        x = np.reshape(X, newshape=(X.shape[0]*X.shape[1], X.shape[2]))
        return np.reshape(super().fit_transform(x, y=y), newshape=X.shape)


def min_max_scaler(x):
    scaler = MinMaxScaler3D()
    return scaler.fit_transform(x)


def rmetrics(a, b):
    
    a = min_max_scaler(a)
    b = min_max_scaler(b)
    #pnsr
    mse = np.mean((a - b)**2)
    psnr = 10*math.log10(1/mse)

    #ssim
    ssim = compare_ssim(a, b, multichannel=True)

    return psnr, ssim

def nmetrics(a):
    rgb = a
    lab = color.rgb2lab(a)
    gray = color.rgb2gray(a)
    # UCIQE
    c1 = 0.4680
    c2 = 0.2745
    c3 = 0.2576
    l = lab[:,:,0]

    #1st term
    chroma = (lab[:,:,1]**2 + lab[:,:,2]**2)**0.5
    uc = np.mean(chroma)
    sc = (np.mean((chroma - uc)**2))**0.5

    #2nd term
    top = np.int(np.round(0.01*l.shape[0]*l.shape[1]))
    sl = np.sort(l,axis=None)
    isl = sl[::-1]
    conl = np.mean(isl[:top])-np.mean(sl[:top])

    #3rd term
    satur = []
    chroma1 = chroma.flatten()
    l1 = l.flatten()
    for i in range(len(l1)):
        if chroma1[i] == 0: satur.append(0)
        elif l1[i] == 0: satur.append(0)
        else: satur.append(chroma1[i] / l1[i])

    us = np.mean(satur)

    uciqe = c1 * sc + c2 * conl + c3 * us

    # UIQM
    p1 = 0.0282
    p2 = 0.2953
    p3 = 3.5753

    #1st term UICM
    rg = rgb[:,:,0] - rgb[:,:,1]
    yb = (rgb[:,:,0] + rgb[:,:,1]) / 2 - rgb[:,:,2]
    rgl = np.sort(rg,axis=None)
    ybl = np.sort(yb,axis=None)
    al1 = 0.1
    al2 = 0.1
    T1 = np.int(al1 * len(rgl))
    T2 = np.int(al2 * len(rgl))
    rgl_tr = rgl[T1:-T2]
    ybl_tr = ybl[T1:-T2]

    urg = np.mean(rgl_tr)
    s2rg = np.mean((rgl_tr - urg) ** 2)
    uyb = np.mean(ybl_tr)
    s2yb = np.mean((ybl_tr- uyb) ** 2)

    uicm =-0.0268 * np.sqrt(urg**2 + uyb**2) + 0.1586 * np.sqrt(s2rg + s2yb)

    #2nd term UISM (k1k2=8x8)
    Rsobel = rgb[:,:,0] * filters.sobel(rgb[:,:,0])
    Gsobel = rgb[:,:,1] * filters.sobel(rgb[:,:,1])
    Bsobel = rgb[:,:,2] * filters.sobel(rgb[:,:,2])

    Rsobel=np.round(Rsobel).astype(np.uint8)
    Gsobel=np.round(Gsobel).astype(np.uint8)
    Bsobel=np.round(Bsobel).astype(np.uint8)

    Reme = eme(Rsobel)
    Geme = eme(Gsobel)
    Beme = eme(Bsobel)

    uism = 0.299 * Reme + 0.587 * Geme + 0.114 * Beme

    #3rd term UIConM
    uiconm = logamee(gray)

    uiqm = p1 * uicm + p2 * uism + p3 * uiconm
    return uiqm,uciqe

def eme(ch,blocksize=8):

    num_x = math.ceil(ch.shape[0] / blocksize)
    num_y = math.ceil(ch.shape[1] / blocksize)
    
    eme = 0
    w = 2. / (num_x * num_y)
    for i in range(num_x):

        xlb = i * blocksize
        if i < num_x - 1:
            xrb = (i+1) * blocksize
        else:
            xrb = ch.shape[0]

        for j in range(num_y):

            ylb = j * blocksize
            if j < num_y - 1:
                yrb = (j+1) * blocksize
            else:
                yrb = ch.shape[1]
            
            block = ch[xlb:xrb,ylb:yrb]

            blockmin = np.float(np.min(block))
            blockmax = np.float(np.max(block))

            # # old version
            # if blockmin == 0.0: eme += 0
            # elif blockmax == 0.0: eme += 0
            # else: eme += w * math.log(blockmax / blockmin)

            # new version
            if blockmin == 0: blockmin+=1
            if blockmax == 0: blockmax+=1
            eme += w * math.log(blockmax / blockmin)
    return eme

def plipsum(i,j,gamma=1026):
    return i + j - i * j / gamma

def plipsub(i,j,k=1026):
    return k * (i - j) / (k - j)

def plipmult(c,j,gamma=1026):
    return gamma - gamma * (1 - j / gamma)**c

def logamee(ch,blocksize=8):

    num_x = math.ceil(ch.shape[0] / blocksize)
    num_y = math.ceil(ch.shape[1] / blocksize)
    
    s = 0
    w = 1. / (num_x * num_y)
    for i in range(num_x):

        xlb = i * blocksize
        if i < num_x - 1:
            xrb = (i+1) * blocksize
        else:
            xrb = ch.shape[0]

        for j in range(num_y):

            ylb = j * blocksize
            if j < num_y - 1:
                yrb = (j+1) * blocksize
            else:
                yrb = ch.shape[1]
            
            block = ch[xlb:xrb,ylb:yrb]
            blockmin = np.float(np.min(block))
            blockmax = np.float(np.max(block))

            top = plipsub(blockmax,blockmin)
            bottom = plipsum(blockmax,blockmin)

            m = top/bottom
            if m ==0.:
                s+=0
            else:
                s += (m) * np.log(m)

    return plipmult(w,s)

def main(num):

    INPUT_FILE_ORG = f"project{num}_resize0.25.mp4"
    INPUT_FILE_SR = f"project{num}_resize0.25_sr.mp4"
    OUTPUT_FILE = f"project{num}_final_metrics1.txt"

    INPUT_ROOT = "test"
    OUTPUT_ROOT = "output/final"

    input_path_org = os.path.join(INPUT_ROOT, INPUT_FILE_ORG)
    input_path_sr = os.path.join(INPUT_ROOT, INPUT_FILE_SR)
    output_path = os.path.join(OUTPUT_ROOT, OUTPUT_FILE)

    cap_org = cv2.VideoCapture(input_path_org)
    cap_sr = cv2.VideoCapture(input_path_sr)

    fps_org = cap_org.get(cv2.CAP_PROP_FPS)
    fps_sr = cap_sr.get(cv2.CAP_PROP_FPS)
    frame_count_org = cap_org.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_width_org = int(cap_org.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height_org = int(cap_org.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size_org = (frame_width_org, frame_height_org)

    frame_count_sr = cap_sr.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_width_sr = int(cap_sr.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height_sr = int(cap_sr.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size_sr = (frame_width_sr, frame_height_sr)

    print(f"[ video_org ] fps: {fps_org}")
    print(f"[ video_org ] frame count: {frame_count_org}")
    print(f"[ video_org ] frame size: {frame_size_org}")
    print()
    print(f"[ video_sr ] fps: {fps_sr}")
    print(f"[ video_sr ] frame count: {frame_count_sr}")
    print(f"[ video_sr ] frame size: {frame_size_sr}")

    sumpsnr, sumssim, sumuiqm, sumuciqe = 0., 0., 0., 0.

    # frame_count_sr //= 30 #TODO 너무 오래걸려서 영상 전체의 1/10 만큼만 평가지표 체크
    N = 0
    with open(output_path, 'a') as f:
        for _ in tqdm(range(int(frame_count_sr))):
            hasFrame1, frame_org = cap_org.read() # hasFrame: 다음 프레임이 존재하는지 여부
            hasFrame2, frame_sr = cap_sr.read()
            if not hasFrame1:
                print("영상1 끝!")
                break
            if not hasFrame2:
                print("영상2 끝!")
                break

            frame_org_upscaled = transforms.Resize(size=(frame_size_sr[1], frame_size_sr[0]), interpolation=InterpolationMode.BICUBIC)(ToPILImage()(np.uint8(frame_org)))
            frame_org_upscaled = np.array(frame_org_upscaled)
            psnr, ssim = rmetrics(frame_sr, frame_org_upscaled)
            # uiqm, uciqe = nmetrics(frame_sr)

            sumpsnr += psnr
            sumssim += ssim
            # sumuiqm += uiqm
            # sumuciqe += uciqe
            N +=1

            # f.write('Frame{}: psnr={} ssim={} uiqm={} uciqe={}\n'.format(N, psnr, ssim, uiqm, uciqe))
            f.write('Frame{}: psnr={} ssim={}\n'.format(N, psnr, ssim))

        mpsnr = sumpsnr/N
        mssim = sumssim/N
        # muiqm = sumuiqm/N
        # muciqe = sumuciqe/N

        # f.write('Average: psnr={} ssim={} uiqm={} uciqe={}\n'.format(mpsnr, mssim, muiqm, muciqe))
        f.write('Average: psnr={} ssim={}\n'.format(mpsnr, mssim))

if __name__ == '__main__':
    for num in [1, 2, 3, 5, 6, 7, 8]:
        main(num)