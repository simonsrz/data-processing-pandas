### Data Processing in R and Python 2022Z
### Homework Assignment no. 2
###
### IMPORTANT
### This file should contain only solutions to tasks in the form of a functions
### definitions and comments to the code.
###
# -----------------------------------------------------------------------------#
# Task 1
# -----------------------------------------------------------------------------#
import pandas as pd
import numpy as np

def solution_1(Posts):
    temp_posts = pd.DataFrame(Posts.copy())
    temp_posts['CreationDate'] = pd.to_datetime(temp_posts['CreationDate'])
    temp_posts['Year'] = temp_posts['CreationDate'].dt.strftime('%Y')
    res = temp_posts.groupby('Year').agg(TotalNumber=('Year', 'count'))
    res = res.reset_index(drop=False)
    return res

# -----------------------------------------------------------------------------#
# Task 2
# -----------------------------------------------------------------------------#

def solution_2(Posts, Users):
    temp_posts = pd.DataFrame(Posts.copy())
    temp_users = pd.DataFrame(Users.copy())
    Questions = temp_posts.loc[temp_posts.PostTypeId == 1, ["OwnerUserId", "ViewCount"]]
    joined = pd.merge(right=temp_users, left=Questions, how='inner', right_on='Id', left_on='OwnerUserId')
    after_grouping = joined.groupby('OwnerUserId', as_index=False).agg(TotalViews=('ViewCount', 'sum'))
    joined2 = pd.merge(left=after_grouping, right=temp_users, left_on='OwnerUserId', right_on='Id')
    joined2 = joined2[['OwnerUserId', 'DisplayName', 'TotalViews']]
    res = joined2.sort_values('TotalViews', ascending=False).iloc[0:10]
    res = res.astype({'OwnerUserId': 'int64'})
    res = res.rename(columns={'OwnerUserId': 'Id'})
    res = res.reset_index(drop=True)
    return res

# -----------------------------------------------------------------------------#
# Task 3
# -----------------------------------------------------------------------------#

def solution_3(Badges):
    temp_badges = pd.DataFrame(Badges.copy())
    temp_badges['Date'] = pd.to_datetime(temp_badges['Date'])
    temp_badges['Year'] = temp_badges['Date'].dt.strftime('%Y')
    BadgesNames = temp_badges.groupby(["Name", "Year"], as_index=False).agg(Count=('Name', 'count'))
    BadgesYearly = temp_badges.groupby("Year", as_index=False).agg(CountTotal=('Year', 'count'))
    joined = pd.merge(left=BadgesNames, right=BadgesYearly, on='Year')
    joined['Percentage'] = (joined['Count']*1.0)/joined['CountTotal']
    x = joined.groupby('Year', as_index=False).agg(MaxPercentage=('Percentage', 'max'))
    y = pd.merge(left=joined, right=x, left_on='Percentage', right_on='MaxPercentage')
    res = y[['Year_x', 'Name', 'MaxPercentage']].sort_values('Year_x').reset_index(drop=True)
    res = res.rename(columns={'Year_x': 'Year'})
    return res
    
# -----------------------------------------------------------------------------#
# Task 4
# -----------------------------------------------------------------------------#

def solution_4(Posts, Users, Comments):
    temp_posts = pd.DataFrame(Posts.copy())
    temp_users = pd.DataFrame(Users.copy())
    temp_comments = pd.DataFrame(Comments.copy())
    CmtTotScr = temp_comments.groupby('PostId', as_index=False).agg(CommentsTotalScore=('Score', 'sum'))
    PostsBestComments = pd.merge(left=temp_posts, right=CmtTotScr, left_on='Id', right_on='PostId')
    PostsBestComments = PostsBestComments.loc[PostsBestComments.PostTypeId == 1, ["OwnerUserId", "Title", "CommentCount", "ViewCount", "CommentsTotalScore"]]
    res = pd.merge(left=temp_users, right=PostsBestComments, left_on='Id', right_on='OwnerUserId')
    res = res[["Title", "CommentCount", "ViewCount", "CommentsTotalScore", "DisplayName", "Reputation", "Location"]]
    res = res.sort_values('CommentsTotalScore', ascending=False).iloc[0:10].reset_index(drop=True)
    return res
    
# -----------------------------------------------------------------------------#
# Task 5
# -----------------------------------------------------------------------------#

def solution_5(Posts, Votes):
    temp_posts = pd.DataFrame(Posts.copy())
    temp_votes = pd.DataFrame(Votes.copy())
    temp_votes['CreationDate'] = pd.to_datetime(temp_votes['CreationDate'])
    temp_votes['VoteDate'] = (np.where(temp_votes['CreationDate'].dt.strftime('%Y') == '2022', 'after',
                            np.where(temp_votes['CreationDate'].dt.strftime('%Y') == '2021', 'during',
                            np.where(temp_votes['CreationDate'].dt.strftime('%Y') == '2020', 'during',
                            np.where(temp_votes['CreationDate'].dt.strftime('%Y') == '2019', 'during',
                            'before')))))
    tmp = temp_votes.loc[temp_votes.VoteTypeId.isin([3, 4, 12]), ]
    VotesDates = tmp.groupby(["PostId", "VoteDate"], as_index=False).agg(Total=('PostId', 'count'))
    VotesDates['BeforeCOVIDVotes'] = np.where(VotesDates['VoteDate'] == 'before', VotesDates['Total'], 0)
    VotesDates['DuringCOVIDVotes'] = np.where(VotesDates['VoteDate'] == 'during', VotesDates['Total'], 0)
    VotesDates['AfterCOVIDVotes'] = np.where(VotesDates['VoteDate'] == 'after', VotesDates['Total'], 0)

    VotesByAge = VotesDates.groupby('PostId', as_index=False).agg(BeforeCOVIDVotes=('BeforeCOVIDVotes', 'max'),
                                                                  DuringCOVIDVotes=('DuringCOVIDVotes', 'max'),
                                                                  AfterCOVIDVotes=('AfterCOVIDVotes', 'max'),
                                                                  Votes=('Total', 'sum'))
    joined = pd.merge(left=temp_posts, right=VotesByAge, left_on='Id', right_on='PostId')

    joined['CreationDate'] = pd.to_datetime(joined['CreationDate'])
    joined['CreationDate'] = joined['CreationDate'].dt.strftime('%Y-%m-%d')
    joined = joined.loc[(joined.Title.notnull()) & (joined.DuringCOVIDVotes > 0), ]
    res = joined.loc[:, ["Title", "CreationDate", "PostId", "BeforeCOVIDVotes", "DuringCOVIDVotes", "AfterCOVIDVotes", "Votes"]]
    res = res.sort_values(by=['DuringCOVIDVotes', 'Votes'], ascending=False).iloc[0:20].reset_index(drop=True)
    res = res.rename(columns={'CreationDate': 'Date'})
    return res
