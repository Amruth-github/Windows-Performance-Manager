#Run this on server side
from tkinter import *
from tkinter import ttk, messagebox
import threading as td
from get_resource import *
from gui_components import GUI
from System_information import System_information
import socket
import pickle


NBPOINTS = 1000
PORT = 5500
NTWK_RANGE = 10000
stop = lambda : flag_for_thread


def connect_to_node(IP, NICKNAME, tabsys : ttk.Notebook): # Connect to another node and prepare the GUI on the server side.
    if messagebox.askokcancel("Send Connection Request", f"Are you sure you want to connect to {IP}?"):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((IP, PORT))
            bytes_of_sys_info = s.recv(1024)
            sys_info : System_information = pickle.loads(bytes_of_sys_info) #Get system information of the client side.
            GUI_for_node = GUI(tabsys, sys_info, NICKNAME)

        except:
            messagebox.showerror("Error", "Connection Timeout!!")
            return
        try:
            while not flag_for_thread:
                data = pickle.loads(s.recv(102))
                monitor_cpu_ntwk(GUI_for_node.l_cpu, GUI_for_node.cpu_g, data[0])
                monitor_ram_ntwk(GUI_for_node.l_ram, GUI_for_node.ram_g, data[1])
                disk_usage_ntwk(GUI_for_node.l_disk, GUI_for_node.disk_g, data[2])
                ntwk_usage_ntwk(GUI_for_node.l_ntwk_up, GUI_for_node.l_ntwk_down, GUI_for_node.ntwk_g_up, GUI_for_node.ntwk_g_down, data[3], data[4])
                sys_info.used_ram.config(text = f"Used RAM: {round(sys_info.information['Total RAM'] * data[1]/100, 2)} GB")
                sys_info.used_ram.pack_configure(pady=20, side= TOP, anchor="w")
                sys_info.available_ram.config(text = f"Available RAM: {round(sys_info.information['Total RAM'] - sys_info.information['Total RAM'] * data[1]/100, 2)} GB")
                sys_info.available_ram.pack_configure(pady=20, side= TOP, anchor="w")
        except:
            try:
                tabsys.forget(GUI_for_node.tabsys1)
            except:
                del(GUI_for_node)
        return

def launch_td(IP, NICKNAME):
    if len(IP) == 0 or IP == "Enter IP Address":
        messagebox.showerror("Error", "All feilds are necessary!!")
        return
    if len(NICKNAME) == 0 or NICKNAME == "Enter a Nickname":
        NICKNAME = IP
    t = td.Thread(target = connect_to_node, args = (IP, NICKNAME, tabsys))
    t.start()

def add_new_device(Tab : Tk):
    IP = StringVar(Tab)
    NICKNAME = StringVar(Tab)
    IP_e = Entry(Tab, textvariable=IP, font=('calibre',10,'normal'), width=50, borderwidth=2)
    IP_e.insert(END, "Enter IP Address")
    IP_e.pack()
    NICKNAME_e = Entry(Tab, textvariable=NICKNAME, font=('calibre',10,'normal'), width=50, borderwidth=2)
    NICKNAME_e.insert(END, "Enter a Nickname")
    NICKNAME_e.pack()
    Submit = Button(Tab, text="Send Request!", command = lambda : launch_td(IP.get(), NICKNAME.get()))
    Submit.pack()


def PrepareTab(monitor_cpu, monitor_ram, disk_usage): # Tab system in the main parent tab

    sys_info = System_information()
    GUI_for_node = GUI(tabsys, sys_info) #Object that constructs required GUI in any page
    tabsys.select(GUI_for_node.tabsys1)

    # Thread to get CPU Usage
    t1 = td.Thread(target = monitor_cpu, args=(
        GUI_for_node.l_cpu, GUI_for_node.cpu_g, stop))
    t1.start()
    # Thread to get RAM Usage
    t2 = td.Thread(target = monitor_ram, args=(
        GUI_for_node.l_ram, GUI_for_node.ram_g, stop))
    t2.start()
    # Thread to get disk Usage
    t3 = td.Thread(target = disk_usage, args=(
        GUI_for_node.l_disk, GUI_for_node.disk_g, stop))
    t3.start()
    # Thread to get Network Usage
    t4 = td.Thread(target=ntwk_usage, args = (GUI_for_node.l_ntwk_up, GUI_for_node.l_ntwk_down, GUI_for_node.ntwk_g_up, GUI_for_node.ntwk_g_down, stop))
    t4.start()

    t5 = td.Thread(target = update_ram_readings, args = (sys_info, stop))
    t5.start()



def on_closing():
    global flag_for_thread
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        flag_for_thread = True
        root.destroy()


if __name__ == '__main__':
    #from startup import *
    root = Tk()
    icon = PhotoImage(file="resource.png")
    root.iconphoto(False, icon)
    root.title("Windows Performance Manager")
    tabsys = ttk.Notebook(root)
    tabsys.pack(expand=1, fill='both')
    Add_device = Frame(root)
    tabsys.add(Add_device, text="Add More Devices")
    LocalTabtd = td.Thread(target = PrepareTab, args=(monitor_cpu, monitor_ram, disk_usage))
    LocalTabtd.start()
    Add_dev_td = td.Thread(target = add_new_device, args = (Add_device, ))
    Add_dev_td.start()
    

    flag_for_thread = False  # A flag to manage all threads
    root.protocol("WM_DELETE_WINDOW", on_closing)
    mainloop()
