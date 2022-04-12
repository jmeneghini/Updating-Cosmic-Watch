import serial
import platform
import serial.tools.list_ports
import time
import sys
from tkinter import Tk
from tkinter.filedialog import asksaveasfile, askdirectory
import numpy as np
import matplotlib.pyplot as plt

def write_to_txt(filename, port, plot = False):
    try:
        with serial.Serial(port = port, baudrate=9600, bytesize=8, parity="N", stopbits=1) as ser, open(f"{filename}", "w") as txt:
            print("\nPress Ctrl + C to Terminate\n")
            line_counter = 0
            times = [0]
            rates = []
            try:
                while True:
                    line_data = ser.readline().decode("utf-8")
                    print(line_data)
                    plt.rcParams["figure.figsize"] = (11, 4)
                    plt.scatter(0, 0, color = "white")
                    plt.xlabel("Time (s)")
                    plt.ylabel("Rate ($s^{-1}$)")
                    if line_counter >= 3:
                        txt.write(line_data)
                        if plot:
                            if line_counter >= 9:
                                sub_data = line_data[line_data.find(" ")+1:]
                                t = int(sub_data[:sub_data.find(" ")])
                                times.append(t)
                                rate = 1/((t - times[-2])*1e-3)
                                rates.append(rate)
                                plt.scatter(t * 1e-3, rate, color="black", s=10)
                                avg_rate = np.array(rates).mean()
                                plt.title(f"Average Rate: {np.round(avg_rate, 4)} 1/s")
                                plt.pause(0.005)

                    line_counter += 1
                plt.show()
            except KeyboardInterrupt:
                print("Data Collection Terminated")
                pass
    except serial.SerialException:
        print("Unable to Open Port")
    except FileNotFoundError:
        print("Invalid File Name")

def copy_SD(directory, port):
    try:
        with serial.Serial(port = port, baudrate=9600, bytesize=8, parity="N", stopbits=1) as ser:
            print("\nPress Ctrl + C to Terminate")
            if ser.readline().decode("utf-8").strip() == 'CosmicWatchDetector':
                time.sleep(1)
                detector_name = ser.readline().decode("utf-8")

                print('\n-- Detector Name --')
                print(detector_name)

                ser.write("read".encode())
                counter = 0
                try:
                    while True:
                        linedata = ser.readline().decode("utf-8")  # Wait and read data
                        if 'Done' in linedata:
                            ser.close()
                        elif 'opening:' in linedata:
                            filename = f"{directory}/{linedata.split(' ')[-1].split('.txt')[0]}.txt"

                            print("Saving to: " + filename)

                            file = open(filename, "w")
                            counter = 0

                        elif 'EOF' in linedata:
                            file.close()

                        else:
                            file.write(linedata)
                            counter += 1
                except KeyboardInterrupt:
                    print("Data Transfer Terminated")
            else:
                print('--- Error ---')
                print('You are trying to read from the SD card.')
                print('Have you uploaded SDCard.ino to the Arduino?')
                print('Is there a microSD card inserted into the detector?')
                print('Exiting ...')
                sys.exit()

    except serial.SerialException:
        print("Unable to Open Port")
    except FileNotFoundError:
        print("Invalid File Name")

def del_SD(port):
    try:
        with serial.Serial(port = port, baudrate=9600, bytesize=8, parity="N", stopbits=1) as ser:
            print("\nPress Ctrl + C to Terminate\n")
            if ser.readline().decode("utf-8").strip() == 'CosmicWatchDetector':
                time.sleep(1)
                ser.write("remove".encode())
                while True:
                    data = ser.readline().decode("utf-8")  # Wait and read data
                    if data == 'Done...\r\n':
                        print("Finished deleting files.")
                        break
                ser.close()
                sys.exit()

            else:
                print('--- Error ---')
                print('You are trying to remove files from the microSD card.')
                print('Is there an SD card inserted?')
                print('Do you have the correct code on the Arduino? SDCard.ino')
                print('Exiting ...')
                sys.exit()

    except serial.SerialException:
        print("Unable to Open Port")
    except FileNotFoundError:
        print("Invalid File Name")

ports = serial.tools.list_ports.comports()
if ports == []:
    print("No Ports Available")
    sys.exit()

print("Available Serial Ports: ")
for port_info, i in zip(sorted(ports), range(len(ports))):
        print(f"[{i + 1}] {port_info[0]}: {port_info[1]} - {port_info[2]}")
try:
    selected_port = sorted(ports)[abs(int(input("\nSelect Serial Port: ")) - 1)][0]
except IndexError:
    print("Invalid Index")
    sys.exit()

options = ["[1] Record data on the computer","[2] Copy data files from SD card to your computer","[3] Remove files from SD card"]

print("\nWhat Would You Like to Do: ")
for options in options:
    print(options)

selected_op = int(input("\nSelected Operation: "))
if selected_op == 1:
    Tk().withdraw()
    txt_filename = asksaveasfile(filetypes = [("Text Document", "*.txt"), ("Comma Seperated Values", "*.csv")],defaultextension= [("Text Document", "*.txt"), ("Comma Seperated Values", "*.csv")])
    print("\nDo you want to plot live data: ")
    ans = input("Type y or n: ").lower()
    if ans == "y":
        plot = True
    else:
        plot = False
    write_to_txt(txt_filename.name, selected_port, plot)

elif selected_op == 2:
    Tk().withdraw()
    directory = askdirectory()
    copy_SD(directory,selected_port)

elif selected_op == 3:
    print("\nAre you sure that you want to remove all files from SD card?")
    ans = input("Type y or n: ").lower()
    if ans == "y":
        del_SD(selected_port)

else:
    print("Invalid Index")
    sys.exit()