
import re
import math
import csv
import time

import tkinter as tk 
import os
import tkinter.messagebox 

import subprocess, signal
import sys,shutil
import psutil
from tkinter import filedialog



def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

def enregistement_traj(r_rosbag,r_sorite):
    c_rosbag = "ros2 bag play -r 100 "+r_rosbag+" --topics /tf /tf_static "
    c_txt = f"ros2 topic echo /tf >> {r_sorite}traj.txt"
    global processe1
    processe2 = subprocess.Popen(c_txt, shell=True, stdout=subprocess.PIPE) 
    # time.sleep(1)
    processe1 = subprocess.Popen(c_rosbag, shell=True, stdout=None) 

    processe1.wait()
    kill(processe2.pid)



def conv_txt2csv(inputFileName,filterRate=20):

    # Initialize 
    outputFileName = inputFileName.replace('.txt', '.csv')
    startTime = time.time()
    output=[]
    outputFilter=[]
    newX = 0
    newY = 0
    newZ = 0
    Z = 0

    # Read input text file
    textFile = open(inputFileName, "r")
    rawLines = textFile.readlines()
    textFile.close()

    # Create a header in the output array (x,y,z,yaw)
    output.append(['x', 'y', 'z', 'yaw'])

    for i in rawLines:
        line = re.split(' |,',i)
        line = [item for item in line if item != ""]
        line = [item.rstrip('\n') for item in line]

        if len(line) >= 2:
            if line[0] == 'x:' and float(line[1]) >=10 :
                X = float(line[1])
                newX = 1

            elif line[0] == 'y:' and float(line[1]) >=10 :
                Y = float(line[1])
                newY = 1

            elif line[0] == 'z:' and float(line[1]) >=10 :
                Z = float(line[1])
                newZ = 1

        
        if newX == 1 and newY ==1 and newZ ==1:
            output.append([X, Y, Z, 0])
            newX = 0
            newY = 0
            newZ = 0

    j=0
    for i in output:
        j=j+1
        if j % filterRate == 1:  # Write only every n line
            outputFilter.append(i)

    # Write results in the output file
    with open(outputFileName, 'w', newline='') as f:
        csv.writer(f, delimiter=',').writerows(outputFilter)

    print("--- %.3f seconds ---" % (time.time() - startTime))



def print_selection(v=""):
    global frequence
    if v=="":
        pass
    else:
        l.config(text='you have selected ' + v)
        frequence = int(v)
    if var1.get() != 0 :
        frequence = var1.get()
        l.config(text='you have selected ' + str(frequence))

def drag_enter(event):
    drop_area.config(bg="lightblue")

def drag_leave(event):
    drop_area.config(bg="white")

# def drag_clique():
#     drop_area.config(bg="gray")
#     pass

def drag_drop(event):
    global file_path
    drop_area.config(bg="white")
    window.withdraw()
    # file_path = filedialog.askopenfilename()
    file_path = filedialog.askdirectory()

    # window.geometry('750x650')
    # window.update()

    file_path = file_path+"/"
    var.set("Repertoire du Rosbag que vous avez choisi: \n"+file_path)
    window.deiconify()
    window.update()

    print(file_path)

def valider():
    global frequence


    if os.path.isdir(file_path): 
        # var.set("le repertoire sortie: "+e1.get()+"\nfilterRate: "+str(frequence))
        r_rosbag = file_path
        r_sorite = r_rosbag
        r_txt = r_sorite+"traj.txt"

        enregistement_traj(r_rosbag,r_sorite)

        processe1.wait()
        if var1.get() != 0 :
            frequence = var1.get()

         
        conv_txt2csv(inputFileName=r_txt,filterRate=frequence)



    else :
        tk.messagebox.showerror(title='Erro', message="c'est pas une bonne repertoire !!")






window = tk.Tk()
window.title("Creation la trajectoire a partir de ROS2 BAG")
window.geometry('750x650')
window.resizable(False, False)


# l0 = tk.Label(window, text='Saisir le repertoire de ROS2BAG  (avec/ à la fin):', bg='green', font=('Arial', 11), width=65, height=2)
# l1 = tk.Label(window, text='Saisir le repertoire sortie (avec/ à la fin):', bg='green', font=('Arial', 11), width=65, height=2)

# e0 = tk.Entry(window, show=None, font=('Arial', 11),width=68)
# e1 = tk.Entry(window, show=None, font=('Arial', 11),width=68)
drop_area = tk.Label(window,text="Ouvrir le dossier \ndu Ros2Bag ", font=('Arial', 14), bg="white",width=20,height=5)



var = tk.StringVar()    # 将label标签的内容设置为字符类型，用var来接收hit_me函数的传出内容用以显示在标签上
a = tk.Label(window, textvariable=var, bg='gray', fg='white', font=('Arial', 11), width=75, height=16)





l = tk.Label(window, bg='green', fg='white', width=80, text='X point every 20 tf value (meaning 1 point per second as output trajectory)')
s = tk.Scale(window, label='HZ', from_=0, to=30, orient=tk.HORIZONTAL, length=400, showvalue=0,tickinterval=2, resolution=1, command=print_selection)
var1 = tk.IntVar()
c1 = tk.Checkbutton(window, text='20HZ',variable=var1, onvalue=20, offvalue=0,command=print_selection) 

b = tk.Button(window, text='Valider', font=('Arial', 12), width=10, height=1, command=valider)


if var1.get() != 0 :
    frequence = var1.get()
    print(frequence)


drop_area.bind("<Enter>",drag_enter)
drop_area.bind("<Leave>",drag_leave)
drop_area.bind("<ButtonRelease-1>",drag_drop)


# l0.pack(pady=10)    
# e0.pack(ipady=3)    
# l1.pack(pady=10)  
# e1.pack(ipady=3) 
drop_area.pack(pady=10) 

l.pack(pady=10)
s.pack()
c1.pack()
b.pack(pady=5)
a.pack(ipady=3,ipadx=3,pady=25)

window.mainloop()





