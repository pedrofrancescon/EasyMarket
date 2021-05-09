
try:
    import RPi.GPIO as GPIO
    rpi = True
except ModuleNotFoundError:
    rpi = False
from enum import Enum, IntEnum


class MotorOrders(Enum):
    STOP = ([1, 0, 0], [0, 0, 0, 0])
    FORWARD = ([0, 1, 0], [1, 0, 1, 0])
    BACKWARD = ([0, 0, 1], [0, 1, 0, 1])
    TURNLEFT = ([1, 1, 1], [0, 0, 1, 0])
    TURNRIGHT = ([1, 1, 1], [1, 0, 0, 0])
    ROTATELEFT = ([1, 0, 1], [0, 1, 1, 0])
    ROTATERIGHT = ([1, 1, 0], [1, 0, 0, 1])
    LOCK = ([0, 0, 0], [1, 1, 1, 1])


# L+ 40 L- 38 R- 32 R+ 36
motor_pins = [40, 38, 32, 36]
led_pins = [11, 15, 13]


def init_motor_pins():
    if not rpi:
        return
    GPIO.setmode(GPIO.BOARD)
    for pin in motor_pins:
        GPIO.setup(pin, GPIO.OUT)


def init_led_pins():
    if not rpi:
        return
    GPIO.setmode(GPIO.BOARD)
    for pin in led_pins:
        GPIO.setup(pin, GPIO.OUT)


def set_motor(nstate):
    if not rpi:
        return
    GPIO.output(motor_pins, nstate.value[1])
    GPIO.output(led_pins, nstate.value[0])


class XCases(IntEnum):
    LEFT = 0
    CLEFT = 1
    CENTER = 2
    CRIGHT = 3
    RIGHT = 4


def x_to_cases(x):
    if x < 0.35:
        return XCases.LEFT
    if x < 0.43:
        return XCases.CLEFT
    if x < 0.57:
        return XCases.CENTER
    if x < 0.65:
        return XCases.CRIGHT
    return XCases.RIGHT


class DistCases(IntEnum):
    TOOCLOSE = 0
    CLOSE = 1
    OK = 2
    FAR = 3
    TOOFAR = 4


def dist_to_cases(dist):
    if dist > 0.4:
        return DistCases.TOOCLOSE
    if dist > 0.29:
        return DistCases.CLOSE
    if dist > 0.17:
        return DistCases.OK
    if dist > 0.12:
        return DistCases.FAR
    return DistCases.TOOFAR


class CameraData:
    def __init__(self, x, dist):
        self.x = x_to_cases(x)
        self.dist = dist_to_cases(dist)


def desired_motor_state_dist(current):
    if current is None:
        return MotorOrders.STOP
    if current.dist >= DistCases.FAR:
        return MotorOrders.FORWARD
    elif current.dist <= DistCases.CLOSE:
        return MotorOrders.BACKWARD
    else:
        return MotorOrders.STOP


def desired_motor_state(in_sight, last):
    # Target never acquired
    if last is None:
        return MotorOrders.STOP
    # Very close, go backwards
    if in_sight and last.dist <= DistCases.CLOSE:
        return MotorOrders.BACKWARD
    # Rotate till we find the lost target again or
    # The target is close, don`t move, just turn in its direction
    if (not in_sight) or last.dist <= DistCases.OK:
        if last.x == XCases.LEFT:
            return MotorOrders.ROTATELEFT
        if last.x == XCases.RIGHT:
            return MotorOrders.ROTATERIGHT
        return MotorOrders.STOP

    # Target far enough, go after it
    if last.dist >= DistCases.FAR:
        if last.x == XCases.LEFT:
            return MotorOrders.TURNLEFT
        if last.x == XCases.RIGHT:
            return MotorOrders.TURNRIGHT
        return MotorOrders.FORWARD


"""
if((!flow.get('camera_in_sight'))||(distance == "NEAR")) {
    switch(flow.get("camera_direction")){
        case "left":
            return "ROTATELEFT";
        case "center":
            return "STOP";
        case "right":
            return "ROTATERIGHT";
    }
}

// Target is in sight but far away

// obstacle very close, stop!
if (msg.payload <= 10) {
    switch(flow.get("camera_direction")){
        case "left":
            return "ROTATELEFT";
        case "center":
            return "STOP";
        case "right":
            return "ROTATERIGHT";
    }
// obstacle close, try to get around it    
} else if (msg.payload <= 20) {
    switch(flow.get("camera_direction")){
        case "left":
            return "TURNLEFT";
        case "center":
            return "TURNLEFT";
        case "right":
            return "TURNRIGHT";
    }
// Free to go, advance
} else {
    switch(flow.get("camera_direction")){
        case "left":
            return "TURNLEFT";
        case "center":
            return "FORWARD";
        case "right":
            return "TURNRIGHT";
    }

}
*/

return msg;

"""
