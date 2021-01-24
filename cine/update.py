import os
from time import sleep
import datetime


hour = "01:00"
while True:
    now = datetime.datetime.now().strftime("%H:%M")
    if now == hour:
        os.system("python3 manage.py runscript actualizacion")
        sleep(3600)
    else:
        sleep(30)
