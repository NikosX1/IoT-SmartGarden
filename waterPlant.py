#!/usr/bin/env python3

from smtplib import SMTP_SSL, SMTP_SSL_PORT
from email.message import EmailMessage
import sys
import Adafruit_DHT
import time
import RPi.GPIO as GPIO
from GmailWrapper import GmailWrapper
from Distance import Distance

# ---- USER EMAIL CREDENTIALS -- #
HOSTNAME = 'imap.gmail.com'      #
USERNAME = ''   #
PASSWORD = ''    #
# ------------------------------ #

GPIO.setmode(GPIO.BCM)
#GPIO.setup(21, GPIO.IN)

def checkGmail():
    gmailWrapper = GmailWrapper(HOSTNAME, USERNAME, PASSWORD)
    ids = gmailWrapper.getIdsBySubject('water plant')
    ids1 = gmailWrapper.getIdsBySubject('get info')
    if(len(ids) > 0):
        try:
            water()
            gmailWrapper.markAsRead(ids)
        except:
            print("Failed to water the plant")

    if(len(ids1) > 0):
        try:
            sendInfo(checkSoil(),checkWater(),checkTemperature(),checkHumidity())
            gmailWrapper.markAsRead(ids1)
        except:
            print("Failed to send Info")
def water():
    # Setting GPIO pins

    GPIO.setup(8, GPIO.OUT)
    try:
        # Opening pump
        print('Watering Plant')
        GPIO.output(8, GPIO.LOW)

        # Leave relay open for 40 seconds
        time.sleep(40)

         # Close pump
        GPIO.output(8, GPIO.HIGH)
        print('Watering Finished')
    except:
        print('Failed to open pump')

def checkSoil():
    GPIO.setup(21, GPIO.IN)

    try:
        soil = GPIO.input(21)
        if soil == 1:
            return "No Water"
        elif soil == 0:
            return "Enough Water"
    except:
        print('Soil exception')

def checkWater():
    dist = 0
    min = 10
    x = 0
    try:
        # Measure five times and take the average price
        for i in range(5):
            dist = dist + Distance()
            time.sleep(1)
        avg_dist = dist/5

        x = min - round(avg_dist,2)
        x_perc = (100 * x)/7.2
        if x_perc < 0:
            x_perc = 0
        elif x_perc > 100:
            x_perc = 100

        return round(x_perc,2)

    except KeyboardInterrupt:
        ("Keyboard interruption")

def checkTemperature():
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    return temperature

def checkHumidity():
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    return humidity

def sendInfo(soil,w_level,temp,humid):
    # Craft the email using email.message.EmailMessage
    from_email = USERNAME  # or simply the email address
    to_emails = [USERNAME]
    email_message = EmailMessage()
    email_message.add_header('To', ', '.join(to_emails))
    email_message.add_header('From', from_email)
    email_message.add_header('Subject', 'IoT Smart Garden Info')
    email_message.add_header('X-Priority', '1')  # Urgency, 1 highest, 5 lowest
    email_message.set_content("Soil: "+str(soil)+"\nTank Water Level: "+str(w_level)+"%\nTemperature: "+str(temp)+"\nHumidity: "+str(humid))

    # Connect, authenticate, and send mail
    smtp_server = SMTP_SSL('smtp.gmail.com', port=SMTP_SSL_PORT)
    smtp_server.set_debuglevel(1)  # Show SMTP server interactions
    smtp_server.login(USERNAME, PASSWORD)
    smtp_server.sendmail(from_email, to_emails, email_message.as_bytes())

    # Disconnect
    smtp_server.quit()


def checkPlant():
    if (checkSoil() == "No Water"):
        if (checkWater() != 0):
            water()
        else:
            sendInfo(checkSoil(),checkWater(),checkTemperature(),checkHumidity())

if __name__ == '__main__':
    try:
        checkGmail()
        checkPlant()
    finally:
        GPIO.cleanup()



