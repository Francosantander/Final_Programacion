from time import sleep
import datetime
import os


hour = "01:00"
while True:
    now = datetime.datetime.now().strftime("%H:%M")
    if now == hour:
        os.system("python manage.py runscript actualizacion")
        sleep(86400)
    else:
        sleep(30)
