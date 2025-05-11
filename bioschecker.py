from customtkinter import *
import wmi
import platform

app = CTk()
app.geometry("800x600")

class NewWindow(CTkToplevel):
    def __init__(self, master, fg_color=None, **kwargs):
        super().__init__(master=master, **kwargs)
        self.geometry("800x600")
        self.master = master
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.destroy()
        self.master.deiconify()

def opennewwindow():
    newwindow = NewWindow(master=app)
    newwindow.focus()
    app.withdraw()
    return newwindow 

def get_full_bios_info():
    c = wmi.WMI()

    new_window = opennewwindow()
    new_window.title("BIOS INFO")

    frame = CTkFrame(new_window)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    text = CTkTextbox(frame, wrap="word", height=500)
    text.pack(fill="both", expand=True)

    def append(info):
        text.insert("end", info + "\n")

    append("=== BIOS Info ===")
    for bios in c.Win32_BIOS():
        append(f"Vendor           : {bios.Manufacturer}")
        append(f"Version          : {bios.SMBIOSBIOSVersion}")
        append(f"Release Date     : {bios.ReleaseDate}")
        append(f"BIOS Caption     : {bios.Caption}")
        append(f"BIOS Description : {bios.Description}")

    append("\n=== Computer System Info ===")
    for cs in c.Win32_ComputerSystem():
        append(f"Manufacturer     : {cs.Manufacturer}")
        append(f"Model            : {cs.Model}")
        append(f"System Type      : {cs.SystemType}")
        append(f"Total Physical RAM: {int(cs.TotalPhysicalMemory) // (1024**3)} GB")

    append("\n=== BaseBoard (Motherboard) ===")
    for board in c.Win32_BaseBoard():
        append(f"Manufacturer     : {board.Manufacturer}")
        append(f"Product          : {board.Product}")
        append(f"Serial Number    : {board.SerialNumber}")

    append("\n=== Processor Info ===")
    for proc in c.Win32_Processor():
        append(f"Name             : {proc.Name}")
        append(f"Architecture     : {proc.Architecture}")
        append(f"Number of Cores  : {proc.NumberOfCores}")
        append(f"Number of Logical Processors : {proc.NumberOfLogicalProcessors}")

    append("\n=== Operating System ===")
    for os in c.Win32_OperatingSystem():
        append(f"OS Name          : {os.Caption}")
        append(f"Version          : {os.Version}")
        append(f"Architecture     : {os.OSArchitecture}")
        append(f"Build Number     : {os.BuildNumber}")
        append(f"Install Date     : {os.InstallDate}")

    append("\n=== Platform Info ===")
    append(f"Python Platform  : {platform.platforsm()}")

    text.configure(state="disabled") 

button = CTkButton(app, text="Get BIOS information", corner_radius=32, command=get_full_bios_info)
button.place(relx=0.5, rely=0.5, anchor="center")

app.mainloop()
