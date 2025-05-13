from customtkinter import *
import wmi
import platform

new_window = None
hwtypes = ['Mainboard','SuperIO','CPU','RAM','GpuNvidia','GpuAti','TBalancer','Heatmaster','HDD']

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
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
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

    new_window.frame.grid_rowconfigure(1, weight=1)
    new_window.frame.grid_columnconfigure((0, 1, 2), weight=1)

    label = CTkLabel(new_window.frame, text="Your BIOS information", font=("Arial", 20))
    label.grid(row=0, column=1, pady=20, padx=20)

    text = CTkTextbox(new_window.frame, wrap="word", height=500)
    text.grid(row=1, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")

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
        label = CTkLabel(new_window.frame, text="This is a test window", font=("Arial", 20))
        label.grid(row = 0, column = 1, pady=20, padx=20)
        label = CTkLabel(new_window.frame, text="")
        label.grid(row = 0, column = 2, pady=20, padx=20)
        result_box = CTkTextbox(new_window.frame, width=700, height=400)
        result_box.grid(row=1, column=0, columnspan=3, padx=20, pady=10)

        def log(msg, level="info"):
            if level == "ok":
                result_box.insert("end", f"[OK] {msg}\n")
            elif level == "warn":
                result_box.insert("end", f"[Warning] {msg}\n")
            elif level == "critical":
                result_box.insert("end", f"[CRITICAL] {msg}\n")
            else:
                result_box.insert("end", f"{msg}\n")

        c = wmi.WMI()
        for proc in c.Win32_Processor():
            log(f"Processor: {proc.Name}")
            if proc.NumberOfCores <= 2:
                log("Processor has less or 2 cores — system performance may be low.", level="warn")
            else:
                log(f"Processor has {proc.NumberOfCores} cores.", level="ok")
            total_ram = 0
            for mem in c.Win32_PhysicalMemory():
                total_ram += int(mem.Capacity)
            ram_gb = total_ram // (1024**3)
            if ram_gb < 4:
                log(f"Only {ram_gb} GB RAM detected — this is below minimum required.", level="critical")
            elif ram_gb < 8:
                log(f"{ram_gb} GB RAM detected — might be insufficient for heavy tasks.", level="warn")
            else:
                log(f"{ram_gb} GB RAM detected.", level="ok")
        gpus = c.Win32_VideoController()
        if not gpus:
            log("No graphics card detected.", level="critical")
        else:
            for gpu in gpus:
                log(f"GPU: {gpu.Name}", level="ok")
        net_adapters = [n for n in c.Win32_NetworkAdapter() if n.MACAddress]
        if not net_adapters:
            log("No active network adapter found.", level="critical")
        else:
            log(f"{len(net_adapters)} network adapter(s) detected.", level="ok")
        
        result_box.configure(state="disabled")    
    elif valuesget == "BIOS information":
        if new_window is not None and new_window.winfo_exists():
            new_window.destroy()
        app.deiconify()
    elif valuesget == "Help":
        new_window = opennewwindow()
        new_window.title("Help")

        help_text = (
            "Welcome to BIOS Checker, a tool designed to help you retrieve and review detailed information "
            "about your system hardware, BIOS, and performance status. The application provides two main "
            "features accessible from the dropdown menu.\n\n"
            "1. BIOS Information: By clicking the \"Get BIOS information\" button, a new window will open displaying "
            "detailed system data, including BIOS version, release date, serial number, port information, system model and RAM, "
            "memory module specifications, storage devices, motherboard details, processor specs, operating system version, "
            "network adapter data, and graphics card info. Additionally, general platform details such as OS architecture and machine type are included.\n\n"
            "2. Test: Selecting \"Test\" from the dropdown menu opens a window that performs a basic system health analysis. "
            "The tool checks the number of CPU cores and flags low-performance setups. It calculates total installed RAM and notifies you "
            "if the memory is below recommended levels. It also detects graphics cards and network adapters, providing status messages labeled "
            "as [OK], [Warning], or [CRITICAL] to highlight the severity of any findings.\n\n"
            "Tips: If any section shows \"N/A\", it means the data could not be retrieved—either because the component is not present or not accessible. "
            "This tool is designed for Windows systems only and should be run with appropriate permissions to access all system data. It is ideal for quick diagnostics, "
            "IT support checks, or verifying system specs.\n\n"
        )

        label = CTkLabel(new_window.frame, text="User Help", font=("Arial", 18, "bold"))
        label.grid(row=0, column=1, pady=(10, 0), padx=20)

        help_box = CTkTextbox(new_window.frame, wrap="word", width=700, height=500)
        help_box.insert("0.0", help_text)
        help_box.configure(state="disabled")
        help_box.grid(row=1, column=0, columnspan=3, padx=20, pady=10)


optionmenu = CTkOptionMenu(app, values=["BIOS information", "Test", "Help"], command=menu)
optionmenu.grid(row=0, column=0 ,pady=20, padx=20)

button = CTkButton(app, text="Get BIOS information", corner_radius=32, command=get_full_bios_info)
button.place(relx=0.5, rely=0.5, anchor="center")

app.mainloop()
