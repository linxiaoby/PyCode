
import re
str = "About 701,000,000 results (0.47 seconds) "
print (re.findall(r"About (.+?) results",str))
