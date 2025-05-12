from customtkinter import *
import wmi
import platform

new_window = None

app = CTk()
app.geometry("800x600")
app.resizable(False, False)
app.title("BIOS Checker")

class NewWindow(CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)
        self.geometry("800x600")
        self.resizable(False, False)
        self.frame = CTkFrame(self)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        optionmenu1 = CTkOptionMenu(self.frame, values=["BIOS information", "Test", "Help"], command=menu)
        optionmenu1.grid(row=0, column=0 ,pady=20, padx=20)
        self.master = master
        self.protocol("WM_DELETE_WINDOW", self.on_close)


    def on_close(self):
        self.destroy()
        self.master.deiconify()

def opennewwindow():
    global new_window
    if new_window is not None and new_window.winfo_exists():
        new_window.destroy()
    new_window = NewWindow(master=app)
    new_window.focus()
    app.withdraw()
    return new_window
def get_full_bios_info():
    c = wmi.WMI()
    global new_window

    new_window = opennewwindow()
    new_window.title("BIOS INFO")

    frame = CTkFrame(new_window)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    text = CTkTextbox(frame, wrap="word", height=500)
    text.pack(fill="both", expand=True)

    def append(info):
        text.insert("end", info + "\n")

    append("=== BIOS Info ===")
    bios_info_set = set()
    for bios in c.Win32_BIOS():
        bios_info = (
            f"Version:            {bios.SMBIOSBIOSVersion or 'N/A'}\n"
            f"Release Date:       {bios.ReleaseDate or 'N/A'}\n"
            f"BIOS Caption:       {bios.Caption or 'N/A'}\n"
            f"BIOS Description:   {bios.Description or 'N/A'}\n"
            f"Serial Number:      {bios.SerialNumber or 'N/A'}\n"
            f"BIOS Version:       {bios.Version or 'N/A'}\n"
        )
        if bios_info not in bios_info_set:
            bios_info_set.add(bios_info)
            append(bios_info)
    append("===============")

    append("\n=== Ports Info ===")
    ports_info_set = set()
    for ports in c.Win32_SerialPort():
        ports_info = (
            f"Name:               {ports.Name or 'N/A'}\n"
            f"Device ID:          {ports.DeviceID or 'N/A'}\n"
            f"Description:        {ports.Description or 'N/A'}\n"
            f"Caption:            {ports.Caption or 'N/A'}\n"
            f"Max Baud Rate:      {ports.MaxBaudRate or 'N/A'}\n"
        )
        if ports_info not in ports_info_set:
            ports_info_set.add(ports_info)
            append(ports_info)
    append("===============")
    
    append("\n=== Computer System Info ===")
    computer_info_set = set()
    for cs in c.Win32_ComputerSystem():
        computer_info = (
            f"Name:               {cs.Name  or 'N/A'}\n"
            f"Manufacturer:       {cs.Manufacturer  or 'N/A'}\n"
            f"Model:              {cs.Model  or 'N/A'}\n"
            f"System Type:        {cs.SystemType  or 'N/A'}\n"
            f"Total Physical RAM: {int(cs.TotalPhysicalMemory) // (1024**3)  or 'N/A'} GB\n"
            f"Domain:             {cs.Domain  or 'N/A'}"
        )
        if computer_info not in computer_info_set:
            computer_info_set.add(computer_info)
            append(computer_info)
    append("===============")

    append("\n=== Memory Info ===")
    memory_info_set = set()
    for mem in c.Win32_PhysicalMemory():
        memory_info = (
            f"Capacity:           {int(mem.Capacity) // (1024**3) or 'N/A'} GB\n"
            f"Manufacturer:       {mem.Manufacturer  or 'N/A'}\n"
            f"Serial Number:      {mem.SerialNumber  or 'N/A'}\n"
            f"Part Number:        {mem.PartNumber  or 'N/A'}\n"
            f"Speed:              {mem.Speed  or 'N/A'} MHz\n"
            f"Memory Type:        {mem.MemoryType  or 'N/A'}"
        )
        if memory_info not in memory_info_set:
            memory_info_set.add(memory_info)
            append(memory_info)
    append("===============")

    append("\n=== Solit State Drive ===")
    SSD_info_set = set()
    for ssd in c.Win32_DiskDrive():
        SSD_info = (
            f"Name:               {ssd.Caption or 'N/A'}\n"
            f"Size:               {int(ssd.Size) // (1024**3)} GB\n"
            f"Model:              {ssd.Model or 'N/A'}\n"
            f"Serial Number:      {ssd.SerialNumber or 'N/A'}\n"
        )
        if SSD_info not in SSD_info_set:
            SSD_info_set.add(SSD_info)
            append(SSD_info)
    append("===============")

    append("\n=== BaseBoard (Motherboard) ===")
    Baseboard_info_set = set()
    for board in c.Win32_BaseBoard():
        Baseboard_info = (
            f"Name:               {board.Name or 'N/A'}\n"
            f"Manufacturer:       {board.Manufacturer or 'N/A'}\n"
            f"Product:            {board.Product or 'N/A'}\n"
            f"Serial Number:      {board.SerialNumber or 'N/A'}\n"
        )
        if Baseboard_info not in Baseboard_info_set:
            Baseboard_info_set.add(Baseboard_info)
            append(Baseboard_info)
    append("===============")

    append("\n=== Processor Info ===")
    Processor_info_set = set()
    for proc in c.Win32_Processor():
        procesor_info = (
            f"Name:               {proc.Name or 'N/A'}\n"
            f"Architecture:       {proc.Architecture or 'N/A'}\n"
            f"Number of Cores:    {proc.NumberOfCores or 'N/A'}\n"
            f"Number of Logical Processors:  {proc.NumberOfLogicalProcessors or 'N/A'}\n"
        )
        if procesor_info not in Processor_info_set:
            Processor_info_set.add(procesor_info)
            append(procesor_info)
    append("===============")

    append("\n=== Operating System ===")
    Operating_info_set = set()
    for os in c.Win32_OperatingSystem():
        Operating_info = (
            f"OS Name:               {os.Name or 'N/A'}\n"
            f"Version:               {os.Version or 'N/A'}\n"
            f"Architecture:          {os.OSArchitecture or 'N/A'}\n"
            f"Build Number:          {os.BuildNumber or 'N/A'}\n"
            f"Install Date:          {os.InstallDate or 'N/A'}\n"
        )
        if Operating_info not in Operating_info_set:
            Operating_info_set.add(Operating_info)
            append(Operating_info)
    append("===============")
    
    append("\n=== Network Adapter ===")
    network_info_set = set()
    for net in c.Win32_NetworkAdapter():
        network_info = (
            f"Name:               {net.Name or 'N/A'}\n"
            f"MAC Address:        {net.MACAddress or 'N/A'}\n"
            f"Speed:              {net.Speed or 'N/A'} bps\n"
            f"Manufacturer:       {net.Manufacturer or 'N/A'}\n"
            f"Description:        {net.Description or 'N/A'}"
        )
        if network_info not in network_info_set:
            network_info_set.add(network_info)
            append(network_info)
    append("===============")
    
    append("\n=== Graphics Card ===")
    graphics_info_set = set()
    for gpu in c.Win32_VideoController():
        graphics_info = (
            f"Name:               {gpu.Name or 'N/A'}\n"
            f"Adapter RAM:        {int(gpu.AdapterRAM) // (1024**3) or 'N/A'} GB\n"
            f"Driver Version:     {gpu.DriverVersion or 'N/A'}\n"
        )
        if graphics_info not in graphics_info_set:
            graphics_info_set.add(graphics_info)
            append(graphics_info)
    append("===============")

    append("\n=== Platform Info ===")  
    append(f"Python Platform:        {platform.platform()}")
    append(f"Platform Architecture:  {platform.architecture()}")
    append(f"Platform System:        {platform.system()}")
    append(f"Platform Release:       {platform.release()}")
    append(f"Platform Version:       {platform.version()}")
    append(f"Platform Machine:       {platform.machine()}")
    append("===============")

    text.configure(state="disabled")    

def menu(valuesget):
    global new_window
    if valuesget == "Test":
        new_window = opennewwindow()
        new_window.title("Test")
        label = CTkLabel(new_window.frame, text="This is a test window")
        label.grid(row = 0, column = 2, pady=20, padx=200)
    elif valuesget == "BIOS information":
        if new_window is not None and new_window.winfo_exists():
            new_window.destroy()
        app.deiconify()
    elif valuesget == "Help":
        new_window = opennewwindow()
        new_window.title("Help")
        label = CTkLabel(new_window.frame, text="This is a help window")
        label.grid(row = 0, column = 2, pady=20, padx=200)
        label = CTkLabel(new_window.frame, text="WIP")
        label.grid(row = 1, column = 0, pady=20, padx=20)

optionmenu = CTkOptionMenu(app, values=["BIOS information", "Test", "Help"], command=menu)
optionmenu.grid(row=0, column=0 ,pady=20, padx=20)

button = CTkButton(app, text="Get BIOS information", corner_radius=32, command=get_full_bios_info)
button.place(relx=0.5, rely=0.5, anchor="center")

app.mainloop()
