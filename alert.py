import datetime
import requests
import time
import smtplib, ssl

print('#'*25)
print("Mailer alert initialized.")
print('#'*25)

def send_mail():
    print("Attempting to send email...")
    currDate = datetime.datetime.now()
    currDate = str(currDate.strftime("%d-%m-%Y %H:%M:%S"))
    gmail_user = 'mail@gmail.com'
    gmail_password = 'password'

    sent_from = gmail_user
    to = ['email@email.com']
    subject = 'Website running slow!'
    body = "Website slow. %s First Website Name: %s Second Website Name: %s" % (currDate, respTime, respTime2)

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()    

        print('Email sent!')
    except:
        print('Something went wrong...')

url = 'First Website'
url2 = 'Second Website'

web = True

while web:
    try:
        r = requests.get(url, timeout=6)
        r2 = requests.get(url2, timeout=6)
        r.raise_for_status()
        r2.raise_for_status()
        respTime = str(round(r.elapsed.total_seconds(), 2))
        respTime2 = str(round(r2.elapsed.total_seconds(), 2))
        currDate = datetime.datetime.now()
        currDate = str(currDate.strftime("%d-%m-%Y %H:%M:%S"))
        if float(respTime) > 0.8: #First Website response
            send_mail()
            print('Response time too high.')
            print(currDate + " " + respTime)
        if float(respTime2) > 0.8: #Second Website response
            send_mail()
            print('Response time too high.')
            print(currDate + " " + respTime2)
        time.sleep(5)
    except requests.exceptions.HTTPError as err01:
        print("HTTP error: ", err01)
    except requests.exceptions.ConnectionError as err02:
        print("Error connecting: ", err02)
    except requests.exceptions.Timeout as err03:
        print("Timeout error:", err03)
    except requests.exceptions.RequestException as err04:
        print("Error: ", err04)

 
