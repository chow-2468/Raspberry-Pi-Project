from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox

close_program = ''  #global variable
LOOP_ACTIVE = True  #global variable
led_control = [False, False, False]
led_state = [False, False, False]

def close_confirm():
	global close_program
	res = messagebox.askyesno("Exit program","Confirm exit?")
	print(res)
	if res:
		close_program = "exit"


def led_switch( led_index):
    global led_control
    led_control[led_index] = not led_control[led_index]
    if led_control[led_index]:
        led_switches[led_index].configure(text="ON",bg="green")
        print(f"LED{led_index + 1} is ON")
    else:
        led_switches[led_index].configure(text="OFF",bg="lightgray")
        print(f"LED{led_index + 1} is OFF")

def led():
    if led_state[0]:
        led_labels[0].configure(bg="red")
    else:
        led_labels[0].configure(bg="grey")   

    if led_state[1]:
        led_labels[1].configure(bg="yellow")
    else:
        led_labels[1].configure(bg="grey")
    
    if led_state[2]:
        led_labels[2].configure(bg="green")
    else:
        led_labels[2].configure(bg="grey")

window =Tk()
window.title("Raspberry Pi GUI")
window.geometry("500x400+100+100")



temp = 100
humi = 50
window.protocol("WM_DELETE_WINDOW",close_confirm)
button_status = 2


lbl1 = Label(window,text=f"Temperature: {temp}°C \n Humidity: {humi}%",font=("Arial Bold",20),fg="black")
lbl1.grid(column=0, row=0)

led_switches = []
for i in range(3):
    switch = Button(window,text="OFF",font=("Arial",16),bg="lightgray",command= lambda idx=i: led_switch(idx))
    led_switches.append(switch)
    led_switches[i].grid(column=0,row=i+1)
led_labels = []
for i in range(3):
    label = Label(window,text=f"LED {i+1}",font=("Arial",16))
    led_labels.append(label)
    led_labels[i].grid(column=1, row=i+1)
    
button_label1 = Label(window,text="Button1 Status: ",font=("Arial",16))
button_label1.grid(column=0, row=4)
button_label2 = Label(window,text="Button2 Status: ",font=("Arial",16))
button_label2.grid(column=0, row=5)
button_label3 = Label(window,text="Motion Status: ",font=("Arial",16))
button_label3.grid(column=0, row=6)
button_label4 = Label(window,font=("Arial",16))
button_label4.grid(column=1, row=4)
button_label5 = Label(window,font=("Arial",16))
button_label5.grid(column=1, row=5)
def update_data():
    lbl1.configure(text=f"Temperature: {temp}°C \n Humidity: {humi}%")
    button_label4.configure(text=f"{'PRESSED' if button_status%2 else 'UNPRESSED'}", bg="green" if button_status%2 else "lightgray")
    button_label5.configure(text=f"{'PRESSED' if int(button_status/2) % 2 else 'UNPRESSED'}", bg="red" if int(button_status/2) % 2 else "lightgray")


while LOOP_ACTIVE:
     window.update()
     led()
     update_data()
     if close_program == 'exit':
          window.quit()
          LOOP_ACTIVE = False