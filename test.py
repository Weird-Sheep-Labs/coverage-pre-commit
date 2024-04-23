import re

destination = open("dest.xml", mode="+a")
for line in open("coverage.xml"):
    destination.write(re.sub(pattern=r"timestamp=\"[0-9]*\"", repl="", string=line))
