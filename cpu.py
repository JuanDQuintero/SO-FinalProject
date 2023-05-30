from tkinter import *
from tkinter import font
import psutil
from psutil import disk_partitions, disk_usage, virtual_memory, cpu_percent 
from tabulate import tabulate

window = Tk()
window.geometry("1024x768")
window.title("CPU - RAM - DISK USAGE")

# Función para mostrar información de la CPU
def show_cpu_info():
    cpu_use = cpu_percent(interval=1, percpu=True)  # Obtiene el porcentaje de uso de cada núcleo
    cpu_label.config(text='{}%'.format(cpu_use[0]))

    # Obtener las frecuencias de cada núcleo
    cpu_freqs = psutil.cpu_freq(percpu=True)
    
    # Actualizar la frecuencia de la CPU en cada iteración
    avg_freq = sum(cpu_freq.current for cpu_freq in cpu_freqs) / len(cpu_freqs)
    cpu_freq_label.config(text='CPU Frequency: {} MHz'.format(int(avg_freq)))
    
    
    # Crear etiquetas para mostrar el porcentaje de uso de cada núcleo
    cpu_cores_labels = []
    for i, core_usage in enumerate(cpu_use):
        core_label = Label(window, bg='#071C1E', fg='#FA5125', font="Arial 20 bold", width=12)
        core_label.place(x=610 + (i % 2) * 200, y=130 + (i // 2) * 50)
        core_label.config(text='Core {}: {}%'.format(i + 1, core_usage))
        cpu_cores_labels.append(core_label)

    cpu_freq_label.after(500, show_cpu_info)
    

# Function converter Bytes to Gigabytes
def conversor_bytes_to_gb(bytes_value):
    one_gigabyte = 1073741824  # Bytes
    giga = bytes_value / one_gigabyte
    giga = '{0:.1f}'.format(giga)
    return giga

# Function to display RAM information
def show_ram_info():
    ram_usage = virtual_memory()
    used = conversor_bytes_to_gb(ram_usage.used)
    total = conversor_bytes_to_gb(ram_usage.total)
    percent = ram_usage.percent
    ram_label.config(text='{} GB / {} GB ({} %)'.format(used, total, percent))
    ram_label.after(200, show_ram_info)  # Agregar llamada recursiva para actualizar la frecuencia de la CPU

data = disk_partitions(all=False)

def details(device_name):
    for i in data:
        if i.device == device_name:
            return i
        
# Function to display disk information
def disk_info(device_name):
    disk_info = {}
    try:
        usage = disk_usage(device_name)
        disk_info['Device'] = device_name
        disk_info['Total'] = f"{conversor_bytes_to_gb(usage.used + usage.free)} GB" 
        disk_info['Used'] = f"{conversor_bytes_to_gb(usage.used)} GB"
        disk_info['Free'] = f"{conversor_bytes_to_gb(usage.free)} GB"
        disk_info['Percent'] = f"{usage.percent} GB"
        
        info = details(device_name)
        if info is not None:
            disk_info.update({"Device": info.device})
            disk_info["Mount Point"] = info.mountpoint
            disk_info["FS-Type"] = info.fstype
            disk_info["Opts"] = info.opts
    except PermissionError:
        pass
    except FileNotFoundError:
        pass
    
    return disk_info

# Function that returns the disk partitions
def get_device_names():
    return [i.device for i in data]

def all_disk_info():
    return_all=[]
    for i in get_device_names():
        return_all.append(disk_info(i))
    return return_all

# Title program
title_program = Label(window, text='PC Performance Manager', font="arial 40 bold", fg='#14747F')
title_program.place(x=110, y=20)               

# CPU title
cpu_title_label = Label(window, text='CPU Usage: ', font="arial 24 bold", fg='#FA5125')
cpu_title_label.place(x=20, y=155)

# Label to show percent of CPU
cpu_label = Label(window, bg='#071C1E', fg='#FA5125', font="Arial 30 bold", width=15)
cpu_label.place(x=230, y=150)

# Label para mostrar la frecuencia de la CPU
cpu_freq_label = Label(window, bg='#071C1E', fg='#FA5125', font="Arial 20 bold", width=28)

# Label para mostrar la temperatura de la CPU
cpu_temp_label = Label(window, font=("Arial", 18))
cpu_temp_label.pack(pady=10)

# RAM title
ram_title_label = Label(window, text='RAM Usage: ', font="arial 24 bold", fg='#34A96C')
ram_title_label.place(x=20, y=270)

# Label to show percent of RAM
ram_label = Label(window, bg='#071C1E', fg='#FA5125', font="Arial 30 bold", width=20)
ram_label.place(x=230, y=260)

# Disk title
disk_title_label = Label(window, text='Disk Usage: ', font="arial 24 bold", fg='#797E1E')
disk_title_label.place(x=20,y=350)

#text area disk information
textArea=Text(window,bg="#071C1E", fg="yellow", width=85,height=6,padx=10, font=("consolas", 14))
textArea.place(x=15,y=410)

if __name__ == '__main__':
    show_cpu_info()
    show_ram_info()
    info = all_disk_info()
    _list = [i.values() for i in info]
    info_tabulated = tabulate(_list, headers=info[0].keys(), tablefmt="simple", missingval=("-"))
    textArea.insert(END, info_tabulated)
    cpu_freq_label.place(x=180, y=210)  # Colocar después del bucle de creación de etiquetas
    cpu_temp_label.place(x=180, y=250)  # Colocar después del bucle de creación de etiquetas
    window.mainloop()
