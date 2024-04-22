import os
import pickle

import pygame

import requests

from constants import CLASS, CLASS_NAME, DEATH_NAMES, LEVELS, MAX_SCORES
from display import printMe


class Score:
    def __init__(
        self, player_name, name, chrClass, deathCause, deathLevel, maxLevel, score
    ):
        self.player_name = player_name.strip()
        self.name = name
        self.chrClass = chrClass
        self.deathCause = deathCause
        self.deathLevel = deathLevel
        self.maxLevel = maxLevel
        self.score = int(score)

    def __str__(self):
        return f"{self.name}, a Level {self.maxLevel} {self.chrClass}. Score: {int(self.score)}"


def rankEarned(game):
    # hate this whole thing
    # get current rank in hiscore list
    score = Score(
        game.player_name,
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
    new_score = Score(
        game.player_name,
        game.player.name,
        CLASS_NAME[game.player.chrClass],
        game.player.deathCause,
        game.level,
        game.player.level,
        game.player.xp,
    )
    game.hiscores.append(new_score)
    # sort the hiscores by score
    game.hiscores = sorted(game.hiscores, key=lambda x: x.score, reverse=True)
    # remove anything after 10
    game.hiscores = game.hiscores[:MAX_SCORES]
    # save scores to file
    save_scores(game)

    # do we have a score URL? And does the player even want to upload scores?
    if game.upload_scores and game.score_url:
        # if this character is eligible to upload...
        if game.player.online_eligible:
            # send the score to the server
            url = game.score_url + "/scores"
            score = new_score
            data = {
                "player_name": score.player_name,
                "character_name": score.name,
                "character_class": score.chrClass,
                "death_cause": score.deathCause,
                "death_level": LEVELS[score.deathLevel],
                "level": score.maxLevel,
                "score": score.score,
                "version": game.version,
            }
            try:
                # timeout of 5 seconds, let's not get crazy here
                requests.post(url, json=data, timeout=5)
            except requests.exceptions.Timeout:
                print("Timeout occurred while sending score")
            except Exception as e:
                print(f"Error sending score: {e}")
        else:
            print("Player not eligible to upload score")


def drawHiScores(game):
    if len(game.hiscores) and (game.retrieve_scores and len(game.global_hiscores) == 0):
        return

    printMe(game, "Greatest NPCs In History", 360, 5)

    # if we're going to show global high scores, clear up some room
    show_scores = len(game.hiscores)
    if game.retrieve_scores:
        show_scores = 5

    for i in range(show_scores):
        if i < len(game.hiscores):
            score = game.hiscores[i]
            printMe(game, f"{i + 1}. {str(score)}", 360, i * 30 + 30)
            death_text = (
                f"Defeated by {score.deathCause} in {LEVELS[score.deathLevel]}."
            )
            printMe(game, death_text, 380, i * 30 + 40)

    # get networked scores
    if game.retrieve_scores:
        printMe(game, "Global High Scores", 360, 200)
        if len(game.global_hiscores) == 0:
            printMe(game, "No scores found", 360, 230)
        else:
            for i in range(len(game.global_hiscores)):
                score = game.global_hiscores[i]

                # if it's our score, make it yellow!
                color = pygame.Color("WHITE")
                if score.player_name == game.player_name:
                    color = pygame.Color("YELLOW")
                printMe(
                    game,
                    f"{i + 1}. {score.player_name}",
                    360,
                    i * 30 + 230,
                    color=color,
                )
                printMe(
                    game,
                    str(score),
                    360,
                    i * 30 + 240,
                    color=color,
                )
                death_text = f"Defeated by {score.deathCause} in {score.deathLevel}."
                printMe(
                    game,
                    death_text,
                    380,
                    i * 30 + 250,
                    color=color,
                )


def retrieve_scores(game):
    scores = []
    if game.retrieve_scores and game.score_url:
        url = game.score_url + f"/scores?version={game.version}"
        print(f"Retrieving scores from {url}...")
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                scores = response.json()
        except requests.exceptions.Timeout:
            print("Timeout occurred while retrieving scores")
        except Exception as e:
            print(f"Error retrieving scores: {e}")
    print("Retrieved scores!")

    global_hiscores = []
    # save to score objects
    for score in scores:
        global_hiscores.append(
            Score(
                player_name=score["player_name"],
                name=score["character_name"],
                chrClass=score["character_class"],
                deathCause=score["death_cause"],
                deathLevel=score["death_level"],
                maxLevel=int(score["level"]),
                score=int(score["score"]),
            )
        )

    return global_hiscores


def drawDeathScore(game):
    printMe(
        game,
        f"{rankEarned(game) + 1}. {game.player.name}, a Level {game.player.level} {CLASS_NAME[game.player.chrClass]}. Score {game.player.xp}",
        200,
        400,
    )

    printMe(
        game,
        f"Defeated by {game.player.deathCause} in {LEVELS[game.level]}.",
        220,
        410,
    )


def save_scores(game):
    print("Saving hiscores")
    with open("hiscores.dat", "wb") as f:
        hiscores = {"local": game.hiscores, "global": game.global_hiscores}
        pickle.dump(hiscores, f)


def load_scores(game):
    # if file exists, load it
    if os.path.exists("hiscores.dat"):
        loaded_dict = {}
        with open("hiscores.dat", "rb") as f:
            loaded_dict = pickle.load(f)
        if loaded_dict:
            game.hiscores = loaded_dict["local"]
            game.global_hiscores = loaded_dict["global"]


if __name__ == "__main__":
    import main

    main.main()
