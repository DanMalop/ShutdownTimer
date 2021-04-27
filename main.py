#!/usr/bin/python3.8
import tkinter as tk
from tkinter import messagebox
from subprocess import call
import time

class Program:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("450x260")
        self.window.title("Shutdown timer")
        self.window.configure(bg = '#202020')
        self.shutdown_hour = tk.IntVar()
        self.shutdown_minute = tk.IntVar()
        self.remaining_t_str = tk.StringVar(value="--:--")
        self.canceled = tk.BooleanVar(value=False)

        self.instruction = tk.Label(self.window, text="At what time (24h format) do you want the PC to turn off?: ", fg = '#cccccc', bg = '#202020').place(x=35, y=20)
        self.hour_input = tk.Entry(self.window, textvariable=self.shutdown_hour, bg = '#505050', fg = '#cccccc').place(x=195, y=60, width = 30)
        self.separator = tk.Label(self.window, text=":", fg = '#cccccc', bg = '#202020').place(x=226, y=60)
        self.minute_input = tk.Entry(self.window, textvariable=self.shutdown_minute, bg = '#505050', fg = '#cccccc').place(x=235, y=60, width = 30)
        self.remaining_t = tk.Label(self.window, text="Remaining time:", fg = '#cccccc', bg = '#202020').place(x=35, y=100)
        self.clock = tk.Label(self.window, textvariable=self.remaining_t_str, bg = '#202020', fg = '#cccccc', font="Arial 20 bold").place(x=210, y=140)
        
        
        self.button1 = tk.Button(self.window, text="Run", command=self.shutdown, bg = '#b0b0b0').place(x=40,y= 200, width = 70)
        self.button2 = tk.Button(self.window, text="Cancel", command=self.cancel_shutdown, bg = '#b0b0b0').place(x= 340,y= 200, width = 70)

        self.window.mainloop()

    def shutdown(self):
        try:
            hour = str(abs(self.shutdown_hour.get()))
            minutes = str(abs(self.shutdown_minute.get()))

            #I generate an error if you enter hours greater than 24 or more than 60 minutes
            assert int(hour) < 24
            assert int(minutes) < 60

            #Terminal command runs
            call("shutdown -h " + hour+":" + minutes, shell=True)

            #message in self.window pop-up with tkinter (you have to import massagebox from tkinter)
            hour1, hour2 = divmod(int(hour), 10)
            minutes1, minutes2 = divmod(int(minutes), 10)
            messagebox.showinfo("Warning!","The PC will shut down at " + str(hour1) + str(hour2) + ":" + str(minutes1) + str(minutes2) + " o'clock")

        except: 
            messagebox.showinfo("Warning!","You entered the hour incorrectly")            
       

        try:
            #calculation of the remaining time
            actual_hour = [int(time.strftime("%H")), int(time.strftime("%M"))]

            if int(hour) < actual_hour[0]:
                final_hour , final_minutes = 23, 59
                remaining_t_min = ((final_hour - actual_hour[0]) * 60 + (final_minutes - actual_hour[1])) + (int(hour) * 60 + int(minutes))
            else:
                remaining_t_min = (int(hour) - actual_hour[0]) * 60 + (int(minutes) - actual_hour[1])

            hour_r, min_r = divmod(remaining_t_min, 60)
            min_r1, min_r2 = divmod(min_r, 10)
            hour_r1, hour_r2 = divmod(hour_r, 10)
            remaining_time = str(hour_r1) + str(hour_r2) + ":" + str(min_r1) + str(min_r2)
            self.remaining_t_str.set(remaining_time)

        except:
            messagebox.showinfo("Warning!","An error has occurred") 
        
    
    def cancel_shutdown(self):

        call("shutdown -c", shell=True)
        messagebox.showinfo("Warning!","Shutdown has been canceled")

        self.canceled.set(True)
        self.remaining_t_str.set("--:--")


def main():
    app = Program()
    return 0

if __name__ == '__main__':
    main()
