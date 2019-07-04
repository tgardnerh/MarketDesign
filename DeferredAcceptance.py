#Define the classes and functions for the gale-shaply simulation
#https://jeremykun.com/2014/04/02/stable-marriages-and-designing-markets/

class Suitor(object):
   def __init__(self, id, prefList):
      self.prefList = prefList
      self.rejections = 0 # num rejections is also the index of the next option
      self.id = id
 
   def preference(self):
      return self.prefList[self.rejections]
 
   def __repr__(self):
      return repr(self.id)
    
class Suited(object):
    def __init__(self, id, prefList):
      self.prefList = prefList
      self.held = None
      self.currentSuitors = set()
      self.id = id

    def __repr__(self):
      return repr(self.id)

    def reject(self):
       if len(self.currentSuitors) == 0:
          return set()

       if self.held is not None:
          self.currentSuitors.add(self.held)
       unacceptable = set(filter(lambda suitor: suitor.id not in self.prefList, self.currentSuitors))
       self.currentSuitors = self.currentSuitors - unacceptable 
       if len(self.currentSuitors) > 0 :
           self.held = min(self.currentSuitors, key=lambda suitor: self.prefList.index(suitor.id))
       rejected = self.currentSuitors - set([self.held]) 
       rejected |= unacceptable
       self.currentSuitors = set()

       return rejected
    
# GSDA: [Suitor], [Suited] -> {Suitor -> Suited}
# construct a stable (monogamous) marriage between suitors and suiteds
def GSDA(suitors, suiteds):
   unassigned = set(suitors)
 
   while len(unassigned) > 0:
      for suitor in unassigned:
            next_proposal = suitor.preference()
            if next_proposal != None:
                suiteds[suitor.preference()].currentSuitors.add(suitor)
      unassigned = set()
      for suited in suiteds:
         unassigned |= suited.reject()


      for suitor in unassigned:
        suitor.rejections += 1
 
   return dict([(suited.held, suited) for suited in suiteds])

# verifyStable: [Suitor], [Suited], {Suitor -> Suited} -> bool
# check that the assignment of suitors to suited is a stable marriage
def verifyStable(suitors, suiteds, marriage):
   import itertools
   suitedToSuitor = dict((v,k) for (k,v) in marriage.items())
   precedes = lambda L, item1, item2: L.index(item1) < L.index(item2)
 
   def suitorPrefers(suitor, suited):
      return precedes(suitor.prefList, suited.id, marriage[suitor].id)
 
   def suitedPrefers(suited, suitor):
      return precedes(suited.prefList, suitor.id, suitedToSuitor[suited].id)
 
   for (suitor, suited) in itertools.product(suitors, suiteds):
      if suited != marriage[suitor] and suitorPrefers(suitor, suited) and suitedPrefers(suited, suitor):
         return False, (suitor.id, suited.id)
 
   return

