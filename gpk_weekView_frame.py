from gpk_utilities import *
import tkinter as tk
from tkinter import ttk
import pandas as pd

class gpk_weekView(tk.Frame):
    def __init__(self,root,geometry,callback  = None):
        super().__init__(bg = 'pink')
        self.root = root
        self.callback = callback
        self.height = geometry['height']
        self.width = geometry['width']
        PROFILE = self.callback(Return = True)
        try:
            df = OKRLOG_to_df(PROFILE.todos.Load.WeekObjective) 
        except:
            df = pd.DataFrame()
        self.Analysis = DF_Analysis(df,(3,6))
        self._draw()
    
    def CF_create(self,master,hc = 2/3, wc = 2/5,side = None):
        "Create a Canvas Frame"
        self.Canvas_height_coef = 1/2 
        self.Canvas_width_coef = 2/3
        self.Canvas_Frame = tk.Frame( master = master, bd = 30 )#, bg = 'green')
        self.Canvas_Frame.configure(height = self.Canvas_height_coef*self.height,
                                  width = self.Canvas_width_coef*self.width)
        self.Canvas_Frame.config(highlightbackground="black" , highlightthickness=2)
        self.Canvas_Frame.pack(side = tk.TOP)
        
    def CF_update(self):
        PROFILE = self.callback(Return = True)
        df = OKRLOG_to_df(PROFILE.todos.Load.WeekObjective) 
        try:
            self.Canvas_Frame.destroy()
        except AttributeError:
            pass 
        self.CF_create(master = self.RightFrame)
        #Plotting 
        self.Analysis.Rest_fig() 
        self.Analysis.Plot_Sec(sec = 'weight', dim = 211, title = 'Weight Distribution')
        self.Analysis.Plot_Sec(sec = 'weight', df = df[df['Task_Type'] == self.View.get()],
                               dim = 212 ,  title = f'Weight Dist of {self.View.get()}')
        #Finally:
        self.fig = self.Analysis.get_fig()
        self.canvas = FigureCanvasTkAgg(self.fig,self.Canvas_Frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side = tk.TOP, anchor = 'n')
        
    def Load_Plan(self):
        filename = tk.filedialog.askopenfile(filetypes=[('OKRLOG', '*.docx')])                                 
        self.file_path = filename.name
        PROFILE = self.callback(Return = True)
        PROFILE.todos.get_Load(self.file_path)
        self.callback(PROFILE,Update = True)
        #Re_init the DF_Analysis
        try:    
            df = OKRLOG_to_df(PROFILE.todos.Load.WeekObjective) 
        except:
            df = pd.DataFrame()
        self.Analysis = DF_Analysis(df,(3,6))
        
        self.Show_View()
        
    def Show_View(self):
        PROFILE = self.callback(Return = True)
        whatWasPrinted = print_collector(PROFILE.todos.Load.WeekObjective.show,
                                         sections = [self.View.get()])
        self.OKRVIEW.set(whatWasPrinted) 
        self.Text_refresh()
        self.CF_update()
    
    def Text_refresh(self):
        self.OKRLOG_Text.delete("1.0","end")
        self.OKRLOG_Text.insert("1.0", self.OKRVIEW.get())
        
    def _draw(self):
        #__________________LeftFrame_____________________#
        self.LeftFrame = tk.Frame(master = self, bg = 'blue')
        self.LeftFrame.config(width = 4*self.width/5, height = self.height)
        self.LeftFrame.config(highlightbackground="black" , highlightthickness=2)
        self.LeftFrame.grid(row = 0, column = 0 ,padx=200, pady=20
                            )#.pack(side = tk.LEFT,fill="y", expand=True, padx=20, pady=20)
            ##_________Text_Display___________##
        self.OKRVIEW = tk.StringVar()
        self.OKRLOG_Text = tk.Text(self.LeftFrame,
                                   height = 50, width = 75, 
              bg = "light cyan")
        self.OKRLOG_Text.configure(font=("Times New Roman", 14, "bold"))
        self.OKRLOG_Text.pack()
        try:
            self.Show_View()
        except AttributeError:
            print("OKRLOG not Loaded")
        #__________________RightFrame_____________________#
        self.RightFrame = tk.Frame(master = self, bg = 'green')
        self.RightFrame.config(width = 2*self.width/5, height = self.height)
        self.RightFrame.grid(row = 0, column = 1)#.pack(side = tk.LEFT)
            ##_________Interaction Frame________##
        self.InterFrame = tk.Frame(master = self.RightFrame, bg = 'orange')
        self.InterFrame.config(width = 2*self.width/5, height = (1/3)*self.height)
        self.InterFrame.pack()
                ###___Radio Buttons___###
        self.View = tk.StringVar()
        self.View.set("Priority_Task")
        self.PT_Rbtn = tk.Radiobutton(self.InterFrame, text = "Priority_Task", variable = self.View,
                                        value = 'Priority_Task',command = self.Show_View)
        self.ST_Rbtn = tk.Radiobutton(self.InterFrame, text = "Special_Task", variable = self.View,
                                        value = 'Special_Task',command = self.Show_View)
        self.RT_Rbtn = tk.Radiobutton(self.InterFrame, text = "Recursive_Task", variable = self.View,
                                        value = 'Recursive_Task',command = self.Show_View)
        
        self.PT_Rbtn.pack(padx = 5, pady = 5)#.gird(row = 1, column = 1,padx = 5, pady = 5)
        self.ST_Rbtn.pack(padx = 5, pady = 5)#.gird(row = 2, column = 1,padx = 5, pady = 5)
        self.RT_Rbtn.pack(padx = 5, pady = 5)#.gird(row = 3, column = 1,padx = 5, pady = 5)
                ###___Buttons___###
        self.RT_setting_btn = tk.Button(self.InterFrame,text = 'Recursive_Task Settings')
        self.Import_btn = tk.Button(self.InterFrame,text = 'Import OKR Week Agenda',
                                    command = self.Load_Plan)
        self.Report_btn = tk.Button(self.InterFrame,text = 'Export Report')
        
        self.RT_setting_btn.pack(padx = 5, pady = 5)#.gird(row = 4, column = 0,padx = 5, pady = 5)
        self.Import_btn.pack(padx = 5, pady = 5)#.gird(row = 5, column = 1,padx = 5, pady = 5)
        self.Report_btn.pack(padx = 5, pady = 5)#.gird(row = 6, column = 2,padx = 5, pady = 5)
                    ##_________Canvas Frame________##
        try:
            self.CF_update()
        except AttributeError:
            pass 
        
# class gpk_weekPlanning(tk.Frame):
#     def __init__(self,root,geometry,callback  = None):
#         super().__init__(bg = 'pink')
#         self.callback = callback
#         self.height = geometry['height']
#         self.width = geometry['width']
#         self.root = root
#         self._draw()
#
#     def _draw(self):
#         #___________LeftFrame______________#
#         self.LeftFrame = tk.Frame(master = self, bg = 'orange')
#         self.LeftFrame.config(width = self.width/2, height = self.height)
#         self.LeftFrame.pack(side = tk.LEFT)
#         #___________RightFrame______________#
#         self.RightFrame = tk.Frame(master = self, bg = 'pink')
#         self.RightFrame.config(width = self.width/2, height = self.height)
#         self.RightFrame.pack(side = tk.LEFT)