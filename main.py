from GameManager import GameManager
from Materials import materials

def main():
    gameManager = GameManager(materials)
    gameManager.print_board()
    while not gameManager.game_is_over:
        # gameManager.is_game_end()
        # if gameManager.game_is_over:
        #     break

        user_input = gameManager.get_user_input()
        gameManager.make_move(user_input)
        if gameManager.made_move:
            if gameManager._GameManager__is_king_in_check(gameManager.get_opponent()):
                print("CHECK.")
            gameManager.print_board()
            # gameManager.change_player()
            
            

if __name__ == "__main__":
    main()