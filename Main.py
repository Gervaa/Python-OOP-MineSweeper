import tkinter as tk
import random

L = 15
H = 10
Bombe = 40
finestra = tk.Tk()
finestra.title("Campo Minato!!")
griglia = []

def clic(evento):
    global griglia
    global H
    global L
    e = evento.widget
    inf = e.grid_info()
    row = inf['row']
    col = inf['column']

    if griglia[row][col]["stringa"] != "⬤" and griglia[row][col]["stringa"] != "0":
        griglia[row][col]["btn"]['text'] = griglia[row][col]["stringa"]
    elif griglia[row][col]["stringa"] == "⬤":
        loss = tk.Button(finestra, bg="red", fg="yellow", text="HAI PERSO!!!")
        loss.grid(row=H, column=0, columnspan=L)
        check_bomb(row, col)
    else:
        scopertura(griglia[row][col]["btn"])
        check_win()

def scopertura(tasto):
    global griglia
    y = tasto.grid_info()['row']
    x = tasto.grid_info()['column']

    if griglia[y][x]["btn"]['text'] == "":
        griglia[y][x]["btn"]['text'] = griglia[y][x]["stringa"]
        if griglia[y][x]["stringa"] == "0":
            if y > 0 and x > 0:
                scopertura(griglia[y - 1][x - 1]["btn"])  # TOP-LEFT
            if y > 0:
                scopertura(griglia[y - 1][x]["btn"])  # TOP
            if y > 0 and x < L - 1:
                scopertura(griglia[y - 1][x + 1]["btn"])  # TOP-LEFT
            if x > 0:
                scopertura(griglia[y][x - 1]["btn"])  # MID-LEFT
            if x < L - 1:
                scopertura(griglia[y][x + 1]["btn"])  # MID-RIGHT
            if y < H - 1 and x > 0:
                scopertura(griglia[y + 1][x - 1]["btn"])  # BOTTOM-LEFT
            if y < H - 1:
                scopertura(griglia[y + 1][x]["btn"])  # BOTTOM
            if y < H - 1 and x < L - 1:
                scopertura(griglia[y + 1][x + 1]["btn"])  # TOP-LEFT

def check_bomb(row, col):
    global griglia
    for x in range(H):
        for y in range(L):
            if griglia[x][y]["stringa"] == "⬤":
                griglia[x][y]["btn"]['text'] = "⬤"
                griglia[x][y]["btn"]['state'] = tk.DISABLED

def check_win():
    global griglia
    clicked_cells = 0
    total_cells = H * L - Bombe
    for x in range(H):
        for y in range(L):
            if griglia[x][y]["btn"]["state"] == tk.NORMAL:
                clicked_cells += 1
    if clicked_cells == total_cells:
        win = tk.Button(finestra, bg="green", fg="white", text="HAI VINTO!!!")
        win.grid(row=H, column=0, columnspan=L)
        for x in range(H):
            for y in range(L):
                if griglia[x][y]["stringa"] == "⬤":
                    griglia[x][y]["btn"]['text'] = "⬤"
                    griglia[x][y]["btn"]['state'] = tk.DISABLED

# Generazione griglia di gioco
for x in range(H):
    griglia.append([])
    for y in range(L):
        griglia[x].append({"btn": tk.Button(finestra, bg="grey", fg="blue", width=4, height=2), "stringa": ""})
        griglia[x][y]["btn"].grid(row=x, column=y)
        griglia[x][y]["btn"].bind('<Button-1>', clic)

# Inserimento delle bombe
for i in range(Bombe):
    ciclo = True
    while ciclo:
        r = random.randint(0, H - 1)
        c = random.randint(0, L - 1)
        if griglia[r][c]["btn"]['text'] != "⬤":
            griglia[r][c]["stringa"] = "⬤"
            ciclo = False

# Calcolo del numero delle bombe adiacenti
for x in range(H):
    for y in range(L):
        if griglia[x][y]["stringa"] != "⬤":
            contatore = 0
            if x > 0 and y > 0:  # NO In alto a sinistra
                if griglia[x - 1][y - 1]["stringa"] == "⬤":  # TOP-LEFT
                    contatore += 1
            if x > 0:  # NO prima riga
                if griglia[x - 1][y]["stringa"] == "⬤":  # TOP
                    contatore += 1
            if x > 0 and y < L - 1:  # NO in  alto a destra
                if griglia[x - 1][y + 1]["stringa"] == "⬤":  # TOP-RIGHT
                    contatore += 1
            if y > 0:
                if griglia[x][y - 1]["stringa"] == "⬤":  # LEFT
                    contatore += 1
            if y < L - 1:
                if griglia[x][y + 1]["stringa"] == "⬤":  # RIGHT
                    contatore += 1
            if x < H - 1 and y > 0:  # NO In basso a sinistra
                if griglia[x + 1][y - 1]["stringa"] == "⬤":  # BOTTOM-LEFT
                    contatore += 1
            if x < H - 1:  # NO ultima riga
                if griglia[x + 1][y]["stringa"] == "⬤":  # BOTTOM
                    contatore += 1
            if x < H - 1 and y < L - 1:  # NO in basso a destra
                if griglia[x + 1][y + 1]["stringa"] == "⬤":  # BOTTOM-RIGHT
                    contatore += 1
            griglia[x][y]["stringa"] = str(contatore)

finestra.mainloop()
