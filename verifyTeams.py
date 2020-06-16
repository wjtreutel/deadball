# Quick script that pings MLB database for a set of year/team combinations 
# Used to look for possible exceptions in ranges of data 

from retrieveMLBRoster import getRoster
from support import org_ids
from time import sleep

novelty_years = [1874,1882,1895,1900,1901,1902]
years = [1919,1947,1969,1977,1995,2017]
teams = [111,117,158,147,121,136,119,135,137,136,209]



for team in [112]:
    print "=========={}==========".format(org_ids[team])
    for year in novelty_years:
        print "=========={}==========".format(year)
        for i in range (0,1):
            try:
                print "Success"
            except Exception, e:
                print "ERROR: " + str(e)
                sleep(5)
                continue
            break

