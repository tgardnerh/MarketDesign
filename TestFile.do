#This is the wrapper file that runs and tests DefAcc.ado
do DefAcc.ado

import delimited preferences.csv, varnames(1) clear 


	gen match = ""
	gen lfr_rank = 0



DefAcc


