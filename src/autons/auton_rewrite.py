from vex import *

brain = Brain()

leftMotorFront = Motor(Ports.PORT20, GearSetting.RATIO_18_1)
leftMotorRear = Motor(Ports.PORT10, GearSetting.RATIO_18_1)
leftMotorGroup = MotorGroup(leftMotorFront, leftMotorRear)

rightMotorFront = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
rightMotorRear = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
rightMotorGroup = MotorGroup(rightMotorFront, rightMotorRear)

centerEnc = Encoder(brain.three_wire_port.a)
rightEnc = Encoder(brain.three_wire_port.c)
leftEnc = Encoder(brain.three_wire_port.e)

class pid():
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
            int
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
                output = self.minimum
        
        self.last_error = self.error
        wait(DELAY, MSEC)
        return output

class Auton():
    def __init__(self, LEFT_SENSOR, RIGHT_SENSOR) -> None:
        self.DRIVE_DIAMETER = 3
        self.TRACKING_DIAMETER = 2.75
        self.DRIVE_TOLERANCE = 5
        self.left_sens = LEFT_SENSOR
        self.right_sens = RIGHT_SENSOR

        print('''Auton initialized. 
              \nBattery voltage at: " + str(brain.battery.capacity()) + "%"''')
        if brain.battery.capacity() < 25: print("WARNING: battery below 25%")

    def forward(self, dist):
        left_pid = pid(0.2, 0.05, 0, 0) # KP < 1, KD < 0.05
        right_pid = pid(0.2, 0.05, 0, 0) # KP < 1, KD < 0.05
        heading_pid = pid(0.2, 0.05, 0, 0) # KP < 1, KD < 0.05

        self.left_sens.reset_position()
        self.right_sens.reset_position()
        
        pid_running = True
        # fill the brain red to warn that the motors are trying to spin
        brain.screen.draw_rectangle(0,0,480,240, Color.RED) 

        # Handle distance calculations


        while pid_running:
            currentLeftValue = -leftEnc.value()
            currentRightValue = -rightEnc.value()

            leftOutput = left_pid.calculate(dist, currentLeftValue)
            rightOutput = right_pid.calculate(dist, currentRightValue)

            pidHeadingError = currentLeftValue - currentRightValue
            headingOutput = heading_pid.calculate(0, pidHeadingError)

            leftMotorGroup.spin(FORWARD, leftOutput + headingOutput)
            rightMotorGroup.spin(FORWARD, rightOutput + headingOutput)
            
            if ((dist - self.DRIVE_TOLERANCE < abs(currentLeftValue) < dist + self.DRIVE_TOLERANCE) and 
                (dist - self.DRIVE_TOLERANCE < abs(currentRightValue) < dist + self.DRIVE_TOLERANCE)):

                pid_running = False

            wait(10, MSEC)
        
        brain.screen.clear_screen()

drivebase = Auton(LEFT_SENSOR=leftEnc, RIGHT_SENSOR=rightEnc)
drivebase.forward(-700)