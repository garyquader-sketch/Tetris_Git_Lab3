"""
   #####   ####  #####   ###    #   ####
     #     #       #     #  #      #
 *   #     ###     #     # #    #   ###   *
     #     #       #     #  #   #      #
     #     ####    #     #   #  #  ####

"""

import curses
import board
import time
from scoreboard import ScoreBoard

# Глобальная переменная для таблицы рекордов
scoreboard = ScoreBoard()

# === УЛУЧШЕНИЕ 2: Статистика блоков ===
block_stats = {
    "T": 0,
    "L": 0,
    "S": 0,
    "O": 0,
    "I": 0,
    "J": 0,
    "Z": 0
}

def get_block_type_by_index(block_type_index):
    """Определяет тип блока по индексу"""
    block_types = ["T", "L", "S", "O", "I", "J", "Z"]
    if block_type_index < len(block_types):
        return block_types[block_type_index]
    return "Unknown"

def update_block_stats(block):
    """Обновляет статистику блоков"""
    if hasattr(block, 'block_type'):
        block_name = get_block_type_by_index(block.block_type)
        if block_name in block_stats:
            block_stats[block_name] = block_stats.get(block_name, 0) + 1
# === КОНЕЦ УЛУЧШЕНИЯ 2 ===

BOARD_WIDTH = 11
BOARD_HEIGHT = 17

GAME_WINDOW_WIDTH = 2 * BOARD_WIDTH + 2
GAME_WINDOW_HEIGHT = BOARD_HEIGHT + 2

HELP_WINDOW_WIDTH = 30
HELP_WINDOW_HEIGHT = 10

STATUS_WINDOW_HEIGHT = 24  # Увеличен для статистики
STATUS_WINDOW_WIDTH = HELP_WINDOW_WIDTH

TITLE_HEIGHT = 6

LEFT_MARGIN = 3

TITLE_WIDTH = FOOTER_WIDTH = 62

# Выбор языка (0-английский, 1-русский, 2-немецкий, 3-французский, 4- итальянский)
LANGUAGE = 1

# Загружаем нужный язык
if LANGUAGE == 0:
    from lang_en import messages
elif LANGUAGE == 1:
    from lang_ru import messages
elif LANGUAGE == 2:
    from lang_de import messages
elif LANGUAGE == 3:
    from lang_fr import messages
elif LANGUAGE == 4:
    from lang_it import messages
else:
    from lang_ru import messages

def init_colors():
    """Init colors"""
    try:
        curses.start_color()

        curses.init_pair(99, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(98, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(97, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(96, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(95, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA)

        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_CYAN)

        # === УЛУЧШЕНИЕ 3: Цвета для уровней ===
        curses.init_pair(10, curses.COLOR_GREEN, curses.COLOR_BLACK)      # 1-3 уровень
        curses.init_pair(11, curses.COLOR_YELLOW, curses.COLOR_BLACK)     # 4-6 уровень
        curses.init_pair(12, curses.COLOR_RED, curses.COLOR_BLACK)        # 7-9 уровень
        curses.init_pair(13, curses.COLOR_MAGENTA, curses.COLOR_BLACK)    # 10+ уровень
        # === КОНЕЦ УЛУЧШЕНИЯ 3 ===
    except:
        pass

def get_level_color(level):
    """Возвращает цвет в зависимости от уровня"""
    if level <= 3:
        return curses.color_pair(10)
    elif level <= 6:
        return curses.color_pair(11)
    elif level <= 9:
        return curses.color_pair(12)
    else:
        return curses.color_pair(13)

def init_game_window():
    """Create and return game window"""
    try:
        window = curses.newwin(GAME_WINDOW_HEIGHT, GAME_WINDOW_WIDTH, TITLE_HEIGHT, LEFT_MARGIN)
        window.nodelay(True)
        window.keypad(1)
        return window
    except:
        return None


def init_status_window():
    """Create and return status window"""
    try:
        window = curses.newwin(STATUS_WINDOW_HEIGHT, STATUS_WINDOW_WIDTH, TITLE_HEIGHT, GAME_WINDOW_WIDTH + 5)
        return window
    except:
        return None


def draw_game_window(window):
    """Draw game window"""
    if not window:
        return

    try:
        window.clear()

        # === УЛУЧШЕНИЕ 3: Цветная рамка в зависимости от уровня ===
        level_color = get_level_color(game_board.level)
        window.attron(level_color)
        window.border()
        window.attroff(level_color)
        # === КОНЕЦ УЛУЧШЕНИЯ 3 ===

        # draw board
        for a in range(BOARD_HEIGHT):
            for b in range(BOARD_WIDTH):
                if a < len(game_board.board) and b < len(game_board.board[a]):
                    if game_board.board[a][b] == 1:
                        try:
                            window.addstr(a + 1, 2 * b + 1, "  ", curses.color_pair(96))
                        except:
                            pass
                    else:
                        try:
                            window.addstr(a + 1, 2 * b + 1, " .", curses.color_pair(99))
                        except:
                            pass

        # draw current block
        if game_board.current_block and game_board.current_block_pos:
            try:
                for a in range(game_board.current_block.size()[0]):
                    for b in range(game_board.current_block.size()[1]):
                        if game_board.current_block.shape[a][b] == 1:
                            x = 2 * game_board.current_block_pos[1] + 2 * b + 1
                            y = game_board.current_block_pos[0] + a + 1
                            window.addstr(y, x, "  ", curses.color_pair(game_board.current_block.color))
            except:
                pass

        if game_board.is_game_over():
            go_title = f" {messages['GAME OVER']} "
            ag_title = f" {messages['Enter - play again']} "
            try:
                window.addstr(int(GAME_WINDOW_HEIGHT*.4), (GAME_WINDOW_WIDTH-len(go_title))//2, go_title, curses.color_pair(95))
                window.addstr(int(GAME_WINDOW_HEIGHT*.5), (GAME_WINDOW_WIDTH-len(ag_title))//2, ag_title, curses.color_pair(95))
            except:
                pass

        if pause:
            p_title = f" {messages['Pause']} "
            try:
                window.addstr(int(GAME_WINDOW_HEIGHT * .4), (GAME_WINDOW_WIDTH - len(p_title)) // 2, p_title, curses.color_pair(95))
            except:
                pass

        window.refresh()
    except Exception as e:
        pass


def draw_status_window(window):
    """Draw status window"""
    if not window or game_board.is_game_over():
        return

    try:
        window.clear()
        window.border()

        # Основная информация
        window.addstr(1, 2, f"{messages['Score']}: {game_board.score}")
        window.addstr(2, 2, f"{messages['Lines']}: {game_board.lines}")

        # === УЛУЧШЕНИЕ 3: Цветной уровень ===
        level_text = f"{messages['Level']}: {game_board.level}"
        try:
            level_color = get_level_color(game_board.level)
            window.addstr(3, 2, level_text, level_color)
        except:
            window.addstr(3, 2, level_text)
        # === КОНЕЦ УЛУЧШЕНИЯ 3 ===

        window.addstr(4, 2, f"{messages['Best Score']}: {game_board.best_score}")

        # === УЛУЧШЕНИЕ 1: Счётчик времени игры ===
        if hasattr(game_board, 'start_time') and game_board.start_time:
            elapsed = int(time.time() - game_board.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            time_text = f"{messages['Timer']}: {minutes:02}:{seconds:02}"
            window.addstr(5, 2, time_text)
        # === КОНЕЦ УЛУЧШЕНИЯ 1 ===

        # === УЛУЧШЕНИЕ 2: Статистика блоков ===
        window.addstr(7, 2, messages["Block Stats"] + ":", curses.A_BOLD)
        y_offset = 8
        total = 0
        for block_type, count in block_stats.items():
            if count > 0:
                try:
                    window.addstr(y_offset, 2, f"{block_type}: {count}")
                    y_offset += 1
                    total += count
                except:
                    pass
        if total > 0:
            try:
                window.addstr(y_offset, 2, f"{messages['Total']}: {total}")
            except:
                pass
        # === КОНЕЦ УЛУЧШЕНИЯ 2 ===

        # Следующий блок
        if game_board.next_block:
            try:
                next_y = STATUS_WINDOW_HEIGHT - 5
                start_col = int(STATUS_WINDOW_WIDTH / 2 - len(game_board.next_block.shape[0]))
                window.addstr(next_y - 1, start_col, messages['Next'])

                for row in range(len(game_board.next_block.shape)):
                    for col in range(len(game_board.next_block.shape[0])):
                        if game_board.next_block.shape[row][col] == 1:
                            window.addstr(next_y + row, start_col + 2 * col, "  ",
 curses.color_pair(game_board.next_block.color))
            except:
                pass

        window.refresh()
    except Exception as e:
        pass


def draw_help_window():
    """Draw help window"""
    try:
        window = curses.newwin(HELP_WINDOW_HEIGHT, HELP_WINDOW_WIDTH, TITLE_HEIGHT + STATUS_WINDOW_HEIGHT,
                               GAME_WINDOW_WIDTH + 5)

        window.border()

        window.addstr(1, 2, f"{messages['Move']}    - ← ↓ →")
        window.addstr(2, 2, f"{messages['Drop']}    - space")
        window.addstr(3, 2, f"{messages['Rotate']}  - ↑")
        window.addstr(4, 2, f"{messages['Pause']}   - p")
        window.addstr(5, 2, f"{messages['Quit']}    - q")

        if scoreboard:
            window.addstr(6, 2, f"{messages['High Scores hint']} - H")

        window.refresh()
    except:
        pass


def draw_title():
    """Draw title"""
    try:
        window = curses.newwin(TITLE_HEIGHT, TITLE_WIDTH, 1, LEFT_MARGIN)
        window.addstr(0, 4, "#####  ####  #####  ###    #   ####", curses.color_pair(98))
        window.addstr(1, 4, "  #    #       #    #  #      #", curses.color_pair(98))
        window.addstr(2, 4, "  #    ###     #    # #    #   ###", curses.color_pair(98))
        window.addstr(3, 4, "  #    #       #    #  #   #      #", curses.color_pair(98))
        window.addstr(4, 4, "  #    ####    #    #   #  #  ####", curses.color_pair(98))

        window.refresh()
    except:
        pass


def draw_footer():
    """Draw footer"""
    try:
        window = curses.newwin(1, FOOTER_WIDTH, TITLE_HEIGHT + GAME_WINDOW_HEIGHT + 1, LEFT_MARGIN)
        title = messages["Made with"]
        col_pos = int((GAME_WINDOW_WIDTH + STATUS_WINDOW_WIDTH - len(title) + 1) / 2)
        window.addstr(0, col_pos, title, curses.color_pair(98))
        window.addstr(0, col_pos + len(title) + 1, "❤", curses.color_pair(97))
        window.refresh()
    except:
        pass


def show_high_scores(stdscr):
    """Отображает таблицу лучших результатов"""
    if not scoreboard:
        return

    try:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        title = messages.get('High Scores', 'HIGH SCORES')
        title_x = (width - len(title)) // 2
        try:
            stdscr.addstr(2, title_x, title, curses.color_pair(98) | curses.A_BOLD)
        except:
            stdscr.addstr(2, title_x, title)

        scores = scoreboard.get_top_scores(10)

        if not scores:
            msg = messages.get('No scores yet', 'No scores yet')
            msg_x = (width - len(msg)) // 2
            stdscr.addstr(5, msg_x, msg, curses.color_pair(99))
        else:
            headers = [
                messages.get('Name', 'Name'),
                messages.get('Points', 'Points'),
                messages.get('Date', 'Date'),
                messages.get('Time', 'Time')
            ]
            col1_x = 5
            col2_x = 25
            col3_x = 45
            col4_x = 65

            try:
                stdscr.addstr(4, col1_x, headers[0], curses.A_BOLD)
                stdscr.addstr(4, col2_x, headers[1], curses.A_BOLD)
                stdscr.addstr(4, col3_x, headers[2], curses.A_BOLD)
                stdscr.addstr(4, col4_x, headers[3], curses.A_BOLD)
            except:
                pass

            for i, record in enumerate(scores):
                y = 6 + i
                if y >= height - 3:
                    break

                name = record.get('name', 'Unknown')[:15]
                score = str(record.get('score', 0))
                date = record.get('date', '')
                time_str = record.get('time', '')

                try:
                    stdscr.addstr(y, col1_x, f"{i + 1}. {name}")
                    stdscr.addstr(y, col2_x, score)
                    stdscr.addstr(y, col3_x, date)
                    stdscr.addstr(y, col4_x, time_str)
                except:
                    pass

        footer = messages.get('Back to game', 'Press any key to continue')
        footer_x = (width - len(footer)) // 2
        stdscr.addstr(height - 2, footer_x, footer, curses.color_pair(99))

        stdscr.refresh()
        stdscr.getch()
        stdscr.clear()

        draw_title()
        draw_footer()
        draw_help_window()
        if game_window:
            draw_game_window(game_window)
        if status_window:
            draw_status_window(status_window)

    except Exception as e:
        pass


def enter_name(stdscr, score):
    """Ввод имени игрока для сохранения рекорда"""
    if not scoreboard:
        return False

    try:
        curses.echo()
        curses.curs_set(1)

        height, width = stdscr.getmaxyx()
        stdscr.clear()

        msg = f"{messages.get('Enter your name', 'Enter your name')} ({messages.get('Points', 'Points')}: {score})"
        msg_x = (width - len(msg)) // 2
        stdscr.addstr(height // 2 - 2, msg_x, msg, curses.color_pair(98))

        prompt = f"{messages.get('Name', 'Name')}: "
        prompt_x = (width - 30) // 2
        stdscr.addstr(height // 2, prompt_x, prompt)

        input_y = height // 2
        input_x = prompt_x + len(prompt)

        stdscr.refresh()
        name = stdscr.getstr(input_y, input_x, 20).decode('utf-8')

        if not name.strip():
            name = "Player"

        curses.noecho()
        curses.curs_set(0)
        stdscr.clear()

        scoreboard.add_score(name.strip(), score)
        return True
    except Exception as e:
        curses.noecho()
        curses.curs_set(0)
        return False


# Глобальные переменные
pause = False
game_board = board.Board(BOARD_HEIGHT, BOARD_WIDTH)
game_board.start()

# === УЛУЧШЕНИЕ 1: Добавляем время старта ===
game_board.start_time = time.time()
# === КОНЕЦ УЛУЧШЕНИЯ 1 ===

old_score = game_board.score
game_over_shown = False
last_block = None  # Считаем экземпляры фигур, включая одинаковые подряд

# Глобальные ссылки на окна
game_window = None
status_window = None

if __name__ == "__main__":
    try:
        scr = curses.initscr()
        height, width = scr.getmaxyx()
        if height < 40 or width < 80:
            raise RuntimeError("Увеличьте терминал минимум до 80 столбцов и 40 строк")
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        if curses.has_colors():
            curses.start_color()

        init_colors()

        draw_title()
        draw_footer()
        draw_help_window()

        game_window = init_game_window()
        status_window = init_status_window()

        if game_window:
            draw_game_window(game_window)
        if status_window:
            draw_status_window(status_window)

        start = time.time()
        last_status_second = -1
        quit_game = False

        while not quit_game:
            if game_window:
                key_event = game_window.getch()
            else:
                key_event = -1

            if key_event == ord('h') or key_event == ord('H'):
                show_high_scores(scr)
                continue

            if key_event == curses.KEY_RESIZE:
                draw_footer()
                draw_help_window()
                if game_window:
                    draw_game_window(game_window)

            if key_event == ord("q"):
                quit_game = True

            if not game_board.is_game_over():
                game_over_shown = False
                if not pause:
                    if time.time() - start >= 1 / game_board.level:
                        game_board.move_block("down")
                        start = time.time()

                    if key_event == curses.KEY_UP:
                        game_board.rotate_block()
                    elif key_event == curses.KEY_DOWN:
                        game_board.move_block("down")
                    elif key_event == curses.KEY_LEFT:
                        game_board.move_block("left")
                    elif key_event == curses.KEY_RIGHT:
                        game_board.move_block("right")
                    elif key_event == ord(" "):
                        game_board.drop()
                if key_event == ord("p"):
                    pause = not pause
                    if game_window:
                        game_window.nodelay(not pause)
            else:
                if game_window:
                    game_window.nodelay(False)

                if not game_over_shown and game_board.score > 0 and scoreboard:
                    if scoreboard.is_high_score(game_board.score):
                        enter_name(scr, game_board.score)
                        if status_window:
                            draw_status_window(status_window)
                    game_over_shown = True

                if key_event == ord("\n"):
                    game_board.start()
                    # === УЛУЧШЕНИЕ 1: Сбрасываем время ===
                    game_board.start_time = time.time()
                    # === УЛУЧШЕНИЕ 2: Сбрасываем статистику блоков ===
                    for key in block_stats:
                        block_stats[key] = 0
                    last_block = None
                    old_score = -1
                    start = time.time()
                    # === КОНЕЦ УЛУЧШЕНИЙ ===
                    if game_window:
                        game_window.nodelay(True)
                    pause = False
                    game_over_shown = False
                    if status_window:
                        draw_status_window(status_window)

            if game_window:
                draw_game_window(game_window)

            # === УЛУЧШЕНИЕ 2: Обновляем статистику блоков ===
            if game_board.current_block and hasattr(game_board.current_block, 'block_type'):
                current_type = game_board.current_block.block_type
                if game_board.current_block is not last_block:
                    block_name = get_block_type_by_index(current_type)
                    if block_name in block_stats:
                        block_stats[block_name] += 1
                        if status_window:
                            draw_status_window(status_window)
                    last_block = game_board.current_block
            # === КОНЕЦ УЛУЧШЕНИЯ 2 ===

            status_second = int(time.time() - game_board.start_time)
            if status_second != last_status_second and status_window:
                draw_status_window(status_window)
                last_status_second = status_second
            time.sleep(0.01)

            if old_score != game_board.score and status_window:
                draw_status_window(status_window)
                old_score = game_board.score

    except Exception as e:
        curses.endwin()
        print(f"Ошибка запуска игры: {e}")
    finally:
        curses.endwin()
