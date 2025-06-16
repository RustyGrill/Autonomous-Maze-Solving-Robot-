import rospy
import time
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from math import pi as PI

def stop(vel_msg, velocity_publisher):  
    vel_msg.linear.x = 0  # set linear x to zero  
    vel_msg.angular.z = 0  # set angular z to zero  
    velocity_publisher.publish(vel_msg)  # publish the velocity to stop the robot
    time.sleep(1)  # stop for 1 second

def movingForward(vel_msg, velocity_publisher, t0, current_distance, distance, speed, forwardSpeed, front):  
    vel_msg.linear.x = forwardSpeed  
    vel_msg.angular.z = 0  # initialize angular z to zero   
    print('Is moving')  

    while current_distance < distance:
        velocity_publisher.publish(vel_msg)  # Publish the velocity  
        t1 = rospy.Time.now().to_sec()
        current_distance = speed * (t1 - t0)  # calculates distance

    if front < 1.0:
        stop(vel_msg, velocity_publisher)
    time.sleep(1)  # stop for 1 second

def movingBackward(vel_msg, velocity_publisher, t0, current_distance, distance, speed, backwardSpeed, front):
    vel_msg.linear.x = backwardSpeed
    vel_msg.angular.z = 0  # initialize angular z to zero
    print('Is backing')  

    while current_distance < (distance / 2):
        velocity_publisher.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        current_distance = speed * (t1 - t0)

    if front < 1.0:
        stop(vel_msg, velocity_publisher)
    time.sleep(1)  # stop for 1 second

def turnCW(vel_msg, velocity_publisher, t0, current_angle, turningSpeed, angle):
    angular_speed = round(turningSpeed * 2 * PI / 360, 1)
    relative_angle = round(angle * 2 * PI / 360, 1)
    vel_msg.linear.x = 0
    vel_msg.angular.z = -abs(angular_speed)
    print('Turning CW')

    while current_angle < relative_angle:
        velocity_publisher.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed * (t1 - t0)

    time.sleep(1)

def turnCCW(vel_msg, velocity_publisher, t0, current_angle, turningSpeed, angle):
    angular_speed = round(turningSpeed * 2 * PI / 360, 1)
    relative_angle = round(angle * 2 * PI / 360, 1)
    vel_msg.linear.x = 0
    vel_msg.angular.z = abs(angular_speed)
    print('Turning CCW')

    while current_angle < relative_angle:
        velocity_publisher.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed * (t1 - t0)

    time.sleep(1)

def escapeMaze():
    rospy.init_node('robot_cleaner', anonymous=True)
    velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    vel_msg = Twist()
    print("Let's move the robot")

    speed = 0.2
    distance = [0.10, 0.20, 0.29]

    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    while not rospy.is_shutdown():
        no_right_wall = None
        no_front_wall = None

        t0 = rospy.Time.now().to_sec()
        current_distance = 0

        scan_msg = rospy.wait_for_message("scan", LaserScan)

        front = scan_msg.ranges[1]
        left = scan_msg.ranges[90]
        top_left = scan_msg.ranges[45]
        right = scan_msg.ranges[270]
        top_right = scan_msg.ranges[315]

        if (right < 2.0) or (top_right < 2.0):
            no_right_wall = False
            print('Right wall is detected')
        else:
            no_right_wall = True
            print('Right wall is not detected')

        if no_right_wall:
            if front < 1.0:
                print('Move backward')
                movingBackward(vel_msg, velocity_publisher, t0, current_distance, distance[1], speed, -0.36, front)

                print('Turn clockwise because no right wall')
                turnCW(vel_msg, velocity_publisher, t0, 0, 3, 90)

            print('Move forward because no right wall')
            if front < 0.5:
                movingForward(vel_msg, velocity_publisher, t0, current_distance, distance[0], speed, 0.36, front)
            else:
                movingForward(vel_msg, velocity_publisher, t0, current_distance, distance[2], speed, 0.36, front)

        else:
            if (front > 1.0) or (top_left > 1.0):
                no_front_wall = True
                print('Front wall is not detected')
            else:
                no_front_wall = False
                print('Front wall is detected')

            if no_front_wall and (front > 1.0):
                if front < 0.5:
                    print('Move forward because no front wall')
                    movingForward(vel_msg, velocity_publisher, t0, current_distance, distance[0], speed, 0.36, front)
                else:
                    movingForward(vel_msg, velocity_publisher, t0, current_distance, distance[2], speed, 0.36, front)

            else:
                if (left > 0.5) and ((right > 3.0) or (top_right > 3.0)):
                    if front < 1.0:
                        print('Move backward')
                        movingBackward(vel_msg, velocity_publisher, t0, current_distance, distance[1], speed, -0.36, front)

                        print('Turn clockwise because no right wall')
                        turnCW(vel_msg, velocity_publisher, t0, 0, 3, 90)

                else:
                    if front < 1.0:
                        print('Move backward')
                        movingBackward(vel_msg, velocity_publisher, t0, current_distance, distance[1], speed, -0.36, front)

                        print('Turn counter-clockwise because have front wall')
                        turnCCW(vel_msg, velocity_publisher, t0, 0, 3, 90)

    rospy.spin()
