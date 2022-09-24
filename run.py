from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import threading as td
from GraphPage import GraphPage
from get_resource import *
from mplcursors import cursor

def PrepareTab(Tab : str):
    tabsys1 = ttk.Notebook(tabsys) #Tab system in the main parent tab
    tabsys.add(tabsys1, text = Tab)

    RAM_tab = Frame(tabsys1) 
    tabsys1.add(RAM_tab, text = "RAM")
    
    ram_g = GraphPage(RAM_tab, "RAM", nb_points=1000)
    ram_g.pack(fill = 'both')

    l_ram = Label(RAM_tab, font=('Calibri', 14))
    l_ram.pack()

    CPU_tab = Frame(tabsys1)
    tabsys1.add(CPU_tab, text = 'CPU')

    cpu_g = GraphPage(CPU_tab,"CPU", nb_points=1000)
    cpu_g.pack(fill = 'both')

    l_cpu = Label(CPU_tab, font=('Calibri', 14))
    l_cpu.pack()

    Disk_tab = Frame(tabsys1)
    tabsys1.add(Disk_tab, text = "Disk")

    disk_g = GraphPage(Disk_tab, "Disk", nb_points=1000)
    disk_g.pack(fill = 'both')

    l_disk = Label(root, font=('Calibri', 14))
    l_disk.pack()
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

    #Threads to map each resource
    t1 = td.Thread(target=monitor_cpu, args=(
        l_cpu, cpu_g, lambda: flag_for_thread))
    t1.start()
    t2 = td.Thread(target=monitor_ram, args=(
        l_ram, ram_g, lambda: flag_for_thread))
    t2.start()
    t3 = td.Thread(target=disk_usage, args=(
        l_disk, disk_g, lambda: flag_for_thread))
    t3.start()



    
    


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
    tabsys.pack(expand = 1, fill = 'both')
    LocalTabtd = td.Thread(target = PrepareTab, args = ("Local", ))
    LocalTabtd.start()
    """ cpu_g = GraphPage(LocalTab,"CPU", nb_points=1000)
    cpu_g.grid(column=1, row=0)
    l_cpu = Label(root, font=('Calibri', 14))
    l_ram = Label(root, font=('Calibri', 14))
    l_cpu.grid(column=1, row=2)
    ram_g = GraphPage(root, "RAM", nb_points=1000)
    ram_g.grid(column=1, row=4)
    l_ram.grid(column=1, row=6)
    disk_g = GraphPage(root, "Disk", nb_points=1000)
    disk_g.grid(column=3, row=0)
    l_disk = Label(root, font=('Calibri', 14))
    l_disk.grid(column=3, row=2) """
    """ cpu_g, l_cpu, ram_g, l_ram, disk_g, l_disk = PrepareTab("Local")
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
    flag_for_thread = False
    t1 = td.Thread(target=monitor_cpu, args=(
        l_cpu, cpu_g, lambda: flag_for_thread))
    t1.start()
    t2 = td.Thread(target=monitor_ram, args=(
        l_ram, ram_g, lambda: flag_for_thread))
    t2.start()
    t3 = td.Thread(target=disk_usage, args=(
        l_disk, disk_g, lambda: flag_for_thread))
    t3.start() """
    flag_for_thread = False #A flag to manage all threads
    root.protocol("WM_DELETE_WINDOW", on_closing)
    mainloop()
