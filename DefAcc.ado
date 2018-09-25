capture program drop DefAcc

program DefAcc
	local not_done = 1
	while `not_done' {
		local not_done = 0
		forvalues i = 1/4 {
			local lfr = lfr_rank[`i']
			local  next_rank = `lfr' + 1
			local proposal = pref`next_rank'[`i'] 
		
			#find the row for the woman in question:
				forvalues j = 5/8 {
					if agentid[`j'] == pref`next_rank'[`i'] local woman_row = `j'
				}
		
			#check if this is a new proposal
			if match[`woman_row'] != "M`i'" {
				#note that we will need to loop through the proposals at least one more time
				local not_done = 1
			
			
				#Woman Decides
				#loop over woman's preference list, stopping when we get to the new proposal,
				#or we get to the current match	
				forvalues j = 1/4 {
					if pref`j'[`woman_row'] == "M`i'" {
						#detect rejection
							replace lfr_rank = lfr_rank + 1 if agentid == match[`woman_row']
						#record the new match
						replace match = "M`i'" in `woman_row'
						#move on
						continue, break
					}
					if pref`j'[`woman_row'] == match[`woman_row'] {
						#record that the proposer was rejected
						replace lfr_rank = lfr_rank + 1 if agentid == "M`i'"
						#move on
						continue, break
					}
				}
			}
		}
	
	
	}


end
