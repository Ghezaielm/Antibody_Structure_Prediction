##### Monitor methods s##################################
# Methods: timer (wrapper to monitor execution time)
########################################################

class monitor():
    
    def __init__(self): 
        pass
    
    @staticmethod
    def timer(func):           
        def wrapper(self,*args,**kwargs):
            start = time.time()
            
            print('\n')
            print("###",func.__name__)
            func(self,*args,**kwargs)
            print("Elapsed time = {} seconds".format(round(time.time()-start)))
            print('\n')
        return wrapper
    
    @staticmethod
    def memoryUsage(func):           
        def wrapper(self):
            func(self)
            process = psutil.Process(os.getpid())
            print("% memory: {}".format(round(process.memory_percent(),2)),"\n")
        return wrapper
  
