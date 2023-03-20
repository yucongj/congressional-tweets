# File for collecting all metadata from all CongressMembers

#import packages
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from CongressMember import CongressMember

#---------------------------------------------------------------------------------------------------------------
#STEP 1: GETTING PROFILE LINKS OF EACH PERSON

url = 'https://ballotpedia.org/List_of_current_members_of_the_U.S._Congress'

data = requests.get(url)

html = BeautifulSoup(data.text, 'html.parser')

table = html.find_all(id = 'officeholder-table')

# Two functions that eliminate extra links unuseful for senator table and house table
def eliminate_extra_links_for_senators(href):
    return href and not re.compile('https://ballotpedia.org/List_of_United_States_Senators_from_').search(href)\
           and not re.compile('https://ballotpedia.org/United_States_congressional_delegations_from_North_Dakota').search(href)\
           and not re.compile('https://ballotpedia.org/Puerto_Rico').search(href)\
           and not re.compile('Zoraida_Buxo_Santiago').search(href)\
           and not re.compile('Melinda_Romero_Donnelly').search(href)

def elimiante_extra_links_for_house(href):
    return href and not re.compile('District').search(href)\
           and not re.compile('Puerto_Rico').search(href)\
           and not re.compile('Roberto_Lefranc_Fortuño').search(href)\
           and not re.compile('María_Meléndez_Altieri').search(href)\
           and not re.compile('Ricardo_Rosselló').search(href)\
           and not re.compile('Elizabeth_Torres_Rodriguez').search(href)\
           and not re.compile('United_States_Virgin_Islands%27_Delegate_to_the_U.S._House_of_Representatives').search(href)

# Get elements of profile pages for each chamber
names_elements_senators = table[0].find_all(href=eliminate_extra_links_for_senators)
names_elements_house = table[1].find_all(href=elimiante_extra_links_for_house)

name_elements = [] # create a list to combine two groups of congressmembers
for links in names_elements_senators:
    name_elements.append(links)

for links in names_elements_house:
    name_elements.append(links)

urls = []
for elements in name_elements:
    urls.append(elements.get('href')) # This gives a list of urls to all members' profile pages.
#---------------------------------------------------------------------------------------------------------
#STEP 2: GETTING INFO FROM BALLOTPEDIA HOME PAGE (DISTRICT, DATE ASSUMED OFFICE)

#Getting all of the name text of all of the senate and house members
Sname_collection = table[0].tbody.find_all('td', style="padding-left:10px;text-align:center;")
Hname_collection = table[1].tbody.find_all('td', style="padding-left:10px;text-align:center;")

#Getting all of the name text of the districts/states
Hdistrict_collection = table[1].tbody.find_all('td', style="padding-left:10px;")

#Getting all of the date elements assumed office for senators
Sdate_collection = table[0].tbody.find_all('td', style="text-align:center;")
Hdate_collection = table[1].tbody.find_all('td', style="text-align:center;")

date_list = [] #making a list of all the dates assumed office
#Adding date text assumed office of senators to date_list
for i in range(len(Sdate_collection) - 2):
    date_list.append(Sdate_collection[i].text)

#Creating a list of non-vacant districts
district_list = []
#Adding dates assumed office of house members to date_list
for i in range(len(Hname_collection) - 4):
    if Hname_collection[i].text != 'Vacant':
        district_list.append(Hdistrict_collection[i].text)
        date_list.append(Hdate_collection[i].text)
#---------------------------------------------------------------------------------------
#Helper function for getting name accurately
def get_last_name(name_split): #helps split last name from first name
    if len(name_split)==2:#just first and last name
        last_name = name_split[1]
    elif "(" in name_split[2]: #has a state in parentheses i.e. (Alabama)
        last_name = name_split[1]
    elif len(name_split)>=3: #has 3 names or more
        last_name  = name_split[-2] + " " + name_split[-1]
    else:
        last_name = "ERROR"
    return last_name
#------------------------------------------------------------------------------------
# STEP 3: COLLECTING THE DATA

index_of_row = 0 #helps keep track of the information from ballotpedia home page
parent_data = [] #instantiate a list of CongressMember objects

# Beginning of data collection: cycles through each members' profile and creates
# a congressmember object containing twitter username, person's first and last name,
# state, party, district, date_assumed_office, and chamber.
for link in urls:
    req = requests.get(link)
    profile_html = BeautifulSoup(req.text, 'html.parser')

    #get state so we can check for non-voting members
    if profile_html.find('a', title = "United States") != None:
        state = profile_html.find('a', title = "United States").next.next.next.get('title')
    else:
        state = 'ERROR' #non-voting
        continue #If the territory is not one of the 50 states, skip.

    #get twitter handle
    twitter_elements = profile_html.find('a', text= 'Official Twitter')

    # get twitter username from twitter link
    if twitter_elements != None:
        twitter_link = twitter_elements.get('href')
        split_link = twitter_link.split('/')
        twitter_name = split_link[len(split_link) - 1]

    else: # if they don't have "Official Twitter" but might have "Campaign Twitter"
        twitter_elements = profile_html.find('a', text= 'Campaign Twitter')

        if twitter_elements != None: # if they have Campaign Twitter
            twitter_link = twitter_elements.get('href')
            split_link = twitter_link.split('/')
            twitter_name = split_link[len(split_link) - 1]
        else: # if they don't have Compaign Twitter....
            twitter_name = 'None'

    #get person's name
    profile_name = profile_html.find('h1')
    name_text = profile_name.text
    split_name = name_text.split()
    first_name = split_name[0]
    last_name = get_last_name(split_name)

    # get party
    inDemo = profile_html.find('div', class_="widget-row value-only Democratic Party")
    inRepub = profile_html.find('div', class_="widget-row value-only Republican Party")
    indep = profile_html.find('div', class_="widget-row value-only Independent")
    if inDemo != None:
        party = "Democratic"
    elif inRepub != None:
        party = "Republican"
    elif indep != None:
        party = "Independent"
    else:
        party = 'New Progessive'

    #get district from data above (House only)
    if index_of_row < 100:#senate doesn't have district
        district = 'None'
    else:
        district = district_list[index_of_row - 100]
        if "District" in district and ("At-large District" not in district):
            district_split = district.split()
            district = district_split[len(district_split)-1]
        elif "At-large District" in district:
            district = '1'
        else:
            district = 'ERROR'

    #get date assumed office
    date_assumed_office = date_list[index_of_row]

    index_of_row += 1 #move to next set of data collected above

    #get Chamber
    if district == "None":
        chamber = "Senate"
    else:
        chamber = "House"

    #add all info to a CongressMember object
    congressmember_data = CongressMember(twitter_name, last_name, first_name, chamber, party, state, district, date_assumed_office)
    congressmember_string = congressmember_data.__repr__() #convert object to a list
    print(congressmember_data.__repr__()) #testing
    parent_data.append(congressmember_string) #add to master
#---------------------------------------------------------------------------------------------------------------------------------------------
# STEP 4: WRITE AN EXCEL FILE
df = pd.DataFrame(parent_data, columns=["Username", "Last Name", "First Name", "Chamber", "Party", 'State', 'District', "Date Assumed Office"])
with pd.ExcelWriter('MetaData.xlsx',
                    mode='a',engine="openpyxl", if_sheet_exists='replace') as writer: df.to_excel(writer)
