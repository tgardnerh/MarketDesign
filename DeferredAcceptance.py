import math
import time
from collections import deque
import heapq as hq

def GSDA(m_pref, w_pref, m):
  men = [Person(i, preferences) for i, preferences in enumerate(m_pref)]
  women = [Person(i, preferences) for i, preferences in enumerate(w_pref)]
    
  #this feels like a kludge here, just stacking all the men m times, but it works?
  available_men = deque(list(range(len(m_pref)))*m)
  while len(available_men):
    man = men[available_men.pop()]
    woman = women[man.preference_queue.pop()[1]]
    # print('man', man.id, "proposes to", 'woman', woman.id)
    if len(woman.held) < m:
      # print('woman', woman.id, 'does not have a fiancee, so they get engaged')
      hq.heappush(woman.held , (woman.preferences[man.id], man))
      hq.heappush(man.held , (man.preferences[woman.id], woman))
    else:
      # i feel like this variable should have a different name
      rejectedMan = hq.heappushpop(woman.held, (woman.preferences[man.id], man))[1]
      available_men.append(rejectedMan.id)
    
  # print("No more people to propose")
  return [(woman.id, [heldMan[1].id for heldMan in woman.held]) for woman in women]

class Person:
  def __init__(self, id, preferences):
    self.id = id
    self.n = len(preferences)
    self.held = []
    self.preference_queue = deque(preferences)
    self.preferences = dict([(j, i) for i, j in preferences])
    
