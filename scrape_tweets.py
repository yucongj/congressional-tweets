import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime
import CongressMember
import ReadingMetaFunctions

# Part I: Input & Initialize
# Read the meta data (excel) collected
meta_data_collected = pd.read_excel('MetaTest.xlsx')
# Creating list to append tweet data
tweets_list = []
# Enter Start Date & End Date
start_Date = datetime.date(2022, 1, 1)
end_Date = datetime.date(2022, 6, 3)
# Part II: Transform Pd Dataframe to Congress by using "row_to_congressmember"

for j in range(len(meta_data_collected)):
    # Locate the row we are going to scrape
    row = meta_data_collected.loc[j]
    # Change into class congress
    con = ReadingMetaFunctions.row_to_congressmember(row)
    # Generate the excel file name after having class congress
    excel_Name = ReadingMetaFunctions.generate_tweets_filename(con)
    # Use usernames from the congress, use for loop to iterate
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper('from:' + con.twitter_name).get_items()):
        #if i > 1: break
        # declare the attributes to be returned
        if ReadingMetaFunctions.check_date(tweet.date.date(), start_Date, end_Date) == 1:
            continue
        elif ReadingMetaFunctions.check_date(tweet.date.date(), start_Date, end_Date) == -1:
            break
        else:
            tweets_list.append([tweet.url, tweet.date.date(), tweet.content, tweet.renderedContent,
                                tweet.id, tweet.tcooutlinks, tweet.replyCount, tweet.retweetCount,
                                tweet.likeCount, tweet.quoteCount, tweet.conversationId, tweet.lang,
                                tweet.source, tweet.media, tweet.retweetedTweet, tweet.quotedTweet,
                                tweet.mentionedUsers])
    # Creating a dataframe from the tweets list above
    tweets_df = pd.DataFrame(tweets_list, columns=['URL', 'Datetime', 'Text', 'Rendered Content',
                                                   'Tweet Id', 'Tcooutlinks', 'Count of Replies',
                                                   'Count of Retweet', 'Count of Like', 'Count of Quote',
                                                   'Conversation ID', 'Lang', 'Resource', 'Media',
                                                   'Retweeted Tweet', 'Quoted Tweet', 'Mentioned Users'])
    # To-Excel, names would be replaced (also the location)
    tweets_df.to_excel(excel_Name + ".xlsx")
    # Reset the list for the next person
    tweets_list = []