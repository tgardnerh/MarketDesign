#Define the classes and functions for the gale-shaply simulation
#https://jeremykun.com/2014/04/02/stable-marriages-and-designing-markets/
##Bug to fix:
## This relies on suited 0 being in the 0 position of the suited list, rather than referencing suited by their ID
##This could create some very odd behavior, because it doesn't neciscarily throw an error if it isn't true
## one way to fix this is to create a "suiteds" and "suitors" object, perhaps just internally, that is a dictionary 
## with the id as the key.
import random
import numpy as np
import operator
import pickle


class Suitor(object):
   def __init__(self, id, prefList):
      self.prefList = prefList
      self.rejections = 0 # num rejections is also the index of the next option
      self.proposals = 0
      self.id = id
      self.assigned_count = 0
   def preference(self):
      print(str(self.id)+ "th's assigned_count " + str(self.assigned_count) + ", proposal number " + str(self.proposals))
      return self.prefList[self.proposals]
 
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
       #Here we tweak it to loop so that self.held can have more than one element
       if len(self.currentSuitors) > 0 :
           self.held = set()
           for i in range(5):
               self.held |= set([min(self.currentSuitors, key=lambda suitor: self.prefList.index(suitor.id))])
       rejected = self.currentSuitors - set(self.held) 
       rejected |= unacceptable
       self.currentSuitors = set()
       
       for reject in rejected:
          reject.assigned_count += -1
          reject.rejections += 1
       return rejected
    
# GSDA: [Suitor], [Suited] -> {Suitor -> Suited}
# construct a stable (monogamous) marriage between suitors and suiteds
def GSDA(suitors, suiteds):
   apply_to = 5
   unassigned = set()
   for suitor in suitors:
        if suitor.assigned_count < apply_to:
            print(type(suitor))
            print(suitor)
            unassigned |= set([suitor])
            
   while len(unassigned) > 0:
      for suitor in unassigned:
            next_proposal = suitor.preference()
            if next_proposal != None:
                suiteds[suitor.preference()].currentSuitors.add(suitor)
                suitor.proposals += 1
                suitor.assigned_count += 1
                print(str(suitor.id) + "is assigned_count: " + str(suitor.assigned_count))
                
      unassigned = set()
      for suitor in suitors:
          if suitor.assigned_count < apply_to:
              unassigned |= set([suitor])     
      
      for suited in suiteds:
         unassigned |= suited.reject()

   returndict = dict()
   for suitor in suitors:
        returndict.update({suitor:[]})
        for suited in suiteds:
            if suitor in suited.held:
                returndict.update({suitor:[suited]+returndict.get(suitor)})
   print(returndict)
   return returndict

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
def preflists_utility(
    n ,
    utility,
    list_length = None,
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


    for i in range(0, n):

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

def preflists(
    n ,
    sigma_fraction ,
    list_length = None,
    achievability_matrix = None,
    match_threshold = 0
):
    #scale sigma
    sigma = sigma_fraction * n /2

    utility = [(k, random.normalvariate(k,sigma)) for k in range(0,n)]
    utility.sort(key=operator.itemgetter(1))
    
    agents = preflists_utility(
        n  = n,
        utility = utility,
        list_length = list_length,
        achievability_matrix = achievability_matrix,
        match_threshold = match_threshold
        )
    return agents
    
    

#Return matching probability array:
def achiev_mat(
    n ,
    sigma_fract,
    force = False,
    runs = 20
    ):
    try:
        with open("/Users/tylerhoppenfeld/Documents/MarketDesign/AM_dict.pkl", "rb") as f:
            AM_dict = pickle.load(f)
    except FileNotFoundError:
        AM_dict = {}

    
    lookup_str = str(n) + "_" + str(sigma_fract*100)
    achievability_matrix = AM_dict.get(lookup_str)
    
    if np.all(achievability_matrix == None) | force == True:
        simulations = np.array([None]* runs)
        
        print("simulating achievability matrix for " + str(lookup_str))
        
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
        with open("/Users/tylerhoppenfeld/Documents/MarketDesign/AM_dict.pkl", "wb") as f:
            pickle.dump(AM_dict, f)
        
    return achievability_matrix
                    