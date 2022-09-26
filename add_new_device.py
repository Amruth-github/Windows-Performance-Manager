from tkinter import messagebox
import socket
from GraphPage import *
from tkinter import ttk
import pickle
from get_resource import monitor_cpu_ntwk, monitor_ram_ntwk, disk_usage_ntwk

def connect_to_node(IP, PORT, NICKNAME, tabsys):
    if messagebox.askokcancel("Send Connection Request", f"Are you sure you want to connect to {IP}?"):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IP, PORT))
        tabsys1 = ttk.Notebook(tabsys)  # Tab system in the main parent tab
        tabsys.add(tabsys1, text=NICKNAME)
        CPU_tab = Frame(tabsys1)
        tabsys1.add(CPU_tab, text='CPU')
        RAM_tab = Frame(tabsys1)
        tabsys1.add(RAM_tab, text="RAM")

        ram_g = GraphPage(RAM_tab, "RAM", 1000)
        ram_g.pack(fill='both')

        l_ram = Label(RAM_tab, font=('Calibri', 14))
        l_ram.pack(fill='both')

        cpu_g = GraphPage(CPU_tab, "CPU", 1000)
        cpu_g.pack(fill='both')

        l_cpu = Label(CPU_tab, font=('Calibri', 14))
        l_cpu.pack(fill = 'both')

        Disk_tab = Frame(tabsys1)
        tabsys1.add(Disk_tab, text="Disk")

        disk_g = GraphPage(Disk_tab, "Disk", 1000)
        disk_g.pack(fill='both')

        l_disk = Label(Disk_tab, font=('Calibri', 14))
        l_disk.pack(fill='both')
        data = pickle.loads(s.recv(1024))
        monitor_cpu_ntwk(l_cpu, cpu_g)