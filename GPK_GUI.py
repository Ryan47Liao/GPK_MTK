#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import ttk
from PIL import ImageTk,Image
from  tkinter import filedialog
from tkinter import messagebox
import os
import Tetris

# In[2]:Costume Packages 

from gpk_cache import GPK_Cache
from GPK_PROFILE import *


class gpk_Shell:
    def __init__(self):
        self.shell_rt = tk.Tk()
        self.shell_rt.title("GPK_LOGIN")
        self.shell_rt.geometry('1000x865')
        self.cwd = os.getcwd()
        self.ACC = None
        self.PW = None
        self.Profile = None
        self.parent_address = "D:/GPK/gpk_saves/"
        try:
            os.makedirs(self.parent_address) 
        except FileExistsError:
            pass

                    
        #_________Finally_________#
        #Fetch Cache 
        try:
            with open(self.parent_address + "gpk_cache" , 'rb') as INfile:
                self.cache = pickle.load(INfile)                    
        except FileNotFoundError:
            self.cache = GPK_Cache(self.parent_address + "gpk_cache")
            self.cache.save() 
        #DRAW
        self._draw()
        #Insert Data
        if self.cache.Re_status():
            print("Remembered Acc")
            self.acc_entry.delete(0, 'end')
            self.acc_entry.insert('0',self.cache.get_AC())   
            self.pw_entry.delete(0, 'end')
            self.pw_entry.insert('0',self.cache.get_PW())  
            self.open_profile(self.cache.gpk_save_path)
        #Finally 
        self.shell_rt.mainloop()
    
    def authenticate(self)->bool:
        "Authenticates the user"
        if self.Profile is None:
            getattr(messagebox,'showwarning')("Access Denied","You must Load the saved file first.") 
            self.open_profile()
            return False
        else:
            return self.Profile.Verified(self.PW) 
        
        
    def gpk_login(self):
        self.ACC = self.acc_entry.get()
        try:
            self.PW = int(self.pw_entry.get())
        except:
            getattr(messagebox,'showwarning')("ERROR","PING must be Digits only!") 
        "If LogIn Successful,open the Main app and destroy the login."
        if self.authenticate():
            #If remember me is toggled 
            if self.remember.get():
                self.cache.set_info(self.ACC,self.PW)
                self.cache.set_save_path(self.file_path)
            else:
                self.cache.Re_Fal()
            self.cache.save()
            self.shell_rt.destroy()
            #________________#
            new_root = gpk_Main(self.Profile,self.file_path)
        else:
            getattr(messagebox,'showwarning')("Access Denied","WRONG PASSWORD")
        
        
    def close(self):
        self.shell_rt.destroy()
        
    #__________________REGISTRATION__________________#
    def new_account(self,name,password):
        self.reg_window.destroy()
        getattr(messagebox,'showwarning')("Creating New Profile","This might take 10-20s to generate encryption keys...")
        self.Profile = PROFILE(name, int(password))
        #Finally, Create such a gpk file...
        if True:
            try:
                file_name = "{}_user_file".format(name)
                entry = "C {} -n {}".format(self.parent_address,file_name)
                file_path = File_Exp(entry,RETURN= True) #Create a file at the destination 
                print("file_path:",file_path)
                self.Profile.Save(str(file_path)) #Dump the information into the file
                
            except Exception as ex:
                print("Error,fail to create account:\n",ex)
                
            finally:
                self.open_profile() 
        
    def gpk_reg(self):
        self.reg_window = tk.Toplevel()
        self.reg_window.title('Create New Account')
        #_____________________Draw_____________________________#
        name_label = tk.Label(master =self.reg_window,text = 'Name:')
        name_entry = tk.Entry(master = self.reg_window)
        pw_label = tk.Label(master =self.reg_window,text = 'PING(digit only):')
        pw_entry = tk.Entry(master = self.reg_window)
        submit_btn = tk.Button(master = self.reg_window, 
                             text = 'Submmit', command = lambda: self.new_account(name_entry.get(),pw_entry.get()) )
        #Packing...
        name_label.grid(padx = 5, pady = 5, row = 0, column = 0)
        name_entry.grid(padx = 5, pady = 5,row = 0, column = 1)
        pw_label.grid(padx = 5, pady = 5,row = 1, column = 0)
        pw_entry.grid(padx = 5, pady = 5,row = 1, column = 1)
        submit_btn.grid(padx = 5, pady = 5,row = 2, column = 1,columnspan = 2)
        
        
        
        
    """
    Creates a new GPK file when the 'New' menu item is clicked.
    """
    def new_profile(self):
        filename = tk.filedialog.asksaveasfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        profile_filename = filename.name
        self.file_path = profile_filename
        
            
        
    """
    Opens an existing DSU file when the 'Open' menu item is clicked and loads the profile
    data into the UI.
    """
    def open_profile(self,path = None):
        if path is None:
            filename = tk.filedialog.askopenfile(filetypes=[('Grand Peach King Profile', '*.gpk')],
                                                 initialdir = self.parent_address)
            self.file_path = filename.name
        else:
            self.file_path = path
        print(f"opening save at {self.file_path}")
        INfile = open( self.file_path ,"rb")
        self.Profile = pickle.load(INfile)
        INfile.close()
        #Update User Name
        user_name = str(self.file_path).split('.')[0].split("gpk_saves")[-1].split('user_file')[0].strip('/_\\')
        print(user_name)
        self.acc_entry.delete(0, 'end')
        self.acc_entry.insert('0',user_name)   
                                                                                                    
                                                                                                    
        
    def _draw(self):
        #ＵＰＰＥＲ　ＦＲＡＭＥ
        #____________Menus_______________
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.shell_rt)
        self.shell_rt['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)
        #___________WelcomePic___________
        self.frame_Upper = tk.Frame(master = self.shell_rt, bg = 'black')
        self.frame_Upper.configure(height = 500,width = 1000)
        self.frame_Upper.pack()
        self.okr_img = ImageTk.PhotoImage(Image.open(self.cwd + "/Pictures/OKR_Menu.png"))
        self.top_pic = tk.Label(master = self.frame_Upper , image = self.okr_img, anchor = tk.S)
        self.top_pic.pack(fill = tk.BOTH ) 
        
        #ＬＯＷＥＲ　ＦＲＡＭＥ
        self.frame_Lower = tk.Frame(master = self.shell_rt) #, bg = 'orange')
        self.frame_Lower.configure(height = 200,width = 1000)
        self.frame_Lower.pack()
        
        #___________Acc_entry_______________
        self.acc_info_entry_frame = tk.Frame(master = self.frame_Lower)# ,bg = 'blue')
        self.acc_info_entry_frame.configure(height = 50,width = 1000)
        self.acc_info_entry_frame.pack(ipady = 0, ipadx = 50, expand = 1)
        
        self.acc_label = tk.Label(master = self.acc_info_entry_frame , text = 'Account:')
        self.acc_entry = tk.Entry(master = self.acc_info_entry_frame, width = 30)
        self.acc_entry.grid(padx = 20, pady = 10, row = 0, column = 1)
        self.acc_label.grid(padx = 20, pady = 10, row = 0, column = 0)
        ##____________pw_entry_________________
        self.pw_entry = tk.Entry(master = self.acc_info_entry_frame, width = 30 )
        self.pw_label = tk.Label(master = self.acc_info_entry_frame ,text = 'Pass Word:')
        self.pw_entry.grid(padx = 20,  pady = (5,10), row = 1, column = 1)
        self.pw_label.grid(padx = 15, pady = (5,10), row = 1, column = 0)
        
        
        #___________login_btn_________________
        self.login_btn_frame = tk.Frame(master = self.frame_Lower )#, bg = 'red' )
        self.login_btn_frame.configure(height = 50,width = 1000)
        self.login_btn_frame.pack( ipady = 0, ipadx = 50, expand = 1)
        
        self.img_login = ImageTk.PhotoImage(Image.open(self.cwd + "/Pictures/new_button_login.ico"))
        
        self.login_btn = tk.Button(master = self.login_btn_frame ,image = self.img_login , command = self.gpk_login)
        self.login_btn.grid(row = 1, column = 4)
        
        #___________Remember_Me_Check_Box___________
        self.remember = tk.IntVar()
        self.remember.set(int(self.cache.Re_status()))
        self.rmchbox = tk.Checkbutton(self.login_btn_frame,variable = self.remember,
                                      onvalue=1, offvalue=0)
        self.rmchbox.grid(row = 0, column = 3)
        self.rmchbox.configure( command = lambda: self.cache.Set_status(self.remember.get()) )
        self.rmchbox_label = tk.Label (self.login_btn_frame,text = "Remember Me").grid(row = 0, column = 4)
        
        #__________Register__________________
        self.reg_btn_frame = tk.Frame( self.frame_Lower)#, bg = 'green' )
        self.reg_btn_frame.configure(height = 50,width = 500)
        self.reg_btn_frame.pack(padx = 100,side = tk.LEFT, ipady = 10, ipadx = 50, expand = 0)
        self.register_btn = tk.Button(master = self.reg_btn_frame ,text = 'Register', command = self.gpk_reg)
        self.register_btn.pack(side = tk.LEFT)#grid( row = 0 , column = 0, columnspan = 1)
        self.version_label = tk.Label(master = self.reg_btn_frame ,
                                     text = """
                                                                                                                  Version: 0.01
                                            """ ).pack(pady = 10, padx = 100, side = tk.RIGHT)#grid(padx = 100, row = 0, column = 5, columnspan = 5)
        


# In[4]:


def df_to_Treeview(master, data:pd.core.frame.DataFrame, col_width = 120,col_minwidth = 25,col_anchor = tk.CENTER
              ,LABEL = False) :
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
        data_i = list(data.loc[row,])
        my_tree.insert(parent = "", index = 'end', iid = iid, text = label_text, values = data_i)
        iid += 1

    return my_tree    


# In[12]:


class gpk_Main():
    def __init__(self,Profile,file_path):
        self.Profile = Profile
        self.file_path = file_path
        self.gpk_main_rt = tk.Tk()
        self.gpk_main_rt.option_add('*tearOff', False)
        self.gpk_main_rt.title("GPK_Main")
        base = 100
        width = base*16
        height = base*9
        self.geometry = {'width':width,'height':height}
        self.gpk_main_rt.geometry('{}x{}'.format(width,height))
        self.FRAMES = []
        
        #_________Finally_________#
        self._draw()
        self.gpk_main_rt.mainloop()
        
    def profile_save(self):
        self.Profile.Save(self.file_path)
        
    def Profile_call_back(self, Profile = None, Update = False, Return = False):
        """
        Interact with subFrames and modify the Profile in the Main APP.
        Toggle Return to Get Profile 
        input Profile and Toggle update to update Profile
        """
        if Update:
            self.Profile = Profile #Update the Profile
            self.profile_save()
        elif Return:
            return self.Profile 
        else:
            pass
    

    def call_frame(self, frame_name):
        self.hide_all_frames(frame_name)
        getattr(self,frame_name).pack(fill = tk.BOTH,expand = 1)
    
    def hide_all_frames(self, exception):
        "Clears the Page for other Frames"
        for frame in self.FRAMES:
            if frame != exception:
                getattr(self,frame).pack_forget()
                
        
    
    def _draw(self):
        #++++++++++++++++++++++++++ＭＥＮＵ++++++++++++++++++++++++++++++++++++++#
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.gpk_main_rt)
        self.gpk_main_rt['menu'] = menu_bar
        #_________________Menu->Today________________________
        menu_today = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_today, label='Today')
        menu_today.add_command(label='To_Do_List', command = lambda: self.call_frame('gpk_todo'))

        self.gpk_todo = gpk_to_do(self.gpk_main_rt,self.geometry,callback = self.Profile_call_back)
        self.FRAMES.append("gpk_todo")
        
        #_________________Menu->WEEK________________________
        menu_Week = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_Week, label='Week')
        menu_Week.add_command(label='Week Planning', command = lambda: self.call_frame('gpk_week'))
        
        self.gpk_week = gpk_week(self.gpk_main_rt)
        self.FRAMES.append("gpk_week")
        #_________________Menu->STORE________________________
        menu_Store = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_Store, label='Store')
        menu_Store.add_command(label='Store', command = lambda: self.call_frame('gpk_store'))
        
        self.gpk_store = gpk_store(self.gpk_main_rt)
        self.FRAMES.append("gpk_store")
        #_________________Menu->ANALYSIS________________________
        menu_Analysis = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_Analysis, label='Analysis')
        menu_Analysis.add_command(label='Statistics', command = lambda: self.call_frame('gpk_analysis'))
        
        self.gpk_analysis = gpk_analysis(self.gpk_main_rt)
        self.FRAMES.append("gpk_analysis")
        #_________________Menu->OKR________________________
        menu_OKR = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_OKR, label='OKR')
        menu_OKR.add_command(label='OKR Settings', command = lambda: self.call_frame('gpk_okr'))
        
        self.gpk_okr = gpk_okr(self.gpk_main_rt)
        self.FRAMES.append("gpk_okr")
        
        #_________________Menu->MeisterTask Add on________________
        MTK = tk.Menu(menu_bar) 
        menu_bar.add_cascade(menu=MTK, label='MTK Sync')
        MTK.add_command(label='Authentication Setting', command = lambda: self.call_frame('gpk_mtk_frame'))
    
        self.gpk_mtk_frame = gpk_mtk_frame(self.gpk_main_rt,call_back = self.Profile_call_back)
        self.FRAMES.append("gpk_mtk_frame")
        
        #_________________Menu->DashBoard________________________
        DashBoard = tk.Menu(menu_bar)#, postcommand = lambda: self.call_frame('gpk_dash_board'))
        menu_bar.add_cascade(menu=DashBoard, label='DashBoard')
        DashBoard.add_command(label='HOME', command = lambda: self.call_frame('gpk_dash_board'))

        
        #++++++++++++++++++++++++++DashBoard(HOME)++++++++++++++++++++++++++++++++++++++#
        self.gpk_dash_board = gpk_dash(self.gpk_main_rt,self.geometry,callback = self.Profile_call_back)
        self.gpk_dash_board.pack(fill = tk.BOTH,expand = 1)
        self.FRAMES.append("gpk_dash_board")
        
        test_btn = tk.Button(master =self.gpk_dash_board  ,text = 'WELCOME')
        test_btn.pack()


# In[13]:

class gpk_mtk_frame(tk.Frame):
    def __init__(self,root,call_back=None):
        super().__init__(bg = 'purple')
        self.root = root
        self.call_back = call_back 
        self.Profile = self.call_back(Return = True)
        self._draw()
        
    def _draw(self):
        self.Key_label = tk.Label(master = self,text = 'Personal access tokens:')
        self.Key_entry = tk.Entry(master = self)
        self.submit_btn = tk.Button(master = self, text = 'Save', 
                               command = lambda: self.set_token(self.Key_entry.get()) )
        #Packing...
        self.Key_label.pack()
        self.Key_entry.pack()
        self.submit_btn.pack()
        self.update_token()
    
    def update_token(self):
        self.get_token()
        self.Key_entry.delete(0,tk.END)
        self.Key_entry.insert(0,self.token)
        
    def get_token(self):
        self.Profile = self.call_back(Return = True)
        try:
            self.token = self.Profile.mtk_token 
        except AttributeError as e:
            print("Token not found at the current profile")
    
    def set_token(self,token):
        self.Profile = self.call_back(Return = True)
        self.token = token 
        self.Profile.mtk_token = token 
        self.call_back(Profile = self.Profile,Update = True)
    
class gpk_okr(tk.Frame):
    def __init__(self,root):
        super().__init__(bg = 'black')
        self.root = root
        self._draw()
        
    def _draw(self):
        self.to_dos = tk.Button(master = self, text = 'WELCOME　to gpk_week')
        self.to_dos.pack()


# In[14]:


class gpk_dash(tk.Frame):
    def __init__(self,root,geometry,callback  = None):
        super().__init__(bg = 'green')
        self.root = root
        self.callback = callback
        self.height = geometry['height']
        self.width = geometry['width']
        self._draw()
        
    def _draw(self):
        #___________LeftFrame______________#
        self.LeftFrame = tk.Frame(master = self, bg = 'red')
        self.LeftFrame.config(width = self.width/2, height = self.height)
        self.LeftFrame.pack(side = tk.LEFT)
        #___________RightFrame______________#
        self.to_dos = tk.Button(master = self, text = 'WELCOME　to gpk_okr')
        self.to_dos.pack()


class gpk_to_do(tk.Frame):
    def __init__(self,root,geometry,callback  = None):
        super().__init__()
        self.root = root
        self.callback = callback
        self.height = geometry['height']
        self.width = geometry['width']
        self._draw()
        
    def Main_Profile(self):
        if self.callback is not None:
            return self.callback(Return = True)
        
    def todo_tree_update(self):
        try:
            self.treeview.destroy()
        except:
            pass
        Profile = self.Main_Profile()
        self.treeview = df_to_Treeview(master=self.treeFrame, data = Profile.todos.todos)
        self.treeview.pack(pady = 20)
        self.treeview.bind("<<TreeviewSelect>>", self.node_select)
        
    def node_select(self,event = None):
        self.tree_index = int(self.treeview.selection()[0]) 
        self.task_info_update() # "Update the Enties of Task info based on tree index"
        
    def set_text_entry(self, text:str):
        self.description_editor.delete('1.0',tk.END)
        self.description_editor.insert(tk.END, text)
    
    def get_text_entry(self) -> str:
        return self.description_editor.get('1.0', 'end').rstrip()
    
    def entry_clear(self):
        if True:
            self.Id_entry.delete(0, 'end')

            self.name_entry.delete(0, 'end')

            self.time_entry.delete(0, 'end')

            self.Dif_entry.delete(0, 'end')
            
            self.deadline_entry.delete(0, 'end')
            
            self.set_text_entry("")
        
    def task_info_update(self):
        "Update the Enties of Task info based on tree index"
        Profile = self.Main_Profile()
        
        self.entry_clear()
        
        ID = Profile.todos.todos['ID'][self.tree_index]
        
        self.Id_entry.insert(tk.END, ID)

        self.name_entry.insert(tk.END, Profile.todos.todos['TaskName'][self.tree_index])

        self.time_entry.insert(tk.END, Profile.todos.todos['Time(H)'][self.tree_index])

        self.Dif_entry.insert(tk.END, Profile.todos.todos['Difficulty'][self.tree_index])
        
        self.deadline_entry.insert(tk.END, str(Profile.todos.todos['Deadline'][self.tree_index]) )
        
        self.set_text_entry(Profile.todos.task_descriptions[ID] )
        
    def submit(self):
        #1.Save file
        ID = self.Id_entry.get()
        Name =  self.name_entry.get()
        Time = float(self.time_entry.get())
        Diff = float(self.Dif_entry.get())
        ddl  = self.deadline_entry.get()
        Description = self.get_text_entry()
        
        #1.5:Update File
        Profile_temp = self.Main_Profile()
        Profile_temp.todos.delete("S_G0-0_K0")
        Profile_temp.todos.edit(Name,ID,Time,Diff,Description,ddl)
        self.callback(Profile = Profile_temp, Update = True)
        #2.Reload Tree
        self.todo_tree_update()
        #3.Update Summary
        self.todo_summary()
    
    def add(self):
        #1.Create a New Task
        Profile_temp = self.Main_Profile()
        Profile_temp.todos.delete("S_G0-0_K0")
        Profile_temp.todos.add(task_name="",task_ID="S_G0-0_K0",task_time=0,task_diff=0 ,task_des="")
        self.callback(Profile = Profile_temp, Update = True)
        #2.Update the Tree Index
        self.todo_tree_update()
        self.tree_index = len(self.treeview.get_children())-1
        self.task_info_update() 
        #5.Update Summary
        self.todo_summary()
        
    def delete(self):
        #1.Get ID
        ID = self.Id_entry.get()        
        #2.Fetch Profile
        Profile_temp = self.Main_Profile()
        #3.Delete Task
        Profile_temp.todos.delete(ID)
        self.callback(Profile = Profile_temp, Update = True)
        #4.Update Tree
        self.todo_tree_update()
        #5.Update Summary
        self.todo_summary()
        
        
    def complete(self):
        #1.Get ID
        ID = self.Id_entry.get()
        #2.Fetch Profile
        Profile_temp = self.Main_Profile()
        #3.Complete Task
        Profile_temp.todos.complete(ID)
        self.callback(Profile = Profile_temp, Update = True)
        #4.Update Tree
        self.todo_tree_update()
        #5.Update Summary
        self.todo_summary()
        
        
    def todo_summary(self):
        Profile_temp = self.Main_Profile()
        time_tot = sum(Profile_temp.todos.todos['Time(H)'])
        reward_tot = sum(Profile_temp.todos.todos['Reward'])
        try:
            self.summary_label.destroy()
        except:
            pass
        self.summary_label = tk.Label(master = self.summaryFrame, text = 
                                     """
                                Total Rewards:  {}
                                Total Time:     {}
                                     """.format(reward_tot,time_tot), font = 10)
        self.summary_label.grid(row = 0, column = 0, padx = 150)
    
    def _draw(self):
        ###Upper Frame###
        self.FrameUPPER = tk.Frame(master = self, bd = 20)#, bg = 'Blue')
        self.FrameUPPER.configure(height = 4*self.height/5 ,width = self.width)
        self.FrameUPPER.pack( )
        #____Tree View_Frame___
        self.tree_height_coef = 4/5 
        self.tree_width_coef = 2/3
        self.treeFrame = tk.Frame( master = self.FrameUPPER, bd = 30)#, bg = 'green')
        self.treeFrame.configure(height = self.tree_height_coef*self.height,
                                  width = self.tree_width_coef*self.width)
        self.treeFrame.grid_propagate(0)
        self.treeFrame.pack(side = tk.LEFT)
        #GET Tree#
        self.todo_tree_update()
        #____Editing_Frame___
        self.editingFrame = tk.Frame(master = self.FrameUPPER, bd = 10)#, bg = 'Yellow')
        self.editingFrame.configure(height = 1/2*self.height ,
                                    width = (1-self.tree_width_coef)*self.width)
        self.editingFrame.grid_propagate(0)
        self.editingFrame.pack(side = tk.LEFT)
        #
        self.Id_label = tk.Label(master = self.editingFrame, text = 'Task-ID:')
        self.Id_entry = tk.Entry(master = self.editingFrame )
        
        self.name_label = tk.Label(master = self.editingFrame, text = 'Task-Name:')
        self.name_entry = tk.Entry(master = self.editingFrame )
        
        self.time_label = tk.Label(master = self.editingFrame, text = 'Time in Hours:')
        self.time_entry = tk.Entry(master = self.editingFrame )
        
        self.Dif_label = tk.Label(master = self.editingFrame, text = 'Difficulty 1 to 10:')
        self.Dif_entry = tk.Entry(master = self.editingFrame )
        
        self.deadline_label = tk.Label(master = self.editingFrame, text = 'Deadline:')
        self.deadline_entry = tk.Entry(self.editingFrame)
        
        self.description_editor_label =  tk.Label(master = self.editingFrame, text = 'Description:')
        self.description_editor = tk.Text(self.editingFrame, width=0)
        
        
        # self.spacer = tk.Label(master = self.editingFrame, text = '')
        # self.spacer.grid(row = 0, pady = 120,column = 0 , columnspan = 2)
        base = 1
        self.Id_label.grid(padx = 5, pady = 10, row = base + 0, column = 0)
        self.Id_entry.grid(padx = 5, pady = 10,row = base +0, column = 1)
        self.name_label.grid(padx = 5, pady = 10,row = base +1, column = 0)
        self.name_entry.grid(padx = 5, pady = 10,row =base + 1, column = 1)
        self.time_label .grid(padx = 5, pady = 10,row = base +2, column = 0)
        self.time_entry.grid(padx = 5, pady = 10,row = base +2, column = 1)
        self.Dif_label.grid(padx = 5, pady = 10,row = base +3, column = 0)
        self.Dif_entry.grid(padx = 5, pady = 10,row = base +3, column = 1)
        self.deadline_label.grid(padx = 5, pady = 10,row = base +4, column = 0)
        self.deadline_entry.grid(padx = 5, pady = 10,row = base +4, column = 1)
        
        self.description_editor_label.grid(padx = 5, pady = 15,row = base +5, column = 0)
        self.description_editor.grid(row = base +6, column = 0, columnspan = 3, ipadx=200, pady=5)
            
        ###Lower Frame### (Middle) 
        self.FrameLOWER = tk.Frame(master = self, bd = 2)#, bg = 'Red')
        self.FrameLOWER.configure(height = self.height/2 ,width = self.width)
        self.FrameLOWER.pack( )
        #____Summary_Frame___
        self.summaryFrame = tk.Frame(master = self.FrameLOWER, bd = 2)#, bg = 'Orange')
        self.summaryFrame.configure(height = self.height/2 , width = (54/100)*self.width)
        self.summaryFrame.grid_propagate(0)
        self.summaryFrame.pack(side = tk.LEFT)
        self.todo_summary()
        
        #____Buttons_Frame___
        self.controlFrame = tk.Frame(master = self.FrameLOWER,  bd = 2)#,bg = 'Purple')
        self.controlFrame.configure(height = self.height/2 ,width = (46/100)*self.width)
        self.controlFrame.grid_propagate(0)
        self.controlFrame.pack(side = tk.LEFT )
        # 
        self.spacer2 = tk.Label(master =self.controlFrame)
        self.img_submit = ImageTk.PhotoImage(Image.open(os.getcwd() + "/Pictures/sumbit_icon_p8d_icon.ico"))
        self.Submit_btn = tk.Button(bd = 2, master =self.controlFrame, image =  self.img_submit, command = self.submit)
        self.img_add = ImageTk.PhotoImage(Image.open(os.getcwd() + "/Pictures/add_task_GGR_icon.ico"))
        self.Add_btn = tk.Button(master =self.controlFrame, image = self.img_add, command = self.add)
        self.img_del = ImageTk.PhotoImage(Image.open(os.getcwd() + "/Pictures/delete_task_li6_icon.ico"))
        self.Delete_btn = tk.Button(master =self.controlFrame, image = self.img_del, command = self.delete)
        self.img_complete = ImageTk.PhotoImage(Image.open(os.getcwd() + "/Pictures/111.png"))
        self.Complete_btn = tk.Button(master =self.controlFrame, image  =  self.img_complete , command = self.complete)
        #Set Location for the buttons 
        self.spacer2.grid(padx = 160, row = 0 ,column = 0 )
        self.Submit_btn.grid(padx = 20, row = 0, column = 3)
        self.Add_btn.grid(padx = 20,row = 0, column = 2)
        self.Delete_btn.grid(padx = 20,row = 0, column = 1)
        self.Complete_btn.grid(pady = 20, ipadx  =50, row = 1, column = 1,columnspan = 3)
        
        #Add Mtk Sync Status 
        self.sync_status = tk.IntVar()
        self.sync_chbx = tk.Checkbutton(self.controlFrame, variable =self.sync_status,
                                        onvalue=1, offvalue=0)
        self.sync_chbx.grid(padx = 20,row = 2, column = 1)
        self.rmchbox_label = tk.Label (self.controlFrame,text = "MTK SYNC")
        self.rmchbox_label.grid(row = 2, column = 2)
        

class gpk_week(tk.Frame):
    def __init__(self,root):
        super().__init__(bg = 'purple')
        self.root = root
        self._draw()
        
    def _draw(self):
        self.to_dos = tk.Button(master = self, text = 'WELCOME　to gpk_week')
        self.to_dos.pack()


# In[17]:


class gpk_store(tk.Frame):
    def __init__(self,root):
        super().__init__(bg = 'orange')
        self.root = root
        self._draw()

    def Tetris_start(self):
        self.Tetris = Tetris.Tetris(master = self)
        self.Tetris.start_game()
        
        
    def _draw(self):
        #Button
        self.Tetris_open = tk.Button(master = self, text = 'Tetris',command = self.Tetris_start)
        self.Tetris_open.pack()

# In[18]:


class gpk_analysis(tk.Frame):
    def __init__(self,root):
        super().__init__(bg = 'blue')
        self.root = root
        self._draw()
        
    def _draw(self):
        self.to_dos = tk.Button(master = self, text = 'WELCOME　to gpk_analysis')
        self.to_dos.pack()


# In[ ]:


if __name__ == "__main__":
    test = gpk_Shell()
