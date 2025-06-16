import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Motor pins
motor_pins = {
    'left_forward': 5,
    'left_backward': 6,
    'right_forward': 13,
    'right_backward': 19
}

# Setup motor pins
for pin in motor_pins.values():
    GPIO.setup(pin, GPIO.OUT)

def move_forward():
    GPIO.output(motor_pins['left_forward'], True)
    GPIO.output(motor_pins['left_backward'], False)
    GPIO.output(motor_pins['right_forward'], True)
    GPIO.output(motor_pins['right_backward'], False)

def turn_right():
    GPIO.output(motor_pins['left_forward'], True)
    GPIO.output(motor_pins['left_backward'], False)
    GPIO.output(motor_pins['right_forward'], False)
    GPIO.output(motor_pins['right_backward'], True)
    time.sleep(0.5)

def turn_left():
    GPIO.output(motor_pins['left_forward'], False)
    GPIO.output(motor_pins['left_backward'], True)
    GPIO.output(motor_pins['right_forward'], True)
    GPIO.output(motor_pins['right_backward'], False)
    time.sleep(0.5)

def stop():
    for pin in motor_pins.values():
        GPIO.output(pin, False)

# Ultrasonic pins
sensors = {
    'front': {'trig': 2, 'echo': 3},
    'left': {'trig': 4, 'echo': 17},
    'right': {'trig': 27, 'echo': 22}
}

for sensor in sensors.values():
    GPIO.setup(sensor['trig'], GPIO.OUT)
    GPIO.setup(sensor['echo'], GPIO.IN)

def get_distance(trig, echo):
    GPIO.output(trig, False)
    time.sleep(0.01)

    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    while GPIO.input(echo) == 0:
        pulse_start = time.time()
    while GPIO.input(echo) == 1:
        pulse_end = time.time()

    duration = pulse_end - pulse_start
    return round((duration * 34300) / 2, 2)

# Wall-following loop
try:
    while True:
        front = get_distance(**sensors['front'])
        left = get_distance(**sensors['left'])
        right = get_distance(**sensors['right'])

        print(f"Front: {front} cm, Left: {left} cm, Right: {right} cm")

        if right > 20:
            turn_right()
            move_forward()
        elif front < 20:
            turn_left()
        else:
            move_forward()

        time.sleep(0.1)

except KeyboardInterrupt:
    stop()
    GPIO.cleanup()
