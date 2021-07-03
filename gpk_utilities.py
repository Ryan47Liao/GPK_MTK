import pandas as pd 
import  tkinter as tk 
import datetime

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
    try:
        STR = String.split("-")
        Y = int(STR[0])
        M = int(STR[1])
        D = int(STR[2])
        return(datetime.date(Y,M,D))
    except:
        print(f"ERROR: {String} ")
        
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
        return self.df.loc[OUT]
    
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
        return (DATE(date_str) + datetime.timedelta(days = 1)).date
    dates_out = []
    freq_out = []
    for idx in range(len(dates)-1):
        gap = DATE(dates[idx]) - DATE(dates[idx+1])
        date = dates[idx]
        dates_out.append(date)
        freq_out.append(freq[idx])
        for _ in range(gap.days-1):
            date = str(yesterday(date))
            dates_out.append(date)
            freq_out.append(0)
    return dates_out,freq_out

if __name__ == '__main__':
    dates = ['2021-07-02','2021-06-30','2021-06-20']
    freq = [4,2,5]
    print( GAP_Filler(dates,freq) )