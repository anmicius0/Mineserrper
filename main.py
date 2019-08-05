import random
import time
import copy
import os
from termcolor import cprint


def clear():
    os.system('clear')

def welcome():
    """welcome()
    welcome text
    """

    # Introduction
    clear()
    print()
    cprint('Welcome to MineSweeper', 'red')
    cprint('=============================', 'red')
    reset()

def reset():
    """reset()
    show the menu needed before the game
    """

    print('''
    MENU
    =========

    ->Play Again(P)
    ->Read the instructions(R)
    ''')
    choice = input("Type here: ").upper()

    if choice == 'I':
        clear()
        print(open('instructions.txt', 'r').read())
        reset()
    elif choice == "P":
        play()
    else:
        clear()
        reset()

def final(status):
    """final()
    args:
        status: textready to be printed (f"You {status}!")
    """
    cprint(f"You {status}!", 'red')
    reset()

def play():
    """play()
    control the game flow
    """

    s = [[0 for _ in range(9)] for _ in range(9)]
    k = [[' ' for _ in range(9)] for _ in range(9)]

   # place mine
    for _ in range(10):
        s = place_mine(s)

    # place number
    for r in range(9):
        for c in range(9):
            if s[r][c] == '*':
                s = update_number(r, c, s)

    while True:
        # render map
        render_map(k)

        # check win
        if check_win(s,k):
            final('win')

        # get input
        while True:
            chosen = input("Choose a square (eg. E4) or place a marker (eg. mE4): ")

            # check what will happen next
            r,c,action = validate_input(chosen)
            if action == "invalid":
                break
            elif action == "mark":
                k = marker(r,c,k)
                break
            elif  action == "rev":
                k, res = reveal(r,c,k,s)

                # if user step on the bomb
                if res == '*':
                    final('lose')
                
                break


def place_mine(s):
    """place_mine()
    args:
        s: solution grid
    return:
        the new list with new bomb
    """
    r = random.choice(range(9))
    c = random.choice(range(9))

    if s[r][c] != '*':
        s[r][c] = '*'
        return s
    else:
        return place_mine(s)

def update_number(r, c, s):
    """update_number()
    args:
        r: row of bomb
        c: column of bomb
        s: solution grid
    return:
        the new list with new bomb
    """

    # row above
    if r - 1 > -1:

        if c - 1 > -1:
            if s[r-1][c-1] != '*':
                s[r-1][c-1] += 1

        if s[r-1][c] != '*':
            s[r-1][c] += 1

        if c + 1 < 9:
            if s[r-1][c+1] != '*':
                s[r-1][c+1] += 1

    # same row
    if c - 1 > -1:
        if s[r][c-1] != '*':
            s[r][c-1] += 1

    if c + 1 < 9:
        if s[r][c+1] != '*':
            s[r][c+1] += 1

    # row below
    if r + 1 < 9:
        if c - 1 > -1:
            if s[r+1][c-1] != '*':
                s[r+1][c-1] += 1

        if s[r+1][c] != '*':
            s[r+1][c] += 1

        if c + 1 < 9:
            if s[r+1][c+1] != '*':
                s[r+1][c+1] += 1

    # return the new solution grid
    return s

def get_info(r, c, g):
    """get_info()
    args:
        r: row
        c: column
        g: solution grid or known grid
    return:
        the info about that column(in solution grid)
    """
    return g[r][c]

def render_map(k):
    """render_map()
    args:
        k: know grid
        s:solution grid
    """
    clear()
    print('    A   B   C   D   E   F   G   H   I')
    print('  ╔═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╗')
    for r in range(9):
        print(r, '║',get_info(r,0,k),'║',get_info(r,1,k),'║',get_info(r,2,k),'║',get_info(r,3,k),'║',get_info(r,4,k),'║',get_info(r,5,k),'║',get_info(r,6,k),'║',get_info(r,7,k),'║',get_info(r,8,k),'║')
        if r != 8:
            print('  ╠═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╣')
    print('  ╚═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╝')

def marker(r,c,k):
    """get_info()
    args:
        r: row
        c: column
        k: known grid
    return:
        k: new known grid
    """
    if k[r][c] == ' ':
        k[r][c] = '⚐'
    elif k[r][c] == '⚐':
        k[r][c] = ' '
    
    return k

def reveal(r,c,k,s):
    """get_info()
    args:
        r: row
        c: column
        k: known grid
        s: solution grid
    return:
        k: new known grid
        res: an identifier to that play() know what will happen next (⚐/*/' ')
    """
    if k[r][c] == '⚐':
        return k, '⚐'
    elif s[r][c] == '*':
        return k, '*'
    else:
        k[r][c] = s[r][c]
        if s[r][c] == 0:
            return reveal_surrounding(r,c,k,s)

        return k, ' '
        
def reveal_surrounding(r,c,k,s):
    """get_info()
    args:
        r: row
        c: column
        k: known grid
        s: solution grid
    return:
        k: new known grid
    """
    numbers = range(9)

    for tr in range(r-1, r+2):
        for tc in range(c-1, c+2):
            if tr in numbers and tc in numbers:

                if get_info(tr, tc, s)  == 0 and k[tr][tc] != 0:
                    k[tr][tc] = get_info(tr, tc, s)
                    k, _  = reveal_surrounding(tr, tc, k, s)
                
                k[tr][tc] = get_info(tr, tc, s)

    
    return k, ' '

def validate_input(chosen):
    """valid_input():
    args:
        chosen: user's input
    return:
        r: row
        c: column
        action: what should play() do next (mark/rev/invalid)
    """
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h' ,'i']
    numbers = range(9)

    try:
        if len(chosen) == 3 and chosen[0].lower() == 'm' and chosen[1].lower() in letters and int(chosen[2]) in numbers:
            r,c = (int(chosen[2]), letters.index(chosen[1].lower()))
            return r,c,'mark'
        elif len(chosen) == 2 and chosen[0].lower() in letters and int(chosen[1]) in numbers:
            r,c = (int(chosen[1]), letters.index(chosen[0].lower()))
            return r,c,'rev'
        else:
            return 0,0,'invalid'
    except:
        return 0,0,'invalid'

def check_win(s,k):
    """check_win()
    args:
        s: solution grid
        k: known grid
    return:
        boolen: win or not
    """
    flag_counter = 0
    num_counter = 0

    # get info
    for r in range(9):
        for c in range(9):
            if k[r][c] == '⚐' and s[r][c] == '*':
                flag_counter += 1
            elif k[r][c] != '⚐' and k[r][c] != ' ':
                num_counter += 1
    
    # check info
    if num_counter == 71 or flag_counter == 10:
        return True
    else:
        return False


if __name__ == "__main__":
    welcome()