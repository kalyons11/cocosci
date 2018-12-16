import pandas as pd
import copy


def parse(filename, stats):
    """
    Parse the csv into a more readable object
    """
    df = pd.read_csv(filename)
    segments = segment(df)
    # print(segments)
    top7 = find_topk(df, segments, category="playMin")
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

    players = set()
    for team in top7:
        for player in team:
            index = player[0]
            name = df.iloc[index]['playDispNm']
            players.add(name)

    num_players = len(players)
    players = list(players)
    
    players_to_use = set()
    for i in range(len(players)//3):
        players_to_use.add(players.pop())

    keys = ["LeBron James",
           "Klay Thompson",
           "Danny Green",
           "Al Horford",
           "Dwight Howard",
           "Dwayne Wade",
           "Iman Shumpert",
           "Elfrid Payton"]
    for k in keys:
        players_to_use.add(k)


    teams = dict()
    for team in top7:
        #first player's team
        for player in team:
            index = player[0]
            player_name = df.iloc[index]['playDispNm']
            if player_name not in players_to_use:
                continue
            for stat in stats:
                d[stat].append(df.iloc[index][stat])

    df = pd.DataFrame(data=d)
    df.to_csv("theLeagueMinutes.csv", index=False)

if __name__ == "__main__":
    filename = "./nba-players-stats/2017-18_playerBoxScore.csv"
    stats = ['playDispNm', 'teamAbbr', 
             'playMin', 
             'playPTS', 'playAST', 'playTO', 'playSTL', 
             'playBLK', 'playPF', 'playFGA', 'playFGM', 
             'playTRB']
    parse(filename, stats)