from GameManager import GameManager
from Materials import materials

def main():
    gameManager = GameManager(materials)
    gameManager.print_board()
    while not gameManager.game_is_over:
        user_input = input("WHITE'S TURN: ") if gameManager.current_player == "white" else input("BLACK'S TURN: ")
        gameManager.make_move(user_input)
        if gameManager.made_move:
            gameManager.print_board()
            #gameManager.change_player()

if __name__ == "__main__":
    main()