from tkinter import Label
from time import sleep
import psutil as ps
from GraphPage import GraphPage

#For local Resources

def monitor_cpu(l_cpu : Label, cpu_g : GraphPage, stop):
    while not stop():
        cpu_usage = ps.cpu_percent()
        l_cpu.config(text = f"CPU usage : {cpu_usage}%")
        cpu_g.animate(cpu_usage)
        sleep(0.5)
    return

def monitor_ram(l_ram:Label, ram_g:GraphPage, stop):
    while not stop():
        ram_usage = ps.virtual_memory()[2]
        l_ram.config(text = f"RAM Usage : {ram_usage}%")
        ram_g.animate(ram_usage)
        sleep(0.5)
    return

def disk_usage(l_disk : Label, disk_g : GraphPage, stop):
    while not stop():
        disk = ps.disk_usage(".")[-1]
        l_disk.config(text = f"Disk Usage : {disk}%")
        disk_g.animate(disk)
        sleep(0.5)
    return

""" def ntwk_usage(l_ntwk_up : Label, l_ntwk_down : Label, ntwk_g_up : GraphPage, ntwk_g_down : GraphPage, stop):
    while not stop():
        up = ps.net_io_counters().
        down = ps.net_io_counters().bytes_recv * 10 ** -6
        l_ntwk_down.config(text = str(down))
        l_ntwk_up.config(text = str(up))
        ntwk_g_up.animate(up)
        ntwk_g_down.animate(down)
        sleep(0.5)
    return  """
#For resources from other nodes
def monitor_cpu_ntwk(l_cpu : Label, cpu_g : GraphPage, data):
    l_cpu.config(text = f"CPU Usage : {data}%")
    cpu_g.animate(data)

def monitor_ram_ntwk(l_ram:Label, ram_g:GraphPage, data):
    l_ram.config(text = f"RAM Usage : {data}%")
    ram_g.animate(data)

def disk_usage_ntwk(l_disk : Label, disk_g : GraphPage, data):
    l_disk.config(text = f"CPU Usage : {data}%")
    disk_g.animate(data)
    

""" def ntwk_usage(l_ntwk_up : Label, l_ntwk_down : Label, ntwk_g_up : GraphPage, ntwk_g_down : GraphPage, stop):
    while not stop():
        up = ps.net_io_counters().
        down = ps.net_io_counters().bytes_recv * 10 ** -6
        l_ntwk_down.config(text = str(down))
        l_ntwk_up.config(text = str(up))
        ntwk_g_up.animate(up)
        ntwk_g_down.animate(down)
        sleep(0.5)
    return  """