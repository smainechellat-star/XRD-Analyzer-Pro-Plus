"""
Reusable matplotlib touch-like canvas handler (pan and zoom).
"""


class TouchCanvas:
    def __init__(self, ax, canvas):
        self.ax = ax
        self.canvas = canvas
        self.press = None
        self.xlim = None
        self.ylim = None

        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("motion_notify_event", self.on_motion)
        self.canvas.mpl_connect("scroll_event", self.on_scroll)

    def on_press(self, event):
        if event.inaxes != self.ax:
            return
        self.press = (event.xdata, event.ydata)
        self.xlim = self.ax.get_xlim()
        self.ylim = self.ax.get_ylim()

    def on_release(self, _event):
        self.press = None
        self.canvas.draw()

    def on_motion(self, event):
        if self.press is None or event.inaxes != self.ax:
            return
        dx = event.xdata - self.press[0]
        dy = event.ydata - self.press[1]
        self.ax.set_xlim(self.xlim[0] - dx, self.xlim[1] - dx)
        self.ax.set_ylim(self.ylim[0] - dy, self.ylim[1] - dy)
        self.canvas.draw()

    def on_scroll(self, event):
        if event.inaxes != self.ax:
            return
        scale = 0.9 if event.button == "up" else 1.1
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        x_center = event.xdata
        y_center = event.ydata
        self.ax.set_xlim(
            [x_center - (x_center - xlim[0]) * scale, x_center + (xlim[1] - x_center) * scale]
        )
        self.ax.set_ylim(
            [y_center - (y_center - ylim[0]) * scale, y_center + (ylim[1] - y_center) * scale]
        )
        self.canvas.draw()
