#!/usr/bin/env python3

from __future__ import print_function
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Python code for Multiple Color Detection

import time
import itertools
import numpy as np
import cv2
import json
import threading

def mouseRGB(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # checks mouse left button down condition
        colors = hsvFrame[y, x]
        print("colors: ", colors)
        print("Coordinates of pixel: X: ", x, "Y: ", y)

misses = 0
acc = []


masks = {
    # Set range for red color and
    # define mask
    "red": [
        np.array([136, 87, 111], np.uint8),
        np.array([180, 255, 255], np.uint8),
    ],
    "green": [
        np.array([25, 52, 72], np.uint8),
        np.array([102, 255, 255], np.uint8),
    ],
    "blue2": [
        np.array([94, 80, 2], np.uint8),
        np.array([120, 255, 255], np.uint8),
    ],
    "blue": [
        np.array([105, 180, 10], np.uint8),
        np.array([120, 255, 255], np.uint8),
    ],
}

gmask = masks['blue']
minRect = 0.7
minHull = 0.8
kk = 0


class KeyboardThread(threading.Thread):
    daemon = True
    def __init__(self, input_cbk = None, name='input-thread'):
        self.daemon = True
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()
    def run(self):
        while True:
            self.input_cbk(input()) #waits to get input + Return

def update_mask_input(inp):

    def convert(o):
        return np.array([
            int((o['h']/360.0)*255),
            int(o['s']*255),
            int(o['v']*255),
        ], np.uint8)
    
    #evaluate the keyboard input
    l = json.loads(inp)
    low = l.get('low')
    minRect = l.get('minRect')
    minHull = l.get('minHull')
    high = l.get('high')
    if minRect is not None:
        global minRect
        minRect = minRect
    if minHull is not None:
        global minHull
        minHull = minHull
    if low:
        gmask[0] = np.array([
            int((low['h']/360.0)*255),
            int(low['s']*255),
            int(low['v']*255),
        ], np.uint8)
    if high:
        gmask[1] = np.array([
            int((high['h']/360.0)*255),
            int(high['s']*255),
            int(high['v']*255),
##
##            255,
##            255,
        ], np.uint8)        


def perftime(pre, tim):
    if not tim:
        tim = time.perf_counter()
    now = time.perf_counter()
    eprint("{}: {}".format(pre, now-tim))
    return now

def runonce(camera, gui=True, save=None):
    global kk
    global hsvFrame
    if save:
        kk = (kk + 1) % save
    # Reading the video from the
    # camera in image frames
    now = perftime("start", None)
    ret, imageFrame = camera.read()
    now = perftime("read", now)
    if not ret:
        print(imageFrame)
        raise Exception("can't read camera: {} {}".format(ret, camera))

    # Convert the imageFrame in
    # BGR(RGB color space) to
    # HSV(hue-saturation-value)
    # color space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    now = perftime("hsvFrame", now)
    mask = cv2.inRange(hsvFrame, gmask[0], gmask[1])
    now = perftime("inRange", now)
    if gui:
        cv2.imshow("mask", mask)
    if save:
        cv2.imwrite("mask-{}.png".format(kk), mask)

    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")

    mask = cv2.dilate(mask, kernal)
    now = perftime("dilate", now)
    if gui:
        cv2.imshow("dilated", mask)
    if save:
        cv2.imwrite("dilated-{}.png".format(kk), mask)
    res = cv2.bitwise_and(imageFrame, imageFrame, mask=mask)
    now = perftime("and", now)
    if gui:
        cv2.imshow("res", res)
    if save:
        cv2.imwrite("res-{}.png".format(kk), res)

    # Creating contour to track green color
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    now = perftime("contours", now)
    t = []
    for pic, contour in enumerate(contours):
        # 		if cv2.isContourConvex(contour):
        # 			continue
        area = cv2.contourArea(contour)
        if area < 200:
            continue
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        rectArea = rect[1][0] * rect[1][1]
        if area / rectArea < minRect:
            continue
        hull = cv2.convexHull(contour)
        hullArea = cv2.contourArea(hull)
        if area / hullArea < minHull:
            continue
        cv2.drawContours(imageFrame, [box], 0, (0, 0, 255), 2)
        oo = np.int0(rect[0])
        cv2.circle(imageFrame, tuple(oo), 3, (0, 255, 0), cv2.FILLED)
        t.append(oo)
        cv2.putText(
            imageFrame,
            "{:.2f}".format(area),
            tuple(oo),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 255, 0),
            2,
        )
    now = perftime("contour analysis", now)
    global misses
    global acc

    for (a, b) in itertools.combinations(t, 2):
        cv2.line(imageFrame, tuple(a), tuple(b), (255, 0, 255), 3)

    now = perftime("lines", now)
    dic = None
    if len(t) == 2:
        a = t[0]
        b = t[1]
        dist = cv2.norm(b - a, cv2.NORM_L2)
        mid = a + (b - a) / 2
        acc.append(dist)
        mean = sum(acc) / len(acc)
        dic = {
            "x": mid[0] / imageFrame.shape[1],
            "y": mid[1] / imageFrame.shape[0],
            "mean_distance": mean,
        }

        cv2.putText(
            imageFrame,
            "{:.2f}".format(mean),
            tuple(np.int0(mid)),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 0, 255),
            4,
        )
    else:
        misses += 1

    if misses >= 5:
        acc = []

    if len(acc) >= 20:
        acc.pop(0)

    now = perftime("other", now)
    if save:
        cv2.imwrite("colour-{}.png".format(kk), imageFrame)
    if gui:
        cv2.imshow("colour", imageFrame)
        cv2.setMouseCallback("colour", mouseRGB)
        if cv2.waitKey(10) & 0xFF == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
            raise Exception("Close program")

    now = perftime("end", now)
    return dic


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("--camera", default=0, help="camera id", type=int)
    parser.add_argument(
        "--color",
        default="blue",
        help="color ({})".format(list(masks.keys())),
        type=str,
    )
    parser.add_argument("--gui", action="store_true", help="enable gui")
    parser.add_argument(
        "--save",
        default=0,
        help="length of save cycle (0 for no save)",
        type=int,
    )
    args = parser.parse_args()

    camera = cv2.VideoCapture(args.camera)
    camera.open(-1)

#   print(camera.set(cv2.CAP_PROP_AUTO_WB, False))
#   print(camera.set(cv2.CAP_PROP_AUTO_WB, 0))
#   print(camera.set(cv2.CAP_PROP_AUTO_WB, 0.0))
#   print(camera.set(cv2.CAP_PROP_GAIN, 20))
#   import time
#   time.sleep(2)
#   print(camera.get(cv2.CAP_PROP_MODE))
#   print(camera.get(cv2.CAP_PROP_BRIGHTNESS))
#   print(camera.get(cv2.CAP_PROP_CONTRAST))
#   print(camera.get(cv2.CAP_PROP_SATURATION))
#   print(camera.get(cv2.CAP_PROP_HUE))
#   print(camera.get(cv2.CAP_PROP_GAIN))
#   print(camera.get(cv2.CAP_PROP_AUTO_WB))
#   print(camera.get(cv2.CAP_PROP_EXPOSURE))
#   print(camera.get(cv2.CAP_PROP_TEMPERATURE))
#   print(camera.get(cv2.CAP_PROP_GAMMA))
    
    try:
        mask = masks[args.color]
    except KeyError:
        mask = masks["blue"]

    kthread = KeyboardThread(update_mask_input)

    while 1:
        now = time.perf_counter()
        dic = runonce(camera, args.gui, args.save)
        if dic:
            print(json.dumps(dic))
        now = perftime("total time", now)
        now = perftime("print", now)
        if not kthread.is_alive():
            raise Exception("terminal")


if __name__ == "__main__":
    main()
