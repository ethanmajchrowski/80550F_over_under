# Module:       auton_test.py
# Author:       ethan
# Created:      7/21/2023, 11:53 AM
# Description:  Isolated program to test autonomous functions

# Library imports
from vex import *

# Define generic
brain = Brain()
con = Controller(PRIMARY)

# Define Ports
leftMotorA = Motor(Ports.PORT1, GearSetting.RATIO_6_1, False)
rightMotorA = Motor(Ports.PORT2, GearSetting.RATIO_6_1, True)
rightMotorB = Motor(Ports.PORT3, GearSetting.RATIO_6_1, True)
leftMotorB = Motor(Ports.PORT4, GearSetting.RATIO_6_1, False)
intakeMotor = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)
inertialSens = Inertial(Ports.PORT6)
armMotor = Motor(Ports.PORT7, GearSetting.RATIO_6_1, False)
cataMotor = Motor(Ports.PORT8, GearSetting.RATIO_36_1, True)
liftMotor = Motor(Ports.PORT9, GearSetting.RATIO_36_1, False)

# Create motor groups
leftMotors = MotorGroup(leftMotorA, leftMotorB)
rightMotors = MotorGroup(rightMotorA, rightMotorB)

# 3 wire ports
wingsPistons = DigitalOut(brain.three_wire_port.g)
underglow = DigitalOut(brain.three_wire_port.h)

# Calibrate sensors
inertialSens.calibrate()
brain.screen.print("test")
while inertialSens.is_calibrating():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.print(" Inertial Sensor Calibrating...")
    wait(50, MSEC)
brain.screen.clear_screen()

selecting = True
touch_areas = []
screen_state = "main" # main, test, tools, thermals
selected = None

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
                selected = None
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

brain.screen.released(touch_check)

def screen_update():
    global touch_areas, selecting
    touch_areas = []

    brain.screen.clear_screen()

    if screen_state == "main":
        button(0, 200, 480, 40, "SKIP AUTONOMOUS", Color(Color.RED), action = "skip") # Skip auton button
        button(0,0, 190, 200, "Friendly Goal", Color(32, 120, 0), action = "friendly") # Friendly goal routine
        button(190, 0, 190, 200, "Opponent Goal", Color(112, 0, 0), action = "opponent") # Opponent goal routing
        button(380, 0, 100, 100, "Tools", Color(Color.BLACK), action = "tools") # tools button
        button(380, 100, 100, 100, "SKILLS", Color(Color.WHITE), text_color = Color(Color.BLACK), action = "skills") # skills autonomous
    if screen_state == "test":
        button(200, 100, 100, 50, "skip", action = "skip")
        button(200, 150, 100, 50, "None", action = None)
    if screen_state == "tools":
        button(0, 0, 100, 50, "Main", action = "main_menu", color = Color(82, 82, 82))
        button(0, 50, 100, 190, "Thermals", color = Color(194, 146, 2), action = "thermals")
    if screen_state == "thermals":
        button(0, 0, 100, 30, "Main", action = "main_menu", color = Color(82, 82, 82))

        button(0, 30, 240, 40, ("Left A: " + str(leftMotorA.temperature()))) # left 1
        button(0, 70, 240, 40, ("Left B: " + str(leftMotorB.temperature())))# left 2
        button(0, 110, 240, 40, ("Right A: " + str(rightMotorA.temperature())))# left 3
        button(0, 150, 240, 40, ("Right B: " + str(rightMotorB.temperature())))# left 4
        button(0, 190, 240, 40, ("Intake: " + str(intakeMotor.temperature())))# left 5

        button(240, 30, 240, 40, ("Catapult: " + str(cataMotor.temperature()))) # right 1
        button(240, 70, 240, 40, ("Arm: " + str(armMotor.temperature())))# right 2
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
        # brain.screen.next_row()
        # brain.screen.print("motorAdjustment = ", str(int(motorAdjustment)))
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
    # wait(0.5, SECONDS)

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

def auton(mode):
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.print("Auton Start")
    if mode == None:
        pass
    # opponent goal side (with goal score, done but too slow and illegal)
    # # opponent goal side (take triball out of match load, preload in goal, touch bar, push ball C across, touch elevation)
    # # putting preload in goal may be illegal, need to work on it if possible at all.
    elif False:
        armMotor.spin(REVERSE, 25, PERCENT) # extend arm
        wait(1, SECONDS)
        armMotor.stop() # arm extended
        leftMotors.spin(FORWARD)
        rightMotors.spin(REVERSE) # turn to grab triball
        wait(1500, MSEC)
        leftMotors.stop()
        rightMotors.stop()
        forward(400) # backup to pull triball out
        armMotor.spin(FORWARD, 25, PERCENT) # retract arm
        turn(-110) # turn left
        armMotor.stop() # arm retracted
        forward(530) 
        turn(85)
        intakeMotor.spin(REVERSE, 100, PERCENT)
        forward(150) # into goal    
        forward(-200)
        intakeMotor.stop()
        turn(125) # turn towards elevation zone
        forward(750) # drive towards bar
        turn(-30)
        turn(180)
        forward(-609.6)
        armMotor.spin(REVERSE, 25, PERCENT) # extend arm
        wait(1, SECONDS)
        armMotor.stop() # arm extended    
    # opponent goal side (done, 12 secs)
    elif mode == "opponent":
        armMotor.spin(REVERSE, 25, PERCENT) # extend arm
        wait(1, SECONDS)
        armMotor.stop() # arm extended
        leftMotors.spin(FORWARD)
        rightMotors.spin(REVERSE) # turn to grab triball
        wait(1500, MSEC)
        leftMotors.stop()
        rightMotors.stop()
        forward(400) # backup to pull triball out
        armMotor.spin(FORWARD, 40, PERCENT)
        turn(-50)
        armMotor.stop()
        forward(-470, tolerance=20)
        turn(-70, tolerance=2)
        forward(-480, tolerance=10)
        armMotor.spin(REVERSE, 30, PERCENT)
        wait(1, SECONDS)
        armMotor.stop()   

    # team side (preload in goal, triballs A & B in goal, triball C in goal?, touch elevation)
    # preload in goal (starting 45 to goal)
    elif mode == "friendly":
        forward(730, tolerance = 40, headingAdjust = True, kP = 0.7)
        turn(-35, tolerance = 2)
        forward(200, tolerance = 10)
        intakeMotor.spin(REVERSE, 100, PERCENT)
        forward(-300, tolerance = 10)
        intakeMotor.stop()
        if False: # go grab other triballs (other teammate can touch elevation bar)
            pass
        if False: # go touch elevation bar (teammate cannot but they can remove match load zone)
            turn(45, tolerance = 2)
            forward(-800, tolerance = 40)
            turn(45, tolerance=2)

    # skills
    elif mode == "skills":
        forward(250, tolerance=20)
        turn(-70, tolerance = 5)
        armMotor.spin(REVERSE, 40, PERCENT)
        cataMotor.spin(FORWARD)
        wait(1, SECONDS)
        armMotor.stop()
        wait(99, SECONDS)
        cataMotor.stop(HOLD)

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
        
        wait(50, MSEC)

        brain.screen.render()

startup()
auton(selected)
brain.screen.clear_screen()
brain.screen.set_cursor(1,1)
brain.screen.print("driver time")
brain.screen.render()