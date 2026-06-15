import BlynkLib
import RPi.GPIO as GPIO
from BlynkTimer import BlynkTimer
import board
import adafruit_dht
import time
import mpu6050

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT, initial=0)                 #use GPIO17 as output
GPIO.setup(22, GPIO.OUT, initial=0)                 #use GPIO22 as output
GPIO.setup(20, GPIO.OUT, initial=0)                 #use GPIO20 as output
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #use GPIO10 as input
GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #use GPIO9 as input
dhtDevice = adafruit_dht.DHT22(board.D18)   #change the GPIO pin according to your connection

BLYNK_AUTH_TOKEN = 'WVSiX_ZUOEA02snLY85kY1LOMZFu5iLw' #paste your token here

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

# Create BlynkTimer Instance
timer = BlynkTimer()

# led control
led1_control = False
led2_control = False
led3_control = False

led1_state = False
led2_state = False
led3_state = False

# keep track of button and motion state to avoid sending duplicate data to Blynk cloud
old_motion = False
old_button = 0


mpu6050 = mpu6050.mpu6050(0x68) #0x68 is the i2c address

# function to connect the Blynk cloud
@blynk.on("connected")
def blynk_connected():
    print("Hi, You have Connected to New Blynk2.0")
    blynk.virtual_sync(7,8,9)  
    time.sleep(2)
@blynk.handle_event('write V7')
def v7_handler(pin, value):
    global led1_control 
    led1_control = bool(int(value[0]))  
    print(f"LED1 Control ({pin}): {led1_control}" )
@blynk.handle_event('write V8')
def v8_handler(pin, value):
    global led2_control 
    led2_control = bool(int(value[0]))  
    print(f"LED2 Control ({pin}): {led2_control}" )
@blynk.handle_event('write V9')
def v9_handler(pin, value):
    global led3_control 
    led3_control = bool(int(value[0]))  
    print(f"LED3 Control ({pin}): {led3_control}" )  

# Functon to send collected data to the Blynk cloud
def myData():
    temp = dhtDevice.temperature
    humi = dhtDevice.humidity
    if temp is not None and humi is not None:
        print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temp, humi))
        
        blynk.virtual_write(0, temp)
        blynk.virtual_write(1, humi)
        print("Values sent to Blynk Server!")
    else:
        print("Sensor failure. Check wiring.")

def myLED():
    if(led1_control):
        led1_state = not led1_state
    else:
        led1_state = False

    if(led2_control):
        led2_state = not led2_state
    else:
        led2_state = False
    if(led3_control):
        led3_state = not led3_state
    else:
        led3_state = False
    GPIO.output(17, led1_state)       #turn on green LED
    GPIO.output(22, led2_state)       #turn on yellow LED
    GPIO.output(20, led3_state)       #turn on red LED
    blynk.virtual_write(4, led1_state)# update state of LED1 in Blynk app
    blynk.virtual_write(5, led2_state)# update state of LED2 in Blynk app
    blynk.virtual_write(6, led3_state)# update state of LED3 in Blynk app

def myMPU():
    accelerometer_data = mpu6050.get_accel_data()
    
    print("accelerometer data")
    print("------------------")
    print("accel_xout: ", accelerometer_data['x'])
    print("accel_yout: ", accelerometer_data['y'])
    print("accel_zout: ", accelerometer_data['z'])

    total_accel = (accelerometer_data['x'] + accelerometer_data['y'] + accelerometer_data['z']) > 16
    return total_accel

# Set the timer to automatically call the function every 20s
timer.set_interval(20, myData)
# Set the led timer to automatically call the function every 1s
timer.set_interval(1,myLED)
myData()
myLED()


while True:
    blynk.run()
    timer.run()
    button1=GPIO.input(10)
    button2=GPIO.input(9)

    # combine the state of two buttons into a single integer (0-3) and send to Blynk cloud if there is a change
    button= ((not button2)<<1) | (not button1)
    if (button != old_button):
        blynk.virtual_write(3, button)
        old_button = button
    # read the motion data from the MPU6050 sensor and send to Blynk cloud if there is a change
    motion = myMPU()
    if (motion != old_motion):
        blynk.virtual_write(2, motion)
        old_motion = motion


    

