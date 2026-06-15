from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox


close_program = ''  #global variable
led_con=[False,False,False]
temp_error = False
def update_window():
    window.update()
    if close_program == 'exit':
        loop = False
    else:
        loop =True
    return loop

def led_switch1():
    global led_con
    led_con[0] = not led_con[0]
def led_switch2():
    global led_con
    led_con[1] = not led_con[1]
def led_switch3():
    global led_con
    led_con[2] = not led_con[2]

def sync_led_con():
    return led_con

def close_confirm():
	global close_program
	res = messagebox.askyesno("Exit program","Confirm exit?")
	print(res)
	if res:
		close_program = "exit"

def display_led_switch(leds_control):
    global led_con
    #sync led control
    led_con = list(leds_control)
    if(led_con[0]):
        switch1.configure(text="ON", bg="#2ecc71", fg="white", relief="sunken")
    else:
        switch1.configure(text="OFF", bg="#bdc3c7", fg="black", relief="raised")
    if(led_con[1]):
        switch2.configure(text="ON", bg="#2ecc71", fg="white", relief="sunken")
    else:
        switch2.configure(text="OFF", bg="#bdc3c7", fg="black", relief="raised")
    if(led_con[2]):
        switch3.configure(text="ON", bg="#2ecc71", fg="white", relief="sunken")
    else:
        switch3.configure(text="OFF", bg="#bdc3c7", fg="black", relief="raised")



def tk_led(leds_state):
    led_labels[0].configure(bg="#27ae60" if leds_state[0] else "#7f8c8d", fg="white")
    led_labels[1].configure(bg="#f1c40f" if leds_state[1] else "#7f8c8d", fg="black" if leds_state[1] else "white")
    led_labels[2].configure(bg="#e74c3c" if leds_state[2] else "#7f8c8d", fg="white")

def button_lab(button):
    if(button%2):
        button_label4.configure(text='PRESSED',fg = 'purple')
    else:
        button_label4.configure(text='UNPRESS',fg = '#2980b9')
    if((button >> 1)%2):
        button_label5.configure(text='PRESSED',fg = 'blue')
    else:
        button_label5.configure(text='UNPRESS',fg = '#2980b9')
        
def motion_lab(motion):
    if motion:
        motion_label2.configure(text='MOVING',fg = 'green')
    else:
        motion_label2.configure(text='STATIONARY',fg = '#2980b9')


def tk_temp_humi(temp,humi,temp_error):
    if (not temp_error):
        lbl1.configure(text=f"Temperature: {temp}°C \n Humidity: {humi}%")
    else :
        lbl1.configure(text=f"Temperature: Error \n Humidity: Error")
    
def tk_gyro_data(acce_list,geo_list):
    gyro_label.configure(text=f"acce_x :{acce_list[0]:.2f} acce_y :{acce_list[1]:.2f} acce_z :{acce_list[2]:.2f}\n\nx: {geo_list[0]:.2f} y: {geo_list[1]:.2f} z: {geo_list[2]:.2f}")
    
window = Tk()
window.title("Raspberry Pi GUI Dashboard")
window.geometry("500x600+100+100")
window.configure(bg="#ecf0f1") # Clean light gray-blue background
window.protocol("WM_DELETE_WINDOW", close_confirm)

# Shared Font Styles
FONT_TITLE = ("Time New Roman", 22, "bold")
FONT_LABEL = ("Time New Roman", 14)
FONT_BTN = ("Time New Roman", 14, "bold")

# ==========================================
# 1. TOP FRAME: SENSORS (Header)
# ==========================================
header_frame = Frame(window, bg="#2c3e50", pady=20)
header_frame.pack(fill=X)

lbl1 = Label(header_frame, text="Temperature: 23.9°C \n Humidity: 66.7%", font=FONT_TITLE, fg="white", bg="#2c3e50")
lbl1.pack()

# ==========================================
# 2. MIDDLE FRAME: CONTROLS & INDICATORS
# ==========================================
body_frame = Frame(window, bg="#ecf0f1", pady=20)
body_frame.pack()


# Column Headers
Label(body_frame, text="App Controls", font=("Helvetica", 14, "underline"), bg="#ecf0f1").grid(row=0, column=0, pady=(0, 10), padx=20)
Label(body_frame, text="Physical LEDs", font=("Helvetica", 14, "underline"), bg="#ecf0f1").grid(row=0, column=1, pady=(0, 10), padx=20)

# Switches (Column 0)
switch1 = Button(body_frame, text="OFF", font=FONT_BTN, bg="#bdc3c7", width=10, command=led_switch1)
switch1.grid(row=1, column=0, pady=8, padx=20)

switch2 = Button(body_frame, text="OFF", font=FONT_BTN, bg="#bdc3c7", width=10, command=led_switch2)
switch2.grid(row=2, column=0, pady=8, padx=20)

switch3 = Button(body_frame, text="OFF", font=FONT_BTN, bg="#bdc3c7", width=10, command=led_switch3)
switch3.grid(row=3, column=0, pady=8, padx=20)

# LED Indicators (Column 1)
led_labels = []
for i in range(3):
    # Using relief="groove" and borderwidth to make them look like actual indicator lights
    label = Label(body_frame, text=f"LED {i+1}", font=FONT_BTN, bg="#7f8c8d", fg="white", width=10, relief="groove", borderwidth=4)
    led_labels.append(label)
    led_labels[i].grid(row=i+1, column=1, pady=8, padx=20)

# ==========================================
# 3. BOTTOM FRAME: STATUSES
# ==========================================
status_frame = Frame(window, bg="#ecf0f1", pady=10)
status_frame.pack(fill=X)

# A sub-grid strictly for perfectly aligning the colon ":" 
status_grid = Frame(status_frame, bg="#ecf0f1")
status_grid.pack()
#button labels
button_label1 = Label(status_grid, text="Button 1 Status:", font=FONT_LABEL, bg="#ecf0f1", anchor="e", width=15)
button_label1.grid(row=0, column=0, pady=5)
button_label4 = Label(status_grid, text="Unpressed", font=FONT_LABEL, fg="#2980b9", bg="#ecf0f1", anchor="w", width=15)
button_label4.grid(row=0, column=1, pady=5)

button_label2 = Label(status_grid, text="Button 2 Status:", font=FONT_LABEL, bg="#ecf0f1", anchor="e", width=15)
button_label2.grid(row=1, column=0, pady=5)
button_label5 = Label(status_grid, text="Unpressed", font=FONT_LABEL, fg="#2980b9", bg="#ecf0f1", anchor="w", width=15)
button_label5.grid(row=1, column=1, pady=5)

#motion labels
motion_label = Label(status_grid, text="Motion Status:", font=FONT_LABEL, bg="#ecf0f1", anchor="e", width=15)
motion_label.grid(row=2, column=0, pady=5)

motion_label2 = Label(status_grid, text="STATIONARY", font=FONT_LABEL, fg="#2980b9", bg="#ecf0f1", anchor="w", width=15)
motion_label2.grid(row=2, column=1, pady=5)

gyro_frame = Frame(window, bg="#ecf0f1", pady=10)
gyro_frame.pack(fill=X)



gyro_label = Label(gyro_frame,text=f"acce_x :{0} acce_y :{0} acce_z :{0}\n\nx: {0} y: {0} z: {0}", font=FONT_LABEL, bg="#ecf0f1", fg="#2980b9",width = 35,anchor="center",relief="groove", borderwidth=4)
gyro_label.grid(row = 0, column=0, pady =10,padx =40)


