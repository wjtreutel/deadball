# TeamGenerator.py
#
# Created: 5/29/21
#
# Library file for high-level team functions


from league import *

# I legitimately can't remember if class creators are private,
# so I hastily made this wrapper function
# and I need to fix this later
def new_league(league_name,names):
    return League(league_name,names)
