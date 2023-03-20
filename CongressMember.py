#CongressMember Class
class CongressMember:
    def __init__(self, twitter_name='', last_name='', first_name='', chamber='',\
                party = '', state = '', district = 'None', date_assumed_office = '', date_collected = '', gender = ''):
        self.twitter_name = twitter_name
        self.last_name = last_name
        self.first_name = first_name
        self.chamber = chamber
        self.state = state
        self.district = district
        self.date_assumed_office = date_assumed_office
        self.party = party
        self.date_collected = date_collected
        self.gender = gender

    def __repr__(self):
        object = [self.twitter_name, self.last_name, self.first_name, self.chamber, \
            self.party, self.state,self.district, self.date_assumed_office, self.gender, self.date_collected]
        return object
