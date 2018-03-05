import curses
import sys

def cursesMain(args):
    stdscr = curses.initscr()
    pad = curses.newpad(200, 100)
    pad_height, pad_width = stdscr.getmaxyx()
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.cbreak()

    stdscr.keypad(True)
    curses.noecho()
    curses.curs_set(0)
    lines = []

    if (len(sys.argv) >= 2):
        filename = sys.argv[1]
    else:
        filename = sys.argv[0]

    with open(filename, "r") as file:
        for line in file:
            lines.append(line)
    textvar = lines[0]
    completed_text = ""
    current_char_pos = 0
    current_char_val = textvar[0]
    current_line_num = 0
    while True:
        is_char_correct = False
        pad.addstr(0, 0, textvar, curses.color_pair(2))
        i = 0
        for item in textvar:
            if item == " ":
                pad.addstr(0, i, item, curses.color_pair(3))
            i += 1

        pad.addstr(0, 0, completed_text, curses.color_pair(1))
        for i in range(current_line_num+1, len(lines)):
            pad.addstr(i-current_line_num, 0, lines[i])

        stdscr.refresh()

        pad.refresh(0, 0, 0, 0, pad_height-1, pad_width-1)
        c = pad.getch()
        # esc
        if c == 27:
            break
        # tab
        if c == 9:
            if textvar[current_char_pos:current_char_pos + 4] == 4*" ":
                # tab key equal 4 spaces
                completed_text += 4*" "
                current_char_pos += 4
                is_char_correct = True
        if c == ord(current_char_val):
            completed_text += current_char_val
            current_char_pos += 1
            is_char_correct = True
        if is_char_correct is True:
            if current_char_pos >= len(textvar):
                current_char_pos = 0
                current_line_num += 1
                if current_line_num >= len(lines):
                    current_line_num = 0
                textvar = lines[current_line_num]
                completed_text = ""
                stdscr.clear()
                pad.clear()
            current_char_val = textvar[current_char_pos]


curses.wrapper(cursesMain)
curses.endwin()
