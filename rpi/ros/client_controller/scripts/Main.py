#!/usr/bin/env python

import rospy
from Client import Client
from ImageSubscriber import ImageSubscriber
from MotorPublisher import MotorPublisher
import sys
import threading as th

HOST = "192.168.137.1"
PORT = 13333
NUM_STEP = 8

LEFT_MOTOR = 0 # Move trash box
RIGHT_MOTOR = 1 # open or close gate

result = None
ok = True

def recv_result(client):
    global result
    global ok

    while ok:
        result = client.recv_result()

def motor_control(result, control_queue):

    if result == 0:
        return
    elif result == 1:
        control_queue.append(LEFT_MOTOR, 0, 250)
        control_queue.append(RIGHT_MOTOR, 0, 100)
        control_queue.append(RIGHT_MOTOR, 1, 100)
        control_queue.append(LEFT_MOTOR, 1, 250)
    elif result == 2:
        control_queue.append(LEFT_MOTOR, 0, 125)
        control_queue.append(RIGHT_MOTOR, 0, 100)
        control_queue.append(RIGHT_MOTOR, 1, 100)
        control_queue.append(LEFT_MOTOR, 1, 125)
    elif result == 3:
        control_queue.append(LEFT_MOTOR, 1, 125)
        control_queue.append(RIGHT_MOTOR, 0, 100)
        control_queue.append(RIGHT_MOTOR, 1, 100)
        control_queue.append(LEFT_MOTOR, 0, 125)
    elif result == 4:
        control_queue.append(LEFT_MOTOR, 1, 250)
        control_queue.append(RIGHT_MOTOR, 0, 100)
        control_queue.append(RIGHT_MOTOR, 1, 100)
        control_queue.append(LEFT_MOTOR, 0, 250)
    else:
        rospy.loginfo("INVALID result " + str(result))
        return

def main(argv):
    global result
    global ok

    rospy.init_node("client_controller", anonymous=True)

    client = Client()
    if client.connect(HOST, PORT) is False:
        return

    image_sub = ImageSubscriber()
    motor_pub = MotorPublisher()

    rate = rospy.Rate(20)

    t = th.Thread(target=recv_result, args=(client,))
    t.start()

    cnt = 0;
    motor_control_queue = []
    wait_for_result = False

    while not rospy.is_shutdown():
        if wait_for_result:
            if result is not None:
                motor_control(result, motor_control_queue)
                result = None
            elif len(motor_control_queue) > 0 and motor_pub.is_ready():
                motor_id, direction, distance = motor_control_queue.pop(0)
                motor_pub.publish(motor_id,direction, distance)
            elif len(motor_control_queue) == 0 and motor_pub.is_ready():
                cnt = 0
                wait_for_result = False
            else:
                rate.sleep()
                continue

        image = image_sub.get_image()
        if image is None:
            rate.sleep();
            continue

        client.send_image(image)
        cnt += 1

        if cnt == NUM_STEP:
            wait_for_result = True

        rate.sleep()

    ok = False
    t.join()

if __name__ == "__main__":
    main(sys.argv)