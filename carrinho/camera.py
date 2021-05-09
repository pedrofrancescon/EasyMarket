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
import collections


def mouseRGB(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # checks mouse left button down condition
        colors = hsvFrame[y, x]
        print("colors: ", colors)
        print("Coordinates of pixel: X: ", x, "Y: ", y)


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

acc = []
kk = 0

config = dict(
    accLen=8,
    minWeight=10,
    minRect=0.7,
    minHull=0.8,
    minArea=250,
    max01AreaRatio=1.75,
    min12AreaRatio=2,
    low=masks["blue"][0],
    high=masks["blue"][1],
)


class KeyboardThread(threading.Thread):
    daemon = True

    def __init__(self, input_cbk=None, name="input-thread"):
        self.daemon = True
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            self.input_cbk(input())  # waits to get input + Return


def update_mask_input(inp):
    def convert(o):
        return np.array(
            [
                int((o["h"] / 360.0) * 255),
                int(o["s"] * 255),
                int(o["v"] * 255),
            ],
            np.uint8,
        )

    # evaluate the keyboard input
    l = json.loads(inp)
    for key, value in l.items():
        if key == "low":
            config["low"] = np.array(
                [
                    int((value["h"] / 360.0) * 255),
                    int(value["s"] * 255),
                    int(value["v"] * 255),
                ],
                np.uint8,
            )
        elif key == "high":
            config["high"] = np.array(
                [
                    int((value["h"] / 360.0) * 255),
                    int(value["s"] * 255),
                    int(value["v"] * 255),
                ],
                np.uint8,
            )
        else:
            config[key] = value


#   print(config, file=sys.stderr)

logfile = open("timelog.txt", "a")
print("------------START------------", file=logfile)

def perftime(pre, tim):
    if not tim:
        tim = time.perf_counter()
    now = time.perf_counter()
    formatted = "{:17}: {:.10f}".format(pre, now - tim)
    if timelog:
        eprint(formatted)
    else:
        print(formatted, file=logfile)
    return now


def readCamera(camera):
    now = perftime("startRead", None)
    ret, imageFrame = camera.read()
    now = perftime("readCamera", now)
    if not ret:
        raise Exception("can't read camera: {} {}".format(ret, camera))
    return imageFrame


currentImageFrame = collections.deque(maxlen=1)


class CameraThread(threading.Thread):
    daemon = True

    def __init__(self, camera, name="camera-thread"):
        self.daemon = True
        self.camera = camera
        super(CameraThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            currentImageFrame.append(readCamera(self.camera))

def wma(acc, v):
    weight_sum = 0
    value_sum = 0
    for weight, value in enumerate(acc):
        if value is None:
            continue
        weight += 1
        weight_sum += weight
        value_sum += value[v]*weight
    if weight_sum < config["minWeight"]:
        return None
    return value_sum / weight_sum

def processImage(imageFrame, gui=True, save=None, savefinal=True):
    global kk
    global hsvFrame
    if save:
        kk = (kk + 1) % save
    # Reading the video from the
    # camera in image frames
    now = perftime("start", None)

    # Convert the imageFrame in
    # BGR(RGB color space) to
    # HSV(hue-saturation-value)
    # color space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    now = perftime("hsvFrame", now)
    mask = cv2.inRange(hsvFrame, config["low"], config["high"])
    now = perftime("inRange", now)
    if gui:
        cv2.imshow("mask", mask)
    if save:
        cv2.imwrite("mask-{}.png".format(kk), mask)
    now = perftime("save-mask", now)

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
    now = perftime("save-dilated", now)
    res = cv2.bitwise_and(imageFrame, imageFrame, mask=mask)
    now = perftime("and", now)
    if gui:
        cv2.imshow("res", res)
    if save:
        cv2.imwrite("res-{}.png".format(kk), res)
    now = perftime("save-res", now)

    # Creating contour to track green color
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    now = perftime("contours", now)
    t = []
    for pic, contour in enumerate(contours):
        # 		if cv2.isContourConvex(contour):
        # 			continue
        area = cv2.contourArea(contour)
        if area < config["minArea"]:
            continue
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        rectArea = rect[1][0] * rect[1][1]
        # TODO: checksquareness
        if area / rectArea < config["minRect"]:
            continue
        hull = cv2.convexHull(contour)
        hullArea = cv2.contourArea(hull)
        if area / hullArea < config["minHull"]:
            continue
        cv2.drawContours(imageFrame, [box], 0, (0, 0, 255), 2)
        oo = np.int0(rect[0])
        cv2.circle(imageFrame, tuple(oo), 3, (0, 255, 0), cv2.FILLED)
        t.append((oo, area))
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
    global acc

    for (a, b) in itertools.combinations(t, 2):
        cv2.line(imageFrame, tuple(a[0]), tuple(b[0]), (255, 0, 255), 3)

    now = perftime("lines", now)
    dic = None

    t = sorted(t, reverse=True, key=lambda x: x[1])

    if len(t) >= 2 and (
        (len(t) == 2)
        or (
            (t[0][1] / t[1][1] < config["max01AreaRatio"])
            and (t[1][1] / t[2][1] > config["min12AreaRatio"])
        )
    ):
        a = t[0][0]
        b = t[1][0]
        dist = cv2.norm(b - a, cv2.NORM_L2)
        mid = a + (b - a) / 2
        dic = {
            "x": mid[0] / imageFrame.shape[1],
            "y": mid[1] / imageFrame.shape[0],
            "dist": dist / imageFrame.shape[1],
        }

        cv2.putText(
            imageFrame,
            "{:.2f}".format(dist),
            tuple(np.int0(mid)),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 0, 255),
            4,
        )
    acc.append(dic)
    if len(acc) > config["accLen"]:
        acc.pop(0)


    ret = collections.OrderedDict({
        "now": dic,
        "x": wma(acc, "x"),
        "y": wma(acc, "y"),
        "dist": wma(acc, "dist"),
    })

    now = perftime("other", now)
    if save and savefinal:
        cv2.imwrite("colour-{}.png".format(kk), imageFrame)
    if gui:
        cv2.imshow("colour", imageFrame)
        cv2.setMouseCallback("colour", mouseRGB)
        if cv2.waitKey(10) & 0xFF == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
            raise Exception("Close program")

    now = perftime("end", now)
    return ret


def main():
    global timelog
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
    parser.add_argument("--nomotor", action="store_true", help="disable motor")
    parser.add_argument("--time", action="store_true", help="enable time logging")
    parser.add_argument(
        "--savefinal", action="store_true", help="enable saving colour image(slow)"
    )
    parser.add_argument(
        "--save",
        default=1,
        help="length of save cycle (0 for no save)",
        type=int,
    )
    args = parser.parse_args()

    timelog = args.time

    camera = cv2.VideoCapture(args.camera)
    camera.open(-1)
    currentImageFrame.append(readCamera(camera))

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
    cameraThread = CameraThread(camera)

    if not args.nomotor:
        import motor

        motor.init_motor_pins()
        motor.set_motor(motor.MotorOrders.STOP)

    while 1:
        now = time.perf_counter()
        try:
            imageFrame = currentImageFrame.pop()
        except IndexError:
            time.sleep(0.005)
            continue
        now = perftime("wait for image", now)
        dic = processImage(imageFrame, not args.gui, args.save)
        now = perftime("processImage", now)
        if not args.nomotor:
            if dic['x']:
                camera_data = motor.CameraData(x=dic["x"], dist=dic["dist"])
            else:
                camera_data = None
            dic['motor'] = motor.desired_motor_state_dist(camera_data)
            motor.set_motor(dic['motor'])
            dic['motor'] = dic['motor'].name
            dic.move_to_end('dist', last=False)
            dic.move_to_end('motor', last=False)
        now = perftime("motor", now)
        print(json.dumps(dic))
        #       if dic['now']:
        #           print("now: x: {:6.2f}, y: {:6.2f}, dist: {:6.2f}".format(dic['now']['x'], dic['now']['y'], dic['now']['dist']))
        #       else:
        #           print(None)
        now = perftime("print", now)
        if not kthread.is_alive():
            raise Exception("terminal")
        if not cameraThread.is_alive():
            raise Exception("camera")
        print("", file=logfile)


if __name__ == "__main__":
    main()
