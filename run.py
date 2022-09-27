from tkinter import *
from tkinter import ttk, messagebox
import threading as td
from GraphPage import GraphPage
from get_resource import *
from mplcursors import cursor
import socket
import pickle

def connect_to_node(IP, PORT, NICKNAME, tabsys : ttk.Notebook):
    if messagebox.askokcancel("Send Connection Request", f"Are you sure you want to connect to {IP}?"):
        try:
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
        except:
            messagebox.showerror("Error", "Connection Timeout!!")
            return
        try:
            while not flag_for_thread:
                data = pickle.loads(s.recv(102))
                monitor_cpu_ntwk(l_cpu, cpu_g, data[0])
                monitor_ram_ntwk(l_ram, ram_g, data[1])
                disk_usage_ntwk(l_disk, disk_g, data[2])
        except:
            tabsys.forget(tabsys1)
        return

def launch_td(IP, PORT, NICKNAME):
    if len(IP) == 0 or PORT == 0:
        messagebox.showerror("Error", "All feilds are necessary!!")
        return
    if len(NICKNAME) == 0:
        NICKNAME = IP
    t = td.Thread(target = connect_to_node, args = (IP, PORT, NICKNAME, tabsys))
    t.start()

def add_new_device(Tab : Tk):
    IP = StringVar(Tab)
    PORT = IntVar(Tab)
    NICKNAME = StringVar(Tab)
    IP_e = Entry(Tab, textvariable=IP, font=('calibre',10,'normal'), width=50, borderwidth=2)
    IP_e.insert(END, "Enter IP Address")
    IP_e.pack()
    PORT_e = Entry(Tab, textvariable=PORT, font=('calibre',10,'normal'), width=50, borderwidth=2)
    PORT_e.pack()
    NICKNAME_e = Entry(Tab, textvariable=NICKNAME, font=('calibre',10,'normal'), width=50, borderwidth=2)
    NICKNAME_e.insert(END, "Enter a Nickname")
    NICKNAME_e.pack()
    Tab.bind("<Return>", lambda: launch_td(IP.get(), PORT.get(), NICKNAME.get()))
    Submit = Button(Tab, text="Send Request!", command = lambda : launch_td(IP.get(), PORT.get(), NICKNAME.get()))
    Submit.pack()
    


def PrepareTab(Tab: str, monitor_cpu, monitor_ram, disk_usage):
    tabsys1 = ttk.Notebook(tabsys)  # Tab system in the main parent tab
    tabsys.add(tabsys1, text=Tab)
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

    tabsys.select(tabsys1)

    # Cursor on graph...
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
    # Thread to get CPU Usage
    t1 = td.Thread(target = monitor_cpu, args=(
        l_cpu, cpu_g, lambda: flag_for_thread))
    t1.start()
    # Thread to get RAM Usage
    t2 = td.Thread(target = monitor_ram, args=(
        l_ram, ram_g, lambda: flag_for_thread))
    t2.start()
    # Thread to get disk Usage
    t3 = td.Thread(target = disk_usage, args=(
        l_disk, disk_g, lambda: flag_for_thread))
    t3.start()
    # Thread to get Network Usage



def on_closing():
    global flag_for_thread
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        flag_for_thread = True
        root.destroy()


if __name__ == '__main__':
    root = Tk()
    icon = PhotoImage(file="resource.png")
    root.iconphoto(False, icon)
    root.title("Windows Performance Manager")
    tabsys = ttk.Notebook(root)
    tabsys.pack(expand=1, fill='both')
    Add_device = Frame(root)
    tabsys.add(Add_device, text="Add More Devices")
    LocalTabtd = td.Thread(target=PrepareTab, args=("Local", monitor_cpu, monitor_ram, disk_usage))
    LocalTabtd.start()
    Add_dev_td = td.Thread(target = add_new_device, args = (Add_device, ))
    Add_dev_td.start()
    

    flag_for_thread = False  # A flag to manage all threads
    root.protocol("WM_DELETE_WINDOW", on_closing)
    mainloop()
