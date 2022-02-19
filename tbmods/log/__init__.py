class Log:
    
    def __init__(self,app):
        self.app = app
        
    def error(self,msg):
        print("ERROR:     {} - {}".format(self.app,msg))
        
    def warning(self,msg):
        print("WARNING:     {} - {}".format(self.app,msg))
        
    def info(self,msg):
        print("INFO:     {} - {}".format(self.app,msg))