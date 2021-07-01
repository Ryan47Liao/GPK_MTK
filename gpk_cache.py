import pickle 

class GPK_Cache:
    def __init__(self,file_path,AC = None,PW = None):
        self.file_path = file_path
        self.__account = AC 
        self.__password = PW 
        self.__remember = False 
        self.save()
        
    def Re_status(self):
        return self.__remember 
    
    def get_AC(self):
        return self.__account 
    
    def get_PW(self):
        return self.__password 
    
    def save(self):
        OUTfile = open(file_path ,"wb")
        pickle.dump(self,OUTfile)
        OUTfile.close()
        
    def Re_True(self):
        self.__remember = True  
        
    def Re_Fal(self):
        self.__remember = False   