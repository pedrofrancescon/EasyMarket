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

try:
    import RPi.GPIO

    rpi = True
except ModuleNotFoundError:
    rpi = False


def clamp(v, ma=255, mi=0):
    max(mi, min(ma, v))


def mouseRGB(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # checks mouse left button down condition
        colors = hsvFrame[y, x]
        eprint("colors: ", colors)
        eprint("Coordinates of pixel: X: ", x, "Y: ", y)


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
    "blue3": [
        np.array([105, 180, 3], np.uint8),
        np.array([120, 255, 255], np.uint8),
    ],
    "blue": [
        np.array([103, 104, 5], np.uint8),
        np.array([120, 255, 255], np.uint8),
    ],
}

acc = []
kk = 0

import os

try:
    SAVE_PREFIX = os.environ["XDG_RUNTIME_DIR"] + "/"
except KeyError:
    SAVE_PREFIX = "/run/user/1001/"

config_lock = threading.Lock()

what = time.time()

config = dict(
    accLen=3,
    minWeight=1,
    minRect=0.7,
    minHull=0.8,
    maxUnsquareness=2,
    minArea=250,
    max01AreaRatio=1.75,
    min12AreaRatio=2,
    low=masks["blue"][0],
    high=masks["blue"][1],
    mutable=None,
    motorOrder=None, # Set to none to free motor controls

    # Absolute values ( X/100 )
    pwm_min = 42.0, # Minimum PWM value in all cases
    pwm_max = 70.0, # Maximum PWM value in all cases
    pwm_turn_offside = 16.0, # Added to minimum PWM when going FORWARD and not ROTATING

    # Multipliers ( X/100 )
    pwm_mul = 95.0, # General multiplier
    pwm_left = 100.0, #Left only multiplier
    pwm_right = 100.0, #Right only multiplier
    pwm_rotate = 65.0, # Multiplier for rotate PWM
    pwm_turn = 120.0, # Multiplier for turn PWM

    # PID parameters ( X/1000)
    pwm_pro = 100, # /1000
    pwm_int = 80, # /1000
    pwm_der = 0, # /1000
    pwm_der2 = 400, # /1000
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
    with config_lock:
        for key, value in l.items():
            if key == "low":
                config["low"] = np.array(
                    [
                        int(value["h"] * 0.5),
                        int(value["s"] * 255),
                        int(value["v"] * 255),
                    ],
                    np.uint8,
                )
            elif key == "high":
                config["high"] = np.array(
                    [
                        int(value["h"] * 0.5),
                        int(value["s"] * 255),
                        int(value["v"] * 255),
                    ],
                    np.uint8,
                )
            else:
                config[key] = value


#   print(config, file=sys.stderr)

logfile = open(SAVE_PREFIX + "timelog.txt", "a")
log2file = open(SAVE_PREFIX + "mainlog.txt", "a")
print("\n\n------------START------------", file=logfile)
print("\n\n------------START------------", file=log2file)


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
        value_sum += value[v] * weight
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
        cv2.imwrite(SAVE_PREFIX + "mask-{}.png".format(kk), mask)
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
    if save and savefinal:
        cv2.imwrite(SAVE_PREFIX + "dilated-{}.png".format(kk), mask)
    now = perftime("save-dilated", now)
    res = cv2.bitwise_and(imageFrame, imageFrame, mask=mask)
    now = perftime("and", now)
    if gui:
        cv2.imshow("res", res)
    if save and savefinal:
        cv2.imwrite(SAVE_PREFIX + "res-{}.png".format(kk), res)
    now = perftime("save-res", now)

    # Creating contour to track green color
    if int(cv2.__version__[0]) < 4:
        _, contours, hierarchy = cv2.findContours(
            mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
    else:
        contours, hierarchy = cv2.findContours(
            mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

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
        if (
            max(rect[1][0], rect[1][1]) / min(rect[1][0], rect[1][1])
            > config["maxUnsquareness"]
        ):
            continue
        if area / rectArea < config["minRect"]:
            continue
        hull = cv2.convexHull(contour)
        hullArea = cv2.contourArea(hull)
        if area / hullArea < config["minHull"]:
            continue
        cv2.drawContours(imageFrame, [box], 0, (0, 0, 255), 2)
        oo = np.int0(rect[0])
        cv2.circle(imageFrame, tuple(oo), 3, (0, 255, 0), cv2.FILLED)
        t.append((oo, area, contour))
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

        if config["mutable"]:
            colmask = np.zeros(mask.shape, np.uint8)
            cv2.drawContours(colmask, [t[0][2], t[1][2]], -1, 255, -1)
            if gui:
                cv2.imshow("colmask", colmask)
            colpixelpoints = np.transpose(np.nonzero(mask))
            contour_color = cv2.mean(hsvFrame, mask=colmask)
            eprint(contour_color)
            with config_lock:
                if config["mutable"][0] and what + 2 < time.time():
                    print(1)
                    config["low"] = np.array(
                        [
                            contour_color[0] + config["mutable"][0][0]
                            if config["mutable"][0][0] is not None
                            else config["low"][0],
                            contour_color[1] + config["mutable"][0][1]
                            if config["mutable"][0][1] is not None
                            else config["low"][1],
                            contour_color[2] + config["mutable"][0][2]
                            if config["mutable"][0][2] is not None
                            else config["low"][2],
                        ],
                        np.uint8,
                    )
                if config["mutable"][1] and what + 2 < time.time():
                    config["high"] = np.array(
                        [
                            contour_color[0] + config["mutable"][1][0]
                            if config["mutable"][1][0] is not None
                            else config["high"][0],
                            contour_color[1] + config["mutable"][1][1]
                            if config["mutable"][1][1] is not None
                            else config["high"][1],
                            contour_color[2] + config["mutable"][1][2]
                            if config["mutable"][1][2] is not None
                            else config["high"][2],
                        ],
                        np.uint8,
                    )
            eprint(config["low"])
            eprint(config["high"])

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

    ret = collections.OrderedDict(
        {
            "now": dic,
            "x": wma(acc, "x"),
            "y": wma(acc, "y"),
            "dist": wma(acc, "dist"),
        }
    )

    now = perftime("other", now)
    if save and savefinal:
        cv2.imwrite(SAVE_PREFIX + "colour-{}.png".format(kk), imageFrame)
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
    parser.add_argument(
        "--motor",
        default="XDIST",
        help="DIST XDIST RANGEXDIST NONE",
        type=str,
    )
    parser.add_argument("--gui", action="store_true", help="enable gui")
    parser.add_argument("--pwm", action="store_true", help="enable pwm")
    parser.add_argument(
        "--logstderr", action="store_true", help="write main log to stderr"
    )
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
    parser.add_argument(
        "--outputcycle",
        default=4,
        help="length of output cycle (1 for always)",
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

    if args.motor != "NONE":
        import motor
        motor.config = config

        motor.init_motor_pins()
        motor.init_led_pins()
        motor.set_motor(motor.MotorOrders.STOP)
        if args.pwm:
            motor.init_pwm_pins()
        if args.motor == "RANGEXDIST":
            motor.init_echo()

    last_camera_data = None
    cycle = time.perf_counter()
    pp = 0
    while 1:
        now = time.perf_counter()
        try:
            imageFrame = currentImageFrame.pop()
        except IndexError:
            time.sleep(0.005)
            continue
        now = perftime("wait for image", now)
        dic = processImage(
            imageFrame, False if rpi else args.gui, args.save, args.savefinal
        )
        now = perftime("processImage", now)
        if args.motor != "NONE":
            if dic["x"]:
                camera_data = motor.CameraData(x=dic["x"], dist=dic["dist"])
            else:
                camera_data = None
            if camera_data:
                last_camera_data = camera_data
            if config["motorOrder"]:
                dic["motor"] = motor.MotorOrders[config["motorOrder"]]
            elif args.motor == "DIST":
                dic["motor"] = motor.desired_motor_state_dist(camera_data)
            elif args.motor == "XDIST":
                if args.pwm:
                    dic["motor"], dic["PWM"] = motor.desired_motor_state_pwm(
                        bool(camera_data), last_camera_data
                    )
                else:
                    dic["motor"] = motor.desired_motor_state(
                        bool(camera_data), last_camera_data
                    )
            elif args.motor == "RANGEXDIST":
                if args.pwm:
                    dic["echov"], dic["motor"], dic["PWM"] = motor.desired_motor_state_pwm_range(
                    bool(camera_data), last_camera_data
                )
                else:
                    dic["echov"], dic["motor"] = motor.desired_motor_state_range(
                    bool(camera_data), last_camera_data
                )
            motor.set_motor(dic["motor"])
            if args.pwm:
                motor.set_pwms(*dic["PWM"])
            dic["motor"] = dic["motor"].name
            dic.move_to_end("dist", last=False)
            dic.move_to_end("motor", last=False)
        now = perftime("motor", now)

        pp = (pp + 1) % args.outputcycle
        if not pp:
            print(json.dumps(dic))

        cycle = perftime("cycle", cycle)
        avglog = (
            "avg: x: {:5.3f}, y: {:5.3f}, dist: {:5.3f}".format(
                dic["x"], dic["y"], dic["dist"]
            )
            if dic["x"]
            else ""
        )
        nowlog = (
            "now: x: {:5.3f}, y: {:5.3f}, dist: {:5.3f}".format(
                dic["now"]["x"], dic["now"]["y"], dic["now"]["dist"]
            )
            if dic["now"]
            else ""
        )
        echovlog = " | echov: {:5.{p}{ty}}".format(dic["echov"], p=0 if dic["echov"] >= 1000 else 1, ty="e" if dic["echov"] >= 1000 else "f") if args.motor == "RANGEXDIST" else ""
        pwmlog = " | PWM: {:.4f} {:.4f}".format(dic["PWM"][0], dic["PWM"][1]) if args.pwm else ""
        log = "T:{:6.3f}, {:11}{}{} | {:36} | {}".format(
            cycle, dic["motor"], echovlog, pwmlog, avglog, nowlog
        )
        if args.logstderr:
            eprint(log)
        print(log, file=log2file)
        now = perftime("print", now)
        if not kthread.is_alive():
            raise Exception("terminal")
        if not cameraThread.is_alive():
            raise Exception("camera")
        print("", file=logfile)


if __name__ == "__main__":
    main()
