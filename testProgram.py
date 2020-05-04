from retrieveMLBRoster import getRoster
from support import org_ids
from time import sleep

years = [1919,1947,1969,1977,1995,2017]
teams = [111,117,158,147,121,136,119,135,137,136]


for team in teams:
    print "=========={}==========".format(org_ids[team])
    for year in years:
        print "=========={}==========".format(year)
        for i in range (0,10):
            try:
                getRoster(year,team)
                print "Success!"
            except Exception, e:
                print "ERROR: " + str(e)
                sleep(5)
                continue
            break

