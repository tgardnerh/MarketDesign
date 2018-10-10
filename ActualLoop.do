//loop over instances


local sizelist 10  100 400
local stdevlist 10  100 400

local reps = 10

clear
generate size  = . 
generate stdev = .

save outputfile, replace
forvalues i = 1/`reps' {
	foreach size of local sizelist {
		global size = "`size'"
		 quietly {
			foreach stdev of local stdevlist {
				global stdev =  "`stdev'"
				do TestFile.do
				clear
				set obs 1
				gen size = `size'
				gen stdev = `stdev'
				gen difference = `r(mean)'
				append using outputfile
				save outputfile, replace
			}
		}
	 display "Rep " `i' ", size " `size' ", stdev " `stdev'	
	 pause 31
	}
}