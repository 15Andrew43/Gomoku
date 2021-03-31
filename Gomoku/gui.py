from itertools import product

import pygame
from pygame import Surface

from src.ai import AI, PositionEvaluation
from src.boardstate import BoardState, EndGame

from box import InputBox

import shelve

import os.path


def draw_board(screen: Surface, pos_x: int, pos_y: int, elem_size: int, board: BoardState):
    screen.fill(color)
    dark = (0, 0, 0)
    white = (255, 255, 255)
    line_color = (182, 93, 37)
    screen.blit(InputBox.FONT.render('GOMOKU', True, dark), (0.7 * screen.get_size()[0], 0.1 * screen.get_size()[1]))
    if abs(board.current_player) == 2:
        winner = board.current_player
        screen.blit(InputBox.FONT.render(('black' if winner == -2 else 'white') + ' player won!!!', True, dark), (0.7 * screen.get_size()[0], 0.2 * screen.get_size()[1]))


    for y, x in product(range(14), range(14)):
        position = pos_x + x * elem_size, pos_y + y * elem_size, elem_size, elem_size
        pygame.draw.rect(screen, line_color, position, 2)

    for y, x in product(range(15), range(15)):
        figure = board.board[y, x]

        if figure == 0:
            continue

        if figure > 0:
            figure_color = dark
        else:
            figure_color = white
        r = elem_size * 3 // 8

        pygame.draw.circle(screen, figure_color, ((x + 1) * elem_size, (y + 1) * elem_size), r)




def game_loop(screen: Surface, board: BoardState, ai: AI):
    max_y, max_x = screen.get_size()[1], screen.get_size()[0]
    elem_size = max_y // 16  # размер одной клетки
    save_box = InputBox('SAVE', max_y + (max_x - max_y)*625//10000, max_y * 4 // 5, 250, 30)
    load_box = InputBox('LOAD', max_y + (max_x - max_y) * 625 // 10000, max_y * 4 // 5 + 50, 250, 30)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
            save_name = save_box.handle_event(event)
            load_name = load_box.handle_event(event)

            if save_name:
                db = shelve.open(save_name)
                db[save_name] = board
                db.close()
            elif load_name:
                if os.path.exists(os.path.join(os.getcwd(), load_name + '.db')):
                    db = shelve.open(load_name)
                    board = db[load_name]
                    db.close()
                else:
                    print('No such file:(')

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click_position = event.pos
                to_x, to_y = [(p - elem_size // 2) // elem_size for p in mouse_click_position]

                try:
                    new_board = board.do_move(to_x, to_y)
                except EndGame as EG:
                    print(EG.winner, 'bruh')
                    board = EG.board
                    board.current_player *= 2
                    new_board = None
                if new_board is not None:
                    board = new_board

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print('kek')
                again = True
                while again:
                    try:
                        position_evalution, *move = ai.next_move(board, (0, 0))
                        again = False
                    except TypeError:
                        pass
                move = move[0]
                print(f'my move = {move}')
                try:
                    new_board = board.do_move(move[1], move[0])
                except EndGame as EG:
                    print(EG.winner)
                    board = EG.board
                    board.current_player *= 2
                    new_board = None
                if new_board is not None:
                    board = new_board


        save_box.update()
        load_box.update()
        draw_board(screen, elem_size, elem_size, elem_size, board)
        save_box.draw(screen)
        load_box.draw(screen)
        pygame.display.flip()


pygame.init()

screen: Surface = pygame.display.set_mode([1008, 608])
pygame.display.set_caption("Гомоку")
color = (224, 204, 180)
screen.fill(color)
ai = AI(PositionEvaluation(), search_depth=2)


game_loop(screen, BoardState.initial_state(), ai)

pygame.quit()
