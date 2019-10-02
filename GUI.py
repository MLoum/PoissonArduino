from __future__ import print_function
import tkinter as tk
from tkinter import ttk
from hardware import Arduino

from tkinter import filedialog




import threading

# Built-in modules
import logging
import threading
import time



class PoissonArduinoGUI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.onQuit)
        self.arduino = Arduino.Arduino(self)
        self.padx = 10
        self.nb_evt = 0
        self.evt_vals = []
        self.create_gui()


    def run(self):
        self.root.title("py Poisson")
        self.root.deiconify()
        self.root.mainloop()


    def create_gui(self):
        self.arduino_frame = tk.LabelFrame(self.root, text="Arduino")
        ttk.Label(self.arduino_frame, text="Nom port COM").grid(row=0, column=0, padx=self.padx)
        self.arduino_com_sv = tk.StringVar(value='COM6')
        ttk.Entry(self.arduino_frame, textvariable=self.arduino_com_sv, justify=tk.CENTER, width=7).grid(row=0, column=1)
        ttk.Button(self.arduino_frame, text="Connexion", width=25, command=self.connect_arduino).grid(row=0,
                                                                                                            column=2,
                                                                                                            padx=self.padx)
        self.arduino_connected_sv = tk.StringVar(value='NON')
        ttk.Label(self.arduino_frame, textvariable=self.arduino_connected_sv).grid(row=0, column=3, padx=self.padx)

        self.arduino_frame.pack(side="top", fill="both", expand=True)

        self.cmd_frame = tk.LabelFrame(self.root, text="Commande")
        ttk.Button(self.cmd_frame, text="Lancer expérience", width=25, command=self.launch_experiment).grid(row=0, column=0, padx=self.padx)
        ttk.Button(self.cmd_frame, text="Stop", width=14, command=self.stop_experiment).grid(row=0,
                                                                                                            column=1,                                                                                                          padx=self.padx)
        ttk.Label(self.cmd_frame, text="Nb d'evenements").grid(row=0, column=2, padx=self.padx)
        self.nb_evt_sv = tk.StringVar(value='0')
        ttk.Entry(self.cmd_frame, textvariable=self.nb_evt_sv, justify=tk.CENTER, width=7).grid(row=0, column=3)
        self.cmd_frame.pack(side="top", fill="both", expand=True)

        self.evt_frame = tk.LabelFrame(self.root, text="Evenements")
        self.evt_frame.pack(side="top", fill="both", expand=True)

        self.evt_list_frame = tk.LabelFrame(self.evt_frame, text="Liste des evenements")

        self.evt_list_frame.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.evt_list_frame)


        self.text = tk.Text(self.evt_list_frame, height=28, width=30)
        self.text.pack(side="left", fill="both", expand=True)

        self.scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scrollbar.set)

        self.evt_export_frame = tk.LabelFrame(self.evt_frame, text="Exporter")
        self.evt_export_frame.pack(side="left", fill="both", expand=True)
        ttk.Button(self.evt_export_frame, text="Exporter", width=12, command=self.export_data).pack(side="left", fill="both", expand=True, padx=self.padx)

        self.log_frame = tk.LabelFrame(self.root, text="log")
        self.log_frame.pack(side="top", fill="both", expand=True)

        self.scrollbar_log = tk.Scrollbar(self.log_frame)

        self.text_log = tk.Text(self.log_frame, height=5, width=30)
        self.text_log.pack(side="left", fill="both", expand=True)

        self.scrollbar_log.config(command=self.text_log.yview)
        self.text_log.config(yscrollcommand=self.scrollbar_log.set)


    def launch_experiment(self):
        self.text.delete('1.0', tk.END)
        self.evt_vals = []
        self.nb_evt = 0
        self.arduino.launch_monitor()

    def stop_experiment(self):
        self.arduino.stop_monitor()

    def add_point(self, val):
        self.evt_vals.append(val)
        self.text.insert(tk.END, str(val) + "\n")
        self.nb_evt += 1
        self.nb_evt_sv.set(str(self.nb_evt))


    def export_data(self):
        f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        text2save = str(self.text.get(1.0, tk.END))  # starts from `1.0`, not `0.0`
        f.write(text2save)
        f.close()


    def connect_arduino(self):
        r = self.arduino.connect(self.arduino_com_sv.get())
        if r is True:
            self.arduino_connected_sv.set("OK")
        else:
            self.arduino_connected_sv.set("NON")

    def onQuit(self):
        # paramFile = open('param.ini', 'w')
        # paramFile.write(self.saveDir)
        self.root.destroy()
        self.root.quit()


    def log(self, text):
        pass
        # self.text_log.insert(tk.END, text + "\n")