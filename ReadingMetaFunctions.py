# Contains functions to help create filenames and create CongressMember objects
import datetime
import xlrd
import pandas as pd
from CongressMember import CongressMember

def row_to_congressmember(row):
    #Converts a row from the dataframe into a CongressMember object
    row_in_list = list(row)
    congressmember = CongressMember()#instantiate CongressMember object
    #take info from row in df and put it in CongressMember object
    congressmember.twitter_name = row_in_list[1]
    congressmember.last_name = row_in_list[2]
    congressmember.first_name = row_in_list[3]
    congressmember.chamber = row_in_list[4]
    congressmember.party = row_in_list[5]
    congressmember.state = row_in_list[6]
    congressmember.district = row_in_list[7]
    congressmember.date_assumed_office = row_in_list[8]
    congressmember.gender = row_in_list[9]
    #This line strips the current date of non-number characters to get the format YYYYMMDD
    congressmember.date_collected = str(datetime.date.today()).replace('-', "")
    return congressmember

print(row_to_congressmember(row).__repr__()) #testing


def abbreviate_state(state_or_territory_name):
    """
    Abbreviates the names of the 50 US states using a dictionary that contains
    'Full State Name:Abbreviation' key-value pairs.
    The dictionary also includes U.S territories (such as Puerto Rico) other than the 50 states.
    Returns the abbreviation as a string.
    """

    abbreviation_dictionary = {'Alabama': 'AL', 'Alaska': 'AK', 'Arizona':'AZ', 'Arkansas':'AR', 'American Samoa':'AS',
    'California':'CA', 'Colorado': 'CO', 'Connecticut':'CT', 'Delaware':'DE', 'District of Columbia':'DC',
    'DC':'DC', 'Florida':'FL', 'Georgia':'GA', 'Guam':'GU', 'Hawaii':'HI', 'Idaho':'ID', 'Illinois': 'IL',
    'Indiana':'IN', 'Iowa':'IA', 'Kansas':'KS', 'Kentucky':'KY', 'Louisiana':'LA', 'Maine':'ME', 'Wyoming':'WY',
    'Maryland':'MD', 'Massachusetts':'MA', 'Michigan':'MI', 'Minnesota':'MN', 'Mississippi':'MS',
    'Missouri':'MO', 'Montana':'MT', 'Nebraska':'NE', 'Nevada':'NV', 'New Hampshire':'NH', 'New Jersey':'NJ',
    'New Mexico':'NM', 'New York':'NY', 'North Carolina':'NC', 'North Dakota':'ND', 'Mariana Islands':'CM',
    'Ohio': 'OH', 'Oklahoma':'OK', 'Oregon':'OR', 'Pennsylvania':'PA', 'Puerto Rico':'PR', 'Rhode Island':'RI',
    'South Carolina':'SC', 'South Dakota':'SD', 'Tennessee':'TN', 'Texas':'TX', 'Trust Territories': 'TT', 'Utah':'UT',
    'Vermont':'VT', 'Virginia':'VA', 'Virgin Island':'VI', 'Washington':'WA', 'West Virginia':'WV', 'Wisconsin':'WI'}

    if state_or_territory_name in abbreviation_dictionary:
        return abbreviation_dictionary[state_or_territory_name]
    else:
        raise NameError("The state you entered was not found - please spell its full name correctly.")

def generate_tweets_filename(congress_member):
    """
    Takes a CongressMember object and uses its data fields to create a file name.
    """
    first_name_initial = congress_member.first_name[0]
    last_name = congress_member.last_name
    state = abbreviate_state(congress_member.state)
    party_initial = congress_member.party[0]
    #differentiates the Senate and House memebers
    if (congress_member.district == 'None'):
        return last_name + "_" + first_name_initial + "_" + state + "_" +\
        party_initial + "_" + congress_member.date_collected
    else:
        district = congress_member.district
        return last_name + "_" + first_name_initial + "_" + state + district +\
        "_" + party_initial + "_" + congress_member.date_collected

print(generate_tweets_filename(row_to_congressmember(row))) #testing



def check_date(datetime, start_date, end_date):
    #compares date of tweet to the start and end dates of the range
    if datetime >= start_date and datetime <= end_date:
        #if the tweet falls within the range of start and end date
        return datetime
    if datetime > end_date:
        #if tweet is more recent than the end date
        return 1
    if datetime < start_date:
        #if tweet is earlier than the start date
        return -1
