import time
import os



# function to read distance from sensor
def read_distance():
    # import GPIO library
    import RPi.GPIO as GPIO

    # specify GPIO pins to use
    GPIO.setmode(GPIO.BCM)
    TRIG = 2 # GPIO02
    ECHO = 3 # GPIO03

    # set pin mode and initialize
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG, GPIO.LOW)

    # send a very short (10 micro seconds) pulse to "TRIG" pin
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    # wait for "ECHO" pin becomes HIGH
    signaloff = time.time()
    while GPIO.input(ECHO) != GPIO.HIGH:
        signaloff = time.time()

    # wait for "ECHO" pin becomes LOW
    signalon = signaloff
    while time.time() < signaloff + 0.1: # timeout in 0.1 seconds
        if GPIO.input(ECHO) == GPIO.LOW:
            signalon = time.time()
            break

    # cleanup GPIO state
    GPIO.cleanup()

    # calculate distance from time difference
    # sound(ultrasonic) travels 340 m / seconds
    # distance (cm) can be obtained by 340(m/s) x 100(m/cm) * time(s) / 2 
    time_passed = signalon - signaloff
    distance = 340 * 100 * time_passed / 2

    # since the sensor cannot guage over 500 cm, 
    # distance over 500 is considered as a noise
    if distance <= 500:
        return distance
    else:
        return None

# if executed directly (not import as library)
if __name__ == '__main__':

    while True:
        start_time = time.time()
        distance = read_distance()
        if distance:
            print "distance: %.1f cm" % (distance)
            os.system("mosquitto_pub -h beam.soracom.io -t beam_ws001 -m 'Hello PubNub from Beam!'")
            

        # wait for next loop
        wait = start_time + 1 - time.time()
        if wait > 0:
            time.sleep(wait)