# Script to tell whether it's a passing period or not (accurate as of February 2023)
# Common meeting times last found at the link below: 
# https://www.colorado.edu/registrar/faculty-staff/scheduling/classes/meeting-patterns
#
# To use: python3 passing_time.py

from datetime import datetime

from utils import *

# get current datetime
dt = datetime.now()

# print current datetime
print(get_datetime_description(dt))

# check if it's currently during class
if not during_class(dt):
    passing_period_message(dt)

# print today's schedule
print(get_daily_schedule(get_class_schedule(dt)))
