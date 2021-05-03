#!/usr/bin/env python3

# Python code for Multiple Color Detection

import itertools
import numpy as np
import cv2


def mouseRGB(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # checks mouse left button down condition
        colors = hsvFrame[y, x]
        print("colors: ", colors)
        print("Coordinates of pixel: X: ", x, "Y: ", y)


# Capturing video through camera
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
        # Set range for green color and
        # define mask
        np.array([25, 52, 72], np.uint8),
        np.array([102, 255, 255], np.uint8),
    ],
    "blue2": [
        # Set range for blue color and
        # define mask
        np.array([94, 80, 2], np.uint8),
        np.array([120, 255, 255], np.uint8),
    ],
    "blue": [
        np.array([105, 180, 10], np.uint8),
        np.array([120, 255, 255], np.uint8),
    ],
}

# Start a while loop


def runonce(camera, gui=True, color="blue"):
    # Reading the video from the
    # camera in image frames
    ret, imageFrame = camera.read()
    if not ret:
        print(imageFrame)
        raise Exception("can't read camera: {} {}".format(ret, camera))

    # Convert the imageFrame in
    # BGR(RGB color space) to
    # HSV(hue-saturation-value)
    # color space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsvFrame, masks[color][0], masks[color][1])
    if gui:
        cv2.imshow("mask", mask)

    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")

    mask = cv2.dilate(mask, kernal)
    if gui:
        cv2.imshow("dilated", mask)
    res = cv2.bitwise_and(imageFrame, imageFrame, mask=mask)
    if gui:
        cv2.imshow("res", res)

    # Creating contour to track green color
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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
        if area / rectArea < 0.7:
            continue
        hull = cv2.convexHull(contour)
        hullArea = cv2.contourArea(hull)
        if area / hullArea < 0.8:
            continue
        cv2.drawContours(imageFrame, [box], 0, (0, 0, 255), 2)
        oo = np.int0(rect[0])
        cv2.circle(imageFrame, tuple(oo), 3, (0, 255, 0), cv2.FILLED)
        t.append(oo)
        if gui:
            cv2.putText(
                imageFrame,
                "{:.2f}".format(area),
                tuple(oo),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 0),
                2,
            )
    global misses
    global acc

    for (a, b) in itertools.combinations(t, 2):
        cv2.line(imageFrame, tuple(a), tuple(b), (255, 0, 255), 3)

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

        if gui:
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

    if gui:
        cv2.imshow("colour", imageFrame)
        cv2.setMouseCallback("colour", mouseRGB)
        if cv2.waitKey(10) & 0xFF == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
            raise Exception("Close program")

    return dic


def main():
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("--camera", default=0, help="camera id", type=int)
    parser.add_argument(
        "--color",
        default="blue",
        help="color ({})".format(list(masks.keys())),
        type=str,
    )
    parser.add_argument("--gui", action="store_true", help="enable gui")
    args = parser.parse_args()

    camera = cv2.VideoCapture(args.camera)

    while 1:
        dic = runonce(camera, args.gui, args.color)
        if dic:
            print(json.dumps(dic))


if __name__ == "__main__":
    main()