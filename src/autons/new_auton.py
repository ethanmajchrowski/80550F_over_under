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
leftMotorA = Motor(Ports.PORT11, GearSetting.RATIO_6_1, True)
rightMotorA = Motor(Ports.PORT12, GearSetting.RATIO_6_1, False)
leftMotorB = Motor(Ports.PORT13, GearSetting.RATIO_6_1, True)
rightMotorB = Motor(Ports.PORT14, GearSetting.RATIO_6_1, False)
leftMotorC = Motor(Ports.PORT15, GearSetting.RATIO_6_1, True)
rightMotorC = Motor(Ports.PORT16, GearSetting.RATIO_6_1, False)
intakeMotor = Motor(Ports.PORT17, GearSetting.RATIO_18_1, True)
cataMotor = Motor(Ports.PORT18, GearSetting.RATIO_36_1, True)
inertialSens = Inertial(Ports.PORT9)

# Create motor groups
leftMotors = MotorGroup(leftMotorA, leftMotorB, leftMotorC)
rightMotors = MotorGroup(rightMotorA, rightMotorB, rightMotorC)

# 3 wire ports
wingsPistons = DigitalOut(brain.three_wire_port.g)
leftEnc = Encoder(brain.three_wire_port.a) # a/b
rightEnc = Encoder(brain.three_wire_port.c) # c/d
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
KP, KI, KD = 0.09, 0.005, 0.13
# KP, KI, KD = 0.1, 0, 0.08
# TURN_KP, TURN_KI, TURN_KD = 0.2, 0.05, 0.08 # KI 0.025? # when using left/right encoders for turn
TURN_KP, TURN_KI, TURN_KD = 0.35,0.001,0.5
# TURN_KP, TURN_KI, TURN_KD = 0, 0, 0
enable_drive_pid = False

def drive_pid(desired_value_in, turn_desired_value):
    # desired_value/turn_desired_value is the desired position in degrees of motors
    # convert desired value from mm to degrees
    desired_value_degrees = (desired_value_in / (2.75 * 3.14)) * 360
    print("desired degrees: ", desired_value_degrees)
    # Variables
    average_position = 0
    enable_drive_pid = True

    error = 0 # Difference between the robot and the desired position
    previous_error = 0 # Error 20 msec ago
    derivative = 0 # Error - Previous error, basically rate of error
    total_error = 0 # Total Error += error
    lateral_motor_power = 0
    
    turn_error = 0 # Difference between the robot and the desired turning position
    turn_previous_error = 0 # Error 20 msec ago
    turn_derivative = 0 # Error - Previous error, basically rate of error
    turn_total_error = 0 # Total Error += error
    turn_motor_power = 0

    hold_check = 0
    speed_limit = 0

    start_time = brain.timer.time()
    
    while enable_drive_pid:
        left_encoder_position = leftEnc.value()
        right_encoder_position = rightEnc.value() * -1
        average_position = (left_encoder_position + right_encoder_position) / 2

        # Lateral PID Control
        error = desired_value_degrees - average_position 
        derivative = error - previous_error
        total_error += error

        lateral_motor_power = ((error * KP) + (total_error * KI) + (derivative * KD)) * 0.5

        # Turning PID Control
        turn_error = left_encoder_position - right_encoder_position 
        turn_derivative = turn_error - turn_previous_error
        turn_total_error += turn_error

        turn_motor_power = (turn_error * TURN_KP) + (turn_total_error * TURN_KI) + (turn_derivative * TURN_KD)
        turn_motor_power *= 1.2

        leftMotors.spin(FORWARD, int(lateral_motor_power - turn_motor_power) * 0.4, VOLT) # type: ignore
        rightMotors.spin(FORWARD, int(lateral_motor_power + turn_motor_power) * 0.4, VOLT) # type: ignore
        
        previous_error = error
        turn_previous_error = turn_error
        speed_limit += 0.1

        if ((-10 < error < 10) and (-10 < turn_error < 10)):
            hold_check += 1
            if hold_check == 20:
                enable_drive_pid = False
        else:
            hold_check = 0

        brain.screen.clear_screen()
        brain.screen.set_cursor(1,1)
        brain.screen.print("error (degrees:)", error)
        brain.screen.next_row()
        brain.screen.print("error (inches):", (error * (2.75 * 3.14)) / 360)
        brain.screen.next_row()
        brain.screen.print("turn error:", turn_error)
        brain.screen.next_row()
        brain.screen.print("avg position (inches):", (average_position * (2.75 * 3.14)) / 360)
        brain.screen.next_row()
        brain.screen.print("avg position (degrees):", average_position)
        brain.screen.next_row()
        brain.screen.print("left position (degrees):", left_encoder_position)
        brain.screen.next_row()
        brain.screen.print("right position (degrees):", right_encoder_position)
        brain.screen.next_row()
        brain.screen.print("forward integral:", total_error * KI)
        brain.screen.next_row()
        brain.screen.render()
 
        sleep(20, MSEC)

    leftMotors.stop(BRAKE)
    rightMotors.stop(BRAKE)
    print("Complete. Time taken:", (brain.timer.time() - start_time) / 1000, "seconds. Final error:", error)
    print("Left encoder error:", abs(leftEnc.position() - desired_value_degrees), "degrees.")
    brain.screen.next_row()
    brain.screen.print("complete")
    brain.screen.render()

print("start program")

# drive_pid(-8, 0)
rightMotors.spin(REVERSE, 10, VOLT) #type:ignore
wait(0.25, SECONDS)
rightMotors.stop()
cataMotor.spin(FORWARD)
wait(1, SECONDS)
cataMotor.stop(BRAKE)
rightMotors.spin(FORWARD, 10, VOLT) #type:ignore
wait(0.25, SECONDS)
rightMotors.stop(BRAKE)
drive_pid(10, 0)
rightMotors.spin(REVERSE)
leftMotors.spin(FORWARD)
wait(0.5, SECONDS)
rightMotors.stop()
leftMotors.stop()
wait(1, SECONDS)
drive_pid(60,0)

print("Routing complete. Time taken: ", brain.timer.time() / 1000, "seconds")