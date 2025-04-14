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
SDA = 2
SCL = 3
BUS = 1
#this is the regs to read.
REG = 0x00
#this is the time of flight address found in the datasheet
#https://www.st.com/resource/en/datasheet/vl53l0x.pdf
DEV_ADDRESS_TOF = 0x52

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

def action_mutiplex_8bit(a):
    """Most starts from g3 least is g1 signifcant bit 2^3"""
    match a:
        case 0:
            # 000
            robo.write(g1, LOW)
            robo.write(g2, LOW)
            robo.write(g3, LOW)
        case 1:
            # 001
            robo.write(g1, HIGH)
            robo.write(g2, LOW)
            robo.write(g3, LOW)
        case 2:
            # 010
            robo.write(g1, LOW)
            robo.write(g2, HIGH)
            robo.write(g3, LOW)
        case 3:
            # 011
            robo.write(g1, HIGH)
            robo.write(g2, HIGH)
            robo.write(g3, LOW)
        case 4:
            # 100
            robo.write(g1, LOW)
            robo.write(g2, LOW)
            robo.write(g3, HIGH)
        case 5:
            # 101
            robo.write(g1, HIGH)
            robo.write(g2, LOW)
            robo.write(g3, HIGH)
        case 6:
            # 110
            robo.write(g1, LOW)
            robo.write(g2, HIGH)
            robo.write(g3, HIGH)
        case 7:
            # 111
            robo.write(g1, HIGH)
            robo.write(g2, HIGH)
            robo.write(g3, HIGH)
        case _:
            print("not valid I2C location")
def I2C_Op(v):
    action_mutiplex_8bit(v)

def action_option(v):
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
            stop()
            state = 0
        case "e":
            vac_on()
        case "ee":
            vac_off()

        case "z":
            leftb()
        case "c":
            rightb()
        case "x":
            I2C_Op(v)
        case _:
            print("not valid")
def vac_on():
    robo.write(v1, HIGH)
def vac_off():
    robo.write(v1, LOW)

def forward(steps=0):
    print("forward " + str(steps))
    robo.write(m1, HIGH)
    robo.write(m2, LOW)
    robo.write(m3, LOW)
    robo.write(m4, HIGH)

def backward(steps = 0):
    print("backwords " + str(steps))
    robo.write(m1, LOW)
    robo.write(m2, HIGH)
    robo.write(m3, HIGH)
    robo.write(m4, LOW)
def left(steps = 0):
    print("left " + str(steps))
    robo.write(m1, HIGH)
    robo.write(m2, LOW)
    robo.write(m3, LOW)
    robo.write(m4, LOW)
def leftb(steps = 0):
    print("left backwords " + str(steps))
    robo.write(m1, LOW)
    robo.write(m2, HIGH)
    robo.write(m3, LOW)
    robo.write(m4, LOW)
def right(steps = 0):
    print("right " + str(steps))
    robo.write(m1, LOW)
    robo.write(m2, LOW)
    robo.write(m3, LOW)
    robo.write(m4, HIGH)
def rightb(steps = 0):
    print("right backwords " + str(steps))
    robo.write(m1, LOW)
    robo.write(m2, LOW)
    robo.write(m3, HIGH)
    robo.write(m4, LOW)
def stop(steps = 0):
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
    #set the SCL and SDA pin to high
    robo.set_pullup_down(SDA, pigpio.PUD_UP)
    robo.set_pullup_down(SCL, pigpio.PUD_UP)



    #instructions
    print("w is forward")
    print("s is backwords")
    print("d is right")
    print("a is left")
    print("e is vac on")
    print("ee is vac off")
    print("q is stop")
    print("r is quit")
    print("1-7 I2C chan select")

def read_lm():
    print("reading left motor")

def read_rm():
    en = robo.read(re1)
    en1 = robo.read(re2)
    print(f"the value is {re1}")
    print(f"the value measured 2 is {re2}")
    print("reading right motor")

def read_I2C(addr=0):
    print("Starting I2C")
    hand = robo.i2c_open(BUS, addr)
    (count, data) = robo.i2c_read_i2c_block_data(hand, REG, 1)
    if(count >= 0):
        #what this line does is gets a float and puts it into the string file.
        print(f"Data read from register 0x{REG:02X}: {data[0]}")
    else:
        print("read failed.")
    robo.i2c_close(hand)

def de_init():
    robo.write(m1, LOW)
    robo.write(m2, LOW)
    robo.write(m3, LOW)
    robo.write(m4, LOW)
    robo.write(g1, LOW)
    robo.write(g2, LOW)
    robo.write(g3, LOW)

def main():
    intro()
    while(state == 1):
        read_rm()
        word = input("option?")
        action_option(word)
        time.sleep(0.1)
    #exits the program puts
    de_init()
    robo.stop()

#main
main()
