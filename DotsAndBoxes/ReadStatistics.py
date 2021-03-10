def get_games(filename):
    """
    Looks at a results file and turns it into a list of games.
    Games are a list of all associated moves and the final score.
    args:
        filename(str): filename for results file
    returns:
        list[][str]
    """
    with open(filename, "r") as infile:
        lines = infile.readlines()
    width = int(lines[0][0])
    height = int(lines[0][2])
    no_moves = ((width-1)*height + (height-1)*width)+2
    games = []
    start = 0
    end = no_moves
    while end <= len(lines):
        game = lines[start:end]
        games.append(game)
        start, end = end, end+no_moves
    return games

def count_winners(games):
    """
    Takes a list of list of games, provided by get_games, and prints the number of
    wins each player got.
    Args:
        games(list[][str]): List of games
    """
    p1wins = 0
    p2wins = 0
    draws = 0
    for game in games:
        p1score = int(game[-1][0])
        p2score = int(game[-1][3])
        if p1score > p2score:
            p1wins += 1
        elif p2score > p1score:
            p2wins += 1
        else:
            draws += 1
    if p1wins == 1:
        p1s = ""
    else:
        p1s = "s"
    if p2wins == 1:
        p2s = ""
    else:
        p2s = "s"
    print("Player 1 won {} time{} and Player 2 won {} time{} out of {}.".format(p1wins, p1s, p2wins, p2s, p1wins+p2wins+draws))
    if draws == 1:
        was = "was"
        draw = "draw"
    else:
        was = "were"
        draw = "draws"
    print("There {} {} {}.".format(was, draws, draw))

def get_scores(filename):
    games = get_games(filename)
    count_winners(games)
