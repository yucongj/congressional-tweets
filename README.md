# Congressional Tweets

## Introduction
This project was designed to measure Anti-Democratic Rhetoric (ADR) in social media posts on Twitter from members of the U.S. Congress, in order to analyze (one aspect of) democratic backsliding in the United States. It involves a textual corpus (dataset) of all tweets sent from the official accounts of sitting members of the 117th Congress during the period spanning January 2020 through June 2022, encompassing the 2020 election and the events of January 6, 2021. This repository contains the data-scraping code and metadata, and a link to the full dataset.

## Code

The Python file `MeataData.py` scrapes the metadata about the members of Congress from `https://ballotpedia.org/List_of_current_members_of_the_U.S._Congress`. The result is an Excel file containing each member's Twitter username, last name, first name, chamber, party, state, district (if the chamber is House), date assumed office, and gender.

The Python file `scrape_tweets.py` gathers all the tweets by the Congressmembers (in the above Excel file) between a start date and an end date. Currently in the code, the start date is set on 2020/01/01, and the end date on 2022/06/30.


## Data

The scraped metadata about the Congressmembers for this project are stored in `data/MetaData.xlsx` (and also in csv format: `data/MetaData.csv`). Each row represents one Congressmember.

The scraped Tweets are stored in an Excel file on Zenodo at [https://doi.org/10.5281/zenodo.8215566](https://doi.org/10.5281/zenodo.8215566). There are 1,048,515 rows, each row representing a Tweet. Each tweet is accompanied by Twitter-derived metadata (e.g., timestamps, hashtags, and number of replies) as well as relevant demographic data about the members (including each congressmember’s name, Twitter username, party ID, gender, state and district represented, chamber of Congress, and tenure in office), drawn from Ballotpedia.org and members’ own web sites.

## License
The contents of this repository are made available under a [Creative Commons Attribution Non-Commercial Share-Alike 4.0 (CC BY-NC-SA 4.0) license](https://creativecommons.org/licenses/by-nc-sa/4.0/). If you use this material in any research, please give credit to Christopher J. Miller and Yucong Jiang, and cite the paper [TBD].

## Acknowledgement

The data scraping and processing was assisted by Maniha Akram, Justin Barrera, Bailey Rossenfeld, Yili Yu, and Ginny Zhang during 2022 Summer Undergraduate Research at the University of Richmond.