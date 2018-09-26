#This is the wrapper file that runs and tests DefAcc.ado
do GenRankList.ado
do DefAcc.ado

local size 100
local stdev 1000


local size_x_2 = `size'*2
local size_plus_1 = `size' + 1


GenRankList, size(`size') stdev(`stdev')

DefAcc, preference_length(`size')
rename match  MP_match
drop lfr_rank
replace agentid = "W" +  substr(agentid, 2, .) in 1/`size'
replace agentid = "M" +  substr(agentid, 2, .) in `size_plus_1'/`size_x_2'

forvalues i = 1/`size' {
	replace pref`i' = "M" +  substr(pref`i', 2, .) in 1/`size'
	replace pref`i' = "W" +  substr(pref`i', 2, .) in `size_plus_1'/`size_x_2'
}
gen agentnumber = substr(agentid, 2, .)
destring agentnumber, replace
gen agentsex = substr(agentid, 1, 1)
sort agentsex agentnumber
drop agentsex agentnumber

DefAcc, preference_length(`size')

rename match WP_match
drop lfr_rank
replace agentid = "W" +  substr(agentid, 2, .) in 1/`size'
replace agentid = "M" +  substr(agentid, 2, .) in `size_plus_1'/`size_x_2'
replace WP_match = "W" +  substr(WP_match, 2, .) in `size_plus_1'/`size_x_2'
forvalues i = 1/`size' {
	replace pref`i' = "M" +  substr(pref`i', 2, .) in 1/`size'
	replace pref`i' = "W" +  substr(pref`i', 2, .) in `size_plus_1'/`size_x_2'
}
gen agentnumber = substr(agentid, 2, .)
destring agentnumber, replace
gen agentsex = substr(agentid, 1, 1)
sort agentsex agentnumber
drop agentsex agentnumber

#code to fill in the missing match 

forvalues i = 1/`size' {
	replace WP_match = "M`i'" if agentid == WP_match[`i']
	
}


forvalues i = `size_plus_1'/`size_x_2' {
	local j = `i' - `size'
	replace MP_match = "W`j'" if agentid == WP_match[`i']
	
}

generate mpwpflag = MP_match == WP_match 
sum mpwpflag


