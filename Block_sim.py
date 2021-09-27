#Import packages used below
import numpy as np
import pandas as pd
##pip3 install multiprocess
import multiprocessing as mp 
import matplotlib.pyplot as plt
import itertools
import copy
import DeferredAcceptance as da
import multiprocessing as mp


def sim_block(n,k,offset,trial = -1):
    if k < offset:
        return(0)
    D= da.block_preferences(n,n,k,short=True, trim_k=k)
    H = da.block_preferences(n,n,k-offset,short=True, trim_k=k)
    DOSM = da.GSDA(D,H,1)
    HOSM = da.GSDA(H,D,1)
    DOSM_HOSM = list(zip([(match[1][0],[match[0]]) for match in sorted(DOSM, key = lambda match:match[1][0])], HOSM))
    HOSM_DOSM = list(zip([(match[1][0],[match[0]]) for match in sorted(HOSM, key = lambda match:match[1][0])], DOSM))
    #Below, we have:                                                 d's name,  doc d's rank list               , d's match      d, with his opt and pes match           
    Doc_pos_DOSM  = sum([match[1].index(match[2])-k-2  for match in [(d[0][0],[entry[1] for entry in D[d[0][0]]],d[0][1][0]) for d in DOSM_HOSM]])/n
    Doc_pos_HOSM  = sum([match[1].index(match[2])-k-2  for match in [(d[1][0],[entry[1] for entry in D[d[1][0]]],d[1][1][0]) for d in DOSM_HOSM]])/n
    Hosp_pos_HOSM = sum([match[1].index(match[2])-k-2  for match in [(h[0][0],[entry[1] for entry in H[h[0][0]]],h[0][1][0]) for h in HOSM_DOSM]])/n 
    Hosp_pos_DOSM = sum([match[1].index(match[2])-k-2  for match in [(h[1][0],[entry[1] for entry in H[h[1][0]]],h[1][1][0]) for h in HOSM_DOSM]])/n 


    #print(Doc_pos_DOSM)
    #print(Doc_pos_HOSM)
    #print(Hosp_pos_HOSM)
    #print(Hosp_pos_DOSM)
    return [sum([not match[0] == match[1] for match in DOSM_HOSM])/n, Doc_pos_DOSM, Doc_pos_HOSM , Hosp_pos_HOSM,Hosp_pos_DOSM]
sim_block(500,20,0)

def sim_normal(n,k,offset,trial = -1):
    n = int(n)
    if k < offset:
        return(0)
    D= da.generate_preferences(n,n,2*k/n)
    H = da.generate_preferences(n,n,2*(k-offset)/n)
    DOSM = da.GSDA(D,H,1)
    HOSM = da.GSDA(H,D,1)
    DOSM_HOSM = list(zip([(match[1][0],[match[0]]) for match in sorted(DOSM, key = lambda match:match[1][0])], HOSM))
    HOSM_DOSM = list(zip([(match[1][0],[match[0]]) for match in sorted(HOSM, key = lambda match:match[1][0])], DOSM))
    
    Doc_pos_DOSM  = sum([match[1].index(match[2]) - match[0] for match in [(d[0][0],[entry[1] for entry in D[d[0][0]]],d[0][1][0]) for d in DOSM_HOSM]])/n
    Doc_pos_HOSM  = sum([match[1].index(match[2]) - match[0] for match in [(d[1][0],[entry[1] for entry in D[d[1][0]]],d[1][1][0]) for d in DOSM_HOSM]])/n
    Hosp_pos_HOSM = sum([match[1].index(match[2]) - match[0] for match in [(h[0][0],[entry[1] for entry in H[h[0][0]]],h[0][1][0]) for h in HOSM_DOSM]])/n 
    Hosp_pos_DOSM = sum([match[1].index(match[2]) - match[0] for match in [(h[1][0],[entry[1] for entry in H[h[1][0]]],h[1][1][0]) for h in HOSM_DOSM]])/n 

    return [sum([not match[0] == match[1] for match in DOSM_HOSM])/n, Doc_pos_DOSM, Doc_pos_HOSM , Hosp_pos_HOSM,Hosp_pos_DOSM]
    

n_list =  [50,500,2500,50000 ]
k_list = [20  ]
offset_list = [0,4,8,12,16,20]
trial_list = range(20)



df = pd.DataFrame(list(itertools.product(n_list,k_list,offset_list,trial_list)), columns=['n', 'k', 'offset','trial'])


def sim(input):
    return sim_normal(input[0], input[1], input[2])
        #df = df.values.tolist()
if __name__ == '__main__':
    with mp.Pool() as p:
        bob = df.join(pd.DataFrame(p.map(sim,df.values.tolist()), columns  = ['size_block', 'Doc_pos_DOSM_block','Doc_pos_HOSM_block','Hosp_pos_HOSM_block','Hosp_pos_DOSM_block'] ) )
        bob.to_csv('/Users/tylerhoppenfeld/Documents/MarketDesign/normal_simulations_sizeVn_sept26.csv', index=False)

#list(df)
#    "df2=df2.join(df2.apply(lambda row: pd.Series(sim_block(row['n'],row['k'],row['offset']), index = ['size_block', 'Doc_pos_DOSM_block','Doc_pos_HOSM_block','Hosp_pos_HOSM_block','Hosp_pos_DOSM_block']), axis = 1))\n",

