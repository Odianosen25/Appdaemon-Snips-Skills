import appdaemon.plugins.hass.hassapi as hass
import os, sys
dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
import json
from datetime import timezone, timedelta, datetime, time, date
import time
from num2words import num2words
    
class ProcessDateTime(hass.Hass):

  def initialize(self):
#    self.logger = logging.getLogger('datetime_intent')
    self.allowed_users = self.app_config["snips_core"]["users"]  #self.args["users"] self.global_vars['users'] 
    
  def start_datetime(self, data):
    
    if type(data.get("Target")) == list:
        msg = self.tell_datetime(data)
        
    elif data.get("Target") == "Time":
        msg = self.tell_time(data)
        
    elif data.get("Target") == "Date":
        msg = self.tell_date(data)
        
    else:
        msg = ""
  
    return msg

  def tell_date(self, data):
    msg = ""
    check = data.get("DateTime", None)
    if check == None: #check if it is the present date that is requested and load it
        d = datetime.now().date()
    else: #convert the date to datetime objects
        d = datetime.strptime(check.split(" ")[0], "%Y-%m-%d").date()
    
    day = num2words(int((d.strftime("%d")).lstrip("0")), to='ordinal')
    day_text = d.strftime("%A")
    month = d.strftime("%B")
    year = num2words(int(d.strftime("%Y")))
    text = ""
    
    if d == datetime.now().date(): #check if its for today
        text = "is"
    elif (d - datetime.now().date()).days > 1: #check if its for some time ahead
        text = "will be"
    elif (d - datetime.now().date()).days < 0: #check if its for some time past
        text = "was"
    else: 
        pass
        
        
    msg = "The date {0} {1} the {2} of {3}, {4}".format(text, day_text, day, month, year)
        
    return msg
    
  def tell_time(self, data):
    msg = ""
    check = data.get("DateTime", None)
    if check == None: #check if it is the present time that is requested and load date
        td = datetime.now(timezone.utc)
    else: #convert the time and date to datetime objects
        pos = check.find('.')
        if pos != -1:
            pos2 = check.find(' ', pos)
            check = check[:pos] + check[pos2:]
        
        pos = check.find(':', 20)
        check = check[:pos] + check[pos+1:]
        td = datetime.strptime(check, "%Y-%m-%d %H:%M:%S %z")

    direction = ""
    mins = ""
    hour = num2words(int((td.strftime("%I")).lstrip("0")))
    section = td.strftime("%p")
    text = "is"

    if (td - datetime.now(timezone.utc)).total_seconds() > 30: #check if its for some time ahead
        text = "will be"
    elif (td - datetime.now(timezone.utc)).total_seconds() < -30: #check if its for some time past
        text = "was"
    else: 
        pass
        
    if td.minute in range(1, 30):
        direction =  "past"
        
    elif td.minute in range(31, 59):
        direction =  "to"
        if int((td.strftime("%I")).lstrip("0")) == 12:
            hour = num2words(1)
        else:
            hour = num2words(int((td.strftime("%I")).lstrip("0")) + 1)
        
    else:
        direction = "o'clock"
    
    if td.minute in range(1, 14) or td.minute in range(16, 29):
        mins =  num2words(td.minute)
        
    elif td.minute in range(31, 44) or td.minute in range(46, 59):
        mins =  num2words(60 - td.minute)
        
    elif td.minute == 15 or td.minute == 45:
        mins = "quarter"
        
    elif td.minute == 30:
        mins = "half"
        
    else:
        mins = td.minute
    
    if direction != "o'clock":
        if mins == "quarter" or mins == "half":
            msg = "The time {0} {1} {2} {3} {4}".format(text, mins, direction, hour, section)
        else:
            msg = "The time {0} {1} minutes {2} {3} {4}".format(text, mins, direction, hour, section)

    else:
        msg = "The time {0} {1} o'clock {2}".format(text, hour, section)
        
    return msg
    
    
  def tell_datetime(self, data):
    
    time_msg = self.tell_time(data)
    date_msg = self.tell_date(data)
    
    if time_msg == "" or date_msg == "":
        msg = ""
    else:
        msg = "{} and {}".format(time_msg, date_msg)
  
    return msg