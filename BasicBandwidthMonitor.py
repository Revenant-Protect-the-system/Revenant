# Move Site-Packages for psutil to correct folder to execute
#   only if " No module named 'psutil' " is shown
import time
import psutil

# Import the Database into the main file
import Database.DatabaseManager
the_database = Database.DatabaseManager.Database()

# Run the main file
last_received = psutil.net_io_counters().bytes_recv
last_sent = psutil.net_io_counters().bytes_sent
last_total = last_received + last_sent

while True:
    bytes_received = psutil.net_io_counters().bytes_recv
    bytes_sent = psutil.net_io_counters().bytes_sent
    bytes_total = bytes_received + bytes_sent

    new_received = bytes_received - last_received
    new_sent = bytes_sent - last_sent
    new_total = bytes_total - last_total

    mb_new_received = new_received / 1024 / 1024
    mb_new_sent = new_sent / 1024 / 1024
    mb_new_total = new_total / 1024 / 1024

    print(f"{mb_new_received:.2f} MB Recieved, {mb_new_sent:.2f} MB Sent, {mb_new_total:.2f} MB Total")

    last_received = bytes_received
    last_sent = bytes_sent
    last_total = bytes_total

    time.sleep(1)