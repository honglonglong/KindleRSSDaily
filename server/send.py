from datetime import timedelta
import smtplib
import os
import dailykindle
#import sendgrid
import time
import sendbyaws

dir = os.path.dirname(__file__)

f = open("/opt/kindle/sources.txt", "r")
feeds = f.readlines()
f.close()

p = open("/opt/kindle/kindle-pass.txt", "r")
s = p.readlines()
p.close()


dailykindle.build(feeds, os.path.join(dir, '../temp/'), timedelta(1))
dailykindle.mobi(os.path.join(dir, '../temp/daily.opf'), os.path.join(dir, '../kindlegen/kindlegen'))

date = time.strftime("%m/%d/%Y")

sendbyaws.send(s[0].strip('\n'), s[1].strip('\n'), ('Daily RSS'+ date), 'RSS DAILY ' + date,os.path.join(dir, '../temp/daily.mobi'))
'''
message = sendgrid.Mail()
sg = sendgrid.SendGridClient(s[0].strip('\n'), s[1].strip('\n'))
message = sendgrid.Mail()
message.add_to(s[2].strip('\n'))
message.set_subject('Daily RSS'+ date)
message.add_attachment("DailyRSS"+date+".mobi",os.path.join(dir, '../temp/daily.mobi'))
message.set_from(s[2].strip('\n'))
message.set_text('RSS DAILY ' + date)
status, msg = sg.send(message)
print('[' + str(status) + ']' + msg)
'''




