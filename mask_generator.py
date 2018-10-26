# -*- coding: utf-8 -*-

import sys
import cv2
import numpy as np
import argparse

"""
もしマニュアルで指定したいならここを編集
"""
def manual(manual, height, width):

    pt1 = (0, 0) # 始点 ( x, y )
    pt2 = (0, 0) # 終点 ( x, y )
    cv2.rectangle(image, pt1, pt2, (255, 255, 255), -1)

# parse args
parser = argparse.ArgumentParser(description="mask_gen")
parser.add_argument("--input", "-i", help="movie file")
parser.add_argument("--output", "-o", default="mask.png", help="output file name")
parser.add_argument("--process", "-p", default="center", help="generate option")
args = parser.parse_args()

# get video
cap = cv2.VideoCapture(args.input)
try:
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
except:
    sys.stderr.write("Could't open video file.")
    exit()
image = np.zeros((height, width), np.uint8)

"""
処理部
"""
if args.process == "center":
    # 端20%を削る
    pt1 = (int(width * 0.2), int(height * 0.2))
    pt2 = (int(width * 0.8), int(height * 0.8))
    cv2.rectangle(image, pt1, pt2, (255, 255, 255), -1)

elif args.process == "all":
    cv2.rectangle(image, (0, 0), (width, height), (255, 255, 255), -1)

elif args.process == "manual":
    # 関数に移譲
    manual(image, height, width)

else:
    sys.stderr.write("Could't match options. Please select process.[center, manual]")
    exit()

cv2.imwrite(args.output,image)
