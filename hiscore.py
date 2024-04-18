import os
import pickle

from constants import className, DEATH_NAMES, LEVELS, MAX_SCORES
from display import printMe


class Score:
    def __init__(self, name, chrClass, deathCause, deathLevel, maxLevel, score):
        self.name = name
        self.chrClass = chrClass
        self.deathCause = deathCause
        self.deathLevel = deathLevel
        self.maxLevel = maxLevel
        self.score = score

    def __str__(self):
        return f"{self.name}, a Level {self.maxLevel} {className(self.chrClass)}. Score: {self.score}"


def rankEarned(game):
    # hate this whole thing
    # get current rank in hiscore list
    score = Score(
        game.player.name,
        game.player.chrClass,
        game.player.deathCause,
        game.level,
        game.player.level,
        game.player.xp,
    )
    for i in range(len(game.hiscores)):
        this_score = game.hiscores[i]
        if score.score == this_score.score and score.name == this_score.name:
            return i
    return -1


def addHiScore(game):
    game.hiscores.append(
        Score(
            game.player.name,
            game.player.chrClass,
            game.player.deathCause,
            game.level,
            game.player.level,
            game.player.xp,
        )
    )
    # sort the hiscores by score
    game.hiscores = sorted(game.hiscores, key=lambda x: x.score, reverse=True)
    # remove anything after 10
    game.hiscores = game.hiscores[:MAX_SCORES]
    # save scores to file
    save_scores(game)


def drawHiScores(game):
    if len(game.hiscores) == 0:
        return

    printMe(game, "Greatest NPCs In History", 360, 5)

    for i in range(len(game.hiscores)):
        score = game.hiscores[i]
        printMe(game, f"{i}. {str(score)}", 360, i * 30 + 30)
        death_text = f"Defeated by {DEATH_NAMES[score.deathCause]} in {LEVELS[score.deathLevel]}."
        if score.deathLevel.value > 9:
            death_text = (
                f"Defeated by {DEATH_NAMES[score.deathCause]} in A Very Bad Place."
            )
        printMe(game, death_text, 380, i * 30 + 40)


def drawDeathScore(game):
    printMe(
        game,
        f"{rankEarned(game) + 1}. {game.player.name}, a Level {game.player.level} {className(game.player.chrClass)}. Score {game.player.xp}",
        200,
        400,
    )
    if game.level.value > 9:
        printMe(
            game,
            f"Defeated by {DEATH_NAMES[game.player.deathCause]} in A Very Bad Place.",
            220,
            410,
        )
    else:
        printMe(
            game,
            f"Defeated by {DEATH_NAMES[game.player.deathCause]} in {LEVELS[game.level]}.",
            220,
            410,
        )


def save_scores(game):
    print("Saving hiscores")
    with open("hiscores.dat", "wb") as f:
        pickle.dump(game.hiscores, f)


def load_scores(game):
    # if file exists, load it
    if os.path.exists("hiscores.dat"):
        with open("hiscores.dat", "rb") as f:
            game.hiscores = pickle.load(f)


if __name__ == "__main__":
    import main

    main.main()
