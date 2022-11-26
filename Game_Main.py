import Project as pj

def main():
    #Initializing the screen
    pj.initial_screen()

    # Initial the game
    gm = pj.game_2048()

    # Refresh the screen
    pg.display.flip()

    pj.game_start(gm)


if __name__ == "__main__":
    main()

