# Script to tell whether it's a passing period or not (accurate as of February 2023)
# Common meeting times last found at the link below: 
# https://www.colorado.edu/registrar/faculty-staff/scheduling/classes/meeting-patterns
#
# To use: python3 passing_time.py

from datetime import datetime
import os

# get current datetime
dt = datetime.now()

# get day of week
day = dt.weekday()
num_to_day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
print('Today is', num_to_day[day], "at {:d}:{:02d}".format(dt.hour, dt.minute))


# class meeting times
# list of lists, each class is in format [start_hour, start_minute, end_hour, end_minute]
MWF_class_times = [[8,00,8,50],
[9,5,9,55],
[10,10,11,00],
[11,15,12,5],
[12,20,13,10],
[13,25,14,15],
[14,30,15,20],
[15,35,16,25],
[16,40,17,30],
[17,45,18,35]]

TR_class_times = [[8,00,9,15],
[9,30,10,45],
[11,00,12,15],
[12,30,13,45],
[14,00,15,15],
[15,30,16,45],
[17,00,18,15]]

during_class = False

# Check if the given time is within the given classtime window
def during_class_now(curr_time, classtime):
    curr_mins = curr_time.hour*60 + curr_time.minute
    classstart_mins = classtime[0]*60 + classtime[1]
    classend_mins = classtime[2]*60 + classtime[3]

    if curr_mins >= classstart_mins and curr_mins < classend_mins:
        return True
    else:
        return False

# Find the next class that begins after the current time
# Assumes the class schedule is in sorted order
def find_next_class_start(curr_time, schedule):
    for classtime in schedule:
        curr_mins = curr_time.hour*60 + curr_time.minute
        classstart_mins = classtime[0]*60 + classtime[1]
        classend_mins = classtime[2]*60 + classtime[3]
    
        if curr_mins < classstart_mins:
            return classtime

# Prints formatted classtime schedule
def print_daily_schedule(schedule):
    print("\n\nToday's common class schedule is: ")
    for classtime in schedule:
        print("{:d}:{:02d} - {:d}:{:02d} ".format(classtime[0], classtime[1], classtime[2], classtime[3]))

class_schedule = ""
if day in [0,2,4]:
    class_schedule = MWF_class_times
if day in [1,3]:
    class_schedule = TR_class_times

if day in [5, 6]:
    print("It's a weekend.")
    during_class = True
elif dt.hour < 8:  #or dt.hour==8 and dt.minute < 40:
    during_class = True
    print("Classes haven't started yet.")
elif dt.hour > 18 or dt.hour==18 and dt.minute > 35:
    print("Classes are over for the day")
    during_class = True
else: # It's a weekday during class hours
    next_class = find_next_class_start(dt, class_schedule)
    for classtime in class_schedule:
        if during_class_now(dt, classtime):
            during_class = True
            if os.name == 'nt': # We're running on a windows machine
                print("It's classtime now {:d}:{:02d} - {:d}:{:02d} ".format(classtime[0], classtime[1], classtime[2], classtime[3]))
            else:
                #This weird escape sequence is to change the color of the terminal output text on linux
                print("\033[1;32mIt's classtime now\033[0m {:d}:{:02d} - {:d}:{:02d} ".format(classtime[0], classtime[1], classtime[2], classtime[3]))
            break
if not during_class:
    if os.name == 'nt':
        print("It's a passing period")
    else:
        print("\033[1;31mIt's a passing period.\033[0m") 
    print("The next class period is {:d}:{:02d} - {:d}:{:02d} ".format(next_class[0], next_class[1], next_class[2], next_class[3]))


if day<5:
    print_daily_schedule(class_schedule)
