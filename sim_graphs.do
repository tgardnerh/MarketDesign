import delimited using /Users/tylerhoppenfeld/Documents/MarketDesign/block_simulations.csv, clear

foreach i of numlist 2/5 7 {
	tempfile temp
	save `temp'
	import delimited using /Users/tylerhoppenfeld/Documents/MarketDesign/block_simulations`i'.csv, clear
	append using `temp'
}

*import delimited using /Users/tylerhoppenfeld/Documents/MarketDesign/block_simulations_sept10.csv, clear


drop if   k < offset

collapse (mean) size_block doc_pos_dosm_block doc_pos_hosm_block hosp_pos_dosm_block hosp_pos_hosm_block  ,by(n k offset )

gen offset2 = 2* offset

gen small_block = k*2+1-offset2

/*
graph twoway ///
	(line  size_block offset2  if k == 5 & n == 500) ///
	(line size_block offset2  if k == 10 & n == 500) ///
	(line size_block offset2  if k == 20 & n == 500) ///
	, legend(order( 1 "11" 2 "21" 3 "41") ///
	title("Size of Larger Randomized Block")) ///
	xtitle("Imbalance in Block Size") ///
	ytitle("Fraction With Multiple Stable Matches") ///
	
	
graph export /Users/tylerhoppenfeld/Documents/MarketDesign/block_size_vs_offset.png, replace	
*/

 
graph twoway ///
	(line size_block n  if k == 20 & offset == 0) ///
	(line size_block n  if k == 20 & offset == 4) ///
	(line size_block n  if k == 20 & offset == 8) ///
	(line size_block n  if k == 20 & offset == 12) ///
	(line size_block n  if k == 20 & offset == 16) ///
	(line size_block n  if k == 20 & offset == 20) ///
	, legend(order( 1 "0" 2 "8" 3 "16" 4 "24" 5 "32" 6 "40") ///
	title("Block Size Imbalance")) ///
	xtitle("Size of Market") ///
	ytitle("Fraction With Multiple Stable Matches") ///
	
	
graph export /Users/tylerhoppenfeld/Documents/MarketDesign/block_size_vs_n.png, replace	
 
 
rename doc_pos_dosm_block optR
rename hosp_pos_hosm_block optL
rename doc_pos_hosm_block pesR
rename hosp_pos_dosm_block pesL

reshape long pes opt,  i( n k offset2 ) j(LvR) s
replace offset2 = - offset2 if LvR == "L"

sort offset2
 replace opt = - opt
 replace pes = - pes

collapse (mean) opt pes, by(n k offset2)	
	
graph twoway ///
	(rcap  opt pes offset2 if k ==20 & n == 500) ///
	, ///
	ytitle("Relative Match Quality") ///
	xtitle("Imbalance in Block Size")
	
	graph export /Users/tylerhoppenfeld/Documents/MarketDesign/matchQ_vs_k.png, replace	

	
	
	
