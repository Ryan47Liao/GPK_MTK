import pandas as pd 
import  tkinter as tk 
import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import copy
import numpy as np
import io
import sys

#
from gpk_Score import *
from Plan_load import *
class Gpk_ToDoList:
    def __init__(self):
        self.todos = pd.DataFrame({"ID":[ ],"TaskName":[ ],"Reward":[ ],
                            "Time":[ ],"Difficulty":[ ],
                            "ObjectID":[ ],"KeyResult ID":[ ],"Task Category":[ ]})
        self.Archive = pd.DataFrame()
        self.task_descriptions = {}
    
    def reset_des(self):
        self.task_descriptions = {}
        print("Task Descriptions Rest")
                
    def add(self,task_name,task_ID,task_time,task_diff,task_des,ddl = None, RETURN = False):
        "task_ID: S_G4-3_K1" #Special/Recurrent/Priority_Goal#_KeyResult#
        try:
            if task_ID  in list(self.todos['ID']):
                print("ERROR,ID Already Exsit")
                return 
        except KeyError: #When it's empty 
            print("Empty")
        reward = self.Reward(task_time,task_diff) #calculate reward based on tasktime and difficulty
        Category = task_ID.split("_")[1].split("-")[0][1] #Fetch Task Category Based on Task_ID format 
        KR_ID = task_ID.split("_")[2] 
        O_ID = task_ID.split("_")[1]
        task = pd.DataFrame({"ID":[task_ID],"TaskName":[task_name],"Reward":[reward],
                            "Time":[task_time],"Difficulty":[task_diff],
                            "ObjectID":[O_ID],"KeyResult ID":[KR_ID],"Task Category":[Category],
                            "Deadline":[ddl]})
        try:
            self.task_descriptions[task_ID] = task_des
        except:
            self.reset_des() 
            #self.task_descriptions[task_ID] = task_des #RESET
             
        if RETURN:
            return
        else:
            self.todos = self.todos.append(task, ignore_index=True)
            
    def add_gpkTask(self,Gtask):
        self.add(task_name = Gtask.name,task_ID = Gtask.ID,
                 task_time = float(Gtask.Time) ,
                 task_diff = float(Gtask.Difficulty),
                 task_des = Gtask.Description)
      
    
    def Reward(self,time,difficulty):
        "Return Rewards Based on Time and Difficulty"
        time_lower_bound = 0.35
        time_upper_bound = 5
        difficulty_upper_bound = 10
        if time < time_lower_bound:
            time = time_lower_bound
        if time > time_upper_bound:
            time = time_upper_bound
        if difficulty > difficulty_upper_bound:
            difficulty = difficulty_upper_bound
        difficulty = abs(difficulty)
        reward = 3*(time**0.6*difficulty**0.4) + random.choice([-0.5,0,0.5,1,1.5,2])
        return(round(reward))
    
    def idx_reset(self,df):
        df = df.reset_index()
        try:
            df =  df.drop('level_0',axis = 1)
        except KeyError:
            pass
        try:
            df =  df.drop(['index'],axis = 1)
        except KeyError:
            pass
        return df
    
        
    def delete(self,task_ID):
        "Delete A Task"
        idx = self.todos.loc[self.todos['ID'] == task_ID].index 
        self.todos = self.todos.drop(idx)
        self.todos = self.idx_reset(self.todos)
        try:
            self.task_descriptions.pop(task_ID)
        except Exception as e:
            print(f'ERROR!ID {task_ID} does not exist.')
            print(f"Exception Raised:{e}")
        
        
    def edit(self,task_name,task_ID,task_time,task_diff,task_des,ddl):
        "Edit An Existing Task"
        self.delete(task_ID)
        self.add(task_name,task_ID,task_time,task_diff,task_des,ddl)
        
    def complete(self,task_ID):
        time_stamp = str(datetime.datetime.now())
        date_today = str(datetime.datetime.now().date())    
        week_day_today = str(datetime.datetime.now().weekday())
        og_task = copy.deepcopy(self.todos.loc[self.todos['ID'] == task_ID])
        og_task.insert(8,"date_done",[date_today])
        og_task.insert(9,"week_day",[week_day_today])
        og_task.insert(10,"time_stamp",[time_stamp])
        try:
            og_task.insert(11,"description",[self.task_descriptions[task_ID]])
        except:
            pass
        self.Archive = self.Archive.append(og_task)
        self.Archive = self.idx_reset(self.Archive)
        self.delete(task_ID)
        
def Fill_date(Dict,start = None,base_line = 0):
    if start is None:
        start = str(Last_monday())
    most_recent = min(Dict.keys(),key = DATE)#lambda L:[DATE(i) for i in L])
    assert DATE(start) <= DATE(most_recent),'Start date must be no larger than the existing smallest date'
    date = start 
    OUT = {}
    while DATE(date) <= DATE(most_recent):
        date = str(tmr(date)) #
        OUT[date] = base_line
    OUT = {**OUT,**Dict}
    return OUT

def Fill_date(Dict,start = None,base_line = 0):
    if start is None:
        start = str(Last_monday())
    most_recent = min(Dict.keys(),key = DATE)#lambda L:[DATE(i) for i in L])
    if DATE(start) <= DATE(most_recent):
        date = start 
        OUT = {start:base_line}
        while DATE(date) < DATE(most_recent):
            date = str(tmr(date)) #
            OUT[date] = base_line
        OUT = {**OUT,**Dict}
        return OUT
    else:
        return Dict
        

def wkday_to_date(wkday):
    "Convert a Wkday of this week into its date"
    DICT = {}
    D = {1:'monday',2:'tuesday',3:'wednesday',4:'thursday',5:'friday',6:'saturday',7:'sunday'}
    date = str(Last_monday())
    while str(date) != str(Next_Sunday()):
        DICT[str(date)] = D[int(DATE(date).weekday()+1)]
        date = str(tmr(date))
    DICT[str(date)] = D[int(DATE(date).weekday()+1)]
    DICT_new = {k:v for v,k in DICT.items()}
    if wkday == 'Inbox':
        return str(yesterday(str(Last_monday())))
    return DICT_new[wkday]

def weekday_today(timezone = "Asia/Shanghai"):
    "Return the weekday number of today"
    from datetime import datetime
    from datetime import date
    from dateutil import tz

    timezone = tz.gettz(timezone)
    year = int(datetime.now(timezone).year)
    month = int(datetime.now(timezone).month)
    day = int(datetime.now(timezone).day)
    return(date(year, month, day).isocalendar()[2])
        
def Plan_to_df(Profile):
    plan = Profile.okr_plan
    todo = Gpk_ToDoList()
    TEMP = []
    for sec in plan: 
        for Gtask in plan[sec]:
            todo.add_gpkTask(Gtask)
            TEMP.append(wkday_to_date(sec))
    todo.todos['Plan_at'] = TEMP
    return todo.todos

def OKRLOG_to_df(DayObject):
    out = {'Task_Type' : [],'Objective' : [],'Section': [], 'ID' : [], 'weight' : [], 'progress' : []}
    sections = ['Priority_Task','Special_Task','Recursive_Task']
    for sec in sections: 
        if eval(f"DayObject.{sec}") != []:
            for okr_task in eval(f"DayObject.{sec}"):
                out['Task_Type'].append(sec)
                out['Objective'].append(okr_task.Objective)
                out['weight'].append(okr_task.weight)
                out['progress'].append(okr_task.PG)
                ID = okr_task.Objective.split(':')[0]
                out['ID'] .append(f"{sec[0]}_{ID}_K-??")
                Sec = ID[1]
                out['Section'].append(Sec)
    return pd.DataFrame(out)
                

def print_collector(function,*args,**kargs):
    "Collect the stuff that's going to be printed"
    old_stdout = sys.stdout # Memorize the default stdout stream
    sys.stdout = buffer = io.StringIO()
    function(*args,**kargs)#Call Function
    sys.stdout = old_stdout # Put the old stream back in place
    whatWasPrinted = buffer.getvalue() # Return a str containing the entire contents of the buffer.
    return whatWasPrinted

def perfect_match(df,target)-> int :
    "Return the index of the best match of the df "
    Conditions = [df[idx] == target[idx] for idx in target.index]
    return np.argmax(sum([np.array(condition*1) for condition in Conditions]))


def df_to_Treeview(master, data:pd.core.frame.DataFrame, col_width = 120,col_minwidth = 25,col_anchor = tk.CENTER
              ,LABEL = False) :
    from tkinter import ttk
    if LABEL:
        label_text = "Parent"
        label_bool = tk.YES
        label_width = col_width
    else:
        label_text = ""
        label_bool = tk.NO
        label_width = 0
        
    my_tree = ttk.Treeview(master)
    #Define Our Columns
    my_tree ['columns'] = list(data.columns)
    #Format the columns & Create Headings (Bar at the very TOP):
    my_tree.column("#0",width = label_width, stretch = label_bool)
    my_tree.heading("#0", text = label_text)
    for col_name in list(data.columns):
        my_tree.column(col_name,anchor = col_anchor , width = col_width)
        my_tree.heading(col_name,text = col_name,anchor = col_anchor)
    #Add Data 
    iid = 0 #Item ID(UNIQUE)
    for row in range(data.shape[0]):
        data_i = list(data.iloc[row,])
        my_tree.insert(parent = "", index = 'end', iid = iid, text = label_text, values = data_i)
        iid += 1

    return my_tree    

def DATE(String):
    import datetime
    STR = String.split("-")
    Y = int(STR[0])
    M = int(STR[1])
    D = int(STR[2])
    return(datetime.date(Y,M,D))
        
class DF_Search:
    def __init__(self,df):
        self.df = df 

    def Search_ID(self,id_pat,df = None):
        import re
        pat = re.compile(f"{id_pat}")
        return self.SEARCH('ID',lambda ID: pat.search(ID) is not None,df)
    
    def SEARCH(self,section,predict,df = None):
        if df is None:
            df = self.df 
        OUT = []
        for idx in df.index:
            entry = df.loc[idx][section]
            if predict(entry):
                OUT.append(idx)
        return df.loc[OUT]
    
    def Stack_Search(self,Sec_Preds: [(str,str)]):
        "Perform Search in Sequence"
        df = self.df 
        for sec,pred in Sec_Preds:
            df = self.SEARCH(sec,pred,df)    
        return df 
    
def GAP_Filler(dates,freq):
    "Take a list of date Strs (Potentially Gapped),and return a patched one, assuming the are in dec order (Recent to Last)"
    og_dates = copy.copy(dates)
    og_freq = copy.copy(freq)
    def yesterday(date_str):
        return (DATE(date_str) - datetime.timedelta(days = 1))
    
    def tmr(date_str):
        return (DATE(date_str) + datetime.timedelta(days = 1))
    
    def ascending(dates):
        out = [DATE(dates[idx]) >= DATE(dates[idx+1 ]) for idx in range(len(dates)-1)]
        return all(out)
    
    def decending(dates):
        out = [DATE(dates[idx]) <= DATE(dates[idx+1 ]) for idx in range(len(dates)-1)]
        return all(out)  
     
    if len(dates) == 1:
        return dates,freq
    
    if ascending(dates):
        print('Dates are Backward Ordered')
        NEXT = yesterday 
    elif decending(dates):
        NEXT = tmr
        print('Dates are Forward Ordered')
    else:
        raise Exception(f"The dates are not ordered. {dates}")

    
    dates_out = []
    freq_out = []
    for idx in range(len(dates)-1):
        gap = DATE(dates[idx]) - DATE(dates[idx+1])
        date = dates[idx]
        dates_out.append(date)
        freq_out.append(freq[idx])
        for _ in range(abs(gap.days)-1):
            date = str(NEXT(date))
            dates_out.append(date)
            freq_out.append(0)
    dates_out.append(og_dates[-1])
    freq_out.append(og_freq[-1])
    return dates_out,freq_out

class DF_Analysis(DF_Search):
    def __init__(self,df,figsize = (5,10)):
        super().__init__(df)
        self.fig = Figure(figsize =figsize , dpi = 100)
    
    def Set_df(self,df):
        self.df = df 
        
        
    def Last_n_day(self,n,df = None,Group = 'date_done'):
        return self.SEARCH(Group,lambda date: DATE(date) >= (datetime.datetime.now() - datetime.timedelta(days = n)).date(),df = df)
    
    def Last_n_week(self,n,df = None,Group = 'date_done'):
        return self.SEARCH(Group,lambda date: DATE(date) >= (datetime.datetime.now() - datetime.timedelta(weeks = n)).date(),df = df)
    
    def Last_n_month(self,n,df = None,Group = 'date_done'):
        return self.SEARCH(Group,lambda date: DATE(date) >= (datetime.datetime.now() - datetime.timedelta(days = n*30)).date(),df = df)
    
    def fig_preview(self,fig = None, geom = '1000x1000'):
        if fig is None:
            fig = self.fig
        window = tk.Tk()
        window.geometry(geom)
        canvas = FigureCanvasTkAgg(fig,window)
        canvas.draw()
        canvas.get_tk_widget().grid(row = 0, column = 0)
        window.mainloop()
        
    def Plot_DateFrame(self, n = None, sec = 'Time', df = None ,dim = 111,title = None,
                       short = False, Group = 'date_done', 
                       key = lambda L: [DATE(i) for i in L]):
        if df is None:
            df = copy.deepcopy( self.df )  
        df = copy.deepcopy(df)
        plot_id = str(dim)[-1]
        if Group == 'date_done':
            DateFrame = 'Day'
        else:
            DateFrame = Group
        if title is None:
            title = f'{sec} distribution for the Last {n} {DateFrame}s'
        exec(f"plot{plot_id} = self.fig.add_subplot(dim,title = title)") 
        ###
        #
        if n is not None:
            Last_n_df = self.Last_n_day(n,df,Group)
        else:
            Last_n_df = df 
        print(Last_n_df)
        temp = eval(f"Last_n_df.groupby(Group).{sec}.agg(sum)")
        res = pd.DataFrame(temp).sort_values(by = Group, key = key,ascending = True)
        #Finally:
        dates = [i for i in res.index]
        freq = res[sec]
        dates,freq = GAP_Filler(dates,freq)#Fill the potential Gaps
        if short:
            dates = [date.split('-')[1]+'.'+date.split('-')[2] for date in dates]
        eval(f'plot{plot_id}.bar(dates,freq)')
        eval(f'plot{plot_id}.set_xlabel(Group)')
        eval(f'plot{plot_id}.set_ylabel(sec)')
        
        
    def Plot_Date(self, n = None, sec = 'Time', df = None ,dim = 111,title = None,short = False,
                  Group = 'date_done'):
        if df is None:
            df = copy.deepcopy( self.df )  
        df = copy.deepcopy(df)
        plot_id = str(dim)[-1]
        if title is None:
            title = f'{sec} distribution for the Last {n} days'
        exec(f"plot{plot_id} = self.fig.add_subplot(dim,title = title)") 
        #
        if n is not None:
            Last_n_df = self.Last_n_day(n,df,Group)
        else:
            Last_n_df = df 
        print(Last_n_df)
        temp = eval(f"Last_n_df.groupby(Group).{sec}.agg(sum)")
        res = pd.DataFrame(temp).sort_values(by = 'date_done', key = lambda L: [DATE(i) for i in L],ascending = True)
        print(res)
        #Finally:
        dates = [i for i in res.index]
        freq = res[sec]
        dates,freq = GAP_Filler(dates,freq)#Fill the potential Gaps
        if short:
            dates = [date.split('-')[1]+'.'+date.split('-')[2] for date in dates]
        eval(f'plot{plot_id}.bar(dates,freq)')
        eval(f'plot{plot_id}.set_xlabel("Date")')
        eval(f'plot{plot_id}.set_ylabel(sec)')
    
    def Plot_Week(self,n = None, sec = 'Time', df = None,dim = 111 ,title = None,Group = 'Week'):
        def Cal_Week(Date_0,date):
            delta = DATE(Date_0) - DATE(date)
            return -round((delta.days/7))
        n = n-1
        plot_id = str(dim)[-1]
        if title is None:
            title = f'{sec} distribution for the Last {n} weeks'
        if df is None:
            df = copy.deepcopy( self.df ) 
        df = copy.deepcopy(df) 
        ###
        exec(f"plot{plot_id} = self.fig.add_subplot(dim,title = title)") 
        ###
        if n is not None:
            Last_n_df = self.Last_n_week(n,df,Group)
        else:
            Last_n_df = df 
        
        
        Most_recent = df.sort_values(by = 'date_done', key = lambda L: [DATE(i) for i in L],ascending = False).iloc[0]['date_done']
        Last_n_df['Week'] = [Cal_Week(Most_recent, date) for date in list(Last_n_df['date_done'])] 
        
        temp = eval(f"Last_n_df.groupby(Group).{sec}.agg(sum)")
        res = pd.DataFrame(temp).sort_values(by = 'Week', key = lambda L: [int(i) for i in L],ascending = False)
        #Finally:
        weeks = [i for i in res.index]
        freq = res[sec]
#         weeks,freq = GAP_Filler(dates,freq)#Fill the potential Gaps
        eval(f'plot{plot_id}.bar(weeks,freq)')
        eval(f'plot{plot_id}.set_xlabel("Week")')
        eval(f'plot{plot_id}.set_ylabel(sec)')
    
    def Plot_Month(self,n = None, sec = 'Time', df = None,dim = 111,title = None,Group = 'Month'):
        def Cal_Month(Date_0,date):
            from math import floor
            year_d = DATE(Date_0).year - DATE(date).year
            month_d = DATE(Date_0).month - DATE(date).month
            delta = -(year_d*12 + month_d)
            return delta
        if title is None:
            title = f'{sec} distribution for the Last {n} months'
        n = n-1
        plot_id = str(dim)[-1]
        if df is None:
            df = copy.deepcopy( self.df )  
        df = copy.deepcopy(df)
        ###
        exec(f"plot{plot_id} = self.fig.add_subplot(dim,title = title)") 
        ###
        if n is not None:
            Last_n_df = self.Last_n_month(n,df)
        else:
            Last_n_df = df 
        Most_recent = df.sort_values(by = 'date_done', key = lambda L: [DATE(i) for i in L],ascending = False).iloc[0]['date_done']
        Last_n_df['Month'] = [Cal_Month(Most_recent, date) for date in list(Last_n_df['date_done'])] 
        
        temp = eval(f"Last_n_df.groupby(Group).{sec}.agg(sum)")
        res = pd.DataFrame(temp).sort_values(by = 'Month', key = lambda L: [int(i) for i in L],ascending = False)
        #Finally:
        months = [i for i in res.index]
        freq = res[sec]
#         weeks,freq = GAP_Filler(dates,freq)#Fill the potential Gaps
        eval(f'plot{plot_id}.bar(months,freq)' )
        eval(f'plot{plot_id}.set_xlabel("Month")')
        eval(f'plot{plot_id}.set_ylabel(sec)')
    
    def Plot_Sec(self, n = None , time_frame = 'Day',sec = 'Time', 
                 shreshold = 0.2, title = None,df = None,dim = 111,Group = 'date_done'):
        """
        -n: Number of time_frame to be plotted 
        -time_frame: type of time_frame, Day,Week,Month
        -sec: Section of Statistic: Time/Reward
        -shreshold: The lowest perecntage required to cause the least section to explode
        """
        if df is None:
            df = copy.deepcopy( self.df )  
        df = copy.deepcopy(df)
        plot_id = str(dim)[-1]
        ###
        if title is None:
            title = f'{sec} distribution among sections for the past {n} {time_frame}s'
        exec(f"plot{plot_id} = self.fig.add_subplot(dim,title = title)") 
        time_frame = time_frame.lower()
        if n is not None:
            Last_n_df = eval(f'self.Last_n_{time_frame}(n,df)')
        else:
            Last_n_df = df 
        Last_n_df['Task Category'] = [str(ID).split("_")[1][1] for ID in Last_n_df['ID']]
        temp = pd.DataFrame(eval(f'Last_n_df.groupby(by = "Task Category").{sec}.agg(sum)'))#pd.DataFrame
        temp_Dict = {Goal_sec:t for Goal_sec,t in zip([i for i in temp.index],temp[sec])}
        Labs = ['Health','Family','Personal Development','Carrer']
        X = {1:0,2:0,3:0,4:0}
        for goal_sec in temp_Dict:
            X[int(goal_sec)] = temp_Dict[goal_sec]/sum(temp_Dict.values())
        print(X)
        explode = [True if x == min(X.values()) and float(x) < shreshold else False for x in X.values()]
        #Labs = [Lab + '\n' + str(Percentage)+"%" for Lab,Percentage in zip(Labs,X)]
        eval(f'plot{plot_id}.pie(X.values(), explode = explode,labels = Labs, autopct = lambda value: str(round(value,2))+"%")') 
        
    def get_fig(self):
        return self.fig 
    
    def Rest_fig(self):
        self.fig.clear()
        
    def Plot_Score(self,Loaded,Scores = None, df = None, dim =111,title = 'Score Projection',
                  grade_cutoff = {"D":(55,'r'),"C":(65,'y'),"B":(75,'b'),"A":(85,'g'),"S":(95,'m')}):
        if df is None:
            df = self.df
        if Scores is None:
            Scores = Get_Scores(df,Loaded) #A dictionary of datetime and scores
        print(Scores)
        Scores = Fill_date(Scores)
        print(Scores)
        LST = list(Scores.values())
        plot1 = self.fig.add_subplot(dim,title = title)
        #
        Trend = trend(list(LST))
        Now = now(list(LST))
        #Plotting
        WEEKDAYS = ["Mon","Tue","Wed","Thur","Fri","Sat","Sun"]
        plot1.plot(WEEKDAYS,Now,label = "NOW")
        plot1.plot(WEEKDAYS,Trend,label = "Projection",linestyle='dashdot')
        for grade in grade_cutoff.keys():
            plot1.plot(WEEKDAYS,constant_line(grade_cutoff[grade][0]),label = grade,linestyle='dashed',color = grade_cutoff[grade][1])
        plot1.legend()
            
            
def Fetch_plan_null(Loaded):
#     Loaded = self.callback(Return = True).todos.Load 
    D = {1:'monday',2:'tuesday',3:'wednesday',4:'thursday',5:'friday',6:'saturday',7:'sunday'}
    OUT = {'Inbox':[]}
    for day in D.values():
        OUT[day] = []
    for sec in ['Priority_Task','Special_Task']:
        for Objective in eval(f'Loaded.WeekObjective.{sec}'):
            O_ID = Objective.Objective.split(":")[0]
            for KR in Objective.KeyResults:
                task_id = f"{sec[0]}_{O_ID}_{KR}"
                task_name = Objective.KeyResults[KR][0]
                temp = Objective.KeyResults[KR][1]
                Gtask = gpk_task(name = task_name,ID=task_id,
                                Difficulty = temp['difficulty'],Time = temp['time'],Reward = temp['reward'],
                                Description = "")
                OUT['Inbox'].append(Gtask)
    return OUT

if __name__ == '__main__':
    dates = ['2021-07-04', '2021-07-05', '2021-07-06', '2021-07-09', '2021-07-11']
    freq = [1,4,6,2,5]
    print( GAP_Filler(dates,freq) )
    dates = ['2021-07-02','2021-06-30','2021-06-20']
    print( GAP_Filler(dates,freq) )
    # Loaded = Load('OKRLOG_S3_W1.docx')
    # Loaded.get_week_objective()
    # OUT = Fetch_plan_null(Loaded)
    # print(OUT)
    print(weekday_today())