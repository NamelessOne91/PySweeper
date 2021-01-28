import tkinter as tk
from classes.Game import Minesweeper
from tkinter import messagebox
from pygame import mixer


PROXIMITY_COLORS = {
    1: "grey",
    2: "orange",
    3: "red",
    4: "purple",
    5: "blue"
}

root = tk.Tk()

def create_top_menu():
    menubar = tk.Menu(root)
    menubar.add_command(
        label="Restart", command=lambda: create_game(game.difficulty))

    difficulty_menu = tk.Menu(menubar, tearoff=0)
    difficulty_menu.add_command(
        label="Easy", command=lambda: create_game("easy"))
    difficulty_menu.add_command(
        label="Medium", command=lambda: create_game("medium"))
    difficulty_menu.add_command(        
        label="Hard", command=lambda: create_game("hard"))

    menubar.add_cascade(label="Difficulty", menu=difficulty_menu)

    menubar.add_command(label="Quit", command=root.quit)

    root.config(menu=menubar)


def create_game(difficulty):
    for x in root.winfo_children():
        if type(x) != tk.Menu:
            x.destroy()

    tag = tk.Label(root, text="Mine Sweeper", bg="white", font=(
        "Calibri", 15, "italic"), borderwidth=2, relief="solid")
    tag.pack(fill="x")

    global game
    game = Minesweeper(difficulty)

    global game_frame
    game_frame = tk.Frame(root, width=500, height=500, bg="white")
    game_frame.pack()

    for row in range(game.board.rows):
        for col in range(game.board.columns):
            temp = tk.Button(game_frame, text="", width=3,
                            bg="#9ed8af", height=2, font=("Helvetica", 11))
            temp.grid(row=row, column=col)
            temp.bind("<Button-1>", clicked)
            temp.bind("<Button-3>", flag)

    bar_frame = tk.Frame(root, height=50)
    bar_frame.pack(side="bottom", fill="x")
    global counter_mine
    counter_mine = tk.Label(bar_frame, text=f"Remaining Mines: {game.flags}")
    counter_mine.pack(side="left")

# LEFT CLICK
def clicked(event):
    r = event.widget.grid_info()["row"]
    c = event.widget.grid_info()["column"]

    cell = game.board.field[r][c]

    if cell.is_flagged:
        return

    if cell.is_mine:
        for x, y in game.board.pos_mines:
            game_frame.grid_slaves(x, y)[0].config(
                text="M", fg="red", bg="white", font=("Helvetica", 11, "bold italic"))
        game.gameover = True
        show_gameover_message()
    else:
        show_or_expand(r, c)

    if game.check_victory():
        show_victory_message()


def show_or_expand(r, c):
    if game.check_limits(r, c):
        return

    curr = game.board.field[r][c]
    on_grid = game_frame.grid_slaves(r, c)[0]

    if not curr.is_visible and not curr.is_flagged:

        curr.is_visible = True
        game.decrement_squares_to_win()
        on_grid.config(state="disabled")

        if curr.proximity != 0:
            on_grid.config(text=str(
                curr.proximity), disabledforeground=PROXIMITY_COLORS[curr.proximity], bg="white", font=("Helvetica", 11))
        else:
            on_grid.config(bg="white")
            for x, y in game.SURROUNDINGS:
                show_or_expand(r + x, c + y)


# RIGHT CLICK
def flag(event):
    r = event.widget.grid_info()["row"]
    c = event.widget.grid_info()["column"]

    cell = game.board.field[r][c]

    if not cell.is_visible:
        cell.flag()
        if cell.is_flagged:
            event.widget.config(text="?", fg="red", font=(
                "Helvetica", 11, "bold italic"))
            game.decrement_counter_mines()
        else:
            event.widget.config(text="", font=("Helvetica", 11, "normal"))
            game.increment_counter_mines()
        counter_mine.config(text=f"Remaining Mines: {game.flags}")


def show_victory_message():
    result = messagebox.askyesno(
        "Congratulations", "You won the game !\nOne more game, perhaps ?")
    if result == True:
        create_game(game.difficulty)
    else:
        root.quit()


def show_gameover_message():
    result = messagebox.askyesno(":( ", "BOOM BITCH !\nWant to play again?")
    if result == True:
        create_game(game.difficulty)
    else:
        root.quit()

def main():
    mixer.init()
    mixer.music.load("clock_bg.mp3")
    mixer.music.set_volume(0.10)
    mixer.music.play(-1)

    create_top_menu()
    create_game("easy")
    root.mainloop()

if __name__ == "__main__":
    main()