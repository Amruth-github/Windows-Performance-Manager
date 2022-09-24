from tkinter import *
from GraphPage import *
from tkinter import ttk
from tkinter import messagebox
import threading as td
from time import sleep
import psutil as ps
import socket
from mplcursors import cursor
import pickle

welcoming_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

flag_for_thread = False

def on_closing():
    global flag_for_thread
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        welcoming_socket.close()
        flag_for_thread = True
        root.destroy()

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

def send_resources(serverSocket : socket.socket, stop):
    while not stop():
        try:
            cpu = ps.cpu_percent()
            ram = ps.virtual_memory()[2]
            disk = ps.disk_usage(".")[-1]
            serverSocket.send(pickle.dumps((cpu, ram, disk)))
            sleep(0.5)
        except OSError:
            return
    return


def handleIncomingRequest(stop):
    global welcoming_socket
    welcoming_socket.bind(('127.0.0.1', 5500))
    welcoming_socket.listen()
    while not stop():
        try:
            serverSocket, clientAddress = welcoming_socket.accept()
            if messagebox.askokcancel("Incoming Connection Request", "Do you want to proceed?"):
                thread_for_sending_resources = td.Thread(target = send_resources, args = (serverSocket, lambda : flag_for_thread))
                thread_for_sending_resources.start()
            else:
                serverSocket.close()
        except OSError:
            return

if __name__ == '__main__':
    root = Tk()
    icon = PhotoImage(file="resource.png")
    root.iconphoto(False, icon)
    root.title("Windows Performance Manager")
    tabsys = ttk.Notebook(root) #Tab system in the main parent tab
    tabsys.pack(expand = 1, fill = 'both')
    Label(tabsys, text = "\n").pack()
    RAM_tab = Frame(tabsys) 
    tabsys.add(RAM_tab, text = "RAM")
    
    ram_g = GraphPage(RAM_tab, "RAM", nb_points=1000)
    ram_g.pack(fill = 'both')

    l_ram = Label(RAM_tab, font=('Calibri', 14))
    l_ram.pack()

    CPU_tab = Frame(tabsys)
    tabsys.add(CPU_tab, text = 'CPU')

    cpu_g = GraphPage(CPU_tab,"CPU", nb_points=1000)
    cpu_g.pack(fill = 'both')

    l_cpu = Label(CPU_tab, font=('Calibri', 14))
    l_cpu.pack()

    Disk_tab = Frame(tabsys)
    tabsys.add(Disk_tab, text = "Disk")

    disk_g = GraphPage(Disk_tab, "Disk", nb_points=1000)
    disk_g.pack(fill = 'both')

    l_disk = Label(Disk_tab, font=('Calibri', 14))
    l_disk.pack()
    
    """ Network = Frame(tabsys1)
    tabsys1.add(Network, text = "Network")

    ntwk_g_up = GraphPage(Network, "Upload", nb_points=10000)
    ntwk_g_up.pack(fill = 'both')

    ntwk_g_down = GraphPage(Network, "Download", nb_points=10000)
    ntwk_g_down.pack(fill = 'both')

    l_ntwk_up = Label(Network, font = ('Calibri', 14))
    l_ntwk_down = Label(Network, font = ('Calibri', 14))

    l_ntwk_up.pack()
    l_ntwk_down.pack() """

    #Cursor on graph...
    crs_cpu = cursor(cpu_g.figure, hover=True)
    crs_cpu.connect("add", lambda sel: sel.annotation.set_text(
        f'{cpu_g.graph_name} : {round(sel.target[1], 2)}'
    ))
    crs_ram = cursor(ram_g.figure, hover=True)
    crs_ram.connect("add", lambda sel: sel.annotation.set_text(
        f'{ram_g.graph_name} : {round(sel.target[1], 2)}'
    ))
    crs_disk = cursor(disk_g.figure, hover=True)
    crs_disk.connect("add", lambda sel: sel.annotation.set_text(
        f'{disk_g.graph_name} : {round(sel.target[1], 2)}'
    ))
    """ crs_ntwk_up = cursor(ntwk_g_up.figure, hover=True)
    crs_ntwk_up.connect("add", lambda sel: sel.annotation.set_text(
        f'{ntwk_g_up.graph_name} : {round(sel.target[1], 2)}'
    ))

    crs_ntwk_down = cursor(ntwk_g_down.figure, hover=True)
    crs_ntwk_down.connect("add", lambda sel: sel.annotation.set_text(
        f'{ntwk_g_down.graph_name} : {round(sel.target[1], 2)}'
    )) """
    thread_for_incoming_connection_request = td.Thread(target = handleIncomingRequest, args = (lambda : flag_for_thread, ))
    thread_for_incoming_connection_request.start()
    thread_for_cpu = td.Thread(target = monitor_cpu, args = (l_cpu, cpu_g, lambda : flag_for_thread))
    thread_for_cpu.start()
    thread_for_ram = td.Thread(target = monitor_ram, args = (l_ram, ram_g, lambda: flag_for_thread))
    thread_for_ram.start()
    thread_for_disk = td.Thread(target = disk_usage, args = (l_disk, disk_g, lambda : flag_for_thread))
    thread_for_disk.start()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    mainloop()


    



