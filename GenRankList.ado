#Generate preferences

capture program drop GenRankList
program GenRankList
	syntax , size(integer) stdev(real)
	local agent_count = 2*`size'
	local first_woman = `size'+1
	clear
	generate agentid = ""
	set obs `agent_count'	
	
	#name the men
	forvalues i = 1/`size' {
		replace agentid = "M`i'" if _n == `i'
	}
	#name the women
	forvalues i = `first_woman'/`agent_count' {
		local woman_id = `i'-`size'
		replace agentid = "W`woman_id'" if _n == `i'
	}
		
	forvalues j = 1/`size' {
		generate utility`j' = `j'
		
	}

	#add in randomness

	gen rvar = 0
	forvalues i = 1/`size' {
		replace rvar = rnormal(0, `stdev')
		replace utility`i' = utility`i' + rvar
	}

	drop rvar
	
	#generate ranklist
	
	forvalues i = 1/`size' {
		generate pref`i' = ""
		generate pref_util = .
		
		#loop over utility values to determine preference for that number
		forvalues j = 1/`size' {
			replace pref_util =  utility`j'  if utility`j' < pref_util
			replace pref`i' = "W`j'" if pref_util == utility`j' & strpos( agentid, "M") 
			replace pref`i' = "M`j'" if pref_util == utility`j' & strpos( agentid, "W")
		}
		
		
		#loop over utility values again to drop out the used utility
		forvalues j = 1/`size' {
			replace  utility`j' = . if pref_util == utility`j'
		}
		
		
		list
		pause 42
		drop pref_util
	}


drop utility*

end