class Player(object):
    '''
    #XX | LF | Irgavarland Torgverilsson | .356 / .120
    --------------------------------------------------
    #01 | P  | John Smith                | Insufficient Data

    -Jersey Number
    -Position
    -Name
    -Batting Average (BA)
    -On Base Percentage (OBP)
    '''
    def __init__(self,player_id=0,jersey_number=-1,position='NA',first_name='NONE',last_name='NONE',batting_average='N/A',on_base_percentage='N/A'):
        self.id = player_id
        self.jersey = int(jersey_number)
        self.position = position
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = "{} {}".format(first_name,last_name)
        self.batting_average = batting_average
        self.on_base_percentage = on_base_percentage
        self.earned_run_average = 99 # Should never be used for non-pitchers

    def pitchDie(self):
        return '-d12'
    
    def display(self):
        slash_line = "{} / {} |".format(self.batting_average,self.on_base_percentage)
        
        if (self.position == 'P'):
            if (self.batting_average in ['.---','.000','N/A']):
                slash_line = "AL  PITCHER |"
            slash_line = "{} {}".format(slash_line,self.pitchDie())
        elif self.batting_average in ['N/A',".---"]:
            slash_line = "NO MLB DATA |"


        print "#{:2d} | {:2} | {:32} | {}".format(self.jersey,self.position,self.full_name,slash_line)

    def setERA(self,earned_run_average):
        self.earned_run_average = earned_run_average



org_ids = {
108 : 'Los Angeles Angels',
109 : 'Arizona Diamondbacks',
110 : 'Baltimore Orioles',
111 : 'Boston Red Sox',
112 : 'Chicago Cubs',
113 : 'Cincinnati Reds',
114 : 'Cleveland Indians',
115 : 'Colorado Rockies',
116 : 'Detroit Tigers',
117 : 'Houston Astros',
118 : 'Kansas City Royals',
119 : 'Los Angeles Dodgers',
120 : 'Washington Nationals',
121 : 'New York Mets',
123 : 'Hartford Dark Blues',
124 : 'Indianapolis Blues',
125 : 'Indianapolis Blues',
126 : 'Indianapolis Hoosiers',
127 : 'Kansas City Blues',
128 : 'Kansas City Packers',
129 : 'Kansas City Cowboys',
130 : 'Kansas City Unions',
132 : 'Louisville Grays',
133 : 'Oakland Athletics',
134 : 'Pittsburgh Pirates',
135 : 'San Diego Padres',
136 : 'Seattle Mariners',
137 : 'San Francisco Giants',
138 : 'St. Louis Cardinals',
139 : 'Tampa Bay Rays',
140 : 'Texas Rangers',
141 : 'Toronto Blue Jays',
142 : 'Minnesota Twins',
143 : 'Philadelphia Phillies',
144 : 'Atlanta Braves',
145 : 'Chicago White Sox',
146 : 'Miami Marlins',
147 : 'New York Yankees',
148 : 'Louisville Colonels',
150 : 'Milwaukee Cream Citys',
151 : 'Milwaukee Brewers',
152 : 'Milwaukee Unions',
153 : 'Newark Peppers',
155 : 'New York Mutuals',
156 : 'New York Metropolitans',
157 : 'New York Giants',
158 : 'Milwaukee Brewers',
161 : 'Altoona Pride',
163 : 'Baltimore Orioles',
165 : 'Baltimore Terrapins',
166 : 'Baltimore Orioles',
167 : 'Baltimore Monumentals',
168 : 'Boston Reds',
169 : 'Boston Unions',
172 : 'Philadelphia Athletics',
173 : 'Philadelphia Athletics',
174 : 'Philadelphia Quakers',
175 : 'Philadelphia Keystones',
176 : 'Pittsburgh Rebels',
177 : 'Pittsburgh Burghers',
178 : 'St. Louis Cardinals',
180 : 'Rochester Hop Bitters',
181 : 'Richmond Virginias',
184 : 'Brooklyn Gladiators',
185 : 'Brooklyn Feds',
186 : 'Brooklyn Wonders',
187 : 'Buffalo Bisons',
188 : 'Buffalo Bisons',
189 : 'Buffalo Feds',
191 : 'Chicago Whales',
192 : 'Chicago Pirates',
193 : 'Chicago Unions',
195 : 'St. Louis Brown Stockings',
196 : 'St. Louis Maroons',
197 : 'St. Louis Terriers',
198 : 'St. Paul Saints',
199 : 'Syracuse Stars',
200 : 'Syracuse Stars',
201 : 'Toledo Blue Stockings',
202 : 'Toledo Maumees',
204 : 'Cincinnati Reds',
205 : "Cincinnati Kelly's Killers",
206 : 'Cincinnati Outlaw Reds',
208 : 'Cleveland Spiders',
209 : 'Cleveland Spiders',
210 : 'Columbus Colts',
211 : 'Columbus Colts',
212 : 'Cleveland Infants',
213 : 'Detroit Wolverines',
219 : 'Washington Nationals',
220 : 'Washington Senators',
221 : 'Washington Senators',
222 : 'Washington Nationals',
223 : 'Wilmington Quicksteps',
224 : 'Providence Grays',
297 : 'Worcester Brown Stockings',
298 : 'Baltimore Orioles',
299 : 'Troy Trojans'
}
