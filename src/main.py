__author__ = "Owen Plimer"
__version__ = "1.0.0"

import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
import tkinter.ttk as ttk
import tkinter.messagebox
import datetime

import generated_countdown as gc


def key_press(event):
    key = event.char
    print(f"'{key}' is pressed")

    if key == "h":print("yeah")

 
class App:
    def __init__(self, root):      
        # Initialise Variables
        self.target = datetime.datetime(2024, 11, 18, 22, 0, 0)
        self.window = "2024-18-11 22:00:00 GMT To 2024-06-06 22:30:00 GMT"
        self.now = datetime.datetime.now()
        self.count_state = "-"

        #get the generated timelines
        self.pre_launch_timeline = gc.pre_launch_timeline
        self.launch_timeline = gc.launch_timeline

        self.milestone_pre_to_post_switch_index = 0

        for index, milestone in enumerate(gc.milestones):
            if milestone == '(self.count_hours <= 0 and self.count_minutes <= 0 and self.count_seconds <= 0 and self.count_state == "-")':
                self.milestone_pre_to_post_switch_index = index
            
        
        #setting title
        root.title("Starship ift-6")

        #Keep window on top
        root.wm_attributes('-topmost', True)
        
        #setting window size
        width=600
        height=450
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.GLabel_969=tk.Label(root)
        self.GLabel_969["cursor"] = "arrow"
        ft = tkFont.Font(family='Times',size=10)
        self.GLabel_969["font"] = ft
        self.GLabel_969["fg"] = "#333333"
        self.GLabel_969["justify"] = "center"
        self.GLabel_969["text"] = f"Current Time:  {self.now.strftime('%H:%M:%S')}"
        self.GLabel_969.place(x=0,y=0,width=133,height=30)

        self.GLabel_825=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.GLabel_825["font"] = ft
        self.GLabel_825["fg"] = "#333333"
        self.GLabel_825["justify"] = "center"
        self.GLabel_825["text"] = f"Target: {self.target}"
        self.GLabel_825.place(x=135,y=0,width=178,height=30)

        self.GLabel_825=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.GLabel_825["font"] = ft
        self.GLabel_825["fg"] = "#333333"
        self.GLabel_825["justify"] = "center"
        self.GLabel_825["text"] = f"Window: {self.window}"
        self.GLabel_825.place(x=100,y=25,width=390,height=30)

        self.GLabel_439=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.GLabel_439["font"] = ft
        self.GLabel_439["fg"] = "#333333"
        self.GLabel_439["justify"] = "left"
        self.GLabel_439["text"] = "T- 00:00:00"
        self.GLabel_439.place(x=5,y=30,width=70,height=25)

        if len(self.pre_launch_timeline) > len(self.launch_timeline):
            self.tree = ttk.Treeview(root, columns=["status"], height=len(self.pre_launch_timeline))
        else:
            self.tree = ttk.Treeview(root, columns=["status"], height=len(self.launch_timeline))

        
        self.tree.pack(padx=10, pady=50)
        self.tree.bind('<ButtonRelease-1>', self.selectItem)

        self.tree.heading('#0', text="Task", command=self.task_message)
        self.tree.heading('status', text="Status", command=self.status_message)

        self.tree.tag_configure('blue', foreground="blue")
        self.tree.tag_configure('green', foreground="ForestGreen")
        self.tree.tag_configure('orange', foreground="DarkOrange")
        self.tree.tag_configure('red', foreground="firebrick2")
        
    def selectItem(self, a):
        curItem = self.tree.focus()
        print(self.tree.item(curItem))

    def task_message(self):
        tkinter.messagebox.showinfo("Task Display", "This section of the view shows all current tasks and their statuses")

    def status_message(self):
        tkinter.messagebox.showinfo("Status Display", "Shows the status of all upcoming tasks in the current phase of operations")

    def update(self):
        self.now = datetime.datetime.now()
        self.GLabel_969["text"] = f"Current Time:  {self.now.strftime('%H:%M:%S')}"
        
        self.count = self.target - self.now
        

        if self.count.days == -1:
            self.count = self.now - self.target
            self.count_state = "+"

        self.count_hours, rem = divmod(self.count.seconds, 3600)
    
        self.count_minutes, self.count_seconds = divmod(rem, 60)

        self.count_days_disp = '{:02d}'.format(self.count.days)
        self.count_hours_disp = '{:02d}'.format(self.count_hours)
        self.count_minutes_disp = '{:02d}'.format(self.count_minutes)
        self.count_seconds_disp = '{:02d}'.format(self.count_seconds)

        self.GLabel_439["text"] = f"T{self.count_state} {self.count_days_disp}:{self.count_hours_disp}:{self.count_minutes_disp}:{self.count_seconds_disp}"


        if self.count_state == "-":
            self.tree.delete(*self.tree.get_children())
            for index, line in enumerate(self.pre_launch_timeline):
                self.tree.insert('', tk.END, iid=index, text= line[0], values=line[1], tags=(line[2],))

        if self.count_state == "+":
            self.tree.delete(*self.tree.get_children())
            for index, line in enumerate(self.launch_timeline):
                self.tree.insert('', tk.END, iid=index, text= line[0], values=line[1], tags=(line[2],))
        

    def milestones(self):
        for index, milestone in enumerate(gc.milestones):
            if eval(milestone):
                if self.count_state == "-":
                    self.tree.height = len(self.pre_launch_timeline)
                    self.pre_launch_timeline[index][1] = "In-Progress"
                    self.pre_launch_timeline[index][2] = "orange"

                    if index == self.milestone_pre_to_post_switch_index-3:
                        for timeline_item in range(0, self.milestone_pre_to_post_switch_index-3):
                            self.pre_launch_timeline[timeline_item][2] = "green"
                            self.pre_launch_timeline[timeline_item][1] = "Complete"
                            
                elif self.count_state == "+":
                    self.launch_timeline[index-self.milestone_pre_to_post_switch_index-1][1] = "Complete"
                    self.launch_timeline[index-self.milestone_pre_to_post_switch_index-1][2] = "green"

        
if __name__ == "__main__":
        
        root = tk.Tk()
        root.bind('<Key>', key_press)
        app = App(root)
        
        while True:
            app.update()
            app.milestones()
            root.update_idletasks()
            root.update()