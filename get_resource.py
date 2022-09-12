from tkinter import Label
from time import sleep
import psutil as ps
from GraphPage import GraphPage

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