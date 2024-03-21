from vex import *

brain = Brain()
con = Controller()

left_enc = Encoder(brain.three_wire_port.e)
right_enc = Encoder(brain.three_wire_port.c)

# Constants
IN_TO_MM_CONVERSION = 25.4
TRACKING_WHEEL_CENTER_OFFSET = (115) # const
TRACKING_WHEEL_RADIUS = ((2.75 / 2) * IN_TO_MM_CONVERSION)
TRACKING_WHEEL_CIRCUMFERENCE = (2 * 3.14 * TRACKING_WHEEL_RADIUS)

position = [0.0, 0.0, 0.0, 0.0]
left_accumulated_travel, right_accumulated_travel = 0.0, 0.0
previous_left_enc, previous_right_enc = 0, 0
prev_heading = 0

def calculate_odom(prev_left_enc: float, prev_right_enc: float, prev_heading: float):
    current_left_enc = left_enc.position(RotationUnits.REV) * -1
    current_right_enc = right_enc.position(RotationUnits.REV) * -1

    left_travel = (current_left_enc - prev_left_enc) * TRACKING_WHEEL_CIRCUMFERENCE
    right_travel = (current_right_enc - prev_right_enc) * TRACKING_WHEEL_CIRCUMFERENCE

    # # might need to do different calculations if we are turning left vs. right - this is for right
    if abs(left_travel) > abs(right_travel):
        print("turning right")
        delta_theta = (left_travel - right_travel) / (2 * TRACKING_WHEEL_CENTER_OFFSET)
    elif abs(left_travel) < abs(right_travel):
        print("turning left")
        delta_theta = (right_travel - left_travel) / (2 * TRACKING_WHEEL_CENTER_OFFSET)
    else:
        print("driving straight")
        delta_theta = 0

    # calculate total distance traveled
    distance = (right_travel + left_travel) / 2

    # calculate delta_x and delta_y
    delta_x = distance * math.cos(prev_heading + (delta_theta / 2))# * (180 / 3.14))
    delta_y = distance * math.sin(prev_heading + (delta_theta / 2))# * (180 / 3.14))

    # apply offset to global position
    return (delta_x, delta_y, delta_theta, distance, (left_travel, right_travel))

while True:
    new_position = calculate_odom(previous_left_enc, previous_right_enc, prev_heading)
    position[0] += new_position[0]
    position[1] += new_position[1]
    position[2] += new_position[2]
    position[3] += new_position[3]
    left_accumulated_travel += new_position[4][0]
    right_accumulated_travel += new_position[4][1]

    previous_left_enc, previous_right_enc = left_enc.position(RotationUnits.REV) * -1, right_enc.position(RotationUnits.REV) * -1
    prev_heading = position[2]

    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("x: ", position[0], " y: ", position[1], " heading:", math.degrees(position[2]))
    brain.screen.next_row()
    brain.screen.print("Left enc: ", left_enc.position(RotationUnits.REV), 
                       "right enc: ", right_enc.position(RotationUnits.REV))
    brain.screen.next_row()
    brain.screen.print("Distance traveled: ", position[3])
    brain.screen.next_row()
    brain.screen.print("Left travel: ", left_accumulated_travel, " right travel: ", right_accumulated_travel)
    if brain.screen.render(): pass
    wait(20, MSEC)