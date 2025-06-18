import tkinter as tk
from tkinter import *

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

window = tk.Tk()
window.title("Symulacja wachadła Foucault")
window.configure(bg="white")

label_phi = tk.Label(window, text="Szerokość geograficzna w stopniach:", bg='white', font=("Segoe UI", 20)).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
entry_phi = tk.Entry(window, font=("Segoe UI", 20))
entry_phi.insert(0, 90)
entry_phi.grid(row=0, column=1, padx=10, pady=10)

label_length = tk.Label(window, text="Długość liny wahadła (50-1000):", bg='white', font=("Segoe UI", 20)).grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
entry_length = tk.Entry(window, font=("Segoe UI", 20))
entry_length.insert(0, 100)
entry_length.grid(row=1, column=1, padx=10, pady=10)

label_rot = tk.Label(window, text="Mnożnik prędkości obrotu ziemi (1-1000):", bg='white', font=("Segoe UI", 20)).grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
entry_rot = tk.Entry(window, font=("Segoe UI", 20))
entry_rot.insert(0, 1000)
entry_rot.grid(row=2, column=1, padx=10, pady=10)

label_speed = tk.Label(window, text="Mnożnik prędkości wahadła (1-15):", bg='white', font=("Segoe UI", 20)).grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
entry_speed = tk.Entry(window, font=("Segoe UI", 20))
entry_speed.insert(0, 10)
entry_speed.grid(row=3, column=1, padx=10, pady=10)

def validate_input():
    try:
        phi = int(entry_phi.get())

        if phi >= 0:
            direction = 1
        else:
            direction = -1

        if phi > 90:
            phi = 90
        elif phi < -90:
            phi = -90
        
        entry_phi.delete(0, END)
        entry_phi.insert(0, str(phi))

        phi = np.radians(phi)

    except ValueError:
        print("Invalid input.")
        return

    try:
        length = int(entry_length.get())

        if length > 1000:
            length = 1000
        elif length < 10:
            length = 10
        
        entry_length.delete(0, END)
        entry_length.insert(0, str(length))

    except ValueError:
        print("Invalid input.")
        return

    try:
        rot_mul = int(entry_rot.get())

        if rot_mul > 1000:
            rot_mul = 1000
        elif rot_mul < 1:
            rot_mul = 1

        entry_rot.delete(0, END)
        entry_rot.insert(0, str(rot_mul))

    except ValueError:
        print("Invalid input.")
        return

    try:
        speed_mul = int(entry_speed.get())

        if speed_mul > 15:
            speed_mul = 15
        elif speed_mul < 1:
            speed_mul = 1

        entry_speed.delete(0, END)
        entry_speed.insert(0, str(speed_mul))

    except ValueError:
        print("Invalid input.")
        return

    return phi, direction, length, speed_mul, rot_mul

plotting = FALSE

def animate_plot():
    global plotting

    if plotting:
        return

    style.use("fivethirtyeight")
    fig = plt.figure()
    fig.canvas.manager.set_window_title("Wizualizacja wahadła Foucault")
    fig.set_size_inches(8, 8) #Wielkość w calach
    ax = fig.add_subplot(1,1,1)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    line, = ax.plot([], [], lw=2)

    data = validate_input()
    if data is None:
        return
    phi, direction, L, speed_mul, rot_mul = data
    R, g = 0.00007292115*rot_mul, 9.80665
    C1 = C2 = 1

    x_val = []
    y_val = []

    def update(t):
        x = C1 * np.cos(np.sqrt(g / L) * t - R * np.sin(phi) * t) + C2 * np.cos(np.sqrt(g / L) * t + R * np.sin(phi) * t)
        y = C1 * np.sin(np.sqrt(g / L) * t - R * np.sin(phi) * t) - C2 * np.sin(np.sqrt(g / L) * t + R * np.sin(phi) * t)

        x_val.append(x)
        y_val.append(y)
        line.set_data(x_val, y_val)
        return line,


    plotting = True

    def on_close(event):
        global plotting
        globals()["plotting"] = FALSE

    fig.canvas.mpl_connect('close_event', on_close)

    ani = animation.FuncAnimation(fig, update, frames=speed_mul*np.linspace(0, 1000, 20000), interval = 50)
    plt.show()

Button(window, text="Symulacja", command=animate_plot, font=("Segoe UI", 20)).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

window.mainloop()