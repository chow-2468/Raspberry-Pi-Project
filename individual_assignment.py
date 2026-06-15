import BlynkLib
import RPi.GPIO as GPIO
from BlynkTimer import BlynkTimer
import board
import adafruit_dht
import time
import mpu6050
from assignment_gui import *


GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT, initial=0)                 #use GPIO17 as output
GPIO.setup(27, GPIO.OUT, initial=0)                 #use GPIO27 as output
GPIO.setup(22, GPIO.OUT, initial=0)                 #use GPIO22 as output
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #use GPIO10 as input
GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #use GPIO9 as input
dhtDevice = adafruit_dht.DHT22(board.D18)   #change the GPIO pin according to your connection

BLYNK_AUTH_TOKEN = 'WVSiX_ZUOEA02snLY85kY1LOMZFu5iLw' #paste your token here

LOOP = True
temp_error = False
# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

# Create BlynkTimer Instance
timer = BlynkTimer()

# led control
led_control = [False, False, False]
led_state = [False, False, False]

# keep track of button and motion state to avoid sending duplicate data to Blynk cloud
old_motion = False
old_button = 0
old_gyro_data = [0,0,0]
acce_list = [0,0,0]
mpu6050 = mpu6050.mpu6050(0x68) #0x68 is the i2c address

# function to connect the Blynk cloud
@blynk.on("connected")
def blynk_connected():
    print("Hi, You have Connected to New Blynk2.0")
    blynk.sync_virtual(7,8,9)  
    time.sleep(2)

@blynk.on('V*')
def vpin_handler(pin, value):
    global led_control
    idx = int(pin) -7
    if 0<=idx<=2:
        led_control[idx] = bool(int(value[0]))  
        print(f"LED{idx + 1} Control ({pin}): {led_control[idx]}" )
        
    display_led_switch(led_control)

# ~ # Functon to send collected data to the Blynk cloud
def myData():
    temp = 0
    humi = 0
    try :
        temp = dhtDevice.temperature 
        humi = dhtDevice.humidity
    except:
        print("tenperature sensor error")
        temp_error = True
    else:
        if temp is not None and humi is not None:
            print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temp, humi))
            
            blynk.virtual_write(0, temp)
            blynk.virtual_write(1, humi)
            temp_error = False
            print("Values sent to Blynk Server!")
        else:
            print("Sensor failure. Check wiring.")
            temp_error = True
        
    tk_temp_humi(temp,humi,temp_error)
        

def myLED():
    global led_state
    for i in range(3):
        if(led_control[i]):
            led_state[i] = not led_state[i]
        else:
            led_state[i] = False
            
    GPIO.output(17, led_state[0])       #turn on green LED
    GPIO.output(27, led_state[1])       #turn on yellow LED
    GPIO.output(22, led_state[2])       #turn on red LED
    blynk.virtual_write(4, int(led_state[0]))# update state of LED1 in Blynk app
    blynk.virtual_write(5, int(led_state[1]))# update state of LED2 in Blynk app
    blynk.virtual_write(6, int(led_state[2]))# update state of LED3 in Blynk app
    tk_led(led_state)

def myMPU():
    global old_gyro_data
    acce_data = mpu6050.get_accel_data()
    gyro_data = mpu6050.get_gyro_data()
    gx=gyro_data['x']
    gy=gyro_data['y']
    gz=gyro_data['z']
    
    global acce_list
    acce_list[0] = acce_data['x']
    acce_list[1] = acce_data['y']
    acce_list[2] = acce_data['z']

        
    if abs(old_gyro_data[0]-gx)>=15 or abs(old_gyro_data[1]-gy)>=15 or abs(old_gyro_data[2]-gz)>=15 :
        is_moving = True
    else:
        is_moving = False
    old_gyro_data[0] = gx;
    old_gyro_data[1] = gy;
    old_gyro_data[2] = gz;

    return is_moving



# Set the timer to automatically call the function every 20s
timer.set_interval(20, myData)
# Set the led timer to automatically call the function every 1s
timer.set_interval(1,myLED)
myData()
myLED()
while LOOP:
    blynk.run()
    timer.run()
    LOOP = update_window()
    tk_led_con = list(sync_led_con())
    try:
        button1=GPIO.input(10)
        button2=GPIO.input(9)
        if led_control != tk_led_con:
            led_control = list(tk_led_con)
            blynk.virtual_write(7, int(led_control[0]))
            blynk.virtual_write(8, int(led_control[1]))
            blynk.virtual_write(9, int(led_control[2]))
            display_led_switch(led_control)
            
        # combine the state of two buttons into a single integer (0-3) and send to Blynk cloud if there is a change
        button= ((not button2)<<1) | (not button1)
        if (button != old_button):
            blynk.virtual_write(3, button)
            button_lab(button)
            old_button = button
        # read the motion data from the MPU6050 sensor and send to Blynk cloud if there is a change
        motion = myMPU()
        #print(motion)
        if (motion != old_motion):
            print('sensor is moving. {}'.format(motion))
            if(motion):
                tk_gyro_data(acce_list,old_gyro_data)
            blynk.virtual_write(2, int(motion))
            motion_lab(motion)
            old_motion = motion
    except KeyboardInterrupt:
        dhtDevice.exit()
        GPIO.cleanup()
        exit()


    

