# Module:       pid.py
# Author:       ethan
# Created:      11/7/2023, 3:38 PM
# Description:  PID

from vex import *

# DEVICES
brain = Brain()
enc1 = Encoder(brain.three_wire_port.a)

left_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_6_1)
right_motor_a = Motor(Ports.PORT2, GearSetting.RATIO_6_1, True)

# CONFIG
KP, KI, KD = 0.05, 0.001, 0
TRACKING_CIRCUMFERENCE = 260 # mm

class PID:
    def __init__(self, proportional_constant, integral_constant):
        self.kP = proportional_constant
        self.kI = integral_constant
        self.integral_sum = 0
    
    def proportional(self, error):
        return self.kP * error
    
    def integral(self, error):
        self.integral_sum += error
        return (self.kI * self.integral_sum)
    
    def get_value(self, error):
        p = self.proportional(error)
        i = self.integral(error)
        print("P:", p, "I:", i)
        return p# + i

def main():
    enc1.reset_position()
    pid = PID(KP, KI)
    left_motor_a.spin(FORWARD)
    right_motor_a.spin(FORWARD)
    integral_error = 0

    while True:
        sleep(1, MSEC)
        # # encoder 1 position / 360 = number of rotations
        # # number of rotations * circumference of wheel
        # # mm traveled / 25.4 to convert to inches
        # enc1_distance = ((enc1.position() / 360) * TRACKING_CIRCUMFERENCE) / 25.4
        error = (abs(left_motor_a.position()) - abs(right_motor_a.position()))
        
        # integral_error += error

        speed = 50
        # p = error * KP
        # i = integral_error * KI
        # adjustment = p + i
        adjustment = pid.get_value(error) * 2
        left_speed, right_speed = speed + adjustment, speed - adjustment

        print("Error: ", error)
        print(left_speed, right_speed)
        brain.screen.clear_screen()
        brain.screen.set_cursor(1,1)
        brain.screen.print("Left Encoder:", abs(left_motor_a.position()))
        brain.screen.next_row()
        brain.screen.print("Right Encoder:", abs(right_motor_a.position()))
        brain.screen.next_row()
        brain.screen.print("Error:", error)
        brain.screen.next_row()
        brain.screen.print("Integral Error:", integral_error)
        brain.screen.next_row()
        # brain.screen.print("P/I:", p, i)
        brain.screen.next_row()
        brain.screen.print("Adjustment:", adjustment)
        brain.screen.render()

        left_motor_a.set_velocity(speed - adjustment, PERCENT)
        right_motor_a.set_velocity(speed + adjustment, PERCENT)

main()