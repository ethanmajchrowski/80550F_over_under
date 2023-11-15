# Module:       main.py
# Author:       ethan
# Created:      7/21/2023, 11:07 AM
# Description:  Main module for robot stuff

# Library imports
from vex import *

# Define generic
brain = Brain()
con = Controller(PRIMARY)

# Define Ports
leftMotorA = Motor(Ports.PORT1, GearSetting.RATIO_6_1, True)
rightMotorA = Motor(Ports.PORT2, GearSetting.RATIO_6_1, False)
leftMotorB = Motor(Ports.PORT3, GearSetting.RATIO_6_1, True)
rightMotorB = Motor(Ports.PORT4, GearSetting.RATIO_6_1, False)
leftMotorC = Motor(Ports.PORT5, GearSetting.RATIO_6_1, True)
rightMotorC = Motor(Ports.PORT6, GearSetting.RATIO_6_1, False)
intakeMotor = Motor(Ports.PORT7, GearSetting.RATIO_18_1, True)
cataMotor = Motor(Ports.PORT8, GearSetting.RATIO_36_1, True)
inertialSens = Inertial(Ports.PORT9)

# Create motor groups
leftMotors = MotorGroup(leftMotorA, leftMotorB, leftMotorC)
rightMotors = MotorGroup(rightMotorA, rightMotorB, rightMotorC)

# 3 wire ports
wingsPistons = DigitalOut(brain.three_wire_port.g)
leftEnc = Encoder(brain.three_wire_port.a) # a/b
rightEnc = Encoder(brain.three_wire_port.c) # c/d
backEnc = Encoder(brain.three_wire_port.e) # e/f
# underglow = DigitalOut(brain.three_wire_port.h)

# Calibrate sensors
inertialSens.calibrate()
brain.screen.print("test")
while inertialSens.is_calibrating():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.print("Inertial Sensor Calibrating...")
    wait(50, MSEC)
brain.screen.clear_screen()

# Robot initialization complete

# Constants / Config
KP, KI, KD = 0.05, 0, 0.04 # KI 0.0075?
TURN_KP, TURN_KI, TURN_KD = 0.1, 0.02, 0.06
enable_drive_pid = False

def drive_pid(desired_value_mm, turn_desired_value):
    # desired_value/turn_desired_value is the desired position in degrees of motors
    # convert desired value from mm to degrees
    desired_value = (desired_value_mm / 260) * 360
    # Variables
    average_position = 0
    enable_drive_pid = True

    error = 6 # Difference between the robot and the desired position
    previous_error = 0 # Error 20 msec ago
    derivative = 0 # Error - Previous error, basically rate of error
    total_error = 0 # Total Error += error
    lateral_motor_power = 0
    
    turn_error = 0 # Difference between the robot and the desired turning position
    turn_previous_error = 0 # Error 20 msec ago
    turn_derivative = 0 # Error - Previous error, basically rate of error
    turn_total_error = 0 # Total Error += error
    turn_motor_power = 0

    start_time = brain.timer.time()

    while enable_drive_pid:#not ((desired_value - 2 )< average_position < (desired_value + 2)): #not (-5 < error < 5):
        left_encoder_position = leftEnc.value()
        right_encoder_position = rightEnc.value() * -1
        average_position = (left_encoder_position + right_encoder_position) / 2

        # # Lateral PID Control
        error = desired_value - average_position 
        derivative = error - previous_error
        total_error += error

        lateral_motor_power = (error * KP) + (total_error * KI) + (derivative * KD)
        # print(desired_value, average_position, lateral_motor_power)

        # Turning PID Control
        turn_error = left_encoder_position - right_encoder_position 
        turn_derivative = turn_error - turn_previous_error
        turn_total_error += turn_error

        turn_motor_power = (turn_error * TURN_KP) + (turn_total_error * TURN_KI) + (turn_derivative * TURN_KD)
        print(turn_desired_value, turn_error, turn_motor_power)

        leftMotors.spin(FORWARD, lateral_motor_power - turn_motor_power, VOLT) # type: ignore
        rightMotors.spin(FORWARD, lateral_motor_power + turn_motor_power, VOLT) # type: ignore

        previous_error = error
        turn_previous_error = turn_error
        sleep(20, MSEC)

    leftMotors.stop()
    rightMotors.stop()
    print("Complete. Time taken:", (brain.timer.time() - start_time) / 1000, "seconds. Final error:", error)
    print("Left encoder error:", abs(leftEnc.position() - desired_value), "degrees.")

drive_pid(600 * 4, 0)
# wait(, SECONDS)