import subprocess
import os
import signal
import sys
import time

PID_FILE = ".django_server.pid"

def get_pid():
    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r") as f:
            return int(f.read().strip())
    return None

def save_pid(pid):
    with open(PID_FILE, "w") as f:
        f.write(str(pid))

def start_server():
    if get_pid():
        print("Server is already running.")
        return

    print("Starting Django server...")
    process = subprocess.Popen(
        ['start', 'cmd', '/k', 'python manage.py runserver'],
        shell=True
    )
    # simulate delay for startup
    time.sleep(2)
    print("Server started in new terminal.")
    save_pid(process.pid)

def stop_server():
    pid = get_pid()
    if not pid:
        print("No server is running.")
        return
    try:
        print(f"Stopping server with PID {pid}...")
        os.kill(pid, signal.SIGTERM)
        os.remove(PID_FILE)
        print("Server stopped.")
    except Exception as e:
        print(f"Failed to stop server: {e}")

def status():
    pid = get_pid()
    if pid is None:
        print("Server is not running.")
        return
    try:
        os.kill(pid, 0)
        print(f"Server is running with PID {pid}.")
    except OSError:
        print("Stale PID file. Server not running.")
        os.remove(PID_FILE)

def main():
    if len(sys.argv) != 2:
        print("Usage: python manage_server.py [start|stop|status|restart]")
        return

    command = sys.argv[1].lower()
    if command == "start":
        start_server()
    elif command == "stop":
        stop_server()
    elif command == "status":
        status()
    elif command == "restart":
        stop_server()
        time.sleep(1)
        start_server()
    else:
        print("Unknown command:", command)

if __name__ == "__main__":
    main()
