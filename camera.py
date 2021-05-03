# Python code for Multiple Color Detection


import numpy as np
import cv2
import argparse

gui = False
camera = 0

hsvFrame = None


def mouseRGB(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # checks mouse left button down condition
        colors = hsvFrame[y, x]
        print("colors: ", colors)
        print("Coordinates of pixel: X: ", x, "Y: ", y)


# Capturing video through webcam
webcam = cv2.VideoCapture(camera)
misses = 0
i = 0
acc = []

# Start a while loop
while 1:

    # Reading the video from the
    # webcam in image frames
    ret, imageFrame = webcam.read()
    if not ret:
        print("error")
        continue

    # Convert the imageFrame in
    # BGR(RGB color space) to
    # HSV(hue-saturation-value)
    # color space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Set range for red color and
    # define mask
    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    # Set range for green color and
    # define mask
    green_lower = np.array([25, 52, 72], np.uint8)
    green_upper = np.array([102, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

    # Set range for blue color and
    # define mask
    blue_lower = np.array([94, 80, 2], np.uint8)
    blue_upper = np.array([120, 255, 255], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

    # 	orangel = np.array([30,100,150], np.uint8)
    # 	orangeh = np.array([40, 255, 255], np.uint8)
    orangel = np.array([105, 180, 10], np.uint8)
    orangeh = np.array([120, 255, 255], np.uint8)
    orange_mask = cv2.inRange(hsvFrame, orangel, orangeh)
    if gui:
        cv2.imshow("mask", orange_mask)

    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")

    # For red color
    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(imageFrame, imageFrame, mask=red_mask)

    # For green color
    green_mask = cv2.dilate(green_mask, kernal)
    res_green = cv2.bitwise_and(imageFrame, imageFrame, mask=green_mask)

    # For blue color
    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(imageFrame, imageFrame, mask=blue_mask)

    orange_mask = cv2.dilate(orange_mask, kernal)
    if gui:
        cv2.imshow("dilated", orange_mask)
    res_orange = cv2.bitwise_and(imageFrame, imageFrame, mask=orange_mask)
    if gui:
        cv2.imshow("res", res_orange)

    # Creating contour to track green color
    contours, hierarchy = cv2.findContours(
        orange_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    # 	print(i)
    i += 1

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
        cv2.putText(
            imageFrame,
            "{:.2f}".format(area),
            tuple(oo),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 255, 0),
            2,
        )

    import itertools

    for (a, b) in itertools.combinations(t, 2):
        cv2.line(imageFrame, tuple(a), tuple(b), (255, 0, 255), 3)

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
        import json

        print(json.dumps(dic))
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

    # 			x, y, w, h = cv2.boundingRect(contour)
    # 			imageFrame = cv2.rectangle(imageFrame, (x, y),
    # 									(x + w, y + h),
    # 									(0, 255, 0), 2)

    # Program Termination
    if gui:
        cv2.imshow("colour", imageFrame)
        cv2.setMouseCallback("colour", mouseRGB)
        if cv2.waitKey(10) & 0xFF == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
            break
