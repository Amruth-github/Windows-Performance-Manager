#Run this on client side
from tkinter import *
from GraphPage import *
from tkinter import ttk
from tkinter import messagebox
import threading as td
from time import sleep
import psutil as ps
import socket
from System_information import System_information
from get_resource import SLEEP_COUNT, monitor_cpu, monitor_ram, disk_usage, ntwk_usage, update_ram_readings
import pickle
import requests as rq
from gui_components import GUI
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
    serverSocket.send(pickle.dumps(System_information()))
    while not stop():
        try:
            cpu = ps.cpu_percent()
            ram = ps.virtual_memory()[2]
            disk = ps.disk_usage(".")[-1]
            bytes_sent, bytes_recv = ps.net_io_counters().bytes_sent, ps.net_io_counters().bytes_recv
            io = ps.net_io_counters()
            us, ds = io.bytes_sent - bytes_sent, io.bytes_recv - bytes_recv
            GUI_elements.l_ntwk_down.config(text = f"Download : {round(ds / 0.5, 2)} Mb/s")
            GUI_elements.l_ntwk_up.config(text = f"Upload : {round(us/0.5, 2)} Mb/s")
            serverSocket.send(pickle.dumps((cpu, ram, disk, round(us/0.5, 2) , round(ds/ 0.5, 2))))
            sleep(SLEEP_COUNT)
        except OSError:
            serverSocket.close()
            return
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
    welcoming_socket.bind((IP, PORT))
    welcoming_socket.listen()
    while not stop():
        try:
            serverSocket, clientAddress = welcoming_socket.accept()
            if messagebox.askokcancel("Incoming Connection Request", "Do you want to proceed?"):
                thread_for_sending_resources = td.Thread(target = send_resources, args = (serverSocket, lambda : flag_for_thread))
                thread_for_sending_resources.start()
        except:
            return
    return

if __name__ == '__main__':
    root = Tk()
    icon = PhotoImage(file="resource.png")
    root.iconphoto(False, icon)
    root.title("Windows Performance Manager")
    tabsys = ttk.Notebook(root) #Tab system in the main parent tab
    tabsys.pack(expand = 1, fill = 'both')
    Label(tabsys, text = "\n").pack()
    sys_info = System_information()
    GUI_elements = GUI(tabsys, sys_info) #Entire GUI component
    
    thread_for_incoming_connection_request = td.Thread(target = handleIncomingRequest, args = (stop, ))
    thread_for_incoming_connection_request.start()
    thread_for_cpu = td.Thread(target = monitor_cpu, args = (GUI_elements.l_cpu, GUI_elements.cpu_g, stop))
    thread_for_cpu.start()
    thread_for_ram = td.Thread(target = monitor_ram, args = (GUI_elements.l_ram, GUI_elements.ram_g, stop))
    thread_for_ram.start()
    thread_for_disk = td.Thread(target = disk_usage, args = (GUI_elements.l_disk, GUI_elements.disk_g, stop))
    thread_for_disk.start()
    thread_for_ntwk = td.Thread(target = ntwk_usage, args = (GUI_elements.l_ntwk_up, GUI_elements.l_ntwk_down, GUI_elements.ntwk_g_up, GUI_elements.ntwk_g_down, stop))
    thread_for_ntwk.start()
    thread_for_updating_ram = td.Thread(target = update_ram_readings, args = (sys_info, stop))
    thread_for_updating_ram.start()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    mainloop()
