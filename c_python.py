import ctypes
import math
import pigpio
import time

#Tyler Evans U1313811
#seinor project python prototype code
#wish to rewrite in c but used python to get some parts done

#init the gpio of the raspberry pi
robo = pigpio.pi()
state = 1
HIGH = 1
LOW = 0

#consts defined here
step_size = 10
step_size_turn = 10

#gpio for I2C
"""TODO I2C is needed here!!!"""
g1 = 16
g2 = 20
g3 = 21
#these are the gpio pins for motor controler
m1 = 5
m2 = 6
m3 = 13
m4 = 19
#this is the motor gpio pin for the vac
v1 = 12
#these are the pins for the motor encoder
re1 = 27
re2 = 22
le1 = 23
le2 = 24

def option(v):
    global state
    """this function does an option according to what is given"""
    #step_size = 10
    #step_size_turn = 10
    match v:
        case "w":
            forward()
        case "s":
            backward()
        case "a":
            left()
        case "d":
            right()
        case "q":
            stop()
        case "r":
            state = 0
        case "e":
            vac_on()
        case "ee":
            vac_off()
        case _:
            return Exception
def vac_on():
    robo.write(v1, HIGH)
def vac_off():
    robo.write(v1, LOW)

def forward(steps=0):
    print("forward " + str(steps))
    robo.write(m1, HIGH)
    robo.write(m2, HIGH)
    robo.write(m3, LOW)
    robo.write(m4, LOW)

def backward(steps = 0):
    print("backwords " + str(steps))
    robo.write(m1, LOW)
    robo.write(m2, LOW)
    robo.write(m3, HIGH)
    robo.write(m4, HIGH)
def left(steps = 0):
    print("left " + str(steps))
    robo.write(m1, LOW)
    robo.write(m2, HIGH)
    robo.write(m3, LOW)
    robo.write(m4, LOW)
def right(steps = 0):
    print("right " + str(steps))
    robo.write(m1, HIGH)
    robo.write(m2, LOW)
    robo.write(m3, LOW)
    robo.write(m4, LOW)
def stop():
    robo.write(m1, LOW)
    robo.write(m2, LOW)
    robo.write(m3, LOW)
    robo.write(m4, LOW)
    print("stoped")

def intro():
    #set the vac. gpio to output
    robo.set_mode(v1, pigpio.OUTPUT)
    #set the motor gpio to output mode
    robo.set_mode(m1, pigpio.OUTPUT)
    robo.set_mode(m2, pigpio.OUTPUT)
    robo.set_mode(m3, pigpio.OUTPUT)
    robo.set_mode(m4, pigpio.OUTPUT)
    #set the encoder gpio
    robo.set_mode(re1, pigpio.INPUT)
    robo.set_mode(re2, pigpio.INPUT)
    robo.set_mode(le1, pigpio.INPUT)
    robo.set_mode(le2, pigpio.INPUT)
    #setup I2C pins
    robo.set_mode(g1, pigpio.OUTPUT)
    robo.set_mode(g2, pigpio.OUTPUT)
    robo.set_mode(g3, pigpio.OUTPUT)


    #instructions
    print("w is forward")
    print("s is backwords")
    print("d is right")
    print("a is left")
    print("e is vac on")
    print("ee is vac off")
    print("q is stop")
    print("r is quit")

def read_lm():
    print("reading left motor")

def read_rm():
    print("reading right motor")

def de_init():
    print("to do at later day")

def main():
    intro()
    while(state == 1):
        word = input("option?")
        option(word)
        time.sleep(0.1)
    #exits the program puts
    """TODO deinit"""
    robo.stop()

#main
main()
