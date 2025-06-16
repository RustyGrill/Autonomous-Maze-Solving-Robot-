import RPi.GPIO as GPIO
import time

# Set mode
GPIO.setmode(GPIO.BCM)

# Ultrasonic Sensor Pins (change as per your wiring)
sensors = {
    'front': {'trig': 2, 'echo': 3},
    'left': {'trig': 4, 'echo': 17},
    'right': {'trig': 27, 'echo': 22}
}

# Setup pins
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
    distance = round((duration * 34300) / 2, 2)  # cm
    return distance

try:
    while True:
        for name, pins in sensors.items():
            dist = get_distance(pins['trig'], pins['echo'])
            print(f"{name.capitalize()} distance: {dist} cm")
        print("-" * 40)
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
