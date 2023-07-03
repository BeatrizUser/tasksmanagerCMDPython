import curses

def print_title(stdscr):
    stdscr.addstr(0, 0, "Lista de Tarefas", curses.A_BOLD)

def print_menu(stdscr, selected_row_idx):
    stdscr.addstr(2, 2, "1. Adicionar Tarefa")
    stdscr.addstr(3, 2, "2. Remover Tarefa")
    stdscr.addstr(4, 2, "3. Marcar/Desmarcar Tarefa")
    stdscr.addstr(5, 2, "4. Visualizar Tarefas")
    stdscr.addstr(6, 2, "5. Sair")

    for idx, row in enumerate(range(2, 7)):
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(row, 0, "  " + str(idx + 1) + ".")
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(row, 0, "  " + str(idx + 1) + ".")

def add_task(stdscr):
    stdscr.clear()
    print_title(stdscr)
    stdscr.addstr(2, 2, "Digite o nome da tarefa:")
    stdscr.refresh()

    curses.echo()  # Habilitar a exibição do texto digitado
    task = stdscr.getstr(3, 2).decode()
    curses.noecho()  # Desabilitar a exibição do texto digitado

    with open("tasks.txt", "a") as f:
        f.write("[ ] " + task + "\n")
    stdscr.addstr(4, 2, "Tarefa adicionada com sucesso!")
    stdscr.refresh()
    stdscr.getch()

def remove_task(stdscr):
    stdscr.clear()
    print_title(stdscr)
    stdscr.addstr(2, 2, "Selecione o número da tarefa a ser removida:")
    tasks = get_tasks()
    for idx, task in enumerate(tasks, start=3):
        stdscr.addstr(idx, 2, "  " + str(idx - 2) + ". " + task)
    selected_task = stdscr.getch() - ord("1")
    if 0 <= selected_task < len(tasks):
        tasks.pop(selected_task)
        with open("tasks.txt", "w") as f:
            for task in tasks:
                f.write(task)
        stdscr.addstr(len(tasks) + 3, 2, "Tarefa removida com sucesso!")
    else:
        stdscr.addstr(len(tasks) + 3, 2, "Tarefa inválida!")
    stdscr.refresh()
    stdscr.getch()

def toggle_task_completion(stdscr):
    stdscr.clear()
    print_title(stdscr)
    stdscr.addstr(2, 2, "Selecione o número da tarefa a ser marcada/desmarcada:")
    tasks = get_tasks()
    for idx, task in enumerate(tasks, start=3):
        task_status = "[X]" if task.startswith("[X]") else "[ ]"
        stdscr.addstr(idx, 2, f"  {task_status}{task[4:]}")
    selected_task = stdscr.getch() - ord("1")
    if 0 <= selected_task < len(tasks):
        task = tasks[selected_task]
        if task.startswith("[X]"):
            tasks[selected_task] = task.replace("[X]", "[ ]", 1)
        else:
            tasks[selected_task] = task.replace("[ ]", "[X]", 1)
        with open("tasks.txt", "w") as f:
            for task in tasks:
                f.write(task)
        stdscr.addstr(len(tasks) + 3, 2, "Tarefa marcada/desmarcada com sucesso!")
    else:
        stdscr.addstr(len(tasks) + 3, 2, "Tarefa inválida!")
    stdscr.refresh()
    stdscr.getch()

def view_tasks(stdscr):
    stdscr.clear()
    print_title(stdscr)
    stdscr.addstr(2, 2, "  Lista de Tarefas:")
    tasks = get_tasks()
    for idx, task in enumerate(tasks, start=3):
        stdscr.addstr(idx, 2, task)
    stdscr.refresh()
    stdscr.getch()

def get_tasks():
    with open("tasks.txt", "r") as f:
        tasks = f.readlines()
    return [task.strip() for task in tasks]

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)

    scr = curses.newwin(8, curses.COLS, curses.LINES // 2 - 4, 0)
    scr.timeout(100)

    current_row_idx = 0

    while True:
        stdscr.clear()

        window_height, window_width = stdscr.getmaxyx()

        if window_height < 8 or window_width < 30:
            stdscr.addstr(0, 0, "A janela é muito pequena. Aumente o tamanho da janela para exibir o conteúdo corretamente.")
            stdscr.refresh()
            stdscr.getch()
            break

        scr.clear()
        scr.refresh()

        print_title(stdscr)
        print_menu(stdscr, current_row_idx)

        footer_text = " Use as teclas de seta para navegar e Enter para selecionar uma opção."
        stdscr.addnstr(window_height - 1, 2, footer_text, window_width - 3)

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < 4:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.clear()
            if current_row_idx == 0:
                add_task(stdscr)
            elif current_row_idx == 1:
                remove_task(stdscr)
            elif current_row_idx == 2:
                toggle_task_completion(stdscr)
            elif current_row_idx == 3:
                view_tasks(stdscr)
            elif current_row_idx == 4:
                break

if __name__ == "__main__":
    curses.wrapper(main)
