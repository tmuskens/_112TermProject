### File methods
def readLeaderboardFile(file):
    leaderboard = dict()
    f = open(file)
    for line in f:
        l = line.split(':')
        score = int(l[0])
        name = l[1][:-1]
        leaderboard[score] = name
    f.close()
    return leaderboard

def writeFileFromLeaderboard(file, leaderboard):
    f = open(file, 'w')
    lines = []
    for score in leaderboard:
        lines.append(f'{score}:{leaderboard[score]}\n')
    f.writelines(lines)

def readHighScore(file, name):
    f = open(file)
    for line in f:
        l = (line.rstrip()).split(':')
        currentName = l[0]
        if name == currentName:
            score = l[1]
            return int(score)
    return 0

def writeHighScore(name, score, file):
    f = open(file, "r")
    newList = []
    found = False
    for line in f:
            l = line.split(':')
            currentName = l[0]
            if name == currentName:
                found = True
                newList.append(f'{name}:{score}\n')
            else:
                newList.append(line)
    if not found:
        newList.append(f'{name}:{score}\n')
    f.close()
    f = open(file, "w")
    print(newList)
    f.writelines(newList)
