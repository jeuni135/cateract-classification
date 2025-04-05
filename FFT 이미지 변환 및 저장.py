#FFT 모든 이미지 파일 변환
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

input_forder_nor = "/content/drive/MyDrive/cateract classification/Healthy_final"
input_forder_cat = "/content/drive/MyDrive/cateract classification/Cateract_final"
output_forder_nor = "/content/drive/MyDrive/백내장 전처리 데이터/normal"
output_forder_cat = "/content/drive/MyDrive/백내장 전처리 데이터/cateract"

def FFT(input_folder,output_folder):
  os.makedirs(output_folder, exist_ok=True)

  image_files = [f for f in os.listdir(input_folder) if f.endswith((".jpg"))]

  for img_file in image_files:

    img_path = os.path.join(input_folder, img_file)
    # 이미지 로드 및 그레이스케일 변환
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
            print(f"{img_file} 로드 실패!")
            continue

    # 가우시안 블러 적용(노이즈제거)
    blurred = cv2.GaussianBlur(img, (5, 5), 0)

    # CLAHE (대비 향상)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    #enhanced = clahe.apply((blurred*255).astype(np.uint8))  # CLAHE는 0~255 입력 필요
    enhanced = clahe.apply(blurred)

    # 2D 푸리에 변환 수행
    f = np.fft.fft2(enhanced)
    fshift = np.fft.fftshift(f)  # 중심을 이동
    magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)  # 로그 연산 보호

    magnitude_spectrum = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX)
    magnitude_spectrum = magnitude_spectrum.astype(np.uint8)

    output_path = os.path.join(output_folder, img_file)

    # 이미지 저장 (OpenCV는 기본적으로 BGR 형식)
    cv2.imwrite(output_path, magnitude_spectrum)

    print("저장완료")

FFT(input_forder_nor,output_forder_nor)
FFT(input_forder_cat,output_forder_cat)
