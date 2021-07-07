import docx
import random 
from dateutil import tz

def weekday_today(timezone = tz.gettz("Asia/Shanghai")):
    from datetime import datetime
    from datetime import date
    year = int(datetime.now(timezone).year)
    month = int(datetime.now(timezone).month)
    day = int(datetime.now(timezone).day)
    return(date(year, month, day).isocalendar()[2])

def getText(filename):
    "This function reads all plain text within a docx document"
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def box_print(text,thickness=1,syms_h ="~",syms_v ="|",to_print = True,n_unicode = 0):
    def place_holder(n):
        return("{:"+str(n)+"}")

    def sandwhich(n,text,thickness,syms = "*"):
        return("{}".format(syms*thickness)+place_holder(n).format(text)+"{}".format(syms*thickness))
    "Print Text surronded by boxes"
    max_len = 0
    for i in text.split("\n"):
        if len(i) > max_len:
            max_len = len(i)
    box_length = round(max_len + 2*thickness + n_unicode*1.5)
    string = syms_h*box_length
    for line in text.split("\n"):
        string += "\n"+sandwhich(max_len,line,thickness,syms_v)
    string += "\n"+syms_h*box_length
    if to_print:
        print(string)
        return
    return string


# In[4]:


class Load:
    "This class is dedicated to load information of OKR weekly logs"
    def __init__(self,file_path):
        global Authorized 
        text = getText(file_path)
        self.log_list = []
        self.week_log = []
        for i in text.split("\n"):
            self.log_list.append(i.strip())  
    
    def add_okr(self,text_in_format):
        try:
            self.WeekObjective.set_Special_Task(text_in_format)
        except:
            print("WeekObjective not loaded")
        
    def get_week_objective(self):
        global Authorized 
        "Load WeekObjectives into self.WeekObjective"
        self.WeekObjective = Day()
        try:
            self.WeekObjective.set_Priority_Task(self.log_list[self.log_list.index("Priority Task of the Week:"):self.log_list.index("Daily Objective:")])
        except :
            print("For WeekObjective, Priority_Task is not logged")
            Authorized = False
        try:
            self.WeekObjective.set_Recursive_Task(self.log_list[self.log_list.index("Daily Objective:"):self.log_list.index("Special Objective: (Dead_Line Required)")])
        except :
            print("For WeekObjective, Recursive_Task is not logged")
            Authorized = False
        try:
            self.WeekObjective.set_Special_Task(self.log_list[self.log_list.index("Special Objective: (Dead_Line Required)"):self.log_list.index("OKR_Logs")])
        except :
            print("For WeekObjective, Special_Task is not logged")
            Authorized = False

    def week_okr_show(self):
        self.WeekObjective.show()

    def log_day(self,n):
        global Authorized 
        "Get the data for specific day of log; n = number of day in the week"
        idx_head = self.log_list.index("Day " + str(n))
        if n < 7:
            idx_tail = self.log_list.index("Day " + str(n+1))
        else: 
            idx_tail = self.log_list.index(str("Week_Summary"))
        self.log_of_day = self.log_list[idx_head:idx_tail]
        n_day = self.log_of_day[0]
        date = self.log_of_day[1]
        new_day_log = Day()
        try:
            new_day_log.set_Priority_Task(self.log_of_day[self.log_of_day.index("Priority Task:"):self.log_of_day.index("Special OKR:")])
        except ValueError:
            print("For day {}, Priority_Task is not logged".format(n))
            Authorized = False
        try:
            new_day_log.set_Special_Task(self.log_of_day[self.log_of_day.index("Special OKR:"):self.log_of_day.index("Recursive OKR:")])
        except ValueError:
            print("For day {}, Special_Task is not logged".format(n))
            Authorized = False
        try:
            new_day_log.set_Recursive_Task(self.log_of_day[self.log_of_day.index("Recursive OKR:"):self.log_of_day.index("Daily Summary:")])
        except ValueError:
            print("For day {}, Recursive_Task is not logged".format(n))
            Authorized = False
        return new_day_log

    def log_all(self):
        "Get the data for all 7 days in a week"
        for i in range(7):
            i = i + 1
            self.week_log.append(self.log_day(i))


    def logs_show(self,day = "all"):
        "Input: show weekday's tasks, show all tasks by default"
        if self.week_log == []:
            print("Load the weekly logs first!")
        else:
            if day == "all":
                for days in range(len(self.week_log)):
                    print("Day:",days+1)
                    self.week_log[days].show(progress = False)
                    print("\n")
            else:
                self.week_log[day-1].show(progress = False)


    def task_progress(self,Task_ID):
        task_type = Task_ID.split("_")[0]
        Objective_ID = Task_ID.split("_")[1]
        KR_ID = Task_ID.split("_")[2]
        if task_type == "R":
            for i in range(len(self.WeekObjective.Recursive_Task)):
                if self.WeekObjective.Recursive_Task[i].Objective.split(":")[0] == Objective_ID:
                    self.WeekObjective.Recursive_Task[i].progress_show()
        if task_type == "S":
            for i in range(len(self.WeekObjective.Special_Task)):
                if self.WeekObjective.Special_Task[i].Objective.split(":")[0] == Objective_ID:
                    self.WeekObjective.Special_Task[i].progress_show()
            for i in range(len(self.week_log[weekday_today()-1].Priority_Task)):
                if self.WeekObjective.Priority_Task[i].Objective.split(":")[0] == Objective_ID:
                    self.WeekObjective.Priority_Task[i].progress_show()
    
    def complete(self,Task_ID,tk_pop = False):
        task_type = Task_ID.split("_")[0]
        Objective_ID = Task_ID.split("_")[1]
        KR_ID = Task_ID.split("_")[2]
        if task_type == "R":
            for i in range(len(self.WeekObjective.Recursive_Task)):
                if self.WeekObjective.Recursive_Task[i].Objective.split(":")[0] == Objective_ID:
                    self.WeekObjective.Recursive_Task[i].complete(KR_ID,False,tk_pop = tk_pop)

        elif task_type == "S":
            for i in range(len(self.WeekObjective.Special_Task)):
                if self.WeekObjective.Special_Task[i].Objective.split(":")[0] == Objective_ID:
                    self.WeekObjective.Special_Task[i].complete(KR_ID,tk_pop = tk_pop)

        elif task_type == "P":
            for i in range(len(self.WeekObjective.Priority_Task)):
                if self.WeekObjective.Priority_Task[i].Objective.split(":")[0] == Objective_ID:
                    self.WeekObjective.Priority_Task[i].complete(KR_ID, tk_pop = tk_pop)
                    
                    
#@title Day Class {display-mode: "form"}
class Day:
    def __init__(self):
        self.Priority_Task = []
        self.Special_Task = []
        self.Recursive_Task = []
        global Authorized

    def set_Priority_Task(self,list_of_tasks):
        global Authorized 
        for string in list_of_tasks:
            if len(string) > 0:
                try:
                    if string[0] == "G":
                        a_task = okr_task()
                        self.Priority_Task.append(a_task)
                        a_task.set_Objective(string)
                    elif string[0].upper() == "K":
                        a_task.set_KeyResult(string)
                    else:
                        pass
                except UnboundLocalError: 
                    Authorized = False
                    print("Failed to load, Check docx format.(If all goals start with G)")

    
    def set_Special_Task(self,list_of_tasks):
        global Authorized 
        for string in list_of_tasks:
            if len(string) > 1:
                try:
                    if string[0] == "G":
                        a_task = okr_task()
                        self.Special_Task.append(a_task)
                        a_task.set_Objective(string)
                    elif string[0].upper() == "K":
                        a_task.set_KeyResult(string)
                    else:
                        pass
                except UnboundLocalError: 
                    Authorized = False
                    print("Failed to load, Check docx format.(If all goals start with G)")

    def set_Recursive_Task(self,list_of_tasks):
        global Authorized 
        for string in list_of_tasks:
            if len(string) > 1:
                try:
                    if string[0] == "G":
                        a_task = okr_task()
                        self.Recursive_Task.append(a_task)
                        a_task.set_Objective(string)
                    elif string[0].upper() == "K":
                        a_task.set_KeyResult(string)
                    else:
                        pass
                except UnboundLocalError: 
                    Authorized = False
                    print("Failed to load, Check docx format.(If all goals start with G)")

    def show(self,sections = ['Priority_Task','Special_Task','Recursive_Task'], progress = True):
        if not isinstance(sections,list):
            sections = [sections]
        for sec in sections: 
            box_print(f"{sec}:")
            if eval(f"self.{sec}") != []:
                for tasks in eval(f"self.{sec}"):
                    if tasks.KeyResults != {} or progress :
                        print(tasks)
                        if progress:
                            tasks.progress_show()
                            print("\n")
            else:
                print('Empty')
            
#@title Task Class {display-mode: "form"}
class okr_task():
    def __init__(self):
        self.Objective = ""
        self.KeyResults = {}
        self.PG = 0
        self.weight = 0
        self.num_KR = len(list(self.KeyResults.keys()))
        self.completed_KR = 0
        self.unchanged = True
        global Authorized

    def set_Objective(self,obj):
        global Authorized 
        try:
            self.Objective = obj.split("[")[0].strip()
            self.weight = int(obj.split("[")[1].strip("]").split(":")[-1])
        except:
            Authorized = False
            print("task_set up failed: {} has wrong format".format(obj))
            

    def set_KeyResult(self,KeyResult):
        global Authorized 
        try:
            code = KeyResult.split("{")[0].split(":")[0]
            content = KeyResult.split("{")[0].split(":")[1]
            try: 
                a_task = task()
                deadline,time,difficulty = self.get_task_info(KeyResult)
                a_task.set_difficulty(difficulty)
                a_task.set_time(time)
                a_task.set_deadline(deadline)
                a_task.set_reward()
            except:
                Authorized = False
                print("task_set up failed: {} has wrong format".format(KeyResult))

            self.KeyResults[code] = [content,a_task]
            
        except:
            Authorized = False
            print("okr_task KeyResult set up failed, {} has wrong format".format(KeyResult))

    def complete(self,KeyResult_ID,Special=True,tk_pop = False):
        from tkinter import messagebox
        if self.unchanged:
            self.num_KR = len(list(self.KeyResults.keys()))
            self.unchanged = False
        try:  
            if Special:
                self.KeyResults.pop(KeyResult_ID)
                self.completed_KR += 1
                self.PG = self.completed_KR/self.num_KR
                bar = progress(self.PG)
            else: 
                self.PG += 1/(7*self.num_KR)
                self.KeyResults[KeyResult_ID][1].COUNT += 1
                bar = progress(self.PG)
            if tk_pop:
                try:
                    messagebox.showinfo(title = 'Objective Updated', 
                           message = f"{str(self)}\nUpdated:\n{bar}")
                except:
                    pass 
        except KeyError:
            print("{} no longer belong to this objective".format(KeyResult_ID))
            print("Current Key Results:")
            for ks in self.KeyResults.keys():
                print(ks, end = ";")
                
        
        

    def progress_show(self):
        return progress(self.PG)

    def __repr__(self):
        rep = self.Objective + "\nweight:" + str(self.weight)
        for k in self.KeyResults:
            rep += "\n"+ "\t" + k + ":{:60}".format(str(self.KeyResults[k][0]))
            if self.KeyResults[k][1]["COUNT"] > 0:
                rep += "  |Counts:{}".format(self.KeyResults[k][1].COUNT)
        return rep

    def get_task_info(self,KeyResult):
        deadline = None
        time = None
        difficulty = None
        line = KeyResult
        temp = line.replace("}","").split("{")[-1].split(",")
        for i in temp:
            if i.split(":")[0].strip() == "deadline":
                deadline = i.split(":")[1].strip()
            elif i.split(":")[0].strip() == "time":
                time = i.split(":")[1].strip()
            elif i.split(":")[0].strip() == "difficulty":
                difficulty = i.split(":")[1].strip()
        return deadline,time,difficulty

class task():
    def __init__(self):
        global Authorized
        self.difficulty = 0
        self.time = 0
        self.reward = 0
        self.completed = False
        self.deadline = None
        self.description = None
        self.COUNT = 0
        
    def set_desc(self,desc):
        self.description = desc 
        
    def set_deadline(self,deadline):
        self.deadline = deadline
    def set_time(self,time):
        self.time = time

    def set_difficulty(self,difficulty):
        self.difficulty = difficulty
    
    def complete(self):
        self.completed = True

    def __repr__(self):
        return(str({"difficulty":self.difficulty,"time":self.time,"reward":self.reward,"completed":self.completed,"deadline":self.deadline,"COUNT":self.COUNT}))
    
    def __getitem__(self,name):
        return(getattr(self,name))

    def set_reward(self):
        global Authorized 
        "Calculate Reward based on time and difficulty"
        try:
            time = abs(float(self.time))
            difficulty = abs(float(self.difficulty))
        except TypeError: 
            Authorized = False
            print("Fail to calculate reward, task has wrong format")
        time_lower_bound = 0.25
        time_upper_bound = 4
        difficulty_upper_bound = 10
        if time < time_lower_bound:
            time = time_lower_bound
        if time > time_upper_bound:
            time = time_upper_bound
        if difficulty > difficulty_upper_bound:
            difficulty = difficulty_upper_bound
        difficulty = abs(difficulty)
        reward = 3*(time**0.5*difficulty**0.5) + random.choice([-1,-0.5,0,0.5,1,1.5,2])
        self.reward = round(reward)



# In[32]:


#@title Progress Mod {display-mode: "form"}
# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import sys, math

def progress(value,  length=40, title = " ", vmin=0.0, vmax=1.0):
    """
    Text progress bar
    Parameters
    ----------
    value : float
        Current value to be displayed as progress
    vmin : float
        Minimum value
    vmax : float
        Maximum value
    length: int
        Bar length (in character)
    title: string
        Text to be prepend to the bar
    """
    # Block progression is 1/8
    blocks = ["", "▏","▎","▍","▌","▋","▊","▉","█"]
    vmin = vmin or 0.0
    vmax = vmax or 1.0
    lsep, rsep = "▏", "▕"

    # Normalize value
    value = min(max(value, vmin), vmax)
    value = (value-vmin)/float(vmax-vmin)
    
    v = value*length
    x = math.floor(v) # integer part
    y = v - x         # fractional part
    base = 0.125      # 0.125 = 1/8
    prec = 3
    i = int(round(base*math.floor(float(y)/base),prec)/base)
    bar = "█"*x + blocks[i]
    n = length-len(bar)
    bar = lsep + bar + " "*n + rsep

    sys.stdout.write("\r" + title + bar + " %.1f%%" % (value*100))
    sys.stdout.flush()
    
    return "\r" + title + bar + " %.1f%%" % (value*100)

# In[20]:


if __name__ == '__main__':
    T = Load('OKRLOG_S2_W10.docx')
    T.get_week_objective() #Fetch Weekly Plans 
    T.week_okr_show() #Show the preview
    T.complete('S_G3-2-99_K1')#Complete One specific Task 
    T.week_okr_show() #Observe that the progress is being kept track of 

