#region VEXcode Generated Robot Configuration
from vex import *

# Brain should be defined by default
brain=Brain()

#endregion VEXcode Generated Robot Configuration
from vex import *

#### Define generic ####
brain = Brain()
con = Controller(PRIMARY)

#### Define Ports ####
leftMotorA =  Motor(Ports.PORT16, GearSetting.RATIO_6_1, False)
rightMotorA = Motor(Ports.PORT20, GearSetting.RATIO_6_1, True)
leftMotorB =  Motor(Ports.PORT11, GearSetting.RATIO_6_1, False)
rightMotorB = Motor(Ports.PORT12, GearSetting.RATIO_6_1, True) 
leftMotorC =  Motor(Ports.PORT18, GearSetting.RATIO_6_1, False)
rightMotorC = Motor(Ports.PORT19, GearSetting.RATIO_6_1, True)

intakeMotor = Motor(Ports.PORT15, GearSetting.RATIO_18_1, True)
cataMotor =   Motor(Ports.PORT9, GearSetting.RATIO_36_1, False)
inertialSens = Inertial(Ports.PORT13)
threeWireExtender = Triport(Ports.PORT8)

# Create motor groups
leftMotors =  MotorGroup(leftMotorA, leftMotorB, leftMotorC)
rightMotors = MotorGroup(rightMotorA, rightMotorB, rightMotorC)

# 3 wire ports
frontLeftWingPiston =  DigitalOut(threeWireExtender.d)
frontRightWingPiston = DigitalOut(threeWireExtender.c)
backLeftWingPiston =   DigitalOut(threeWireExtender.a)
backRightWingPiston =   DigitalOut(threeWireExtender.b)
headlightLED =    DigitalOut(threeWireExtender.d)
leftTurnLED =     DigitalOut(threeWireExtender.c)
rightTurnLED =    DigitalOut(threeWireExtender.b)
cataLimit =       Limit(threeWireExtender.f)

# #### Calibrate inertial ####
# inertialSens.calibrate()
# while inertialSens.is_calibrating(): wait(50, MSEC)

#### Drivetrain setup ####
drivetrain = SmartDrive(leftMotors, rightMotors, inertialSens, (2.75 * 3.14) * 25.4, (10.13 * 25.4), (10.5 * 25.4), MM, 1)

#### Variables ####
front_wings_cooldown = 0
back_wings_cooldown = 0

#### Config ####
drivetrain.set_drive_velocity(40, PERCENT)
drivetrain.set_turn_velocity(5, PERCENT)
drivetrain.set_timeout(2, SECONDS)

#### Controls ####
CONTROL_DRIVE_TURN_AXIS =    con.axis1 # used to turn the robot
CONTROL_DRIVE_FORWARD_AXIS = con.axis2 # drives the robot forward (3 for normal, 2 for right stick only)
CONTROL_INTAKE_OUT =         con.buttonR2 # extakes
CONTROL_INTAKE_IN =          con.buttonR1 # intakes
CONTROL_FRONT_WINGS =        con.buttonA # toggles front wings
CONTROL_BACK_WINGS =         con.buttonX # toggle back wings
CONTROL_CATA_TOGGLE =        con.buttonB # toggles the catapult

## overall flow: 
# startup (screen & controller selection)
# comp variable:
    # auton (based on selection)
    # driver control

###################################
########### File Logger ###########
###################################

def log():
    file = open("data/latest.txt", "a")
    # Header: "time, L1 TEMP, L2 TEMP, L3 TEMP, R1 TEMP, R2 TEMP, R3 TEMP"
    # file.write("\n" + str(brain.timer.system()) + ", " +  str(leftMotorA.temperature()) + ", " 
    #            +  str(leftMotorB.temperature()) + ", " + str(leftMotorC.temperature()) + ", " 
    #            +  str(rightMotorA.temperature()) + ", " +  str(rightMotorB.temperature()) 
    #            + ", " + str(rightMotorC.temperature())) # TEMPS
    file.write("\n" + str(brain.timer.system()) + ", " +  str(leftMotorA.velocity()) + ", " 
               +  str(leftMotorB.velocity()) + ", " + str(leftMotorC.velocity()) + ", " 
               +  str(rightMotorA.velocity()) + ", " +  str(rightMotorB.velocity()) 
               + ", " + str(rightMotorC.velocity())) # TEMPS
    file.close()
    brain.timer.event(log, 15)

# File manipulation
def temp_logger():
    # get number of existing files from info.txt
    info_file = open("data/info.txt", "r")
    num_files = int(info_file.read())
    info_file.close()

    # open info and increment number of files
    f = open("data/info.txt", "w")
    f.write(str(num_files + 1))
    f.close()

    # get latest.txt and the new file for archiving
    recent_file = open("data/latest.txt", "r")
    new_file = open("data/" + str(num_files) + ".txt", "w")

    # open new_file to write to it
    new_file.write(recent_file.read())
    recent_file.close()
    new_file.close()

    # clear latest.txt
    f = open("data/latest.txt", "w")
    # f.write("time, L1 TEMP, L2 TEMP, L3 TEMP, R1 TEMP, R2 TEMP, R3 TEMP")
    f.write("time, L1 VOLT, L2 VOLT, L3 VOLT, R1 VOLT, R2 VOLT, R3 VOLT")
    f.close()
    # log data
    log()

###################################
########## Drive Control ##########
###################################

### Press controls
'''
This area should include all button functions that are defined by a control tap
Ex.
    def tap():
        print("tap!")

    con.buttonB.pressed(tap)
'''

#region controls

def toggleCata():
    if cataMotor.command() == 0:
        print("spin cata")
        cataMotor.spin(FORWARD, 100, PERCENT)
    else:
        cataMotor.stop(COAST)
        print("stop cata")

def toggleFrontWings():
    if frontRightWingPiston.value() == True or frontLeftWingPiston.value() == True:
        frontRightWingPiston.set(False)
        frontLeftWingPiston.set(False)
    else:
        frontRightWingPiston.set(True)
        frontLeftWingPiston.set(True)

def toggleBackWings():
    if backRightWingPiston.value() == True or backLeftWingPiston.value() == True:
        backRightWingPiston.set(False)
        backLeftWingPiston.set(False)
    else:
        backRightWingPiston.set(True)
        backLeftWingPiston.set(True)

def frontRightWing():
    frontRightWingPiston.set(not frontRightWingPiston.value())

def frontLeftWing():
    frontLeftWingPiston.set(not frontLeftWingPiston.value())

def backLeftWing():
    backLeftWingPiston.set(not backLeftWingPiston.value())

def backRightWing():
    backRightWingPiston.set(not backRightWingPiston.value())

def intake():
    if intakeMotor.command(PERCENT) != 0:
        if intakeMotor.command(PERCENT) < 0:
            intakeMotor.spin(FORWARD, 100, PERCENT)
        else:
            intakeMotor.stop()
    else:
        intakeMotor.spin(FORWARD, 100, PERCENT)

def extake():
    if intakeMotor.command(PERCENT) != 0:
        if intakeMotor.command(PERCENT) < 0:
            intakeMotor.stop()
        else:
            intakeMotor.spin(REVERSE, 100, PERCENT)
    else:
        intakeMotor.spin(REVERSE, 100, PERCENT)

#endregion controls

### Hold controls
def hold_buttons():
    '''
    This is where all the controls go that are simply 
    "if this button is actively pressed, do this"
    '''
    pass

# Main threads
def cosmetic_thread():
    '''
    Handles all cosmetic / misc things for the drive control (brain screen animations, 
    LED control, etc.). 
    Essentially if you disable this function the robot will still work fine.
    '''
    pass

def control_thread():
    '''
    Handles everything that actually drives the robot. Controls, motor movement, etc.
    '''
    # Button Controls (button.pressed)
    CONTROL_INTAKE_IN.pressed(intake)
    CONTROL_INTAKE_OUT.pressed(extake)
    CONTROL_CATA_TOGGLE.pressed(toggleCata)
    CONTROL_FRONT_WINGS.pressed(toggleFrontWings)
    CONTROL_BACK_WINGS.pressed(toggleBackWings)

    while True:
        # Convert controller axis to voltage levels
        turnVolts = (CONTROL_DRIVE_TURN_AXIS.position() * 0.12) * 0.9
        forwardVolts = CONTROL_DRIVE_FORWARD_AXIS.position() * 0.12

        # Spin motors and combine controller axes
        leftMotorA.spin(FORWARD, forwardVolts + turnVolts, VOLT)
        leftMotorB.spin(FORWARD, forwardVolts + turnVolts, VOLT)
        leftMotorC.spin(FORWARD, forwardVolts + turnVolts, VOLT)
        rightMotorA.spin(FORWARD, forwardVolts - turnVolts, VOLT)
        rightMotorB.spin(FORWARD, forwardVolts - turnVolts, VOLT)
        rightMotorC.spin(FORWARD, forwardVolts - turnVolts, VOLT)

        # hold_buttons()

        sleep(5)

def user_control():
    Thread(control_thread)
    Thread(cosmetic_thread)

user_control()