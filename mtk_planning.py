from GPK_MTK import GPK_MTK
from gpkTask import gpk_task
from Plan_load import Load
from gpkTask import gpk_task
from time import sleep

class GPK_MTK_Plan(GPK_MTK):
    def __init__(self,plan_path,api_token,project_id = 'Null',Post = False,nap = 1):
        self.Load = Load(plan_path)
        self.Load.get_week_objective()
        GPK_MTK.__init__(self,api_token,project_id)
        print(f"GPK_MTK Initialized with Project_id:{project_id}")
        sleep(nap)
        if project_id == 'Null':
            #Create Project and Settings 
            self.RESET(name = 'OKR_Plannng',
                       sections = ['Inbox','monday','tuesday','wednesday',
                                  'thursday','friday','saturday','sunday'], 
                  colors = ['orange','red','grass green','turquoise','purple','grass green',
                           'orange','blue'],
                  features = ["enable_timetracking","enable_taskrelationships"])
        self.Sync()
        print('GPK Sync Complete')
        if Post:
            sleep(nap)
            print("Posting All Tasks from the Loaded Plan")
            self.Post_All() #Post all Scheduled Task into the meistertask Planner 
              
    def Incubent_tasks(self):
        df = self.View_df('Inbox')
        if len(df) == 0 :
            return []
        tasks = []
        for idx in df.index:
            try:
                tsk = gpk_task(df.loc[idx]['name'],df.loc[idx]['notes'])
                tasks.append(tsk)
            except Exception as e:
                print(f"Fail to include task:{df.loc[idx]}\n due to Exception{e}")
        return [task.ID for task in tasks]
        
    def Post_All(self):
        sec_id = self.Get_Sec_ID('Inbox')
        Incubent_tasks = set(self.Incubent_tasks())
        for category in ['Priority_Task','Special_Task']:#Recursive_Task are Irrelevant
            List_of_objectives = eval(f"self.Load.WeekObjective.{category}")
            for Obj in List_of_objectives:
                O_id = Obj.Objective.split(':')[0]
                for Kr_id in Obj.KeyResults:
                    task_name,task_obj = Obj.KeyResults[Kr_id][0],Obj.KeyResults[Kr_id][1]
                    #S_G4-3_K1
                    task_id = category[0] + '_' + Obj.Objective.split(':')[0] + '_' + Kr_id
                    if task_id not in Incubent_tasks:
                        note_og = f" ID:{task_id}\n\n[Reward]\n{task_obj.reward}\n[Time]\n\
                        {task_obj.time}\n[Difficulty]\n{task_obj.difficulty}\n\
                        [Description]\n{task_obj.description}"
                        #Change Notes Appearance 
                        try:
                            g_task = gpk_task(task_name,note_og)
                            note = g_task.Get_notes()
                            #Post the Task:
                            self.Post_task(sec_id,task_name,note)
                            print(f'task {task_id} posted')
                        except Exception as e:
                            print(f"Fail to POST task:{task_name,note_og}\n\n due to Exception{e}")
                            print("PLEASE WAIT for 3 sec")
                            sleep(3)
                            try:
                                self.Post_task(sec_id,task_name,note)
                            except Exception as e:
                                print(f"Unable to POST task {task_name,note_og}")
        
        print(f'All Tasks were Sent to Project {self.project_id}')

        
    def Task_today(self):
        "Return a data frame of the tasks of today"
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
        
        if self.PROJECTs[int(self.project_id)] == 'OKR_Plannng':
            weekday = list(self.SECTIONs.values())[weekday_today()]
            self.Sync()
            return self.View_df(weekday)
        else:
            if 'OKR_Plannng' in self.PROJECTs.values():
                for project_id,pro_name in self.PROJECTs.items():
                    if pro_name == 'OKR_Plannng':
                        self.set_project_id(project_id) #Try to Set Project ID
                self.Task_today()
            else:
                print("ERROR,OKR_Planning Project Set_UP Required")
                    
if __name__ == '__main__':
    test = GPK_MTK_Plan(plan_path='OKRLOG_S3_W1.docx',
                        api_token='u1IqrMvqjFA99sNL9_RnipaYnXKd9cc7wUZXHCUhJ-I',
                        project_id= '6277887', Post= False)
    df = test.Task_today()
    tasks = [gpk_task(df.loc[idx]['name'],df.loc[idx]['notes']) for idx in df.index]
    print(tasks)
    print("DONE")
        