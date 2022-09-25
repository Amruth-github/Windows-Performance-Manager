from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import threading as td
from GraphPage import GraphPage
from get_resource import *
from mplcursors import cursor


def PrepareTab(Tab: str):
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
    """ crs_ntwk_up = cursor(ntwk_g_up.figure, hover=True)
    crs_ntwk_up.connect("add", lambda sel: sel.annotation.set_text(
        f'{ntwk_g_up.graph_name} : {round(sel.target[1], 2)}'
    ))

    crs_ntwk_down = cursor(ntwk_g_down.figure, hover=True)
    crs_ntwk_down.connect("add", lambda sel: sel.annotation.set_text(
        f'{ntwk_g_down.graph_name} : {round(sel.target[1], 2)}'
    )) """

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
    """ t4 = td.Thread(target = ntwk_usage, args = (l_ntwk_up, l_ntwk_down, ntwk_g_up, ntwk_g_down, lambda : flag_for_thread))
    t4.start() """


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
    LocalTabtd = td.Thread(target=PrepareTab, args=("Local", ))
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

    flag_for_thread = False  # A flag to manage all threads
    root.protocol("WM_DELETE_WINDOW", on_closing)
    mainloop()
