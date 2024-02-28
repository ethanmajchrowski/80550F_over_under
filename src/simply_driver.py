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
inertialSens = Inertial(Ports.PORT19)
threeWireExtender = Triport(Ports.PORT20)

# Create motor groups
leftMotors = MotorGroup(leftMotorA, leftMotorB, leftMotorC)
rightMotors = MotorGroup(rightMotorA, rightMotorB, rightMotorC)

# 3 wire ports
leftWingPiston =  DigitalOut(brain.three_wire_port.f)
rightWingPiston = DigitalOut(brain.three_wire_port.h)
blockerPiston =   DigitalOut(brain.three_wire_port.g)
endgamePiston =   DigitalOut(brain.three_wire_port.e)

cataLimit =    Limit(threeWireExtender.a)
headlightLED = DigitalOut(threeWireExtender.d)
leftTurnLED =  DigitalOut(threeWireExtender.c)
rightTurnLED = DigitalOut(threeWireExtender.b)

# DRIVETRAIN
drivetrain = SmartDrive(leftMotors, rightMotors, inertialSens, (2.75 * 3.14) * 25.4, (11 * 25.4), (10.5 * 25.4), MM, 0.75)
drivetrain.set_drive_velocity(40, PERCENT)
drivetrain.set_turn_velocity(5, PERCENT)
drivetrain.set_timeout(2, SECONDS)

# VARIABLES
intakeStatus = False
intakeDir = "in"
armState = "closed"
gifState = True
selecting = True
selected = None
touch_areas = []
screen_state = "main" # main, test, tools, thermals
ledState = True
cataState = False

cataMotor.set_velocity(95, PERCENT)
cataMotor.set_max_torque(100, PERCENT)
intakeMotor.set_velocity(100, PERCENT)

# define controller functions
def r2Pressed():
    global intakeStatus, intakeDir
    if intakeStatus == False:
        intakeStatus = True
        intakeDir = "in"
    elif intakeStatus == True and intakeDir == "in":
        intakeStatus = False
    elif intakeStatus == True and intakeDir == "out":
        intakeDir = "in"

def r1Pressed():
    global intakeStatus, intakeDir
    if intakeStatus == False:
        intakeStatus = True
        intakeDir = "out"
    elif intakeStatus == True and intakeDir == "out":
        intakeStatus = False
    elif intakeStatus == True and intakeDir == "in":
        intakeDir = "out"

def toggleWings():
    if rightWingPiston.value() == True or leftWingPiston.value() == True:
        rightWingPiston.set(False)
        leftWingPiston.set(False)
    else:
        rightWingPiston.set(True)
        leftWingPiston.set(True)

def rightWing():
    if rightWingPiston.value() == True:
        rightWingPiston.set(False)
    else:
        rightWingPiston.set(True)

def leftWing():
    if leftWingPiston.value() == True:
        leftWingPiston.set(False)
    else:
        leftWingPiston.set(True)

def toggleBlocker():
    blockerPiston.set(not blockerPiston.value())

def lowerCata():
    while not cataLimit.pressing():
        cataMotor.spin(FORWARD, 80)
        if con.buttonDown.pressing(): break
    cataMotor.stop(HOLD)

def thread_main():
    # def thread vars
    global intakeStatus, intakeDir    
    # thread loop
    while True:
        if intakeStatus == True:
            if intakeDir == "in":
                intakeMotor.spin(FORWARD)
            else:
                intakeMotor.spin(REVERSE)
        else:
            intakeMotor.stop()

        if con.buttonB.pressing():
            endgamePiston.set(True)
        else:
            endgamePiston.set(False)
        
        sleep(5)

def toggleCata():
    global cataState
    cataState = not cataState

    if cataState:
        cataMotor.spin(FORWARD)
    else:
        while not cataLimit.pressing():
            cataMotor.spin(FORWARD, 60)
        cataMotor.stop(HOLD)
        
def thread_driveControl():
    global ledState
    hold = 100
    while True:
        # handle LED control if allowed
        if ledState == True:
            headlightLED.set(True)
            if con.axis1.position() > 10:
                leftTurnLED.set(False)
                rightTurnLED.set(True)
            elif con.axis1.position() < -10:
                rightTurnLED.set(False)
                leftTurnLED.set(True)
            else:
                rightTurnLED.set(False)
                leftTurnLED.set(False)
        else:
            headlightLED.set(False)
            rightTurnLED.set(False)
            leftTurnLED.set(False)

        if con.buttonL1.pressing() and con.buttonL2.pressing():
            hold -= 1
            if hold == 0: ledState = not ledState
        else:
            hold = 100

        # Convert controller axis to voltage levels
        turnVolts = con.axis2.position() * -0.12
        forwardVolts = con.axis1.position() * -0.12 

        # Spin motors and combine controller axes
        leftMotorA.spin(REVERSE, forwardVolts + turnVolts, VOLT)
        leftMotorB.spin(REVERSE, forwardVolts + turnVolts, VOLT)
        leftMotorC.spin(REVERSE, forwardVolts + turnVolts, VOLT)
        rightMotorA.spin(FORWARD, forwardVolts - turnVolts, VOLT)
        rightMotorB.spin(FORWARD, forwardVolts - turnVolts, VOLT)
        rightMotorC.spin(FORWARD, forwardVolts - turnVolts, VOLT)
        sleep(5)

def gifThread():
    index = 1
    while True:
        wait(20, MSEC)
        if gifState:
            brain.screen.clear_screen()

            brain.screen.draw_image_from_file(("fractal (" + str(index) + ").png"), 0, 0)
            if index < 60:
                index += 1
            else:
                index = 1
            brain.screen.render()

def userControl():
    Thread(gifThread)
    Thread(thread_main)
    Thread(thread_driveControl)

# Assign controller functions
con.buttonR1.pressed(r1Pressed)
con.buttonR2.pressed(r2Pressed)
con.buttonA.pressed(toggleWings)
con.buttonX.pressed(toggleBlocker)
con.buttonUp.pressed(lowerCata)
con.buttonDown.pressed(toggleCata)
con.buttonRight.pressed(rightWing)
con.buttonLeft.pressed(leftWing)

userControl()