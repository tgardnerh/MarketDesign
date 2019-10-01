import math
import time
from collections import deque

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
      woman.held.add(man)
      man.held.add(woman)
    else:
      # i feel like this variable should have a different name
      woman_worst_held = min(woman.held , key = lambda m : woman.preferences[m.id])
      if woman.preferences[man.id] > woman.preferences[woman_worst_held.id]:
        # print("woman", woman.id, 'likes man', man.id, ', better than her fiancee, man', woman.fiancee.id)
        #this add/remove from set business feels kludgy.  Should I be making the breakup process somehow more automated, maybe as a function of the Person object?
        available_men.append(woman_worst_held.id)
        woman.held.remove(woman_worst_held)
        woman_worst_held.held.remove(woman)
        woman.held.add( man)
        man.held.add(woman)
      else:
        available_men.append(man.id)
        # print('woman', woman.id, 'likes her fiancee, man', woman.fiancee.id, 'more than man', man.id)

  # print("No more people to propose")
  return [(man.id, man.held) for man in men]

class Person:
  def __init__(self, id, preferences):
    self.id = id
    self.n = len(preferences)
    self.held = set()
    self.preference_queue = deque(preferences)
    self.preferences = dict([(j, i) for i, j in preferences])
    
