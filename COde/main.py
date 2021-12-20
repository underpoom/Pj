from game import Game

g = Game()

while g.running:
    print('0',g.curr_menu.name)
    g.curr_menu.display_menu()
    g.game_loop()