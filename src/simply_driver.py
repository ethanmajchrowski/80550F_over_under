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
rightMotorA = Motor(Ports.PORT17, GearSetting.RATIO_6_1, True)
leftMotorB =  Motor(Ports.PORT11, GearSetting.RATIO_6_1, False)
rightMotorB = Motor(Ports.PORT12, GearSetting.RATIO_6_1, True) 
leftMotorC =  Motor(Ports.PORT18, GearSetting.RATIO_6_1, False)
rightMotorC = Motor(Ports.PORT19, GearSetting.RATIO_6_1, True)

intakeMotor = Motor(Ports.PORT15, GearSetting.RATIO_18_1, True)
cataMotor =   Motor(Ports.PORT9, GearSetting.RATIO_36_1, False)
inertialSens = Inertial(Ports.PORT14)
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

#### Calibrate inertial ####
inertialSens.calibrate()
while inertialSens.is_calibrating(): wait(50, MSEC)

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
CONTROL_DRIVE_FORWARD_AXIS = con.axis2 # drives the robot forward (3 for normal, 2 for right)
CONTROL_INTAKE_OUT =         con.buttonR2 # extakes
CONTROL_INTAKE_IN =          con.buttonR1 # intakes
CONTROL_FRONT_WINGS =        con.axis3 # toggles front wings
CONTROL_BACK_WINGS =         con.axis3 # toggle back wings
CONTROL_BACK_LEFT_WING =     con.buttonLeft # toggles the left wing
CONTROL_BACK_RIGHT_WING =    con.buttonRight # toggles the right wing
CONTROL_FRONT_LEFT_WING =    con.buttonY # toggles the left wing
CONTROL_FRONT_RIGHT_WING =   con.buttonA # toggles the right wing
CONTROL_CATA_TOGGLE =        con.buttonB # toggles the catapult

## overall flow: 
# startup (screen & controller selection)
# comp variable:
    # auton (based on selection)
    # driver control

###################################
#### Startup / Auton Selection ####
###################################
# usable size of brain is 480x240 pixels
#### Classes ####

class autonSelector():
    '''
    Handles the auton selection code including menus, 
    buttons, and finalizing the autonomous selection.
    '''
    def __init__(self, initial_screen) -> None:
        self.touch_areas = []
        self.selecting = True
        self.screen_state = initial_screen
    
    def button(self, x: int, y: int, width: int, height: int, text: str, 
               color = Color(Color.BLACK), text_color = Color(Color.WHITE), 
               action = None, end_selection = True) -> None: 
        '''
        Draws a button on the brain screen at the specified coordinates
        with the specified text.

        Args:
            x (int): the x position for the top left corner
            y (int): the y position for the top left corner
            width (int): the width of the button (left -> right)
            height (int): the height of the button (top -> bottom)
            color (Color): the fill color of the button
            text_color (Color): the color of the text
            action (str): The action to be added to touch_areas when the button is pressed
            end_selection (bool): Wether or not to end auton selection when this button is pressed

        Returns:
            none
        '''
        string_width = brain.screen.get_string_width(text)
        
        brain.screen.set_fill_color(color)
        brain.screen.draw_rectangle(x, y, width, height)
        brain.screen.set_pen_color(text_color)
        brain.screen.print_at(text, x = (x + (width / 2)) - (string_width / 2), y = (y + (height * 0.5)))
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.set_fill_color(Color.BLACK)

        self.touch_areas.append((x, y, width, height, action, end_selection))

    def onTouch(self):
        '''
        Function to be called when the brain is touched. 
        If the screen is to be changed, screen state is set to the button's action.
        If the screen is not changed, auton has been selected and screen state is set to "completed"
        '''
        touch_x = brain.screen.x_position()
        touch_y = brain.screen.y_position()

        for area in self.touch_areas:
            x, y, width, height, action, end_selection = area[0], area[1], area[2], area[3], area[4], area[5]
            if (x < touch_x < x + width) and (y < touch_y < y + height): # if button is touched
                print("Touched button with action", action)
                if not end_selection:
                    self.screen_state = action
                else:
                    brain.screen.clear_screen()
                    self.selecting = False
                    self.screen_state = "completed"
                    self.selected = action
                # Redraw buttons for new screen
                self.drawButtons(self.screen_state)

    def drawButtons(self, screen: str):
        '''
        Function to draw the buttons on the screen. All buttons to be drawn on screen should
        be listed under the if statement for that screen.

        Args:
            screen (str): The screen to be drawn
        
        Returns: 
            void
        '''
        brain.screen.clear_screen()
        self.touch_areas = []
        if screen == "main":
            self.button(0, 160, 480, 80, "SKIP AUTONOMOUS", Color(Color.RED), action = "skip") # Skip auton button
            self.button(0,0, 190, 160, "Far (Friendly)", Color(32, 120, 0), action = "far")
            self.button(190, 0, 190, 160, "Close (opponent)", Color(112, 0, 0), action = "close")
            self.button(380, 0, 100, 50, "Tools", Color(Color.BLACK), action = "tools", end_selection=False) # tools button
            self.button(380, 50, 100, 50, "SKILLS", Color(Color.WHITE), text_color = Color(Color.BLACK), action = "skills") # skills autonomous
        if screen == "test":
            self.button(200, 100, 100, 50, "skip", action = "skip")
            self.button(200, 150, 100, 50, "None", action = None)
        if screen == "tools":
            self.button(0, 0, 100, 50, "Main", action = "main", color = Color(82, 82, 82), end_selection=False)
            self.button(0, 50, 100, 190, "Thermals", color = Color(194, 146, 2), action = "thermals", end_selection=False)
            self.button(100, 50, 100, 190, "Driver", color = Color(82, 82, 82), action = "skip_comp_driver")
            self.button(200, 50, 100, 190, "Close", color = Color(82, 82, 82), action = "skip_comp_close_auton")
            self.button(300, 50, 100, 190, "Far", color = Color(82, 82, 82), action = "skip_comp_far_auton")
            self.button(400, 50, 100, 190, "Skills", color = Color(82, 82, 82), action = "skip_comp_skills_auton")
        if screen == "thermals":
            self.button(0, 0, 100, 30, "Main", action = "main", color = Color(82, 82, 82), end_selection=False)

            self.button(0, 30, 240, 40, ("Left A: " + str(leftMotorA.temperature()))) # left 1
            self.button(0, 70, 240, 40, ("Left B: " + str(leftMotorB.temperature())))# left 2
            self.button(0, 110, 240, 40, ("Right A: " + str(rightMotorA.temperature())))# left 3
            self.button(0, 150, 240, 40, ("Right B: " + str(rightMotorB.temperature())))# left 4
            self.button(0, 190, 240, 40, ("Intake: " + str(intakeMotor.temperature())))# left 5

            self.button(240, 30, 240, 40, ("Catapult: " + str(cataMotor.temperature()))) # right 1
            # self.button(240, 110, 240, 40, "None: 55*C")# right 3
            # self.button(240, 150, 240, 40, "None: 55*C")# right 4
            # self.button(240, 190, 240, 40, "motor: 55*C")# right 5
        elif screen == "completed":
            brain.screen.set_cursor(1,1)
            brain.screen.set_font(FontType.MONO30)
            brain.screen.print("SELECTED:", self.selected)
            brain.screen.new_line()
        brain.screen.render()

    def run(self):
        while self.selecting:
            self.drawButtons(self.screen_state)

###################################
########## Autonomous #############
###################################

def auton():    
    brain.timer.clear()
    if isinstance(selector, autonSelector):
        if selector.selected == "skip" or None:
            return

        elif selector.selected == "skills" or selector.selected == "skip_comp_skills_auton":
            inertialSens.reset_heading()

            drivetrain.set_timeout(2, SECONDS)
            drivetrain.set_turn_constant(0.28)
            drivetrain.set_turn_threshold(0.25)

            drivetrain.stop(HOLD)
            cataMotor.spin(FORWARD, 95)
            wait(2, SECONDS) # normal 27
            # while not cataLimit.pressing():
            #     cataMotor.spin(FORWARD, 25, PERCENT)
            cataMotor.stop(HOLD)
            drivetrain.stop(COAST)
            wait(0.1, SECONDS)

            drivetrain.turn_to_heading(90, DEGREES, 40, PERCENT)
            print("Error: ", 90 - inertialSens.heading())

            drivetrain.drive_for(REVERSE, 700, MM, 50, PERCENT)
            wait(0.2, SECONDS)
            drivetrain.drive_for(FORWARD, 800, MM, 50, PERCENT)

            intakeMotor.spin(FORWARD, 100, PERCENT)
            wait(0.1, SECONDS)
            drivetrain.turn_to_heading(32, DEGREES, 40, PERCENT)
            print("Error: ", 32 - inertialSens.heading())

            drivetrain.drive_for(FORWARD, 2050, MM, 80, PERCENT)

            intakeMotor.stop()

            wait(0.1, SECONDS)
            drivetrain.turn_to_heading(0, DEGREES, 40, PERCENT)
            print("Error: ", 0 - inertialSens.heading())

            drivetrain.drive_for(FORWARD, 650, MM, 50, PERCENT)

            drivetrain.turn_to_heading(310, DEGREES, 40, PERCENT)
            print("Error: ", 310 - inertialSens.heading())

            intakeMotor.spin(REVERSE, 100, PERCENT)
            drivetrain.drive_for(FORWARD, 400, MM, 50, PERCENT)
            wait(0.2, SECONDS)
            drivetrain.drive_for(REVERSE, 200, MM, 50, PERCENT)
            intakeMotor.stop()
            wait(0.1, SECONDS)
            drivetrain.turn_to_heading(235, DEGREES, 40, PERCENT)
            print("Error: ", 235 - inertialSens.heading())

            drivetrain.drive_for(FORWARD, 1200, MM, 60, PERCENT)
            wait(0.1, SECONDS)

            drivetrain.turn_to_heading(0, DEGREES, 40, PERCENT)
            print("Error: ", 0 - inertialSens.heading())

            frontLeftWingPiston.set(True)
            frontRightWingPiston.set(True)
            wait(0.2, SECONDS)
            intakeMotor.spin(REVERSE, 100, PERCENT)
            drivetrain.drive_for(FORWARD, 900, MM, 70, PERCENT) # Front push into goal

            frontLeftWingPiston.set(False)
            frontRightWingPiston.set(False)
            intakeMotor.stop()
            drivetrain.drive_for(REVERSE, 600, MM, 70, PERCENT)
            wait(0.1, SECONDS)

            frontLeftWingPiston.set(True)
            frontRightWingPiston.set(True)
            intakeMotor.spin(REVERSE, 100, PERCENT)
            drivetrain.drive_for(FORWARD, 900, MM, 70, PERCENT) # Front push into goal

            frontLeftWingPiston.set(False)
            frontRightWingPiston.set(False)
            intakeMotor.stop()
            wait(0.1, SECONDS)
            drivetrain.drive_for(REVERSE, 700, MM, 70, PERCENT)

            drivetrain.turn_to_heading(295, DEGREES, 40, PERCENT)
            print("Error: ", 20 - inertialSens.heading())
                
            drivetrain.drive_for(FORWARD, 1000, MM, 70, PERCENT)
            drivetrain.turn_to_heading(80, DEGREES, 40, PERCENT)
            frontLeftWingPiston.set(True)
            frontRightWingPiston.set(True)
            wait(0.1, SECONDS)
            drivetrain.drive_for(FORWARD, 600, MM , 70, PERCENT)
            drivetrain.turn_to_heading(50, DEGREES)
            wait(0.1, SECONDS)
            intakeMotor.spin(REVERSE, 100, PERCENT)
            wait(0.2, SECONDS)
            drivetrain.drive_for(FORWARD, 500, MM , 70, PERCENT)
            wait(0.2, SECONDS)
            drivetrain.drive_for(REVERSE, 200, MM , 70, PERCENT)
            wait(0.2, SECONDS)
            intakeMotor.stop()
            frontLeftWingPiston.set(False)
            frontRightWingPiston.set(False)

            print("Inertial heading: ", inertialSens.heading())
            con.screen.print(inertialSens.heading())
            print("Remaining time: ", 60 - brain.timer.time(SECONDS) - 28, "s")

        elif selector.selected == "close" or selector.selected == "skip_comp_close_auton":
            drivetrain.set_timeout(2, SECONDS)
            drivetrain.set_turn_constant(0.28)
            drivetrain.set_turn_threshold(0.25)
            cataMotor.spin(FORWARD, 100)
            wait(.5,SECONDS)
            cataMotor.stop()
            drivetrain.turn_for(RIGHT, 115, DEGREES, 10, PERCENT) # Turn right to setup to pull triball out of match load
            frontRightWingPiston.set(True) # Lower wing to shove triball
            wait(0.3, SECONDS) # Wait for wing to lower
            drivetrain.turn_for(LEFT, 90, DEGREES, 20, PERCENT) # Turn to shove triball out of match load area
            frontRightWingPiston.set(False) # Retract wing to not clip wall
            wait(0.5, SECONDS) # Wait for wing retraction
            drivetrain.turn_to_heading(50, DEGREES)
            drivetrain.drive_for(FORWARD, 270, MM) # 
            drivetrain.turn_to_heading(30, DEGREES) # Turn to adjust for underpass
            intakeMotor.spin(FORWARD, 100, PERCENT)
            drivetrain.drive_for(FORWARD, 630, MM) #
            drivetrain.drive_for(FORWARD, 20, MM, 10, PERCENT)
            wait(3, SECONDS)
            intakeMotor.stop()

        elif selector.selected == "far" or selector.selected == "skip_comp_far_auton":
            drivetrain.set_timeout(2, SECONDS)
            drivetrain.set_turn_constant(0.28)
            drivetrain.set_turn_threshold(.5)
            drivetrain.set_turn_velocity(50, PERCENT)
            drivetrain.set_drive_velocity(60, PERCENT)

            drivetrain.drive_for(FORWARD, 100, MM)
            frontRightWingPiston.set(True)
            wait(.6, SECONDS)
            drivetrain.drive_for(FORWARD, 380, MM, 30, PERCENT)

            frontRightWingPiston.set(False)
            drivetrain.turn_for(LEFT, 50, DEGREES)
            drivetrain.turn_for(LEFT, 150, DEGREES)
            drivetrain.drive_for(REVERSE, 600, MM, 100, PERCENT)
            drivetrain.drive_for(FORWARD, 240, MM)
            drivetrain.turn_to_heading(237, DEGREES)
            intakeMotor.spin(REVERSE, 100, PERCENT)
            drivetrain.drive_for(FORWARD, 1200, MM, 70, PERCENT)
            drivetrain.turn_to_heading(0, DEGREES)
            intakeMotor.spin(FORWARD, 120, PERCENT)
            drivetrain.drive_for(FORWARD, 300, MM, 50, PERCENT)
            drivetrain.turn_to_heading(272, DEGREES)
            intakeMotor.spin(REVERSE, 100, PERCENT)
            drivetrain.drive_for(FORWARD, 650, MM, 80, PERCENT)
            drivetrain.turn_to_heading(45, DEGREES)
            frontLeftWingPiston.set(True)
            frontRightWingPiston.set(True)
            intakeMotor.spin(FORWARD, 100, PERCENT)
            drivetrain.drive_for(FORWARD, 1200, MM, 100, PERCENT)
            drivetrain.drive_for(REVERSE, 200, MM)
            intakeMotor.stop()


            # intakeMotor.spin(REVERSE, 100, PERCENT)
            # wait(.5,SECONDS)
            # drivetrain.drive_for(FORWARD, 90, MM)
            # wait(.2,SECONDS)
            # drivetrain.drive_for(REVERSE, 110, MM)
            # drivetrain.turn_to_heading(170, DEGREES)
            # intakeMotor.stop()
            # drivetrain.drive_for(FORWARD, 850, MM, 100, PERCENT)
            # drivetrain.turn_to_heading(135, DEGREES)
            # frontRightWingPiston.set(True)
            # intakeMotor.spin(FORWARD, 100, PERCENT)
            # drivetrain.drive_for(FORWARD, 550, MM)
            # drivetrain.turn_for(LEFT, 200, DEGREES)
            # frontRightWingPiston.set(False)
            # drivetrain.drive_for(REVERSE, 400, MM, 60, PERCENT)
            # intakeMotor.stop()
            # drivetrain.drive_for(FORWARD, 300, MM, 60, PERCENT)

            # drivetrain.turn_to_heading(238, DEGREES)
            # intakeMotor.spin(REVERSE, 100, PERCENT)
            # drivetrain.drive_for(FORWARD, 1550, MM, 60, PERCENT)
            # drivetrain.turn_to_heading(15, DEGREES)
            # intakeMotor.spin(FORWARD, 100, PERCENT)
            # drivetrain.drive_for(FORWARD, 300, MM)
            # drivetrain.turn_to_heading(38, DEGREES)
            # intakeMotor.spin(REVERSE, 100, PERCENT)
            # drivetrain.drive_for(FORWARD, 700, MM)
            # drivetrain.turn_to_rotation(180, DEGREES)
            # frontRightWingPiston.set(True)
            # frontLeftWingPiston.set(True)
            # intakeMotor.spin(FORWARD, 100, PERCENT)
            # drivetrain.drive_for(FORWARD, 900, MM)
            # drivetrain.drive_for(REVERSE, 200, MM)

        elif selector.selected == "test":
            drivetrain.drive_for(FORWARD, 600, MM, 20, PERCENT)

    print("Time taken:", brain.timer.value(), "s")

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
    # global front_wings_cooldown
    # if front_wings_cooldown > 0: front_wings_cooldown -= 1
    # if CONTROL_FRONT_WINGS.position() > 10 and front_wings_cooldown == 0:
    #     if frontLeftWingPiston.value():
    #         frontLeftWingPiston.set(False)
    #         frontRightWingPiston.set(False)
    #     else:
    #         frontLeftWingPiston.set(True)
    #         frontRightWingPiston.set(True)
    #     front_wings_cooldown = 30
    # print(front_wings_cooldown)
    if CONTROL_FRONT_WINGS.position() > 10:
        frontLeftWingPiston.set(True)
        frontRightWingPiston.set(True)
    else:
        frontLeftWingPiston.set(False)
        frontRightWingPiston.set(False)

    if CONTROL_BACK_WINGS.position() < -10:
        backLeftWingPiston.set(True)
        backRightWingPiston.set(True)
    else:
        backLeftWingPiston.set(False)
        backRightWingPiston.set(False)
        

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
    # CONTROL_FRONT_WINGS.pressed(toggleFrontWings)
    # CONTROL_BACK_WINGS.pressed(toggleBackWings)
    CONTROL_BACK_LEFT_WING.pressed(backLeftWing) 
    CONTROL_BACK_RIGHT_WING.pressed(backRightWing) 
    CONTROL_FRONT_LEFT_WING.pressed(frontLeftWing)
    CONTROL_FRONT_RIGHT_WING.pressed(frontRightWing)


    while True:
        # Convert controller axis to voltage levels
        turnVolts = CONTROL_DRIVE_TURN_AXIS.position() * 0.12
        # turnVolts = CONTROL_DRIVE_FORWARD_AXIS.position() * -0.12 * 0.75
        forwardVolts = CONTROL_DRIVE_FORWARD_AXIS.position() * 0.12
        # if CONTROL_DRIVE_FORWARD_AXIS.position() > 90:
        #     forwardVolts = CONTROL_DRIVE_FORWARD_AXIS.position() * -0.12 * 0.9

        # Spin motors and combine controller axes
        leftMotorA.spin(FORWARD, forwardVolts + turnVolts, VOLT)
        leftMotorB.spin(FORWARD, forwardVolts + turnVolts, VOLT)
        leftMotorC.spin(FORWARD, forwardVolts + turnVolts, VOLT)
        rightMotorA.spin(FORWARD, forwardVolts - turnVolts, VOLT)
        rightMotorB.spin(FORWARD, forwardVolts - turnVolts, VOLT)
        rightMotorC.spin(FORWARD, forwardVolts - turnVolts, VOLT)

        hold_buttons()

        sleep(5)

def user_control():
    Thread(control_thread)
    Thread(cosmetic_thread)

selector = autonSelector("main")

user_control()