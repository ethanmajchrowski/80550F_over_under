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
inertialSens = Inertial(Ports.PORT19)
leftMotorA = Motor(Ports.PORT11, GearSetting.RATIO_6_1, True)
rightMotorA = Motor(Ports.PORT12, GearSetting.RATIO_6_1, False)
leftMotorB = Motor(Ports.PORT13, GearSetting.RATIO_6_1, True)
rightMotorB = Motor(Ports.PORT14, GearSetting.RATIO_6_1, False)
leftMotorC = Motor(Ports.PORT15, GearSetting.RATIO_6_1, True)
rightMotorC = Motor(Ports.PORT16, GearSetting.RATIO_6_1, False)
intakeMotor = Motor(Ports.PORT17, GearSetting.RATIO_18_1, True)
cataMotor = Motor(Ports.PORT18, GearSetting.RATIO_36_1, True)
threeWireExtender = Triport(Ports.PORT20)

# Create motor groups
leftMotors = MotorGroup(leftMotorA, leftMotorB, leftMotorC)
rightMotors = MotorGroup(rightMotorA, rightMotorB, rightMotorC)

# 3 wire ports
leftWingPiston = DigitalOut(brain.three_wire_port.f)
rightWingPiston = DigitalOut(brain.three_wire_port.h)
blockerPiston = DigitalOut(brain.three_wire_port.g)
endgamePiston = DigitalOut(brain.three_wire_port.e)
cataLimit = Limit(threeWireExtender.a)

# Calibrate sensors
inertialSens.calibrate()
while inertialSens.is_calibrating():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.print("Inertial Sensor Calibrating...")
    wait(50, MSEC)
brain.screen.clear_screen()

# # Lower Cata
# while(not cataLimit.pressing()):
#     cataMotor.spin(FORWARD, 60, PERCENT)
# cataMotor.stop(HOLD)

# Robot initialization complete

# drivetrain = SmartDrive(leftMotors, rightMotors, inertialSens, (2.75 * 3.14), 11, 10.5, DistanceUnits.IN, 0.75)
drivetrain = SmartDrive(leftMotors, rightMotors, inertialSens, (2.75 * 3.14) * 25.4, (11 * 25.4), (10.5 * 25.4), MM, 0.75)
drivetrain.set_drive_velocity(40, PERCENT)
drivetrain.set_turn_velocity(5, PERCENT)
drivetrain.set_timeout(2, SECONDS)

def main():
    print("starting")
    # # Far (version A)
    # intakeMotor.spin(REVERSE, 100, PERCENT) # intak to control triball
    # wait(1, SECONDS)
    # drivetrain.drive_for(FORWARD, (610 * 2), MM, wait = True) # drive forwards to align next to goal
    # intakeMotor.stop()
    # drivetrain.turn_for(RIGHT, 90, DEGREES) # turn to face into goal
    # intakeMotor.spin(FORWARD, 100, PERCENT) # extake
    # wait(0.5, SECONDS)
    # drivetrain.drive_for(FORWARD, 135, MM) # push triball into goal
    # wait(1, SECONDS)
    # intakeMotor.stop()
    # drivetrain.drive_for(REVERSE, 200, MM) # back away from goal
    # drivetrain.turn_for(RIGHT, 125, DEGREES)
    # print(inertialSens.heading())
    # drivetrain.drive_for(FORWARD, 730, MM)
    # wingsPistons.set(True)
    # drivetrain.drive_for(FORWARD, 20, MM, wait = False)
    # drivetrain.turn_for(LEFT, 50)

    # Far (Version B) NEW (friendly goal)
    # drivetrain.drive_for(FORWARD, 100, MM)
    # rightWingPiston.set(True)
    # drivetrain.drive_for(FORWARD, 150, MM)
    # drivetrain.turn_for(LEFT, 45)
    # drivetrain.drive_for(FORWARD, 540, MM, 60, PERCENT)
    # rightWingPiston.set(False)
    # wait(0.1, SECONDS)
    # drivetrain.drive_for(REVERSE, 240, MM)
    # drivetrain.turn_to_heading(250, DEGREES)
    # intakeMotor.spin(REVERSE, 100, PERCENT)
    # drivetrain.drive_for(FORWARD, 1000, MM, 70, PERCENT)
    # drivetrain.turn_to_heading(45, DEGREES)
    # intakeMotor.stop()
    # drivetrain.drive_for(FORWARD, 300, MM, 80, PERCENT)
    # leftWingPiston.set(True)
    # drivetrain.turn_for(RIGHT, 60, DEGREES)
    # intakeMotor.spin(FORWARD, 100, PERCENT)
    # drivetrain.drive_for(FORWARD, 650, MM, 80, PERCENT)

    # Close OLD
    # rightWingPiston.set(True)
    # wait(0.2, SECONDS)
    # drivetrain.turn(LEFT, 60)
    # wait(1.7, SECONDS)
    # drivetrain.stop(COAST)
    # cataMotor.spin(FORWARD, 10, VOLT)
    # wait(1.5, SECONDS)
    # cataMotor.stop(BRAKE)
    # rightWingPiston.set(False)
    # drivetrain.turn_for(RIGHT, 32)
    # drivetrain.drive_for(FORWARD, 1100, MM)
    # wait(5, SECONDS)

    # # Close NEW
    # rightWingPiston.set(True)
    # wait(0.5, SECONDS)
    # drivetrain.turn_for(LEFT, 115, DEGREES, 10, PERCENT)
    # wait(0.5, SECONDS)
    # while not cataLimit.pressing():
    #     cataMotor.spin(FORWARD, 100, PERCENT)
    # cataMotor.spin(FORWARD, 100, PERCENT)
    # wait(0.2, SECONDS)
    # cataMotor.stop(HOLD)
    # rightWingPiston.set(False)
    # drivetrain.turn_to_heading(285, DEGREES)
    # drivetrain.drive_for(FORWARD, 450, MM)
    # drivetrain.turn_to_heading(270, DEGREES)
    # drivetrain.drive_for(FORWARD, 550, MM)
    # wait(10, SECONDS)

    # # Skills OLD but still works
    # cataMotor.spin(FORWARD, 62, PERCENT) # catapult match loads
    # wait(34, SECONDS) # need to set this up to do about 48 launches
    # # wait(5, SECONDS) # need to set this up to do about 48 launches
    # while not cataLimit.pressing():
    #     cataMotor.spin(FORWARD, 62, PERCENT)
    # cataMotor.stop(BRAKE) # 
    # drivetrain.drive_for(FORWARD, 100, MM) # move away from pipe
    # drivetrain.turn_for(RIGHT, 40, DEGREES) # turn towards side of field
    # intakeMotor.spin(FORWARD, 100, PERCENT) # drop intake to fit under bar
    # drivetrain.drive_for(FORWARD, 500, MM) # drive somewhat under elevation bar
    # intakeMotor.stop()
    # drivetrain.turn_for(LEFT, 10, DEGREES) # turn to adjust slightly on side of field
    # drivetrain.drive_for(FORWARD, 1530, MM) # finish driving across
    # drivetrain.turn_for(LEFT, 45, DEGREES) # turn towards goal
    # leftWingPiston.set(True)  
    # rightWingPiston.set(True)  
    # drivetrain.drive_for(FORWARD, 900, MM) # first shove into goal
    # leftWingPiston.set(False)  
    # rightWingPiston.set(False)  
    # drivetrain.drive_for(REVERSE, 240, MM) # 
    # drivetrain.turn_for(LEFT, 120, DEGREES) # turn left to move to next push
    # drivetrain.drive_for(FORWARD, 1100, MM) # move to next push
    # drivetrain.turn_for(RIGHT, 165, DEGREES) # face goal for push
    # leftWingPiston.set(True)  
    # rightWingPiston.set(True)  
    # wait(0.5, SECONDS)
    # drivetrain.drive_for(FORWARD, 400, MM) # second push into goal
    # drivetrain.turn_for(RIGHT, 40, DEGREES)
    # drivetrain.drive_for(FORWARD, 600, MM, 70, PERCENT)
    # drivetrain.drive_for(REVERSE, 400, MM)
    # drivetrain.drive_for(FORWARD, 500, MM)
    # drivetrain.drive_for(REVERSE, 200, MM)
    # leftWingPiston.set(False)  
    # rightWingPiston.set(False)  

    # Skills NEW attempt 1
    # cataMotor.spin(FORWARD, 62, PERCENT) # catapult match loads
    # # wait(34, SECONDS) # need to set this up to do about 48 launches
    # wait(5, SECONDS) # need to set this up to do about 48 launches
    # while not cataLimit.pressing():
    #     cataMotor.spin(FORWARD, 62, PERCENT)
    # cataMotor.stop(HOLD) # 
    # drivetrain.drive_for(FORWARD, 100, MM) # move away from pipe
    # drivetrain.turn_for(RIGHT, 42, DEGREES) # turn towards side of field
    # intakeMotor.spin(FORWARD, 100, PERCENT) # drop intake to fit under bar
    # drivetrain.drive_for(FORWARD, 500, MM) # drive somewhat under elevation bar
    # intakeMotor.stop()
    # drivetrain.turn_for(LEFT, 10, DEGREES) # turn to adjust slightly on side of field
    # drivetrain.drive_for(FORWARD, 1550, MM) # finish driving across
    # drivetrain.turn_to_heading(300, DEGREES)
    # rightWingPiston.set(True)
    # drivetrain.drive_for(FORWARD, 400, MM)
    # leftWingPiston.set(True)
    # drivetrain.drive_for(FORWARD, 600, MM)
    # drivetrain.turn_for(LEFT, 70, DEGREES)
    # drivetrain.drive_for(FORWARD, 200, MM)
    # drivetrain.turn_for(RIGHT, 220, DEGREES)
    # drivetrain.drive_for(FORWARD, 500, MM)
    # drivetrain.turn_for(RIGHT)

    # # Skills new (part 2)
    # cataMotor.spin(FORWARD, 62, PERCENT) # catapult match loads
    # wait(34, SECONDS) # need to set this up to do about 48 launches
    # # wait(5, SECONDS) # need to set this up to do about 48 launches
    # while not cataLimit.pressing():
    #     cataMotor.spin(FORWARD, 62, PERCENT)
    # cataMotor.stop(BRAKE) # 
    # drivetrain.drive_for(FORWARD, 100, MM) # move away from pipe
    # drivetrain.turn_for(RIGHT, 40, DEGREES) # turn towards side of field
    # intakeMotor.spin(FORWARD, 100, PERCENT) # drop intake to fit under bar
    # drivetrain.drive_for(FORWARD, 500, MM) # drive somewhat under elevation bar
    # intakeMotor.stop()
    # drivetrain.turn_for(LEFT, 10, DEGREES) # turn to adjust slightly on side of field
    # drivetrain.drive_for(FORWARD, 1530, MM) # finish driving across
    # drivetrain.turn_for(LEFT, 45, DEGREES) # turn towards goal
    # drivetrain.drive_for(FORWARD, 900 - 240, MM) # first shove into goal
    # drivetrain.turn_for(LEFT, 120, DEGREES) # turn left to move to next push
    # drivetrain.drive_for(FORWARD, 1100, MM) # move to next push
    # drivetrain.turn_for(RIGHT, 165, DEGREES) # face goal for push
    # leftWingPiston.set(True)  
    # rightWingPiston.set(True)  
    # wait(0.5, SECONDS)
    # drivetrain.drive_for(FORWARD, 400, MM) # second push into goal
    # drivetrain.turn_for(RIGHT, 40, DEGREES)
    # drivetrain.drive_for(FORWARD, 600, MM, 70, PERCENT)
    # leftWingPiston.set(False)  
    # rightWingPiston.set(False) 
    # drivetrain.drive_for(REVERSE, 600, MM)
    # drivetrain.turn_for(LEFT, 90, DEGREES)
    # drivetrain.drive_for(FORWARD, 800, MM)
    # drivetrain.turn_for(RIGHT, 115, DEGREES, 10, PERCENT)
    # leftWingPiston.set(True)  
    # rightWingPiston.set(True)  
    # drivetrain.drive_for(FORWARD, 500, MM, 100, PERCENT)
    # leftWingPiston.set(False)  
    # rightWingPiston.set(False) 

    cataMotor.spin(FORWARD, 100, PERCENT) # catapult match loads default 62 pct
    wait(34, SECONDS)
    # wait(5, SECONDS)
    while not cataLimit.pressing():
        cataMotor.spin(FORWARD, 62, PERCENT)
    cataMotor.stop(BRAKE) # 
    drivetrain.drive_for(FORWARD, 100, MM) # move away from pipe
    drivetrain.turn_for(RIGHT, 40, DEGREES) # turn towards side of field
    intakeMotor.spin(FORWARD, 100, PERCENT) # drop intake to fit under bar
    drivetrain.drive_for(FORWARD, 500, MM) # drive somewhat under elevation bar
    intakeMotor.stop()
    drivetrain.turn_for(LEFT, 6, DEGREES) # turn to adjust slightly on side of field Maybe more less
    drivetrain.drive_for(FORWARD, 1530, MM) # finish driving across
    drivetrain.turn_for(LEFT, 45, DEGREES) # turn towards goal
    drivetrain.drive_for(FORWARD, 900 - 240, MM) # first shove into goal
    drivetrain.turn_for(LEFT, 120, DEGREES) # turn left to move to next push
    drivetrain.drive_for(FORWARD, 1100, MM) # move to next push
    drivetrain.turn_for(RIGHT, 165, DEGREES) # face goal for push
    leftWingPiston.set(True)  
    rightWingPiston.set(True)  
    wait(0.5, SECONDS)
    drivetrain.drive_for(FORWARD, 400, MM) # second push into goal
    drivetrain.turn_for(RIGHT, 40, DEGREES)
    drivetrain.drive_for(FORWARD, 600, MM, 70, PERCENT)
    leftWingPiston.set(False)  
    rightWingPiston.set(False) 
    drivetrain.drive_for(REVERSE, 600, MM)
    drivetrain.turn_for(LEFT, 90, DEGREES)
    drivetrain.drive_for(FORWARD, 800, MM)
    drivetrain.turn_for(RIGHT, 115, DEGREES, 10, PERCENT)
    leftWingPiston.set(True)  
    rightWingPiston.set(True)  
    drivetrain.drive_for(FORWARD, 500, MM, 100, PERCENT)
    leftWingPiston.set(False)  
    rightWingPiston.set(False)

    print("Done at ", brain.timer.time(SECONDS), " / 15 seconds")
    wait(2, SECONDS)
    intakeMotor.spin(FORWARD, 100, PERCENT)
    wait(1, SECONDS)
    intakeMotor.stop()
    drivetrain.stop(COAST)
    leftWingPiston.set(False)
    rightWingPiston.set(False)

main()