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
inertialSens = Inertial(Ports.PORT19)
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

headlightLED = DigitalOut(threeWireExtender.d)
leftTurnLED = DigitalOut(threeWireExtender.c)
rightTurnLED = DigitalOut(threeWireExtender.b)

# Calibrate sensors
inertialSens.calibrate()
while inertialSens.is_calibrating():
    wait(50, MSEC)
brain.screen.clear_screen()

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

# CONFIG
cataMotor.set_velocity(62, PERCENT)
cataMotor.set_max_torque(100, PERCENT)
intakeMotor.set_velocity(100, PERCENT)
headlightLED.set(True)

leftTurnLED.set(True)
rightTurnLED.set(True)

def button(x, y, width, height, text = "", color = Color(Color.BLACK), text_color = Color(Color.WHITE), action = None): # usable size of brain is 480x240
    brain.screen.set_fill_color(color)
    brain.screen.draw_rectangle(x, y, width, height)
    string_width = brain.screen.get_string_width(text)
    brain.screen.set_pen_color(text_color)
    brain.screen.print_at(text, x = (x + (width / 2)) - (string_width / 2), y = (y + (height * 0.5)))
    touch_areas.append((x,y,width,height,action))
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.set_fill_color(Color.BLACK)

def touch_check():
    global screen_state, selected
    touch_x = brain.screen.x_position()
    touch_y = brain.screen.y_position()

    for area in touch_areas:
        x, y, width, height, action = area[0], area[1], area[2], area[3], area[4]
        if (x < touch_x < x + width) and (y < touch_y < y + height): # if button is touched
            print("touched button with action ", action)
            if action == None:
                break
            if action == "skip":
                selected = action
                screen_state = "completed"
            if action == "friendly":
                selected = action
                screen_state = "completed"
            if action == "close":
                selected = action
                screen_state = "completed"
            if action == "skills":
                selected = action
                screen_state = "completed"
            if action == "skip_comp_driver": 
                selected = action
                screen_state = "completed"
            if action == "skip_comp_close_auton":
                selected = action
                screen_state = "completed"
            if action == "skip_comp_far_auton":
                selected = action
                screen_state = "completed"
            if action == "skip_comp_skills_auton":
                selected = action
                screen_state = "completed"

            if action == "tools": screen_state = action
            if action == "thermals": screen_state = action
            if action == "main_menu": screen_state = "main"

brain.screen.released(touch_check)

def screen_update():
    global touch_areas, selecting
    touch_areas = []

    brain.screen.clear_screen()

    if screen_state == "main":
        button(0, 160, 480, 80, "SKIP AUTONOMOUS", Color(Color.RED), action = "skip") # Skip auton button
        button(0,0, 190, 160, "Far (Friendly)", Color(32, 120, 0), action = "friendly") # Friendly goal routine
        button(190, 0, 190, 160, "Close (opponent)", Color(112, 0, 0), action = "close") # Opponent goal routing
        button(380, 0, 100, 50, "Tools", Color(Color.BLACK), action = "tools") # tools button
        button(380, 50, 100, 50, "SKILLS", Color(Color.WHITE), text_color = Color(Color.BLACK), action = "skills") # skills autonomous
    if screen_state == "test":
        button(200, 100, 100, 50, "skip", action = "skip")
        button(200, 150, 100, 50, "None", action = None)
    if screen_state == "tools":
        button(0, 0, 100, 50, "Main", action = "main_menu", color = Color(82, 82, 82))
        button(0, 50, 100, 190, "Thermals", color = Color(194, 146, 2), action = "thermals")
        button(100, 50, 100, 190, "Driver", color = Color(82, 82, 82), action = "skip_comp_driver")
        button(200, 50, 100, 190, "Close", color = Color(82, 82, 82), action = "skip_comp_close_auton")
        button(300, 50, 100, 190, "Far", color = Color(82, 82, 82), action = "skip_comp_far_auton")
        button(400, 50, 100, 190, "Skills", color = Color(82, 82, 82), action = "skip_comp_skills_auton")
    if screen_state == "thermals":
        button(0, 0, 100, 30, "Main", action = "main_menu", color = Color(82, 82, 82))

        button(0, 30, 240, 40, ("Left A: " + str(leftMotorA.temperature()))) # left 1
        button(0, 70, 240, 40, ("Left B: " + str(leftMotorB.temperature())))# left 2
        button(0, 110, 240, 40, ("Right A: " + str(rightMotorA.temperature())))# left 3
        button(0, 150, 240, 40, ("Right B: " + str(rightMotorB.temperature())))# left 4
        button(0, 190, 240, 40, ("Intake: " + str(intakeMotor.temperature())))# left 5

        button(240, 30, 240, 40, ("Catapult: " + str(cataMotor.temperature()))) # right 1
        # button(240, 110, 240, 40, "None: 55*C")# right 3
        # button(240, 150, 240, 40, "None: 55*C")# right 4
        # button(240, 190, 240, 40, "motor: 55*C")# right 5
    if screen_state == "completed":
        brain.screen.set_cursor(1,1)
        brain.screen.print("Selected: ", selected)
        selecting = False
        # if selected == "close":
        #     while(not cataLimit.pressing()):
        #         cataMotor.spin(FORWARD, 60, PERCENT)
        #     cataMotor.stop(HOLD)

    brain.screen.render()

def startup():
    brain.screen.print("Startup - gui.py")
    wait(50, MSEC)
    brain.screen.clear_screen()

    while selecting:
        screen_update()
    wait(1, SECONDS)

def forward(dist = 609.6, kP = 0.1, tolerance = 5, headingAdjust = True):
    # wait(0.5, SECONDS)
    dist *= -1
    degrees = (dist * 1.125)
    degrees /= (3/7)
    initialHeading = inertialSens.heading()

    leftMotorA.reset_position()
    currentDegrees = leftMotorA.position()

    while ((currentDegrees > (degrees + tolerance)) or (currentDegrees < (degrees - tolerance))):
        currentDegrees = leftMotorA.position()

        error = degrees - currentDegrees
        speed = error * kP
        if speed > 100: speed = 100

        currentHeading = inertialSens.heading()
        headingError = abs(initialHeading - currentHeading)
        if headingError > 180:
            headingError = -360 + headingError
        # if initialHeading > 180:
        #     if headingError > 180: headingError = 360 - headingError

        motorAdjustment = headingError * kP * 10
        if headingAdjust:
            leftSpeed = speed - motorAdjustment
            rightSpeed = speed + motorAdjustment
        else:
            leftSpeed = speed
            rightSpeed = speed

        brain.screen.clear_screen()
        brain.screen.set_cursor(1,1)
        brain.screen.print("initialHeading = ", str(int(initialHeading)))
        brain.screen.next_row()
        brain.screen.print("current heading = ", str(int(currentHeading)))
        brain.screen.next_row()
        brain.screen.print("heading error = ", str(int(headingError)))

        brain.screen.next_row()
        brain.screen.print("left/right speeds = ", str(int(leftSpeed)), str(int(rightSpeed)))
        brain.screen.next_row()
        brain.screen.print("distance error = ", str(int(error)))
        brain.screen.render()

        leftMotors.spin(FORWARD, leftSpeed, PERCENT)
        rightMotors.spin(FORWARD, rightSpeed, PERCENT)

    leftMotors.stop()
    rightMotors.stop()

def turn(degrees, speed = 5, tolerance = 0.5, kP = 0.4):
    brain.screen.clear_screen()
    brain.screen.set_cursor(2, 1)    
    brain.screen.print("turn ", degrees)

    initialHeading = inertialSens.heading()
   
    targetHeading = initialHeading + degrees # set intial value, can by any value

    while (targetHeading > 360) or (targetHeading < 0): # repeatedly iterate until heading is in bounds
        if targetHeading > 360: # if greater than 360 then subtract 360
            targetHeading -= 360
        if targetHeading < 0: # if less than 0 add 360
            targetHeading += 360
    
    brain.screen.next_row()
    brain.screen.print("refined target:", targetHeading)
    
    if degrees < 0: # left turn until the heading is at target w/tolerance
        while (targetHeading - tolerance) > (inertialSens.heading()) or (targetHeading + tolerance) < (inertialSens.heading()):
            error = abs(targetHeading - inertialSens.heading())
            if error > 180:
                error = (360 - error)

            speed = error * kP
            if speed < 5:
                speed = 5

            # if speed > 100:
            #     speed = 100
            # if speed < 0:
            #     speed *= -1
            
            brain.screen.clear_row(4)
            brain.screen.set_cursor(4,1)
            brain.screen.print("heading: ", inertialSens.heading())
            brain.screen.clear_row(5)
            brain.screen.set_cursor(5,1)
            brain.screen.print("error: ",error)
            brain.screen.clear_row(6)
            brain.screen.set_cursor(6,1)
            brain.screen.print("speed: ", speed)
            brain.screen.render()

            rightMotors.spin(REVERSE, speed, PERCENT)
            leftMotors.spin(FORWARD, speed, PERCENT)

    else: # right turn
        while (targetHeading - tolerance) > (inertialSens.heading()) or (targetHeading + tolerance) < (inertialSens.heading()):
            error = abs(targetHeading - inertialSens.heading())
            if error > 180:
                error = (360 - error)
            speed = error * kP

            if speed < 5:
                speed = 5

            # if speed > 100:
            #     speed = 100

            brain.screen.clear_row(4)
            brain.screen.set_cursor(4,1)
            brain.screen.print("heading: ", inertialSens.heading())
            brain.screen.clear_row(5)
            brain.screen.set_cursor(5,1)
            brain.screen.print("error: ",error)
            brain.screen.clear_row(6)
            brain.screen.set_cursor(6,1)
            brain.screen.print("speed: ", speed)
            brain.screen.render()

            rightMotors.spin(FORWARD, speed, PERCENT)
            leftMotors.spin(REVERSE, speed, PERCENT)
    
    rightMotors.stop()
    leftMotors.stop()

def auton():    
    headlightLED.set(False)
    leftTurnLED.set(False)
    rightTurnLED.set(False)
    if selected == "skip" or None:
        return
    elif selected == "skills":
        cataMotor.spin(FORWARD, 62, PERCENT) # catapult match loads
        wait(30, SECONDS)
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

    # elif selected == "close":
    #     rightWingPiston.set(True)
    #     wait(0.5, SECONDS)
    #     drivetrain.turn_for(LEFT, 115, DEGREES, 10, PERCENT)
    #     wait(0.5, SECONDS)
    #     # while not cataLimit.pressing():
    #     #     cataMotor.spin(FORWARD, 100, PERCENT)
    #     cataMotor.spin(FORWARD, 100, PERCENT)
    #     wait(0.7, SECONDS)
    #     cataMotor.stop(HOLD)
    #     rightWingPiston.set(False)
    #     drivetrain.turn_to_heading(285, DEGREES)
    #     drivetrain.drive_for(FORWARD, 450, MM)
    #     drivetrain.turn_to_heading(270, DEGREES)
    #     drivetrain.drive_for(FORWARD, 550, MM)
    #     intakeMotor.spin(FORWARD, 100, PERCENT)
    #     wait(1.5, SECONDS)
    #     intakeMotor.stop()
    #     wait(1, SECONDS)
    #     drivetrain.stop(COAST)
    #     rightWingPiston.set(False)
    #     leftWingPiston.set(False)
        
    elif selected == "close":
        brain.timer.reset()
        cataMotor.spin(FORWARD, 100)
        while not cataLimit.pressing():
            pass
        wait(0.2, SECONDS)
        cataMotor.spin(FORWARD, 40)
        while not cataLimit.pressing():
            pass
        cataMotor.stop(HOLD)
        drivetrain.turn_for(RIGHT, 115, DEGREES, 10, PERCENT) # Turn right to setup to pull triball out of match load
        rightWingPiston.set(True) # Lower wing to shove triball
        wait(0.3, SECONDS) # Wait for wing to lower
        drivetrain.turn_for(LEFT, 75, DEGREES, 20, PERCENT) # Turn to shove triball out of match load area
        rightWingPiston.set(False) # Retract wing to not clip wall
        wait(0.5, SECONDS) # Wait for wing retraction
        drivetrain.drive_for(FORWARD, 270, MM) # 
        drivetrain.turn_to_heading(30, DEGREES) # Turn to adjust for underpass
        intakeMotor.spin(FORWARD, 100, PERCENT)
        drivetrain.drive_for(FORWARD, 630, MM) #
        drivetrain.drive_for(FORWARD, 20, MM, 10, PERCENT)
        wait(3, SECONDS)
        intakeMotor.stop()
        print("done at ", brain.timer.time(SECONDS), "s")

    if selected == "friendly":
        drivetrain.drive_for(FORWARD, 100, MM)
        rightWingPiston.set(True)
        drivetrain.drive_for(FORWARD, 150, MM)
        drivetrain.turn_for(LEFT, 45)
        drivetrain.drive_for(FORWARD, 540, MM, 60, PERCENT)
        rightWingPiston.set(False)
        wait(0.1, SECONDS)
        drivetrain.drive_for(REVERSE, 240, MM)
        drivetrain.turn_to_heading(250, DEGREES)
        intakeMotor.spin(REVERSE, 100, PERCENT)
        drivetrain.drive_for(FORWARD, 1000, MM, 70, PERCENT)
        drivetrain.turn_to_heading(45, DEGREES)
        intakeMotor.stop()
        drivetrain.drive_for(FORWARD, 400, MM, 80, PERCENT)
        leftWingPiston.set(True)
        drivetrain.turn_for(RIGHT, 60, DEGREES)
        intakeMotor.spin(FORWARD, 100, PERCENT)
        drivetrain.drive_for(FORWARD, 650, MM, 80, PERCENT)
        drivetrain.drive_for(REVERSE, 200, MM, 80, PERCENT)
 
        wait(1, SECONDS)
        intakeMotor.stop()
        drivetrain.stop(COAST)
        leftWingPiston.set(False)

    headlightLED.set(True)
    leftTurnLED.set(True)
    rightTurnLED.set(True)

def inertValuesThread():
    timer = Timer()
    while True:
        brain.screen.clear_row(1)
        brain.screen.set_cursor(1,1)

        brain.screen.print("Heading: ", inertialSens.heading(), " degrees")
        brain.screen.next_row()
        brain.screen.print("Acceleration: ", inertialSens.acceleration(XAXIS), inertialSens.acceleration(YAXIS), inertialSens.acceleration(ZAXIS))
        brain.screen.next_row()
        brain.screen.print("Acceleration m/s^2: ", inertialSens.acceleration(XAXIS) * 9.8, inertialSens.acceleration(ZAXIS) * 9.8) # type:ignore
        # brain.screen.next_row()
        # brain.screen.print("time since last call:", timer.time())
        # timer.reset()
        
        wait(50, MSEC)

        brain.screen.render()

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
        cataMotor.spin(FORWARD, 40)
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

        if selected != "skip_comp_driver":
            if con.buttonDown.pressing(): 
                cataMotor.spin(FORWARD)
            else: 
                cataMotor.stop(HOLD)
        
        sleep(5)

def toggleCata():
    print("toggle cata")
    global cataState
    cataState = not cataState
    if cataState: cataMotor.spin(FORWARD, 90, PERCENT)
    else: cataMotor.stop(HOLD)

def thread_driveControl():
    global ledState
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
            ledState = not ledState

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
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.print("Driver Control Start")
    wait(0.1, SECONDS)
    
    Thread(gifThread)
    Thread(thread_main)
    Thread(thread_driveControl)

headlightLED.set(True)
leftTurnLED.set(True)
rightTurnLED.set(True)
wait(0.5, SECONDS)
headlightLED.set(False)
leftTurnLED.set(False)
rightTurnLED.set(False)

startup()

# Assign controller functions
con.buttonR1.pressed(r1Pressed)
con.buttonR2.pressed(r2Pressed)
con.buttonA.pressed(toggleWings)
con.buttonX.pressed(toggleBlocker)
con.buttonUp.pressed(lowerCata)
con.buttonDown.pressed(toggleCata)
con.buttonRight.pressed(rightWing)
con.buttonLeft.pressed(leftWing)

if selected == "skip_comp_driver": # skip competition for testing
    userControl()
elif selected == "skip_comp_close_auton":
    selected = "close"
    auton()
elif selected == "skip_comp_far_auton":
    selected = "friendly"
    auton()
elif selected == "skip_comp_skills_auton":
    selected = "skills"
    auton()

comp = Competition(userControl, auton)