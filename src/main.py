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

# VARIABLES
intakeStatus = False
intakeDir = "in"
armState = "closed"
gifState = True
selecting = True
touch_areas = []
screen_state = "main" # main, test, tools, thermals

# CONFIG
cataMotor.set_velocity(62, PERCENT)
cataMotor.set_max_torque(100, PERCENT)
intakeMotor.set_velocity(100, PERCENT)

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
            if action == "opponent":
                selected = action
                screen_state = "completed"
            if action == "skills":
                selected = action
                screen_state = "completed"
            if action == "tools": screen_state = action
            if action == "thermals": screen_state = action
            if action == "main_menu": screen_state = "main"
            # if action == "driver":
            #     user_control()
            #     return
            #     # selected = action
            #     # screen_state = "completed"

brain.screen.released(touch_check)

def screen_update():
    global touch_areas, selecting
    touch_areas = []

    brain.screen.clear_screen()

    if screen_state == "main":
        button(0, 160, 480, 80, "SKIP AUTONOMOUS", Color(Color.RED), action = "skip") # Skip auton button
        button(0,0, 190, 160, "Friendly Goal", Color(32, 120, 0), action = "friendly") # Friendly goal routine
        button(190, 0, 190, 160, "Opponent Goal", Color(112, 0, 0), action = "opponent") # Opponent goal routing
        button(380, 0, 100, 50, "Tools", Color(Color.BLACK), action = "tools") # tools button
        button(380, 50, 100, 50, "SKILLS", Color(Color.WHITE), text_color = Color(Color.BLACK), action = "skills") # skills autonomous
    if screen_state == "test":
        button(200, 100, 100, 50, "skip", action = "skip")
        button(200, 150, 100, 50, "None", action = None)
    if screen_state == "tools":
        button(0, 0, 100, 50, "Main", action = "main_menu", color = Color(82, 82, 82))
        button(0, 50, 100, 190, "Thermals", color = Color(194, 146, 2), action = "thermals")
        # button(100, 50, 100, 190, "Driver", color = Color(82, 82, 82), action = "driver")
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
    global selected
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.print("Auton Start")
    if selected == "skip" or None:
        return
    elif selected == "skills":
        return

def user_control():
    brain.screen.print("Driver Control Start")

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
def r1Pressed():
    global intakeStatus, intakeDir
    if intakeStatus == False:
        intakeStatus = True
        intakeDir = "in"
    elif intakeStatus == True and intakeDir == "in":
        intakeStatus = False
    elif intakeStatus == True and intakeDir == "out":
        intakeDir = "in"

def r2Pressed():
    global intakeStatus, intakeDir
    if intakeStatus == False:
        intakeStatus = True
        intakeDir = "out"
    elif intakeStatus == True and intakeDir == "out":
        intakeStatus = False
    elif intakeStatus == True and intakeDir == "in":
        intakeDir = "out"

def toggleWings():
    if wingsPistons.value() == True:
        wingsPistons.set(False)
    else:
        wingsPistons.set(True)

# Assign controller functions
con.buttonR1.pressed(r1Pressed)
con.buttonR2.pressed(r2Pressed)
con.buttonA.pressed(toggleWings)

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
        
        if con.buttonDown.pressing(): cataMotor.spin(FORWARD)
        else: cataMotor.stop(HOLD)
        
        sleep(5)

def printValues():
    global gifState
    gifState = False
    # Display values and stuff on brain screen
    # WHEN PRINTING ON BRAIN COMMENT OUT GIF THREAD OR ADD TEXT TO THREAD
    while True:
        pass

def thread_driveControl():
    while True:
                            
        # Convert controller axis to voltage levels
        if False:
            turnVolts = con.axis1.position() * -0.12
            forwardVolts = con.axis2.position() * -0.12 
        else:
            forwardVolts = con.axis1.position() * -0.12 
            turnVolts = con.axis3.position() * -0.12
        # Spin motors and combine controller axes
        leftMotorA.spin(FORWARD, forwardVolts + turnVolts, VOLT)
        leftMotorB.spin(FORWARD, forwardVolts + turnVolts, VOLT)
        leftMotorC.spin(FORWARD, forwardVolts + turnVolts, VOLT)
        rightMotorA.spin(FORWARD, forwardVolts - turnVolts, VOLT)
        rightMotorB.spin(FORWARD, forwardVolts - turnVolts, VOLT)
        rightMotorC.spin(FORWARD, forwardVolts - turnVolts, VOLT)
        sleep(5)    
        # brain.screen.render()

def gifThread():
    index = 1
    while True:
        if gifState:
            brain.screen.clear_screen()
            # brain.screen.set_cursor(1,1)
            # brain.screen.print(("fractal (" + str(index) + ")"))
            brain.screen.draw_image_from_file(("fractal (" + str(index) + ").png"), 0, 0)
            if index < 29:
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
    #Thread(printValues)

# startup()
# auton()
userControl()
# comp = Competition(userControl, auton)