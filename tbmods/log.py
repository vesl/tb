class Log:
    
    def __init__(self,app):
        self.app = app

    # something goes wrong and execution should stop
    def error(self,msg):
        print("ERROR:     {} - {}".format(self.app,msg))
        raise Exception('Execution aborted')
    
    # something goes wrong and execution should continue
    def warning(self,msg):
        print("WARNING:     {} - {}".format(self.app,msg))
        
    # something interesting happened
    def info(self,msg):
        print("INFO:     {} - {}".format(self.app,msg))