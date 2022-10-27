from tkinter import *
from tkinter import ttk
from GraphPage import *
from mplcursors import cursor


NBPOINTS = 1000
PORT = 5500
NTWK_RANGE = 10000

class GUI:
    def __init__(self, tabsys : ttk.Notebook, System_information, NICKNAME = "Local"):
        self.tabsys1 = ttk.Notebook(tabsys)  # Tab system in the main parent tab
        tabsys.add(self.tabsys1, text=NICKNAME)
        self.sys_info_tab = Frame(self.tabsys1)
        System_information.render(self.sys_info_tab)
        self.tabsys1.add(self.sys_info_tab, text = "System Information")
        self.CPU_tab = Frame(self.tabsys1)
        self.tabsys1.add(self.CPU_tab, text='CPU')
        self.RAM_tab = Frame(self.tabsys1)
        self.tabsys1.add(self.RAM_tab, text="RAM")

        self.ram_g = GraphPage(self.RAM_tab, "RAM", NBPOINTS)
        self.ram_g.pack(fill='both')

        self.l_ram = Label(self.RAM_tab, font=('Calibri', 14))
        self.l_ram.pack(fill='both')

        self.cpu_g = GraphPage(self.CPU_tab, "CPU", NBPOINTS)
        self.cpu_g.pack(fill='both')

        self.l_cpu = Label(self.CPU_tab, font=('Calibri', 14))
        self.l_cpu.pack(fill = 'both')

        self.Disk_tab = Frame(self.tabsys1)
        self.tabsys1.add(self.Disk_tab, text="Disk")

        self.disk_g = GraphPage(self.Disk_tab, "Disk", NBPOINTS)
        self.disk_g.pack(fill='both')

        self.l_disk = Label(self.Disk_tab, font=('Calibri', 14))
        self.l_disk.pack(fill='both')

        self.Network = Frame(tabsys)
        self.tabsys1.add(self.Network, text = "Network")

        self.ntwk_g_up = GraphPage(self.Network, "Upload", NBPOINTS, (2, 2), NTWK_RANGE)
        self.ntwk_g_up.pack(fill = 'both')
        self.l_ntwk_up = Label(self.Network, font = ('Calibri', 14))
        self.l_ntwk_up.pack()

        self.ntwk_g_down = GraphPage(self.Network, "Download", NBPOINTS, (2, 2), NTWK_RANGE)
        self.ntwk_g_down.pack(fill = 'both')

        self.l_ntwk_down = Label(self.Network, font = ('Calibri', 14))

        self.l_ntwk_up.pack()
        self.l_ntwk_down.pack()

        self.tabsys1.select(self.CPU_tab)

        crs_cpu = cursor(self.cpu_g.figure, hover = True)
        crs_cpu.connect("add", lambda sel: sel.annotation.set_text(
            f'{self.cpu_g.graph_name} : {round(sel.target[1], 2)}'
        ))
        crs_ram = cursor(self.ram_g.figure, hover=True)
        crs_ram.connect("add", lambda sel: sel.annotation.set_text(
            f'{self.ram_g.graph_name} : {round(sel.target[1], 2)}'
        ))
        crs_disk = cursor(self.disk_g.figure, hover=True)
        crs_disk.connect("add", lambda sel: sel.annotation.set_text(
            f'{self.disk_g.graph_name} : {round(sel.target[1], 2)}'
        ))
        crs_ntwk_up = cursor(self.ntwk_g_up.figure, hover=True)
        crs_ntwk_up.connect("add", lambda sel: sel.annotation.set_text(
            f'{self.ntwk_g_up.graph_name} : {round(sel.target[1], 2)}'
        ))

        crs_ntwk_down = cursor(self.ntwk_g_down.figure, hover=True)
        crs_ntwk_down.connect("add", lambda sel: sel.annotation.set_text(
            f'{self.ntwk_g_down.graph_name} : {round(sel.target[1], 2)}'
        ))