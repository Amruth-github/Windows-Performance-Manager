from tkinter import Label
from time import sleep
import psutil as ps
from GraphPage import *

SLEEP_COUNT = 0.5

def color_for_label(data : float):
    if data < 50:
        return "Green"
    if data >= 50 and data < 90:
        return "orange"
    if data >= 90:
        return "red"

#For local Resources

def monitor_cpu(l_cpu : Label, cpu_g : GraphPage, stop):
    while not stop():
        cpu_usage = ps.cpu_percent()
        l_cpu.config(text = f"CPU usage : {cpu_usage}%", fg = color_for_label(cpu_usage))
        cpu_g.animate(cpu_usage)
        sleep(SLEEP_COUNT)
    return

def monitor_ram(l_ram:Label, ram_g:GraphPage, stop):
    while not stop():
        ram_usage = ps.virtual_memory()[2]
        l_ram.config(text = f"RAM Usage : {ram_usage}%", fg = color_for_label(ram_usage))
        ram_g.animate(ram_usage)
        sleep(SLEEP_COUNT)
    return

def disk_usage(l_disk : Label, disk_g : GraphPage, stop):
    while not stop():
        disk = ps.disk_usage(".")[-1]
        l_disk.config(text = f"Disk Usage : {disk}%", fg = color_for_label(disk))
        disk_g.animate(disk)
        sleep(SLEEP_COUNT)
    return

def ntwk_usage(l_ntwk_up : Label, l_ntwk_down : Label, ntwk_g_up : GraphPage, ntwk_g_down : GraphPage, stop):
    while not stop():
        bytes_sent, bytes_recv = ps.net_io_counters().bytes_sent, ps.net_io_counters().bytes_recv
        io = ps.net_io_counters()
        us, ds = io.bytes_sent - bytes_sent, io.bytes_recv - bytes_recv
        l_ntwk_down.config(text = f"Download : {round(ds / SLEEP_COUNT, 2)} Kb/s")
        l_ntwk_up.config(text = f"Upload : {round(us/SLEEP_COUNT, 2)} Kb/s")
        ntwk_g_up.animate(us/0.5)
        ntwk_g_down.animate(ds/0.5)
        sleep(SLEEP_COUNT)
    return
#For resources from other nodes
def monitor_cpu_ntwk(l_cpu : Label, cpu_g : GraphPage, data):
    l_cpu.config(text = f"CPU Usage : {data}%", fg = color_for_label(data))
    cpu_g.animate(data)

def monitor_ram_ntwk(l_ram:Label, ram_g:GraphPage, data):
    l_ram.config(text = f"RAM Usage : {data}%", fg = color_for_label(data))
    ram_g.animate(data)

def disk_usage_ntwk(l_disk : Label, disk_g : GraphPage, data):
    l_disk.config(text = f"Disk Usage : {data}%", fg = color_for_label(data))
    disk_g.animate(data)

def ntwk_usage_ntwk(l_ntwk_up: Label, l_ntwk_down: Label, ntwk_g_up: GraphPage, ntwk_g_down: GraphPage, data_up, data_down):
    l_ntwk_up.config(text = f"Upload = {data_up} Kb/s")
    l_ntwk_down.config(text = f"Download = {data_down} Kb/s")
    ntwk_g_up.animate(data_up)
    ntwk_g_down.animate(data_down) 

#Update RAM Reading in system information Tab
def update_ram_readings(sys_info, stop):
    while not stop():
        sys_info.used_ram.config(text = f"Used RAM: {str(round(ps.virtual_memory().used/1000000000, 2)) + ' GB'} ")
        sys_info.used_ram.pack_configure(pady=10, side= TOP, anchor="w")
        sys_info.available_ram.config(text = f"Available RAM: {str(round(ps.virtual_memory().available/1000000000, 2)) + ' GB'}")
        sys_info.available_ram.pack_configure(pady=10, side= TOP, anchor="w")
        sleep(SLEEP_COUNT)
    