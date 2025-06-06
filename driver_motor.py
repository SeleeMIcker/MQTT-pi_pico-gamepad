from motor_driver import *         

# Drive Motor

motor = motor_driver(4,5,2,3)      # M1A = 4, M1B = 5, M2A = 2, M2B = 3

motor.speed(50,50)                 # move forward at speed 50
utime.sleep(5)                     # sleep 5 second

motor.speed(0,50)                  # turn left at speed 50
utime.sleep(5)

motor.speed(50,0)                  # turn right at speed 50
utime.sleep(5)

motor.speed(-50,-50)               # move backward at speed 50
utime.sleep(5)   

motor.brake()    
