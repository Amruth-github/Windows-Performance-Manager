from tkinter import *
from tkinter import ttk
import psutil as ps
import platform

class System_information:
    def __init__(self):
        self.scrollbarV = None
        self.scrollbarH = None
        self.information = {}
        self.used_ram = None
        self.available_ram = None
        self.information["Name on Network"] = platform.node()
        self.information["Operating System"] = platform.system()
        self.information["Release"] = platform.release()
        self.information["Architecture"] = platform.architecture()[0]
        self.information["Operating System Version"] = platform.version()

        self.information["Machine type"] = platform.machine()
        self.information["Processor Type"] = platform.processor()
        self.information["Logical Cores"] = ps.cpu_count(True)
        self.information["Physical Cores"] = ps.cpu_count(False)
        self.information["CPU Speed"] = str(ps.cpu_freq().max) + " MHz"

        self.information["Total RAM"] = round(ps.virtual_memory().total/1000000000, 2)
        self.information["Used RAM"] = round(ps.virtual_memory().used/1000000000, 2)
        self.information["Available RAM"] = round(ps.virtual_memory().available/1000000000, 2)

    def render(self, master):
        for info in self.information.keys():
            if info == "Total RAM":
                Label(master, text = f"{info}: {self.information[info]} GB", font = ('Calibri', 9)).pack(pady=10, side= TOP, anchor="w")
            elif info == "Used RAM":
                self.used_ram = Label(master, text = f"{info}: {self.information[info]} GB", font = ('Calibri', 9))
                self.used_ram.pack(pady=10, side= TOP, anchor="w")
            elif info == "Available RAM":
                self.available_ram = Label(master, text = f"{info}: {self.information[info]} GB", font = ('Calibri', 9))
                self.available_ram.pack(pady=10, side= TOP, anchor="w")
            else:
                Label(master, text = f"{info}: {self.information[info]}", font = ('Calibri', 9)).pack(pady=10, side= TOP, anchor="w")
            separator = ttk.Separator(master, orient='horizontal',)
            separator.pack(fill='both') 
