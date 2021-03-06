try:
    import RPi.GPIO as GPIO

    rpi = True
except ModuleNotFoundError:
    rpi = False
from enum import Enum, IntEnum

import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def clamp(v, ma, mi):
    return max(mi, min(ma, v))


# fmt: off
class MotorOrders(Enum):
    STOP =        ([1, 0, 0], [0, 0, 0, 0])
    FORWARD =     ([0, 1, 0], [1, 0, 1, 0])
    BACKWARD =    ([0, 0, 1], [0, 1, 0, 1])
    TURNLEFT =    ([1, 1, 1], [0, 0, 1, 0])
    TURNRIGHT =   ([1, 1, 1], [1, 0, 0, 0])
    ROTATELEFT =  ([1, 0, 1], [0, 1, 1, 0])
    ROTATERIGHT = ([1, 1, 0], [1, 0, 0, 1])
    LOCK =        ([0, 0, 0], [1, 1, 1, 1])
# fmt: on

#BCM
# L+ 40 L- 38 R- 32 R+ 36
#motor_pins = [40, 38, 32, 36]
motor_pins = [21, 20, 12, 16]
# R G B
#led_pins = [11, 15, 13]
led_pins = [17, 22, 27]
# Trigger, echo
# 16 18
echo_pins = [23, 24]

# Left, right
pwm_pins = [19, 26]
PWM_FREQ=100
PWM_FULL=(1.0, 1.0)

ECHOV_STOP_DISTANCE = 18
ECHOV_DODGE_DISTANCE = 18


class XCases(IntEnum):
    FARLEFT = 0
    LEFT = 1
    CLEFT = 2 
    CENTER = 3
    CRIGHT = 4
    RIGHT = 5
    FARRIGHT = 6


X_TOLERANCE = 0.15

def x_to_cases(x):
    if x < 0.15:
        return XCases.FARLEFT
    if x < 0.50-X_TOLERANCE:
        return XCases.LEFT
    if x < 0.43: # Ignored
        return XCases.CLEFT
    if x < 0.57: # Ignored
        return XCases.CENTER
    if x < 0.50+X_TOLERANCE: 
        return XCases.CRIGHT
    if x < 0.85:
        return XCases.RIGHT
    return XCases.FARRIGHT


class DistCases(IntEnum):
    TOOCLOSE = 0
    CLOSE = 1
    OK = 2
    FAR = 3
    TOOFAR = 4


def dist_to_cases(dist):
    if dist > 0.6: # Ignored
        return DistCases.TOOCLOSE
    if dist > 0.5:
        return DistCases.CLOSE
    if dist > 0.21:
        return DistCases.OK
    if dist > 0.14: # Ignored
        return DistCases.FAR
    return DistCases.TOOFAR


def init_motor_pins():
    if not rpi:
        return
    GPIO.setmode(GPIO.BCM)
    for pin in motor_pins:
        GPIO.setup(pin, GPIO.OUT)


def c_pwm(v, m):
    ret = config['pwm_min'] + clamp(v*(m/100.0)*(config['pwm_mul']/100.0), 1, 0)*(config['pwm_max']-config['pwm_min'])
    return ret


def c_left_pwm(v):
    return config['pwm_left_abs'] + c_pwm(v, config['pwm_left'])


def c_right_pwm(v):
    return config['pwm_right_abs'] + c_pwm(v, config['pwm_right'])


def init_pwm_pins():
    if not rpi:
        return
    GPIO.setmode(GPIO.BCM)
    global left_pwm, right_pwm
    GPIO.setup(pwm_pins[0], GPIO.OUT)
    GPIO.setup(pwm_pins[1], GPIO.OUT)
    left_pwm = GPIO.PWM(pwm_pins[0], PWM_FREQ)
    right_pwm = GPIO.PWM(pwm_pins[1], PWM_FREQ)
    left_pwm.start(c_left_pwm(1))
    right_pwm.start(c_right_pwm(1))


def init_led_pins():
    if not rpi:
        return
    GPIO.setmode(GPIO.BCM)
    for pin in led_pins:
        GPIO.setup(pin, GPIO.OUT)


def init_echo():
    from Bluetin_Echo import Echo

    global echo
    echo = Echo(echo_pins[0], echo_pins[1])


def set_motor(nstate, led):
    if not rpi:
        return
    GPIO.output(motor_pins, nstate.value[1])
    if led:
        GPIO.output(led_pins, nstate.value[0])


def set_pwms(left, right):
    if not rpi:
        return
    left_pwm.ChangeDutyCycle(c_left_pwm(left))
    right_pwm.ChangeDutyCycle(c_right_pwm(right))


class CameraData:
    def __init__(self, x, dist):
        self.x = x_to_cases(x)
        self.x_value = x
        self.dist = dist_to_cases(dist)
        self.dist_value = dist


def desired_motor_state_dist(current):
    if current is None:
        return MotorOrders.STOP
    if current.dist >= DistCases.FAR:
        return MotorOrders.FORWARD
    elif current.dist <= DistCases.CLOSE:
        return MotorOrders.BACKWARD
    else:
        return MotorOrders.STOP


def turn_order(in_sight, last):
    if last.x == XCases.FARLEFT:
        return MotorOrders.ROTATELEFT
    if last.x == XCases.FARRIGHT:
        return MotorOrders.ROTATERIGHT
    return MotorOrders.FORWARD


def rotate_order(in_sight, last):
    if not in_sight:
        return MotorOrders.LOCK
    if last.x <= XCases.LEFT:
        return MotorOrders.ROTATELEFT
    if last.x >= XCases.RIGHT:
        return MotorOrders.ROTATERIGHT
    if not in_sight:
        if last.x == XCases.CLEFT:
            return MotorOrders.ROTATELEFT
        if last.x == XCases.CRIGHT:
            return MotorOrders.ROTATERIGHT
    return MotorOrders.LOCK


error_int_acc = 0
previous_error = 0


def get_pwm(in_sight, last):
    global error_int_acc
    global previous_error
    error_pro = abs(last.x_value-0.5)*2.0 if in_sight else 1.0
    error_int = abs(last.x_value-0.5)-X_TOLERANCE if in_sight else 1.0 # TODO: something
    if error_int < 0:
        error_int_acc = 0
    error_int_acc += error_int
    error_int_acc = min(error_int_acc, 5/(config["pwm_int"]/1000.0)) # Maximum error
    error_int_acc = max(error_int_acc, 0)
    pwm = 0.0
    pwm += error_pro*config["pwm_pro"]/1000.0
    pwm += error_int_acc*config["pwm_int"]/1000.0
    pwm += previous_error*config["pwm_der"]/1000.0
    pwm += min(0, error_pro-previous_error)*config["pwm_der2"]/1000.0
    pwm *= config["pwm_rotate"]/100.0
    previous_error = error_pro
    return pwm


def get_rotate_pwm(in_sight, last):
    pwm = get_pwm(in_sight, last)
    pwm *= config["pwm_rotate"]/100.0
    return (pwm, pwm)


def get_turn_pwm(in_sight, last):
    offside_pwm = config['pwm_turn_offside']/100.0
    pwm = get_pwm(in_sight, last)
    pwm *= config["pwm_turn"]/100.0
    ret = [offside_pwm, offside_pwm]
    if last.x_value < 0.5:
        ret[1] += pwm
    else:
        ret[0] += pwm
    return ret


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
        return rotate_order(in_sight, last)

    # Target far enough, go after it
    if last.dist >= DistCases.FAR:
        return turn_order(in_sight, last)


def desired_motor_state_pwm(in_sight, last):
    # Target never acquired
    if last is None:
        return MotorOrders.STOP, PWM_FULL
    # Very close, go backwards
    if in_sight and last.dist <= DistCases.CLOSE:
        return MotorOrders.BACKWARD, PWM_FULL
    # Rotate till we find the lost target again or
    # The target is close, don`t move, just turn in its direction
    if (not in_sight) or last.dist <= DistCases.OK:
        return rotate_order(in_sight, last), get_rotate_pwm(in_sight, last)

    # Target far enough, go after it
    if last.dist >= DistCases.FAR:
        return turn_order(in_sight, last), get_turn_pwm(in_sight, last)


def desired_motor_state_range(in_sight, last):
    echov = echo.read("cm", 1)

    # Target never acquired
    if last is None:
        return echov, MotorOrders.STOP
    # Very close, go backwards
    if in_sight and last.dist <= DistCases.CLOSE:
        return echov, MotorOrders.BACKWARD

    if echov <= ECHOV_STOP_DISTANCE:
        return echov, rotate_order(in_sight, last)

    # Rotate till we find the lost target again or
    # The target is close, don`t move, just turn in its direction
    if (not in_sight) or last.dist <= DistCases.OK:
        return echov, rotate_order(in_sight, last)

    # Target far enough, go after it
    if last.dist >= DistCases.FAR:
        lturn_order = turn_order(in_sight, last)
        if lturn_order == MotorOrders.FORWARD and echov < ECHOV_DODGE_DISTANCE:
            return echov, MotorOrders.TURNLEFT
        else:
            return echov, lturn_order


def desired_motor_state_pwm_range(in_sight, last):
    echov = echo.read("cm", 1)

    # Target never acquired
    if last is None:
        return echov, MotorOrders.STOP, PWM_FULL
    # Very close, go backwards
    if in_sight and last.dist <= DistCases.CLOSE:
        return echov, MotorOrders.BACKWARD, PWM_FULL

    # Rotate till we find the lost target again or
    # The target is close, don`t move, just turn in its direction
    if echov <= ECHOV_STOP_DISTANCE or (not in_sight) or last.dist <= DistCases.OK:
        order = rotate_order(in_sight, last)
        return echov, order, get_rotate_pwm(in_sight, last) if order != MotorOrders.LOCK else PWM_FULL

    # Target far enough, go after it
    if last.dist >= DistCases.FAR:
        order = turn_order(in_sight, last)
        return echov, order, get_turn_pwm(in_sight, last) if order == MotorOrders.FORWARD else get_rotate_pwm(in_sight, last)


