from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import matplotlib.dates as mdates


class GraphPage(Frame):

    def __init__(self, parent, graph_name, nb_points, fig_size = (5, 5), y_lim = 100):
        # nb_points: number of points for the graph
        Frame.__init__(self, parent)
        # matplotlib figure
        self.graph_name = graph_name
        self.figure = Figure(figsize=fig_size, dpi=100)
        self.ax = self.figure.add_subplot(111)
        # format the x-axis to show the time
        myFmt = mdates.DateFormatter("%H:%M:%S")
        self.ax.xaxis.set_major_formatter(myFmt)

        # initial x and y data
        dateTimeObj = datetime.now() + timedelta(seconds=-nb_points)
        self.x_data = [dateTimeObj +
                       timedelta(seconds=i) for i in range(nb_points)]
        self.y_data = [0 for i in range(nb_points)]
        # create the plot
        self.plot = self.ax.plot(self.x_data, self.y_data, label=self.graph_name)[0]
        self.ax.set_ylim(0, y_lim)
        self.ax.set_xlim(self.x_data[0], self.x_data[-1])

        label = Label(self, text=self.graph_name)
        label.pack(pady=10, padx=10)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

    def animate(self, data):
        # append new data point to the x and y data
        self.x_data.append(datetime.now())
        self.y_data.append(data)
        # remove oldest data point
        self.x_data = self.x_data[1:]
        self.y_data = self.y_data[1:]
        #  update plot data
        self.plot.set_xdata(self.x_data)
        self.plot.set_ydata(self.y_data)
        self.ax.set_xlim(self.x_data[0], self.x_data[-1])
        self.canvas.draw_idle()  # redraw plot
