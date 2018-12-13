import pandas as pd
import copy


def parse(filename, stats):
    """
    Parse the csv into a more readable object
    """
    df = pd.read_csv(filename)
    segments = segment(df)
    # print(segments)
    top7 = find_topk(df, segments)
    # print(top7)
    create_csv(df, top7, stats)

def segment(df):
    """
    Parse the data to find pivot points between teams.
    Returns a list of integers i where each i represents
        the row index of a new team (new game)
    """
    segments = [0]
    currentTeam = df.iloc[0][5]
    lastrow = 0
    for index, row in df.iterrows():
        # playerName = "%s %s " % (row['playFNm'], row['playLNm']) 
        team = row['teamAbbr']
        if team != currentTeam:
            segments.append(index)
            currentTeam = team

        lastrow = index

    # last index
    segments.append(lastrow + 1)

    return segments

def find_topk(df,segments, category="playPTS", k=7):

    teams = []
    teamgames = dict()

    for i in range(len(segments)-1):
        compare = []
        start = segments[i]
        end = segments[i+1]

        teamAbbr = df.iloc[start]['teamAbbr']

        team = []
        for j in range(start, end):
            index = j
            # print(index)
            pts = df.iloc[j][category]
            team.append((index, pts, teamAbbr))
        team.sort(key = lambda x: x[1], reverse=True)

        teams.append(team[:k])

    return teams

def create_csv(df, top7, stats):

    d = {s:[] for s in stats}
    d['gameNum'] = []

    teams = dict()
    for team in top7:
        #first player's team
        teamAbbr = team[0][2]
        if teamAbbr not in teams:
            teams[teamAbbr] = 1

        
        for player in team:
            index = player[0]
            for stat in stats:
                d[stat].append(df.iloc[index][stat])
            d['gameNum'].append(teams[teamAbbr])

        teams[teamAbbr] += 1

    df = pd.DataFrame(data=d)
    df.to_csv("theLeague.csv", index=False)

if __name__ == "__main__":
    filename = "./nba-players-stats/2017-18_playerBoxScore.csv"
    stats = ['playDispNm', 'teamAbbr', 'teamLoc', 
             'playStat', 'playMin', 'playHeight', 
             'playPTS', 'playAST', 'playTO', 'playSTL', 
             'playBLK', 'playPF', 'playFGA', 'playFGM', 
             'playFTA', 'playFTM','playTRB', 'opptAbbr', 'opptRslt']
    parse(filename, stats)