
from Task import Task
from Schedule import Schedule
class CompositeTask(Task):
    
    def __init__(self, id, name, desc, date, duration, startTask, finalTasks, pred, succ, children, resources, deliverables):
    	Task.__init__(self, id, name, desc, date, duration, pred, succ, resources, deliverables)
    	self.children = children
        self.startTask = startTask
        self.finalTasks = finalTasks
        
        
    def setTaskInfo(self, info):
        pass
        
    def getTaskInfo(self):
        pass

    def newtask(self, taskInfo):
        pass
        
    def setFinalTask(self, taskInfo):
        pass
        
    def testing(self):
        return "Testing pass"
    
    def addChildTask(self, task):
        self.children.append(task)
        
    def generateSchedule(self):
        self.schedule = Schedule.entry
        
    def addResource(self, resource):
        self.resources.append(resource)
        
    def addDeliverable(self, deliverable):
        self.deliverables.append(deliverable)
        
#test = CompositeTask(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)
#test.testing()
        
         
