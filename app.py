import sys
from operator import attrgetter

class Task:
  def __init__(self, input):
    self.name, self.priority, self.start, self.length = str(input).split(",")
    self.priority = int(self.priority)
    self.start = int(self.start)
    self.length = int(self.length)
    self.remaining = self.length
    self.waiting = 0

  def wait(self):
    self.waiting += 1

  def run(self):
    self.remaining -= 1


class RoundRobin:
  def __init__(self, scheduler):
    self.ran = 0
    self.slice = 2
    self.activeTask = None
    self.scheduler = scheduler
    self.queue = []

  def add(self, task):
    self.queue.append(task)

  def checkEmpty(self):
    return (len(self.queue) == 0 and self.activeTask == None)

  def tick(self):
    if self.checkEmpty(): return

    self.ran += 1
    
    if len(self.queue) > 0 and self.ran == self.slice:
      if self.activeTask != None:
        self.queue.append(self.activeTask)
      self.activeTask = self.queue.pop(0)
      self.scheduler.change(self.activeTask)
      self.ran = 0

    if len(self.queue) > 0 and self.activeTask == None:
      self.activeTask = self.queue.pop(0)
      self.scheduler.change(self.activeTask)
      self.ran = 0
    
    if self.ran == self.slice: self.ran = 0
    for task in self.queue: task.wait()
    
    if self.activeTask != None:
      self.activeTask.run()
      if self.activeTask.remaining == 0: 
        self.activeTask = None

class ShortestRemainingTimeFirst:
  def __init__(self, scheduler):
    self.scheduler = scheduler
    self.activeTask = None
    self.active = False
    self.isSwap = False
    self.ran = 0
    self.list = []
    
  def start(self):
    self.active = True
    if self.activeTask == None:
      self.isSwap = True

  def stop(self):
    self.active = False
    self.ran = 0
    if self.activeTask != None:
      self.list.append(self.activeTask)
    self.activeTask = None

  def add(self, task):
    self.list.append(task)
    if self.activeTask == None or self.activeTask.remaining > task.remaining:
      self.isSwap = True

  def checkEmpty(self):
    return (len(self.list) == 0 and self.activeTask == None)

  def tick(self):
    if not self.active:
      if self.activeTask != None: self.activeTask.wait()
      for task in self.list:
        task.wait()
      return

    if self.isSwap:
      minRemaining = min(self.list, key=attrgetter('remaining'))

      if self.activeTask != None:
          self.list.append(self.activeTask)
      
      self.list.remove(minRemaining)
      self.activeTask = minRemaining

      self.scheduler.change(self.activeTask)
      self.isSwap = False

    self.activeTask.run()
    for task in self.list: task.wait()

    if self.activeTask.remaining == 0:
      self.isSwap = True
      self.activeTask = None

class Scheduler:
  def __init__(self):
    self.strf = ShortestRemainingTimeFirst(self)
    self.rr = RoundRobin(self)
    self.isEmpty = True
    self.result = ""

  def add(self, task):
    self.isEmpty = False
    if task.priority:
      self.rr.add(task)
    else:
      self.strf.add(task)

  def change(self, task):
    self.result += str(task.name)

  def tick(self):
    if self.strf.checkEmpty() and self.rr.checkEmpty():
      self.isEmpty = True
      return

    if not self.rr.checkEmpty():
      self.strf.stop()
    else:
      self.strf.start()
    
    self.rr.tick()
    self.strf.tick()

def main():
  tasks = []
  runningTasks = []
  scheduler = Scheduler()
  for line in sys.stdin:
    line = line.rstrip('\n').rstrip('\r')
    items = line.split(",")
    if len(items) != 4: break
    for index, item in enumerate(items):
      if index == 0 and not item.isalpha(): break
      if index == 1 and int(item) not in [0,1]: break
      if index == 2 and (int(item) < 0): break
      if index == 3 and (int(item) < 1): break
    tasks.append(Task(line))

  counter = 0
  while len(tasks) > 0 or not scheduler.isEmpty:
    if counter == 30: break
    for task in tasks[:]:
      if task.start == counter:
        scheduler.add(task)
        runningTasks.append(task)
        tasks.remove(task)
    scheduler.tick()
    counter += 1

  print(scheduler.result)
  result = ""
  for task in runningTasks:
    result += task.name + ":" + str(task.waiting) + ","
  print(result[:-1])

if __name__ == "__main__":
    main()