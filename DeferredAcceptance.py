import math
import time
from collections import deque
import heapq as hq
import random


def generate_preferences(n, sigma):
  sigma = sigma * n / 2
  pref = [sorted([(random.gauss(j, sigma), j) for j in range(n)]) for i in range(n)]
  return pref


def GSDA(m_pref, w_pref, m):
  men = [Person(i, preferences) for i, preferences in enumerate(m_pref)]
  women = [Person(i, preferences) for i, preferences in enumerate(w_pref)]
    
  #this feels like a kludge here, just stacking all the men m times, but it works?
  available_men = deque(list(range(len(m_pref)))*m)
  while len(available_men):
    #print('start of loop, available men are: ' + str(available_men))
    man = men[available_men.pop()]
    #print("man " + str(man.id) )
    try:
        woman = women[man.preference_queue.pop()[1]]
    except IndexError:
        #print('Man ' + str(man.id) + ' is out of options')
        continue
    #print( " proposes to woman " + str(woman.id) + " who holds " + str([man[1].id for man in woman.held])) 
    if (woman.preferences[man.id], man) in woman.held:
        available_men.append(man.id)
        print("man " + str(man.id) + " is a duplicate")
    else:
        if len(woman.held) < m:
          # print('woman', woman.id, 'does not have a fiancee, so they get engaged')
          hq.heappush(woman.held , (woman.preferences[man.id], man))
        else:
          # i feel like this variable should have a different name
          rejectedMan = hq.heappushpop(woman.held, (woman.preferences[man.id], man))[1]
          available_men.append(rejectedMan.id)
          #print(str(rejectedMan.id) + " is rejected")
    #print('matching is: ' + str([(woman.id, [heldMan[1].id for heldMan in woman.held]) for woman in women]))
  # print("No more people to propose")
  return [(woman.id, [heldMan[1].id for heldMan in woman.held]) for woman in women]

class Person:
  def __init__(self, id, preferences):
    self.id = id
    self.n = len(preferences)
    self.held = []
    self.preference_queue = deque(preferences)
    self.preferences = dict([(j, i) for i, j in preferences])
    
