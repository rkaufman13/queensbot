import gymnasium, time
from gymnasium import error, spaces, utils
from gymnasium.utils import seeding
import random
from points import get_points
import numpy as np



class QueensEnv(gymnasium.Env):
  metadata = {'render.modes': ['human']}
  def __init__(self):
    super(gymnasium.Env, self).__init__()
    self.game = np.zeros(shape=(8,8))
    self.x = random.randint(0,7)
    self.y = random.randint(0,7)
    self.action_space = spaces.Discrete(5,)

  def step(self, action):
    
    reward = 1
    win = False
  
    if action==0:
      value = self.game[self.y][self.x]
      if value==0:
        self.game[self.y][self.x]=1
      else:
        self.game[self.y][self.x]=0
      reward+= get_points(self.game)[0]
      win=get_points(self.game)[1]
      
    elif action==1:
      self.y = self.clamp(self.y-1, 0, 7)
      reward+= get_points(self.game)[0]
      win=get_points(self.game)[1]
    
    elif action==2:
      self.x = self.clamp(self.x+1,0,7)
      reward+= get_points(self.game)[0]
      win=get_points(self.game)[1]
    
    elif action==3:
      self.y = self.clamp(self.y+1,0,7)
      reward+= get_points(self.game)[0]
      win=get_points(self.game)[1]

    elif action==4:
      self.x = self.clamp(self.x-1,0,7)
      reward+= get_points(self.game)[0]
      win=get_points(self.game)[1]
    
    return self.game,reward,win, []
  def reset(self):
    self.game = np.zeros(shape=(8,8))
    self.x = random.randint(0,7)
    self.y = random.randint(0,7)
    return self.game
  def render(self, mode='human', close=False):
    for line in self.game:
        print(line)
    print(" ")
  def get_action_meanings(self):
    return {0: 'Flip square', 1: 'Move up', 2: 'Move right', 3: 'Move down', 4: 'Move left'}
  def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)
  



env = QueensEnv()
obs = env.reset()
steps = 0
while steps <100000:
  action = env.action_space.sample()
  obs, reward, win, info = env.step(action)
  env.render()
  if steps % 1000 == 0:
    print(reward, win)
    time.sleep(2)
  if win == True:
    break
  steps+=1

env.close()