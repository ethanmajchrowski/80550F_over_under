from vex import *

brain = Brain()

#### Define Ports ####
leftMotorA =  Motor(Ports.PORT16, GearSetting.RATIO_6_1, False)
rightMotorA = Motor(Ports.PORT20, GearSetting.RATIO_6_1, True)
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

# auton drive
# leftMotorFront = Motor(Ports.PORT20, GearSetting.RATIO_18_1)
# leftMotorRear = Motor(Ports.PORT10, GearSetting.RATIO_18_1)
# leftMotorGroup = MotorGroup(leftMotorFront, leftMotorRear)

# rightMotorFront = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
# rightMotorRear = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
# rightMotorGroup = MotorGroup(rightMotorFront, rightMotorRear)

# centerEnc = Encoder(brain.three_wire_port.a)
# rightEnc = Encoder(brain.three_wire_port.c)
# leftEnc = Encoder(brain.three_wire_port.e)

class pid:
    def __init__(self, KP, KD, KI, KI_MAX, MIN = None) -> None:
        '''
        Create a multipurpose PID that has individually tuned control variables.

        Args:
            KP (int): kP value for tuning controller
            KD (int): kD value for tuning controller
            KI (int): kI value for tuning controller
            KI_MAX (int): integral will not be allowed to pass this value
            MIN (int): a minimum value that the PID will output

        Returns:
            None
        '''
        
        self.kP, self.kD, self.kI = KP, KD, KI
        self.kI_max = KI_MAX
        self.error = 0
        self.integral = 0
        self.derivative = 0
        self.last_error = 0
        self.minimum = MIN
    def calculate(self, TARGET, INPUT, DELAY = 0) -> int:
        '''
        Calculates the output based on the PID's tuning and the provided target & input

        Args:
            TARGET (int): a number that the PID will try to reach
            INPUT (int): the current sensor or other input
            DELAY (int): the delay for the loop

        Returns:
            PID outpit (int)
        '''
        self.error = TARGET - INPUT
        if self.kI != 0:
            if abs(self.error) < self.kI_max:
                self.integral += self.error
            else:
                self.integral = 0
        else:
            self.integral = 0

        self.derivative = self.error - self.last_error
        
        output = (self.error * self.kP) + (self.integral * self.kI) + (self.derivative * self.kD)
        if self.minimum is not None:
            if abs(output) < self.minimum:
                if self.error < 0: output = -self.minimum
                else: output = self.minimum
        
        self.last_error = self.error
        wait(DELAY, MSEC)
        return output

class Auton:
    def __init__(self, LEFT_SENSOR, RIGHT_SENSOR, drive_tolerance = 0) -> None:
        """
        Auton controller that handles all auton functions.

        args:
            LEFT_SENSOR: VEX sensor object. motor or shaft encoder
            RIGHT_SENSOR: VEX sensor object. motor or shaft encoder
            drive_tolerance (int): num of degree error the PID will accept before it stops
        """
        self.DRIVE_DIAMETER = 3 # size of the drive wheels?
        self.TRACKING_DIAMETER = 2.75 # size of the tracking wheels (2.75 on auton bot)
        # the tolerance that movements will finish in mm
        self.DRIVE_TOLERANCE = drive_tolerance 
        self.left_sens = LEFT_SENSOR
        self.right_sens = RIGHT_SENSOR

        # calculate the drive wheel circumference in millimeters from inches
        self.DRIVE_WHEEL_CIRCUMFERENCE = (self.DRIVE_DIAMETER * 25.4) * 3.14159

        # battery check to console
        print('''Auton initialized 
              \nBattery voltage at:''' + str(brain.battery.capacity()) + "%")
        if brain.battery.capacity() < 25: print("!!!!!!! WARNING: battery below 25% !!!!!!!")

    def forward(self, dist: float) -> None:
        """
        Drive PID forwards.

        Args:
            dist (float): distance to drive in mm
        """
        left_pid = pid(0.5, 0.4, 0, 0, MIN=0) # KP < 1, KD < 0.05
        right_pid = pid(0.5, 0.4, 0, 0, MIN=0) # KP < 1, KD < 0.05
        heading_pid = pid(1, 0, 0, 0) # KP < 1, KD < 0.05

        self.left_sens.reset_position()
        self.right_sens.reset_position()
        
        pid_running = True
        # fill the brain red to warn that the motors are trying to spin
        brain.screen.draw_rectangle(0,0,480,240, Color.RED) 

        # Handle distance calculations - basically, degrees to mm based on wheel size
        degrees_travel = (dist / self.DRIVE_WHEEL_CIRCUMFERENCE) * 360

        while pid_running:
            currentLeftValue = leftMotorA.position()
            currentRightValue = rightMotorA.position()

            leftOutput = left_pid.calculate(degrees_travel, currentLeftValue)
            rightOutput = right_pid.calculate(degrees_travel, currentRightValue)

            # print(currentLeftValue / degrees_travel)

            pidHeadingError = currentLeftValue - currentRightValue
            headingOutput = heading_pid.calculate(0, pidHeadingError)
            # headingOutput = 0

            leftMotors.spin(FORWARD, leftOutput + headingOutput)
            rightMotors.spin(FORWARD, rightOutput + headingOutput)
            
            if ((dist - self.DRIVE_TOLERANCE < abs(currentLeftValue) < dist + self.DRIVE_TOLERANCE) and 
                (dist - self.DRIVE_TOLERANCE < abs(currentRightValue) < dist + self.DRIVE_TOLERANCE)):

                pid_running = False

            wait(10, MSEC)
        
        brain.screen.clear_screen()
        leftMotors.stop(COAST)
        rightMotors.stop(COAST)

drivebase = Auton(LEFT_SENSOR=leftMotorA, RIGHT_SENSOR=rightMotorA, drive_tolerance=1)

# 500 mm is 790 DEGREES
drivebase.forward(500)
# drivebase.forward(-500)