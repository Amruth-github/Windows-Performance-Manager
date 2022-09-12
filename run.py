from tkinter import *
from tkinter import messagebox
import threading as td
from GraphPage import GraphPage
from get_resource import *
from mplcursors import cursor


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
    cpu_g = GraphPage(root, "CPU", nb_points=1000)
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
    l_disk.grid(column=3, row=2)
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
    t3.start()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    mainloop()
