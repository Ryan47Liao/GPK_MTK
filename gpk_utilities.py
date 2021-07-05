import pandas as pd 
import  tkinter as tk 
import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import copy
import numpy as np

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
    return dates_out,freq_out

class DF_Analysis(DF_Search):
    def __init__(self,df,figsize = (5,10)):
        super().__init__(df)
        self.fig = Figure(figsize =figsize , dpi = 100)
    
    def Set_df(self,df):
        self.df = df 
        
        
    def Last_n_day(self,n,df = None):
        return self.SEARCH('date_done',lambda date: DATE(date) >= (datetime.datetime.now() - datetime.timedelta(days = n)).date(),df = df)
    
    def Last_n_week(self,n,df = None):
        return self.SEARCH('date_done',lambda date: DATE(date) >= (datetime.datetime.now() - datetime.timedelta(weeks = n)).date(),df = df)
    
    def Last_n_month(self,n,df = None):
        return self.SEARCH('date_done',lambda date: DATE(date) >= (datetime.datetime.now() - datetime.timedelta(days = n*30)).date(),df = df)
    
    def fig_preview(self,fig = None, geom = '1000x1000'):
        if fig is None:
            fig = self.fig
        window = tk.Tk()
        window.geometry(geom)
        canvas = FigureCanvasTkAgg(fig,window)
        canvas.draw()
        canvas.get_tk_widget().grid(row = 0, column = 0)
        window.mainloop()
        
    def Plot_Date(self, n = None, sec = 'Time', df = None ,dim = 111,title = None,short = False):
        if df is None:
            df = copy.deepcopy( self.df )  
        plot_id = str(dim)[-1]
        if title is None:
            title = f'{sec} distribution for the Last {n} days'
        exec(f"plot{plot_id} = self.fig.add_subplot(dim,title = title)") 
        #
        if n is not None:
            Last_n_df = self.Last_n_day(n,df)
        else:
            Last_n_df = df 
        print(Last_n_df)
        temp = eval(f"Last_n_df.groupby('date_done').{sec}.agg(sum)")
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
    
    def Plot_Week(self,n = None, sec = 'Time', df = None,dim = 111 ,title = None):
        def Cal_Week(Date_0,date):
            delta = DATE(Date_0) - DATE(date)
            return -round((delta.days/7))
        n = n-1
        plot_id = str(dim)[-1]
        if title is None:
            title = f'{sec} distribution for the Last {n} weeks'
        if df is None:
            df = copy.deepcopy( self.df )  
        ###
        exec(f"plot{plot_id} = self.fig.add_subplot(dim,title = title)") 
        ###
        if n is not None:
            Last_n_df = self.Last_n_week(n,df)
        else:
            Last_n_df = df 
        
        
        Most_recent = df.sort_values(by = 'date_done', key = lambda L: [DATE(i) for i in L],ascending = False).iloc[0]['date_done']
        Last_n_df['Week'] = [Cal_Week(Most_recent, date) for date in list(Last_n_df['date_done'])] 
        
        temp = eval(f"Last_n_df.groupby('Week').{sec}.agg(sum)")
        res = pd.DataFrame(temp).sort_values(by = 'Week', key = lambda L: [int(i) for i in L],ascending = False)
        #Finally:
        weeks = [i for i in res.index]
        freq = res[sec]
#         weeks,freq = GAP_Filler(dates,freq)#Fill the potential Gaps
        eval(f'plot{plot_id}.bar(weeks,freq)')
        eval(f'plot{plot_id}.set_xlabel("Week")')
        eval(f'plot{plot_id}.set_ylabel(sec)')
    
    def Plot_Month(self,n = None, sec = 'Time', df = None,dim = 111,title = None):
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
        ###
        exec(f"plot{plot_id} = self.fig.add_subplot(dim,title = title)") 
        ###
        if n is not None:
            Last_n_df = self.Last_n_month(n,df)
        else:
            Last_n_df = df 
        Most_recent = df.sort_values(by = 'date_done', key = lambda L: [DATE(i) for i in L],ascending = False).iloc[0]['date_done']
        Last_n_df['Month'] = [Cal_Month(Most_recent, date) for date in list(Last_n_df['date_done'])] 
        
        temp = eval(f"Last_n_df.groupby('Month').{sec}.agg(sum)")
        res = pd.DataFrame(temp).sort_values(by = 'Month', key = lambda L: [int(i) for i in L],ascending = False)
        #Finally:
        months = [i for i in res.index]
        freq = res[sec]
#         weeks,freq = GAP_Filler(dates,freq)#Fill the potential Gaps
        eval(f'plot{plot_id}.bar(months,freq)' )
        eval(f'plot{plot_id}.set_xlabel("Month")')
        eval(f'plot{plot_id}.set_ylabel(sec)')
    
    def Plot_Sec(self, n = None , time_frame = 'Day',sec = 'Time', shreshold = 0.2, title = None,df = None,dim = 111):
        """
        -n: Number of time_frame to be plotted 
        -time_frame: type of time_frame, Day,Week,Month
        -sec: Section of Statistic: Time/Reward
        -shreshold: The lowest perecntage required to cause the least section to explode
        """
        if df is None:
            df = self.df 
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
        Last_n_df['Goal_Sec'] = [str(ID).split("_")[1][1] for ID in Last_n_df['ID']]
        temp = pd.DataFrame(eval(f'Last_n_df.groupby(by = "Goal_Sec").{sec}.agg(sum)'))#pd.DataFrame
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
        
if __name__ == '__main__':
    dates = ['2021-06-20','2021-06-30','2021-07-02']
    freq = [4,2,5]
    print( GAP_Filler(dates,freq) )
    dates = ['2021-07-02','2021-06-30','2021-06-20']
    print( GAP_Filler(dates,freq) )