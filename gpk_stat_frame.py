from gpk_utilities import *
from tkinter import ttk
from PIL import ImageTk,Image
import os
import pickle
import copy
from  tkinter import messagebox

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

from gpk_archive_frame import gpk_archive

class DF_Analysis(DF_Search):
    def Set_df(self,df):
        self.df = df 
        
    def Last_n_day(self,n):
        return self.SEARCH('date_done',lambda date: DATE(date) > (datetime.datetime.now() - datetime.timedelta(days = n)).date())
    
    def Last_n_week(self,n):
        return self.SEARCH('date_done',lambda date: DATE(date) > (datetime.datetime.now() - datetime.timedelta(weeks = n)).date())
    
    def Last_n_month(self,n):
        return self.SEARCH('date_done',lambda date: DATE(date) > (datetime.datetime.now() - datetime.timedelta(days = n*30)).date())
    
    def fig_preview(self,fig , geom = '1000x1000'):
        window = tk.Tk()
        window.geometry(geom)
        canvas = FigureCanvasTkAgg(fig,window)
        canvas.draw()
        canvas.get_tk_widget().grid(row = 0, column = 0)
        window.mainloop()
        
    def Plot_Date(self, n, sec = 'Time', figsize = (5, 5), df = None ):
        if df == None:
            df = copy.deepcopy( self.df )  
        fig = Figure(figsize =figsize , dpi = 100)
        plot1 = fig.add_subplot(111)
        #
        Last_n_df = self.Last_n_day(n)
        temp = eval(f"Last_n_df.groupby('date_done').{sec}.agg(sum)")
        res = pd.DataFrame(temp).sort_values(by = 'date_done', key = lambda L: [DATE(i) for i in L],ascending = False)
        #Finally:
        dates = [i for i in res.index]
        freq = res[sec]
        dates,freq = GAP_Filler(dates,freq)#Fill the potential Gaps
        plot1.bar(dates,freq)
        plot1.set_xlabel('Date')
        plot1.set_ylabel(f'{sec}')
        return fig
    
    def Plot_Week(self,n, sec = 'Time', figsize = (5,10), df = None):
        def Cal_Week(Date_0,date):
            delta = DATE(Date_0) - DATE(date)
            return -round((delta.days/7))
        n = n-1
        if df == None:
            df = copy.deepcopy( self.df )  
        ###
        fig = Figure(figsize =figsize , dpi = 100)
        plot1 = fig.add_subplot(111)
        ###
        Last_n_df = self.Last_n_week(n)
        
        
        Most_recent = df.sort_values(by = 'date_done', key = lambda L: [DATE(i) for i in L],ascending = False).iloc[0]['date_done']
        Last_n_df['Week'] = [Cal_Week(Most_recent, date) for date in list(Last_n_df['date_done'])] 
        
        temp = eval(f"Last_n_df.groupby('Week').{sec}.agg(sum)")
        res = pd.DataFrame(temp).sort_values(by = 'Week', key = lambda L: [int(i) for i in L],ascending = False)
        #Finally:
        weeks = [i for i in res.index]
        freq = res[sec]
#         weeks,freq = GAP_Filler(dates,freq)#Fill the potential Gaps
        plot1.bar(weeks,freq)
        plot1.set_xlabel('Week')
        plot1.set_ylabel(f'{sec}')
        return fig
    
    def Plot_Month(self,n, sec = 'Time', figsize = (5,10), df = None):
        def Cal_Month(Date_0,date):
            from math import floor
            year_d = DATE(Date_0).year - DATE(date).year
            month_d = DATE(Date_0).month - DATE(date).month
            delta = -(year_d*12 + month_d)
            return delta
        n = n-1
        if df == None:
            df = copy.deepcopy( self.df )  
        ###
        fig = Figure(figsize =figsize , dpi = 100)
        plot1 = fig.add_subplot(111)
        ###
        Last_n_df = self.Last_n_month(n)
        Most_recent = df.sort_values(by = 'date_done', key = lambda L: [DATE(i) for i in L],ascending = False).iloc[0]['date_done']
        Last_n_df['Month'] = [Cal_Month(Most_recent, date) for date in list(Last_n_df['date_done'])] 
        
        temp = eval(f"Last_n_df.groupby('Month').{sec}.agg(sum)")
        res = pd.DataFrame(temp).sort_values(by = 'Month', key = lambda L: [int(i) for i in L],ascending = False)
        #Finally:
        months = [i for i in res.index]
        freq = res[sec]
#         weeks,freq = GAP_Filler(dates,freq)#Fill the potential Gaps
        plot1.bar(months,freq)
        plot1.set_xlabel('Month')
        plot1.set_ylabel(f'{sec}')
        return fig 
    
class gpk_analysis(gpk_archive):
    def __init__(self,root,geometry,call_back = None):
        tk.Frame.__init__(self,bg = 'blue')
        self.root = root
        self.call_back = call_back 
        self.Profile = call_back(Return = True)
        self.height = geometry['height']
        self.width = geometry['width']
        self.Search =  DF_Search(self.Profile.todos.Archive)
        self.Analysis = DF_Analysis(self.Profile.todos.Archive)
        self._draw()
        
        
    def frame_create(self):
        self.Canvas_height_coef = 2/3 
        self.Canvas_width_coef = 2/3
        self.Canvas_Frame = tk.Frame( master = self.FrameUPPER, bd = 30, bg = 'green')
        self.Canvas_Frame.configure(height = self.Canvas_height_coef*self.height,
                                  width = self.Canvas_width_coef*self.width)
        self.Canvas_Frame.pack(side = tk.LEFT)
        
    def frame_refresh(self):
        self.Canvas_Frame.destroy()
        self.frame_create()
        
    
    def Submit(self):
        self.frame_refresh()
        self.fig = Figure(figsize = (5, 5),dpi = 100) 
        plot1 = self.fig.add_subplot(111)
        #_____PLOTING______#
        if self.By_Section.get():
            plot1.pie([1,2,3])
            #_____PLOTING______#
            self.canvas = FigureCanvasTkAgg(self.fig,self.Canvas_Frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().grid(row = 0, column = 0)   
        else:
            if self.Combo.get() == 'Pick an Option':
                getattr(messagebox,'showwarning')("Option Error","You must Select an Option first (Time/Reward)") 
            else:
                #Deafault:Last 7 Days
                if self.plot_option.get() == 'Day':
                    self.fig = self.Analysis.Plot_Date(int(self.NUM.get()),
                                                       sec = self.Combo.get(),figsize = (10, 5))
                elif self.plot_option.get() == 'Week': 
                    self.fig = self.Analysis.Plot_Week(int(self.NUM.get()),
                                                       sec = self.Combo.get(),figsize = (10, 5))
                elif self.plot_option.get() == 'Month':
                    self.fig = self.Analysis.Plot_Month(int(self.NUM.get()),
                                                       sec = self.Combo.get(),figsize = (10, 5))  
                else:
                    plot1.bar([1,2,3,4,5],[1,2,3,2,1])
            #_____PLOTING______#
            self.canvas = FigureCanvasTkAgg(self.fig,self.Canvas_Frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().grid(row = 0, column = 0)        
            
    def Apply_df(self,df):
        self.Search = DF_Search(df)
        
    def pop_df(self,df):
        res_temp = gpk_archive.pop_df(self,df)
        save_btn = tk.Button(master = res_temp,text = 'Apply Filter')
        save_btn.configure(command = lambda :self.Apply_df(df))
        save_btn.pack()
        
    
    def _draw(self):
    #____Upper Frame___
        self.FrameUPPER = tk.Frame(master = self, bd =20, bg = 'blue')
        self.FrameUPPER.configure(height = 4*self.height/5 ,width = self.width)
        self.FrameUPPER.pack()
        #Canvas Frame 
        self.Canvas_height_coef = 3/5 
        self.Canvas_width_coef = 1
        self.Canvas_Frame = tk.Frame( master = self.FrameUPPER, bd = 30, bg = 'green')
        self.Canvas_Frame.configure(height = self.Canvas_height_coef*self.height,
                                  width = self.Canvas_width_coef*self.width)
        self.Canvas_Frame.pack(side = tk.LEFT)

        
        
    #____Lower Frame___ 
        self.FrameLOWER = tk.Frame(master = self, bd = 2, bg = 'orange')
        self.FrameLOWER.configure(height = self.height/2 ,width = self.width)
        self.FrameLOWER.pack( )
        
        #______Quick Plot Frame___________ 
        self.QP_Frame = tk.Frame(master = self.FrameLOWER, bd = 10, bg = 'Yellow')
        self.QP_Frame.configure(height = self.Canvas_height_coef*self.height,
                                  width = (1-self.Canvas_width_coef)*self.width)
        self.QP_Frame.pack(side = tk.LEFT)
        
        ##__________Radio Buttons__________:
        self.plot_option = tk.StringVar()
        self.plot_option.set('Day')
        self.BD_7_Rbtn = tk.Radiobutton(self.QP_Frame, text = "By Day", variable = self.plot_option,
                                        value = 'Day')
        self.BD_w_Rbtn = tk.Radiobutton(self.QP_Frame, text = "By Week", variable = self.plot_option,
                                        value = 'Week')
        self.BD_m_Rbtn = tk.Radiobutton(self.QP_Frame, text = "By Month", variable = self.plot_option,
                                        value = 'Month')
        # self.BD_a_Rbtn = tk.Radiobutton(self.QP_Frame, text = "--ALL--", variable = self.plot_option,
        #                         value = 4)
        self.BD_7_Rbtn.grid(row = 0, column = 1, padx = 5, pady = 5)
        self.BD_w_Rbtn.grid(row = 1, column = 1,padx = 5, pady = 5)
        self.BD_m_Rbtn.grid(row = 2, column = 1,padx = 5, pady = 5)
        # self.BD_a_Rbtn.grid(row = 3, column = 1,padx = 5, pady = 5)
        
        #Entry BOX
        
        self.option_lab = tk.Label(self.QP_Frame, textvariable = self.plot_option)
        self.NUM = tk.IntVar()
        self.NUM.set(7)
        self.NUM_Entry = tk.Entry(self.QP_Frame,textvariable = self.NUM, width = 4)
        tk.Label(self.QP_Frame, text = 'Last ').grid(row = 3, column = 0)
        self.NUM_Entry.grid(row = 3, column = 1)
        self.option_lab.grid(row = 3, column = 2)
        
        
        #Combo Box 
        Option = ['Time','Reward']
        self.Combo = ttk.Combobox(self.QP_Frame, values = Option)
        self.Combo.set("Pick an Option")
        self.Combo.grid(row = 4, column = 1,padx = 5, pady = 5)
        #Section Check Box:

        self.By_Section = tk.IntVar()
        self.SEC_ChkBttn = tk.Checkbutton(self.QP_Frame, text = 'By Section',width = 15, variable = self.By_Section,
                                       onvalue=1, offvalue=0)
        self.SEC_ChkBttn.grid(row = 5, column = 1)
        
        #Advanced Setting 
        self.adv_set_btn = tk.Button(self.QP_Frame,text='Advanced Setting',
                                     command = self.archive_Search)
        self.adv_set_btn.grid(row = 6,column = 1, pady = 10)
        
        #Filter Frame 
        self.Filter_Frame = tk.Frame(master = self.FrameLOWER, bd = 10, bg = 'red')
        self.Filter_Frame.configure(height = (1-self.Canvas_height_coef)*self.height,
                                  width = (1-self.Canvas_width_coef)*self.width)
        self.Filter_Frame.pack(side = tk.LEFT)
        ##Query Summary:
        
        ##Submit Button
        self.img_complete = ImageTk.PhotoImage(Image.open(os.getcwd() + "/Pictures/Confirm.png"))
        self.Submit_btn = tk.Button(master =self.Filter_Frame, image  =  self.img_complete , command = self.Submit)
        self.Submit_btn.pack()
        
        
        

if __name__ == '__main__':
    with  open( 'D:\GPK\gpk_saves\MrFAKE_user_file.gpk' ,"rb") as INfile:
        Profile = pickle.load(INfile)
    df = Profile.todos.Archive 
    T = DF_Analysis(df)
    # fig = T.Plot_Week(7,figsize = (10, 5))
    # T.fig_preview(fig,'1000x500')
    fig = T.Plot_Month(7,figsize = (10, 5))
    T.fig_preview(fig,'1000x500')

