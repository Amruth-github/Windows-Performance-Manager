#Run this on client side
from tkinter import *
from GraphPage import *
from tkinter import ttk
from tkinter import messagebox
import threading as td
from time import sleep
import psutil as ps
import socket
from mplcursors import cursor
from get_resource import SLEEP_COUNT, monitor_cpu, monitor_ram, disk_usage, ntwk_usage
import pickle
import requests as rq
NTWK_RANGE = 10000
NBPOINTS = 1000

welcoming_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

flag_for_thread = False

stop = lambda : flag_for_thread

PORT = 5500

def on_closing():
    global flag_for_thread
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        welcoming_socket.close()
        flag_for_thread = True
        root.destroy()

def send_resources(serverSocket : socket.socket, stop):
    while not stop():
        try:
            cpu = ps.cpu_percent()
            ram = ps.virtual_memory()[2]
            disk = ps.disk_usage(".")[-1]
            bytes_sent, bytes_recv = ps.net_io_counters().bytes_sent, ps.net_io_counters().bytes_recv
            io = ps.net_io_counters()
            us, ds = io.bytes_sent - bytes_sent, io.bytes_recv - bytes_recv
            l_ntwk_down.config(text = f"Download : {round(ds / 0.5, 2)} Mb/s")
            l_ntwk_up.config(text = f"Upload : {round(us/0.5, 2)} Mb/s")
            serverSocket.send(pickle.dumps((cpu, ram, disk, round(us/0.5, 2) , round(ds/ 0.5, 2))))
            sleep(SLEEP_COUNT)
        except OSError:
            serverSocket.close()
    return

def handleIncomingRequest(stop):
    global welcoming_socket
    IP = ""
    try:
        rq.get("https://www.google.co.in", timeout=3)
        IP = socket.gethostbyname_ex(socket.gethostname())[-1][-1]
    except:
        IP = '127.0.0.1'
    #print(IP)
    welcoming_socket.bind((IP, PORT))
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
    CPU_tab = Frame(tabsys)
    tabsys.add(CPU_tab, text = 'CPU')
    tabsys.add(RAM_tab, text = "RAM")
    
    ram_g = GraphPage(RAM_tab, "RAM", nb_points=NBPOINTS)
    ram_g.pack(fill = 'both')

    l_ram = Label(RAM_tab, font=('Calibri', 14))
    l_ram.pack()


    cpu_g = GraphPage(CPU_tab,"CPU", nb_points=NBPOINTS)
    cpu_g.pack(fill = 'both')

    l_cpu = Label(CPU_tab, font=('Calibri', 14))
    l_cpu.pack()

    Disk_tab = Frame(tabsys)
    tabsys.add(Disk_tab, text = "Disk")

    disk_g = GraphPage(Disk_tab, "Disk", nb_points=NBPOINTS)
    disk_g.pack(fill = 'both')

    l_disk = Label(Disk_tab, font=('Calibri', 14))
    l_disk.pack()
    
    Network = Frame(tabsys)
    tabsys.add(Network, text = "Network")

    ntwk_g_up = GraphPage(Network, "Upload", NBPOINTS, (2, 2), NTWK_RANGE)
    ntwk_g_up.pack(fill = 'both')
    l_ntwk_up = Label(Network, font = ('Calibri', 14))
    l_ntwk_up.pack()

    ntwk_g_down = GraphPage(Network, "Download", NBPOINTS, (2, 2), NTWK_RANGE)
    ntwk_g_down.pack(fill = 'both')

    l_ntwk_down = Label(Network, font = ('Calibri', 14))

    l_ntwk_down.pack()

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
    crs_ntwk_up = cursor(ntwk_g_up.figure, hover=True)
    crs_ntwk_up.connect("add", lambda sel: sel.annotation.set_text(
        f'{ntwk_g_up.graph_name} : {round(sel.target[1], 2)}'
    ))

    crs_ntwk_down = cursor(ntwk_g_down.figure, hover=True)
    crs_ntwk_down.connect("add", lambda sel: sel.annotation.set_text(
        f'{ntwk_g_down.graph_name} : {round(sel.target[1], 2)}'
    )) 
    thread_for_incoming_connection_request = td.Thread(target = handleIncomingRequest, args = (stop, ))
    thread_for_incoming_connection_request.start()
    thread_for_cpu = td.Thread(target = monitor_cpu, args = (l_cpu, cpu_g, stop))
    thread_for_cpu.start()
    thread_for_ram = td.Thread(target = monitor_ram, args = (l_ram, ram_g, stop))
    thread_for_ram.start()
    thread_for_disk = td.Thread(target = disk_usage, args = (l_disk, disk_g, stop))
    thread_for_disk.start()
    thread_for_ntwk = td.Thread(target = ntwk_usage, args = (l_ntwk_up, l_ntwk_down, ntwk_g_up, ntwk_g_down, stop))
    thread_for_ntwk.start()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    mainloop()
