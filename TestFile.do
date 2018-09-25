#This is the wrapper file that runs and tests DefAcc.ado
do GenRankList.ado
do DefAcc.ado

import delimited preferences.csv, varnames(1) clear 





GenRankList, size(5) stdev(1)

DefAcc, preference_length(5)

