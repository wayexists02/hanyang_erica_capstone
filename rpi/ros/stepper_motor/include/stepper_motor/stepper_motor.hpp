#ifndef __STEPPER_MOTOR_H__
#define __STEPPER_MOTOR_H__

#define BOX_MOTOR_ENABLE 25

#define BOX_LEFT_MOTOR_CLK 1
#define BOX_LEFT_MOTOR_DIR 0

#define BOX_RIGHT_MOTOR_CLK 24
#define BOX_RIGHT_MOTOR_DIR 27

#define SUPPORT_LEFT_MOTOR_CLK 2
#define SUPPORT_LEFT_MOTOR_DIR 3
#define SUPPORT_RIGHT_MOTOR_CLK 4
#define SUPPORT_RIGHT_MOTOR_DIR 5
#define SUPPORT_MOTOR_ENABLE 6

void setWiringPi();

#endif
