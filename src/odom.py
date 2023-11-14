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
leftMotorA = Motor(Ports.PORT1, GearSetting.RATIO_6_1, False)
rightMotorA = Motor(Ports.PORT2, GearSetting.RATIO_6_1, False)
leftMotorB = Motor(Ports.PORT3, GearSetting.RATIO_6_1, False)
rightMotorB = Motor(Ports.PORT4, GearSetting.RATIO_6_1, False)
leftMotorC = Motor(Ports.PORT5, GearSetting.RATIO_6_1, False)
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
    brain.screen.print(" Inertial Sensor Calibrating...")
    wait(50, MSEC)
brain.screen.clear_screen()

while True:
    left_encoder_position = leftEnc.value()
    right_encoder_position = rightEnc.value() * -1
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.print(left_encoder_position, right_encoder_position)
    brain.screen.render()
    print(left_encoder_position, right_encoder_position)