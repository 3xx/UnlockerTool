import psutil
import os

def unlock_file_by_process(process_name):
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if proc.info['name'] == process_name:
            print(f"Found process: {proc.info['name']} (PID: {proc.info['pid']})")
            try:
                for file in proc.open_files():
                    print(f"File in use: {file.path}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                print("Could not access some files.")
            return proc.info['pid']
    print("Process not found.")
    return None

def kill_process(pid):
    try:
        p = psutil.Process(pid)
        p.terminate() 
        print(f"Process with PID {pid} has been terminated.")
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        print("Could not terminate the process.")

if __name__ == "__main__":
    while True:
        process_name = input("Enter the process name (e.g., notepad.exe) or type 'exit' to quit: ")
        if process_name.lower() == 'exit':
            break
        
        pid = unlock_file_by_process(process_name)
        
        if pid is not None:
            confirm = input(f"Do you want to terminate the process {process_name} (PID: {pid})? (yes/no): ")
            if confirm.lower() == 'yes':
                kill_process(pid)
