import tkinter as tk
from tkinter import Toplevel, Button

class ToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind('<Enter>', self.enter)
        self.widget.bind('<Leave>', self.leave)
        self.tipwindow = None

    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # Creates a toplevel window
        self.tipwindow = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tipwindow.wm_overrideredirect(True)
        self.tipwindow.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tipwindow, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def leave(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    login_frame = tk.Frame(root)
    login_frame.pack()

    login_button = Button(login_frame, text="Login", font=("Calibri", 18, "bold"), bg="#b89b3f", fg="white", cursor="hand2")
    login_button.place(x=150, y=300)

    # Add tooltip to login_button
    ToolTip(login_button, 'Login')

    root.mainloop()
