from GameManager import GameManager
from Materials import materials

def main():
    gameManager = GameManager(materials)
    gameManager.print_board()
    while not gameManager.game_is_over:
        user_input = input("WHITE'S TURN: ") if gameManager.current_player == "white" else input("BLACK'S TURN: ")
        gameManager.make_move(user_input)
        if gameManager.made_move:
            gameManager.change_player()
            if gameManager.is_king_in_check():
                print("CHECK.")
            gameManager.print_board()
            

if __name__ == "__main__":
    main()