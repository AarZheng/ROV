import RPi.GPIO as GPIO
import time
import curses   

# GPIO pin mapping (change as needed)
LEFT_IN1 = 17   # GPIO pin connected to LEFT_IN1
LEFT_IN2 = 27   # GPIO pin connected to LEFT_IN2
LEFT_EN  = 22   # GPIO pin connected to LEFT_EN (PWM)

RIGHT_IN1 = 23
RIGHT_IN2 = 24
RIGHT_EN = 25

VERT_IN1 = 5
VERT_IN2 = 6
VERT_EN = 13


# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_IN1, GPIO.OUT)
GPIO.setup(LEFT_IN2, GPIO.OUT)
GPIO.setup(LEFT_EN, GPIO.OUT)

GPIO.setup(RIGHT_IN1, GPIO.OUT)
GPIO.setup(RIGHT_IN2, GPIO.OUT)
GPIO.setup(RIGHT_EN, GPIO.OUT)

GPIO.setup(VERT_IN1, GPIO.OUT)
GPIO.setup(VERT_IN2, GPIO.OUT)
GPIO.setup(VERT_EN, GPIO.OUT)

# Create PWM object on LEFT_EN pin
pwm_left = GPIO.PWM(LEFT_EN, 1000)  # 1 kHz frequency
pwm_left.start(0)  # Start with 0% duty cycle (off)
pwm_right = GPIO.PWM(RIGHT_EN, 1000)
pwm_right.start(0)
pwm_vert = GPIO.PWM(VERT_EN, 1000)
pwm_vert.start(0)

def drive_lat(forward=True, speed=50):
    """Set motor direction and speed (0-100%)"""
    if forward:
        GPIO.output(LEFT_IN1, GPIO.HIGH)
        GPIO.output(LEFT_IN2, GPIO.LOW)
        GPIO.output(RIGHT_IN1, GPIO.HIGH)
        GPIO.output(RIGHT_IN2, GPIO.LOW)
    else:
        GPIO.output(LEFT_IN1, GPIO.LOW)
        GPIO.output(LEFT_IN2, GPIO.HIGH)
        GPIO.output(RIGHT_IN1, GPIO.LOW)
        GPIO.output(RIGHT_IN2, GPIO.HIGH)
    pwm_left.ChangeDutyCycle(speed)
    pwm_right.ChangeDutyCycle(speed)

def turn(clockwise=True, speed = 50):
    if clockwise:
        GPIO.output(LEFT_IN1, GPIO.HIGH)
        GPIO.output(LEFT_IN2, GPIO.LOW)
        GPIO.output(RIGHT_IN1, GPIO.LOW)
        GPIO.output(RIGHT_IN2, GPIO.HIGH)
    else:
        GPIO.output(LEFT_IN1, GPIO.LOW)
        GPIO.output(LEFT_IN2, GPIO.HIGH)
        GPIO.output(RIGHT_IN1, GPIO.HIGH)
        GPIO.output(RIGHT_IN2, GPIO.LOW)
    pwm_left.ChangeDutyCycle(speed)
    pwm_right.ChangeDutyCycle(speed)


def stop_drive_lat():
    """Stop the motor"""
    pwm_left.ChangeDutyCycle(0)
    pwm_right.ChangeDutyCycle(0)
    GPIO.output(LEFT_IN1, GPIO.LOW)
    GPIO.output(LEFT_IN2, GPIO.LOW)
    GPIO.output(RIGHT_IN1, GPIO.LOW)
    GPIO.output(RIGHT_IN2, GPIO.LOW)

def drive_vert(up = True, speed = 50):
    if up:
        GPIO.output(VERT_IN1, GPIO.LOW)
        GPIO.output(VERT_IN2, GPIO.HIGH)
    else:
        GPIO.output(VERT_IN1, GPIO.HIGH)
        GPIO.output(VERT_IN2, GPIO.LOW)
    pwm_vert.ChangeDutyCycle(speed)

def stop_drive_vert():
    pwm_vert.ChangeDutyCycle(0)
    GPIO.output(VERT_IN1, GPIO.LOW)
    GPIO.output(VERT_IN2, GPIO.LOW)