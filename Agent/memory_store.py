import json
from pathlib import Path
from datetime import datetime

class MemoryStore:
    def __init__(self):
        self.state={}
        self.conversation_history=[]
        self.execution_log=[]
        self.created_at=datetime.now().isoformat()
    
    def store(self,key,value):
        self.state[key]=value
    
    def get(self,key,default=None):
        return self.state.get(key,default)
    
    def add_conversation(self,user_msg,agent_msg):
        self.conversation_history.append({
            'timestamp':datetime.now().isoformat(),
            'user':user_msg,
            'agent':agent_msg
        })
    
    def log_execution(self,step,code,result):
        self.execution_log.append(
            {
                'timestamp':datetime.now().isoformat(),
                "step":step,
                'code':code,
                'result':result
            }
        )
    
    def save(self,file_path):
        data={
            'created_at':self.created_at,
            'state':self.state,
            'conversations':self.conversation_history,
            'executions':self.execution_log
        }

        with open(file_path,'w') as f:
            json.dump(data,f,indent=2)
        
        print(f"Memory saved at{file_path}")
    
    def load(self,file_path):
        with open(file_path) as f:
            data=json.load(f)
        
        self.created_at=data.get('created_at')
        self.state=data.get('state')
        self.conversation_history=data.get('conversations')
        self.execution_log=data.get('executions',[])

