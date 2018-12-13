import pandas as pd




def parse(filename, stats):
    df = pd.read_csv(filename)

    segments = segment(df)

    # print(df.iloc[0]['playPTS'])

    top7 = find_top_7(df, segments)
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
    for index, row in df.iterrows():
        # playerName = "%s %s " % (row['playFNm'], row['playLNm']) 
        team = row['teamAbbr']
        if team != currentTeam:
            segments.append(index)
            currentTeam = team

    return segments

def find_top_7(df,segments, category="playPTS"):

    segments.append(len(segments) + 1)
    teams = []

    for i in range(2): #range(len(segments)-1):
        compare = []
        start = segments[i]
        end = segments[i+1]

        team = []
        for j in range(start, end):
            index = j
            pts = df.iloc[j][category]
            team.append((index, pts))
        print(team)

        team.sort(key = lambda x: x[1], reverse=True)

        teams.append(team[:7])

    return teams

def create_csv(df, top7, stats):

    d = {s:[] for s in stats}


    for team in top7:
        for player in team:
            index = player[0]
            # print(df.iloc[index]['playPTS'])
            for stat in stats:
                # print(df.iloc[index])
                d[stat].append(df.iloc[index][stat])

    print(d)

    df = pd.DataFrame(data=d)

    print(df)
    df.to_csv("output.csv", index=False)



    




if __name__ == "__main__":
    filename = "./nba-players-stats/2017-18_playerBoxScore.csv"
    stats = ['playDispNm', 'teamAbbr', 'teamLoc', 
             'playStat', 'playMin', 'playHeight', 
             'playPTS', 'playAST', 'playTO', 'playSTL', 
             'playBLK', 'playPF', 'playFGA', 'playFGM', 
             'playFTA', 'playFTM','playTRB', 'opptAbbr', 'opptRslt']
    parse(filename, stats)