#Define the classes and functions for the gale-shaply simulation
#https://jeremykun.com/2014/04/02/stable-marriages-and-designing-markets/

import random
import numpy as np
import operator
import pickle


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



#make preflists for a side of market:
def preflists(
    n ,
    sigma_fraction ,
    list_length,
    achievability_matrix = None,
    match_threshold = 0
):
    if list_length == None:
        list_length = n
        
    #make randomly assigned preferences
    suitors = [None] * n
    suiteds = [None] * n
    long_suitors = [None] * n
    long_suiteds = [None] * n

    #determine padding length

    #scale sigma
    sigma = sigma_fraction * n /2

    for i in range(0, n):

        utility = [(k, random.normalvariate(k,sigma)) for k in range(0,n)]
        utility.sort(key=operator.itemgetter(1))
        #room for ranked partners, plus a "none" at the end
        ranklist = [None] * (n + 1)
        long_ranklist = [None] * n
        for x in range(n):
            ranklist[x] = utility[x][0]
            long_ranklist[x] = utility[x][0]
        if list_length < n:
            
            #Because list length is the number of objects, but list_bottom is a position
            list_bottom = list_length-1
            
            achievability_vector = [None] * n
            for j in range(0, n):
                
                achievability_vector[j] = 1- achievability_matrix[utility[j][0]][i]
            
            achievability = 1- np.prod(achievability_vector[list_bottom- list_length: list_bottom])
            
            #Notice that these are copy/psted below, because I couldn't get the wile loop to work otherwise
            threshold_condition = achievability  <= match_threshold    
            EoL_condition = list_bottom +1 < n

            while threshold_condition & EoL_condition :
                list_bottom = list_bottom + 1
                EoL_condition = list_bottom +1 < n
                achievability = 1- np.prod(achievability_vector[list_bottom- list_length: list_bottom])
                threshold_condition =achievability  <= match_threshold
            ranklist =   ranklist = [None] *(n + 1)  
            list_top = list_bottom - list_length
            for x in range(list_top + 1,list_bottom +1):
                ranklist[x-(list_top +1)]= utility[x][0]
                
        id =  i
        ranklist = tuple(ranklist)
        long_ranklist = tuple(long_ranklist)
        suiteds[i] = Suited(id, ranklist)
        suitors[i] = Suitor(id, ranklist)
        long_suitors[i] = Suitor(id, long_ranklist)
        long_suiteds[i] = Suited(id, long_ranklist)
        agents = [suitors, suiteds, long_suitors, long_suiteds]
    return agents

#Return matching probability array:
def achiev_mat(
    n ,
    sigma_fract,
    force = False,
    runs = 100
    ):
    try:
        AM_dict = pickle.load(open("AM_dict.pkl", "rb"))
    except FileNotFoundError:
        AM_dict = {}

    
    lookup_str = str(n) + "_" + str(sigma_fract*100)
    achievability_matrix = AM_dict.get(lookup_str)
    
    if np.all(achievability_matrix == None) | force == True:
        simulations = np.array([None]* runs)

        for i in range(0,runs):

            men = preflists(n, sigma_fract, list_length = n)[0]
            women = preflists(n, sigma_fract, list_length = n)[1]
          
            MoSm = GSDA(men, women)
            MoSm_list = [(k, v) for k, v in MoSm.items()] 
            MoSm_list.sort(key = lambda x: x[1].id)

            simulations[i] = np.array([[None]*n]*n)
            for woman in women:
                woman_got_man =  MoSm_list[woman.id][0]
                woman_got_rank = woman.prefList.index(woman_got_man.id)
                counter = 0
                for man in woman.prefList:
                    simulations[i][woman.id,man] =  int(counter <= woman_got_rank)
                    counter = counter + 1    

        achievability_matrix = np.mean(simulations, axis = 0)


        AM_dict.update({lookup_str : achievability_matrix})

        pickle.dump(AM_dict, open(AM_dict, "wb"))
                    
    return achievability_matrix
                    