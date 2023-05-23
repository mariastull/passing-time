import os

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

Weekend_class_times = []

# convert datetime day to string
def get_day_string(dt):
    day = dt.weekday()
    num_to_day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return num_to_day[day]

# make a string of the current day and time
def get_datetime_description(dt):
    day = get_day_string(dt)
    return f'\nIt is {day} at {dt.hour:d}:{dt.minute:02d}\n'

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
        
# Formats classtime schedule string
def get_daily_schedule(schedule):
    schedule_string = ""
    schedule_string = schedule_string + "Today's common class schedule is:\n\n"
    if len(schedule) == 0:
        schedule_string = schedule_string + "No classes today\n"
    else:
        for classtime in schedule:
            schedule_string = schedule_string + "{:d}:{:02d} - {:d}:{:02d}\n\n".format(classtime[0], classtime[1], classtime[2], classtime[3])
    return schedule_string

# get daily schedule
def get_class_schedule(dt):
    if dt.weekday() in [0,2,4]:
        class_schedule = MWF_class_times
    if dt.weekday() in [1,3]:
        class_schedule = TR_class_times
    if dt.weekday() in [5,6]:
        class_schedule = Weekend_class_times
    return class_schedule

def check_for_classtime(dt):
    for classtime in get_class_schedule(dt):
            if during_class_now(dt, classtime):
                return True
    return False

# check if it's currently during class
def during_class(dt):
    during_class = False
    if dt.day in [5, 6]:
        print("It's a weekend.")
        during_class = True
    elif dt.hour < 8:  #or dt.hour==8 and dt.minute < 40:
        print("Classes haven't started yet.")
        during_class = True
    elif dt.hour > 18 or dt.hour==18 and dt.minute > 35:
        print("Classes are over for the day.")
        during_class = True
    else: # It's a weekday during class hours
        for classtime in get_class_schedule(dt):
            if during_class_now(dt, classtime):
                during_class = True
                if os.name == 'nt': # We're running on a windows machine
                    print("It's currently classtime from {:d}:{:02d} - {:d}:{:02d}\n".format(classtime[0], classtime[1], classtime[2], classtime[3]))
                else:
                    #This weird escape sequence is to change the color of the terminal output text on linux
                    print("\033[1;32mIt's classtime now\033[0m {:d}:{:02d} - {:d}:{:02d} ".format(classtime[0], classtime[1], classtime[2], classtime[3]))
                break
    return during_class

# notify that it is passing period
def passing_period_message(dt):
    if os.name == 'nt':
        print("It's a passing period")
    else:
        print("\033[1;31mIt's a passing period.\033[0m") 
    next_class = find_next_class_start(dt, get_class_schedule(dt))
    print("The next class period is {:d}:{:02d} - {:d}:{:02d} ".format(next_class[0], next_class[1], next_class[2], next_class[3]))
