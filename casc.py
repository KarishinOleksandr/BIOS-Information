from customtkinter import *
import platform
import psutil
import subprocess

def get_output(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    except Exception as e:
        return f"Error: {e}"

def get_bios_info():
    return get_output("sudo dmidecode -t bios")

def get_baseboard_info():
    return get_output("sudo dmidecode -t baseboard")

def get_memory_info():
    return get_output("sudo dmidecode -t memory")

def get_cpu_info():
    return get_output("lscpu")

def get_gpu_info():
    return get_output("lspci | grep VGA")

def get_disk_info():
    return get_output("lsblk -o NAME,SIZE,MODEL,SERIAL")

def get_os_info():
    return get_output("cat /etc/os-release")

def get_network_info():
    return get_output("ip -brief addr")

def get_temp_info():
    try:
        temps = psutil.sensors_temperatures()
        output = ""
        for name, entries in temps.items():
            output += f"{name}:\n"
            for entry in entries:
                label = entry.label or "Unnamed"
                output += f"  {label}: {entry.current} °C\n"
        return output if output else "No temperature sensors found."
    except Exception as e:
        return f"Error reading temperatures: {e}"

def opennewwindow():
    global new_window
    if new_window is not None and new_window.winfo_exists():
        new_window.destroy()
    new_window = NewWindow(master=app)
    new_window.focus()
    app.withdraw()
    return new_window

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

def get_full_bios_info():
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
    append(get_bios_info())
    append("===============")

    append("\n=== Motherboard ===")
    append(get_baseboard_info())
    append("===============")

    append("\n=== Memory Info ===")
    append(get_memory_info())
    append("===============")

    append("\n=== CPU Info ===")
    append(get_cpu_info())
    append("===============")

    append("\n=== GPU Info ===")
    append(get_gpu_info())
    append("===============")

    append("\n=== Storage Info ===")
    append(get_disk_info())
    append("===============")

    append("\n=== Network Info ===")
    append(get_network_info())
    append("===============")

    append("\n=== OS Info ===")
    append(get_os_info())
    append("===============")

    append("\n=== Temperature Info ===")
    append(get_temp_info())
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
        label.grid(row=0, column=1, pady=20, padx=20)
        result_box = CTkTextbox(new_window.frame, width=700, height=400)
        result_box.grid(row=1, column=0, columnspan=3, padx=20, pady=10)

        def log(msg, level="info"):
            tags = {"ok": "[OK]", "warn": "[Warning]", "critical": "[CRITICAL]"}
            prefix = tags.get(level, "[INFO]")
            result_box.insert("end", f"{prefix} {msg}\n")

        log(f"CPU: {platform.processor()}")
        cores = psutil.cpu_count(logical=False)
        if cores <= 2:
            log("Processor has 2 or fewer cores — system performance may be low.", level="warn")
        else:
            log(f"Processor has {cores} cores.", level="ok")

        ram = psutil.virtual_memory().total // (1024**3)
        if ram < 4:
            log(f"Only {ram} GB RAM — below minimum required.", level="critical")
        elif ram < 8:
            log(f"{ram} GB RAM — might be insufficient for heavy tasks.", level="warn")
        else:
            log(f"{ram} GB RAM detected.", level="ok")

        gpu = get_gpu_info()
        if "VGA" not in gpu:
            log("No GPU found.", level="critical")
        else:
            log(f"GPU: {gpu}", level="ok")

        net_info = get_network_info()
        if not net_info:
            log("No network adapter found.", level="critical")
        else:
            log("Network interfaces detected.", level="ok")

        temp_info = get_temp_info()
        if "°C" in temp_info:
            log("CPU Temperature Info:\n" + temp_info, level="ok")
        else:
            log("No temperature data available", level="warn")

        result_box.configure(state="disabled")

    elif valuesget == "BIOS information":
        if new_window is not None and new_window.winfo_exists():
            new_window.destroy()
        app.deiconify()

    elif valuesget == "Help":
        new_window = opennewwindow()
        new_window.title("Help")
        help_text = (
            "Welcome to BIOS Checker on Linux...\n\n"
            "1. BIOS Information — Retrieves data using dmidecode, lscpu, lspci, lsblk, and other Linux tools.\n"
            "2. Test — Performs a basic health check on CPU cores, RAM, GPU, temperature, and network.\n\n"
            "NOTE: Some commands (e.g., dmidecode) require sudo/root access.\n"
        )

        label = CTkLabel(new_window.frame, text="User Help", font=("Arial", 18, "bold"))
        label.grid(row=0, column=1, pady=(10, 0), padx=20)

        help_box = CTkTextbox(new_window.frame, wrap="word", width=700, height=500)
        help_box.insert("0.0", help_text)
        help_box.configure(state="disabled")
        help_box.grid(row=1, column=0, columnspan=3, padx=20, pady=10)

# GUI setup
new_window = None
app = CTk()
app.geometry("800x600")
app.resizable(False, False)
app.title("BIOS Checker")

optionmenu = CTkOptionMenu(app, values=["BIOS information", "Test", "Help"], command=menu)
optionmenu.grid(row=0, column=0 ,pady=20, padx=20)

button = CTkButton(app, text="Get BIOS information", corner_radius=32, command=get_full_bios_info)
button.place(relx=0.5, rely=0.5, anchor="center")

app.mainloop()
