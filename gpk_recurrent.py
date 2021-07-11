from gpk_utilities import *
from gpkTask import gpk_task
from GPK_PROFILE import Gpk_ToDoList
from Plan_load import *
from random import randint
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk,Image
import os

class gpk_Recurrent(Gpk_ToDoList):
    "A Class That Manages Recurrent Tasks"
    def __init__(self):
        self.todos = pd.DataFrame({"ID":[ ],"TaskName":[ ],"Reward":[ ],
                            "Time":[ ],"Difficulty":[ ],
                            "ObjectID":[ ],"KeyResult ID":[ ],"Task Category":[ ],"Deadline":[],
                            'Recur_At':[ ]})
        
    def add(self,task_name,task_ID,task_time,task_diff,task_des,days,ddl = None, RETURN = False):
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
                            "Deadline":[ddl], 'Recur_At':[days]})
        
        if RETURN:
            return
        else:
            self.todos = self.todos.append(task, ignore_index=True)
        
    def add_gpkTask(self,Gtask,days = {1,2,3,4,5,6,7}):
        ddl = str((datetime.datetime.now()+ datetime.timedelta(days = 1)).date())
        self.add(task_name = Gtask.name,task_ID = Gtask.ID,
                 task_time = float(Gtask.Time) ,
                 task_diff = float(Gtask.Difficulty),
                 task_des = Gtask.Description , ddl = ddl , days = days)
        
    def Modify_Recur(self,Gtask_ID,days):
        #Find row 
        idx = self.todos[self.todos['ID'] == Gtask_ID].index [0]
        #Modify Days
        self.todos.at[idx,'Recur_At'] = days 
        
    def task_recur_at(self,day):
        Analysis = DF_Analysis(self.todos)
        return Analysis.SEARCH('Recur_At',lambda L: day in L)
    

class gpk_Recur_frame(tk.Frame):
    def __init__(self,root,geometry,callback  = None):
        super().__init__()
        self.root = root
        self.callback = callback
        self.height = geometry['height']
        self.width = geometry['width']
        
        try:
            Profile = self.callback(Return = True)
            self.RECUR = Profile.gpk_Recur
        except AttributeError:
            self.RECUR = Profile.gpk_Recur = gpk_Recurrent()
            self.callback(Profile,Update = True)
             
        ###
        # Loaded = Load('OKRLOG_S3_W1.docx')
        # Loaded.get_week_objective() #Fetch Weekly Plans 
        ### TEST
        try:
            self.Recur_RESET() #Loaded
        except:
            print("[gpk_Recur_frame.__init__] Error: Fail to load recursive tasks")
            pass 
        #     #
        # Plan = Fetch_plan_null(Loaded,'Recursive_Task')
        # for Gtask in Plan['Inbox']:
        #     self.RECUR.Modify_Recur(Gtask.ID,{randint(1,7) for _ in range(3)})
        ###
        #Finally 
        self._draw()
        
    def Recur_RESET(self):
        Profile = self.callback(Return = True)
        Profile.gpk_Recur = gpk_Recurrent() 
        self.RECUR = Profile.gpk_Recur
        self.Recur_Fetch(Profile.todos.Load)
        #Finally 
        self.callback(Profile,Update = True)
        
    def Recur_Fetch(self, Loaded = None):
        try:
            if Loaded is None:
                Profile = self.callback(Return = True)
                try: 
                    Loaded = Profile.todos.Load
                except AttributeError:
                    Loaded = None
            for Gtask in Fetch_plan_null(Loaded,'Recursive_Task')['Inbox']:
                self.RECUR.add_gpkTask(Gtask)
        except:
            print("Fail to Fetch Recurrent Task")
        
    def Refresh_txt(self,event):#Refresh texts 
        ID = self.CB.get()
        days = self.RECUR.todos[
            self.RECUR.todos['ID'] == ID]['Recur_At'] 
        self.text_update()
        self.ckbox_update(list(days)[0])
                
    def Ref(self):#Refresh Com Box
        self.Recur_RESET()
        self.Recur_Fetch()
        Option = list(self.RECUR.todos.ID)
        print(f"Options refeshed with: \n{Option}")
        self.CB.config(values = Option)
    
    def text_update(self):
        ID = self.CB.get()
        df = self.RECUR.todos[self.RECUR.todos['ID'] == ID]
        text = "Task Name:\n"+list(df.TaskName)[0]
        text += "\n" + str(Df_to_Gtask(df)[0])
                
        self.Task_Info.delete("1.0","end")
        self.Task_Info.insert("1.0", text)
        
    def ckbox_update(self,days = {1,2,3,4,5,6,7}):
        for day in range(1,8):
            eval(f"self.select_{day}.set(0)")
        for day in days:
            eval(f"self.select_{day}.set(1)")
            
    def fetch_days(self):
        OUT = set()
        for day in range(1,8):
            if eval(f"self.select_{day}.get() == 1"):
                OUT.add(day)
        return OUT 
            
    def SAVE(self):
        days = self.fetch_days()
        self.RECUR.Modify_Recur(self.CB.get(), days)
        #Update Profile 
        Profile = self.callback(Return = True)
        Profile.gpk_Recur = self.RECUR 
        self.callback(Profile,Update = True)
        
            
    def _draw(self):
    #Spacer 
        spacer = tk.Label(self,text = "")
        spacer.pack(side = tk.LEFT, padx = 270)
    #Left Frame
        self.LeftFrame = tk.Frame(self)#,bg = 'orange')
        self.LeftFrame.config(width = self.width/2, height = self.height)
        self.LeftFrame.pack(side=tk.LEFT, fill = 'y', padx = 20)
        ## Com Box
        Option = list(self.RECUR.todos.ID)
        self.CB = ttk.Combobox(self.LeftFrame, values = Option)
        self.CB.bind("<<ComboboxSelected>>", self.Refresh_txt)
        self.CB.grid(row = 0, column = 1)
        ## Task Info Text 
        self.Task_Info = tk.Text(self.LeftFrame, height =30, width = 50, 
              bg = "light cyan", font = ('times new roman',14))
        self.Task_Info.grid(row = 1, column = 1)
    #Right Frame 
        self.RightFrame = tk.Frame(self)#,bg = 'green')
        self.RightFrame.config(width = self.width/2, height = self.height)
        self.RightFrame.pack(side=tk.LEFT,fill = 'both')
        ## Days Check_Boxes 
        spacer = tk.Label(self.RightFrame,text = "")
        spacer.grid(row = 0, column = 0,pady = 20)
        self.ND = {1:'monday',2:'tuesday',3:'wednesday',4:'thursday',5:'friday',6:'saturday',7:'sunday'}
        self.DN = {v:k for k,v in self.ND.items()}
        
        ## Ref
        row = 1
        self.img = ImageTk.PhotoImage(Image.open(os.getcwd() + "/Pictures/sync_refresh.ico"))
        self.Ref_btn = tk.Button(self.RightFrame,image = self.img, command = self.Ref)
        self.Ref_btn.grid(row = row, column = 0,padx = 10,pady = 20)
        
        ## Save 
        for day in self.ND:
            row += 1 
            exec(f"self.select_{day} = tk.IntVar()")
            exec(f"self.ckbox_{day} = tk.Checkbutton(master = self.RightFrame, text=self.ND[day], variable = self.select_{day})")
            eval(f"self.ckbox_{day}.grid(row = {row}, column = 0,padx = 10,pady = 10)")
        self.ckbox_update()
        
        self.save_btn = tk.Button(self.RightFrame,text = 'Save', command = self.SAVE, font = ('times new roman',14))
        self.save_btn.grid(row = row +1 , column = 0 ,padx = 10,pady = 20)

        
def SET_RT():
    root = tk.Tk()
    
    geom = '600x600'
    root.geometry(geom)
    test = gpk_Recur_frame(root,geom)
    test.pack()
    
    root.mainloop()
    
if __name__ == '__main__':
#Testing gpk_Recurrent class 
    # #Fetch Gtasks 
    #     #GET PLAN
    # Loaded = Load('OKRLOG_S3_W1.docx')
    # Loaded.get_week_objective() #Fetch Weekly Plans 
    # Plan = Fetch_plan_null(Loaded,'Recursive_Task')
    # Test = gpk_Recurrent()
    # #Test Add Gtask
    # for Gtask in Plan['Inbox']:
    #     Test.add_gpkTask(Gtask)
    # #Test Modify Recur
    # for Gtask in Plan['Inbox']:
    #     Test.Modify_Recur(Gtask.ID,{randint(1,7) for _ in range(3)})
    # #Test Locate Recur 
    # print(Df_to_Gtask(Test.task_recur_at(3).drop('Recur_At',axis = 1)))

#Testing gpk_Recurrent Frame
    SET_RT()
    