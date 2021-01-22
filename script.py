import pandas as pd
import numpy as np
import requests

candidates = pd.read_csv("ICPC15.csv")

processed = []

contestId = '1474'

numParticipants = 0
contestName = ''


def getContestDetails():
    global numParticipants, contestName
    base = 'https://codeforces.com/api/contest.standings?contestId='
    URL = base + contestId + '&showUnofficial=true'
    data = requests.get(url=URL).json()['result']
    numParticipants = len(data['rows'])
    contestName = data['contest']['name']


def get_url(username):
    base = 'https://codeforces.com/api/contest.standings?contestId='
    url = base + contestId +'&handles='+ username +'&showUnofficial=true'
    return url


def get_rank(username):
    URL = get_url(username)
    return requests.get(url=URL).json()['result']['rows'][0]['rank']


def get_details(i):
    username = candidates['Codeforces Username'][i]
    rank = get_rank(username)
    percentile = 100 * (1 - (rank / numParticipants))
    return rank, percentile


getContestDetails()
numEntries = candidates.shape[0]
RANK = [-1 for i in range(numEntries)]
PERCENTILE = [0 for i in range(numEntries)]
for i in range(numEntries):
    try:
        rank, percentile = get_details(i)
    except:
        rank, percentile = -1, 0
    RANK[i] = rank
    if rank == 0:
        percentile = 0
    PERCENTILE[i] = percentile
#candidates['Ranks ' + contestName] = RANK                  # uncomment this if you want a column for rank as well
candidates['Percentiles ' + contestName] = PERCENTILE
candidates.to_csv('ICPC15.csv')        