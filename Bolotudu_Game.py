from tkinter import *
import tkinter.messagebox as mb
from PIL import ImageTk
import sqlite3
import random


class Menu(Tk):
    def __init__(self):
        super().__init__()
        self.start_of_the_prog()

    def start_of_the_prog(self):                # отрисовка меню и всех кнопок
        self.wm_iconphoto(False, ImageTk.PhotoImage(file="Bolotudu_Game/icon.png", master=self))
        self.title('БОЛОТУДУ')
        self.configure(bg="#c29b6b")
        w = 800
        h = 430
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.resizable(False, False)
        self.change_lbl = False
        self.image = ImageTk.PhotoImage(file="Bolotudu_Game/TheChessboard.png", master=self)
        self.lbl_front = Label(self, image=self.image, bg="#c29b6b", font='Areal 14', justify="left",
                               wraplength=550)
        self.lbl_front.place(x=0, y=0)
        lbl_name = Label(self, bg="#c29b6b", text="шашечная игра\nБОЛОТУДУ", font='Arial 20')
        lbl_name.place(x=575, y=40)
        self.btn_startgame = Button(self, bg="#c29b6b", text="Начать игру", font="Arial 12", command=self.new_game)
        self.btn_startgame.place(x=630, y=250)
        self.btn_rule = Button(self, bg="#c29b6b", text="Правила игры", font="Arial 12", command=self.changing_lbl)
        self.btn_rule.place(x=625, y=290)
        self.btn_out = Button(self, bg="#c29b6b", text="Выход", font="Arial 12", command=lambda: exit(0))
        self.btn_out.place(x=652, y=330)

    def changing_lbl(self):         # смена правил игры на иконку шахмат и наоборот
        if self.change_lbl:
            self.lbl_front.configure(image=self.image, text="")
            self.change_lbl = False
            return
        if not self.change_lbl:
            with open('Bolotudu_Game/rules.txt', 'r', encoding='utf8') as file:
                rules = file.read()
                file.close()
            self.lbl_front.configure(image="", text=rules)
            self.change_lbl = True
            return

    def new_game(self):             # кнопка НАЧАТЬ ИГРУ
        self.btn_guest = Button(self, bg="#c29b6b", text="Продолжить как гость", font="Arial 12", command=
        self.start_game_without_user)
        self.btn_enter = Button(self, bg="#c29b6b", text="Войти в профиль", font="Arial 12", command=self.enter)
        self.btn_regist = Button(self, bg="#c29b6b", text="Зарегистрироваться", font="Arial 12",
                                 command=self.register)
        self.btn_back = Button(self, bg="#c29b6b", text="Назад", font="Arial 12", command=self.back)
        self.btn_guest.place(x=595, y=250)
        self.btn_enter.place(x=615, y=290)
        self.btn_regist.place(x=600, y=330)
        self.btn_back.place(x=655, y=370)

    def back(self):                             # кнопка НАЗАД
        self.btn_guest.destroy()
        self.btn_enter.destroy()
        self.btn_regist.destroy()
        self.btn_back.destroy()

    def start_game_without_user(self):          # кнопка ПРОДОЛЖИТЬ КАК ГОСТЬ
        self.withdraw()
        with open("Bolotudu_Game/User.txt", 'r+') as f:
            f.truncate()
        Bolotudu(self)
        self.deiconify()

    def overwrite_user(self, username):
        with open("Bolotudu_Game/User.txt", "w+") as f2:
            f2.truncate()
            f2.write(username)

    def CreateNewUser(self, username, password, password_again):  # проверка на правильное заполнение полей в окне рег.
        if username == '' or password == '' or password_again == '':
            msg = 'Заполните все поля'
            mb.showerror("Ошибка", msg)
        else:
            try:
                f1 = open('Bolotudu_Game/Users.txt', 'r+')
                text = f1.read().split()
                for i in text:
                    if username == i.split(':')[0]:
                        msg = 'Имя пользователя уже существует'
                        mb.showerror("Ошибка", msg)
                        return
                else:
                    if password != password_again:
                        msg = 'Пароли не совпадают'
                        mb.showerror("Ошибка", msg)
                        return
                    else:
                        f1.write(username + ':' + password + ':' + '0' + '\n')
                        self.overwrite_user(username)
                        f1.close()
                        self.window_Reg.destroy()
                        self.withdraw()
                        Bolotudu(self)
                        self.deiconify()
                        return
            except:
                f1 = open('Bolotudu_Game/Users.txt', 'w')
                if password != password_again:
                    msg = 'Пароли не совпадают'
                    mb.showerror("Ошибка", msg)
                    return
                else:
                    f1.write(username + ':' + password + ':' + '0' + '\n')
                    self.overwrite_user(username)
                    f1.close()
                    self.window_Reg.destroy()
                    self.back()
                    self.withdraw()
                    Bolotudu(self)
                    self.deiconify()
                return

    def register(self):                     # отрисовка окна регистрации
        self.window_Reg = Tk()
        self.window_Reg.title('Регистрация')
        self.window_Reg.geometry('300x300')
        self.window_Reg.eval('tk::PlaceWindow . center')
        username_label = Label(self.window_Reg, text='Имя пользователя', )
        username_entry = Entry(self.window_Reg)
        password_label = Label(self.window_Reg, text='Пароль')
        password_entry = Entry(self.window_Reg)
        password_label_confirm = Label(self.window_Reg, text='Повторите пароль')
        password_entry_confirm = Entry(self.window_Reg)
        send_btn = Button(self.window_Reg, text='Зарегистрироваться', command=lambda:
        self.CreateNewUser(username_entry.get(), password_entry.get(), password_entry_confirm.get(), ))
        username_label.pack(padx=10, pady=8)
        username_entry.pack(padx=10, pady=8)
        password_label.pack(padx=10, pady=8)
        password_entry.pack(padx=10, pady=8)
        password_label_confirm.pack(padx=10, pady=8)
        password_entry_confirm.pack(padx=10, pady=8)
        send_btn.pack(padx=10, pady=8)
        self.window_Reg.mainloop()

    def CheckExist(self, username, password):           # проверка на правильность заполнения полей в окне входа
        if username == '' or password == '':
            msg = 'Заполните все поля'
            mb.showerror("Ошибка", msg)
        else:
            try:
                f1 = open('Bolotudu_Game/Users.txt', 'r')
                text = f1.read().split()
                for i in text:
                    if i.split(':')[0] == username:
                        if password == i.split(':')[1]:
                            self.overwrite_user(username)
                            f1.close()
                            self.window_enter.destroy()
                            self.withdraw()
                            Bolotudu(self)
                            self.deiconify()
                            return
                        else:
                            msg = 'Пароль не совпадает'
                            mb.showerror("Ошибка", msg)
                            return
                msg = 'Такой пользователь не зарегестрирован'
                mb.showerror("Ошибка", msg)
                self.window_enter.destroy()
                self.register()
                return
            except:
                msg = 'Еще ни один пользователь не зарегестрирован'
                mb.showerror("Ошибка", msg)
                self.window_enter.destroy()
                self.register()

    def enter(self):                # функция отрисовки окна входа
        self.window_enter = Tk()
        self.window_enter.title('Вход')
        self.window_enter.geometry('300x250')
        self.window_enter.eval('tk::PlaceWindow . center')
        username_label = Label(self.window_enter, text='Имя пользователя', )
        username_entry = Entry(self.window_enter)
        password_label = Label(self.window_enter, text='Пароль')
        password_entry = Entry(self.window_enter)
        send_btn = Button(self.window_enter, text='Войти', command=lambda:
        self.CheckExist(username_entry.get(), password_entry.get()))

        username_label.pack(padx=10, pady=8)
        username_entry.pack(padx=10, pady=8)
        password_label.pack(padx=10, pady=8)
        password_entry.pack(padx=10, pady=8)
        send_btn.pack(padx=10, pady=8)

        self.window_enter.mainloop()


class Bolotudu(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.reload()               # запуски игры

    def reload(self):            # запуск/перезагрузка игры
        self.wm_iconphoto(False, ImageTk.PhotoImage(file="Bolotudu_Game/icon.png"))
        self.title('БОЛОТУДУ')
        self.configure(bg="#c29b6b")
        w = 800
        h = 430
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.resizable(False, False)
        self.first_part = True         # флаг этапа игры (первый этап - раставление, второй - передвижение)
        self.choice = False            # флаг выбрана ли фишка во втором этапе
        self.score = 0                 # очки игрока
        self.zeros = []   # массив в который записываются координаты фишек оппонента для выбора: "которую из них съесть"
        self.player = 1        # кто сейчас играет: 1 - игрок; 2 - компьютер
        self.count = 0           # счетчик фишек для первого этапа игры
        self.count_figur = 0     # счетчик поставленных фишек для перехода во второй этап игры
        self.field = [["ы", "ы", "ы", "ы", "ы", "ы", "ы", "ы"],
                      ["ы", 0, 0, 0, 0, 0, 0, "ы"],
                      ["ы", 0, 0, 0, 0, 0, 0, "ы"],             # поле игры (ы-мусор, 0-путое поле, Х-игрк, О-комп)
                      ["ы", 0, 0, 0, 0, 0, 0, "ы"],
                      ["ы", 0, 0, 0, 0, 0, 0, "ы"],
                      ["ы", 0, 0, 0, 0, 0, 0, "ы"],
                      ["ы", "ы", "ы", "ы", "ы", "ы", "ы", "ы"]]
        self.image1 = ImageTk.PhotoImage(file="Bolotudu_Game/green.png")
        self.image2 = ImageTk.PhotoImage(file="Bolotudu_Game/blue.png")
        self.image3 = ImageTk.PhotoImage(file="Bolotudu_Game/empty.png")
        image_settings = ImageTk.PhotoImage(file="Bolotudu_Game/question_mark.png")
        self.button_help = Button(self, bg="#c29b6b", image=image_settings, command=self.rules)
        self.button_help.place(x=763, y=0)
        lbl_2 = Label(self, bg="#c29b6b", text='<--ИГРОК')
        lbl_1 = Label(self, bg="#c29b6b", text='<--ИИ')
        lbl_2.place(x=595, y=38)
        lbl_1.place(x=740, y=38)
        panel1 = Label(self, bg="#c29b6b", image=self.image1)
        panel2 = Label(self, bg="#c29b6b", image=self.image2)
        panel1.place(x=660, y=0)
        panel2.place(x=515, y=0)
        self.lbl_score = Label(self, bg="#c29b6b", text=f'SCORE:{self.score}', font='Areal 10')
        self.lbl_score.place(x=520, y=90)
        self.lbl_part = Label(self, bg="#c29b6b", text="Сейчас идёт ПЕРВЫЙ этап игры", font='Areal 10')
        self.lbl_part.place(x=520, y=120)
        self.lbl_popup = Label(self, bg="#c29b6b", text='', font='Areal 10', justify='left', wraplength=278)
        self.lbl_popup.place(x=520, y=175)
        lbl_line = Label(self, bg="#c29b6b", text='_'*57)
        lbl_line.place(x=514, y=215)
        lbl_score = Label(self, bg="#c29b6b", text='таблица лидеров', font='Areal 10')
        lbl_score.place(x=610, y=240)
        self.lbl_table_1 = Label(self, bg="#c29b6b", text='', font="Areal 10")
        self.lbl_table_2 = Label(self, bg="#c29b6b", text='', font="Areal 10")
        self.lbl_table_1.place(x=580, y=260)
        self.lbl_table_2.place(x=710, y=260)
        self.table_of_records()
        self.b = []               # заготовка поля из матрицы кнопок для визуала
        for i in range(7):
            self.b.append(i)
            self.b[i] = []
            for j in range(8):
                self.b[i].append(j)
                if (0 < i < 6) and (0 < j < 7):         # выводим только поле размером 5х6 с сохранением координат 7х8
                    self.b[i][j] = Button(self, height=80, width=80, image=self.image3,
                                          command=lambda r=i, c=j: self.click(r, c))
                    self.b[i][j].grid(row=i, column=j)
        self.colour_change()
        self.wait_window(self)

    def rules(self):               # окно с правилами во время игры
        self.button_help.configure(command="")
        rule = Toplevel(self)
        rule.wm_iconphoto(False, ImageTk.PhotoImage(file="Bolotudu_Game/icon.png"))
        rule.title("ПРАВИЛА ИГРЫ")
        rule.geometry("462x330")
        rule.configure(bg="#c29b6b")
        rule.resizable(False, False)
        with open('Bolotudu_Game/rules.txt', 'r', encoding='utf8') as file:
            rules = file.read()
        lbl = Label(rule, bg="#c29b6b", text=rules, font='Areal 12', justify="left", wraplength=460)
        lbl.place(x=0, y=0)

        def quit_window():
            self.button_help.config(command=self.rules)
            rule.destroy()
        rule.protocol("WM_DELETE_WINDOW", quit_window)

    def colour_change(self):        # перекраска поля
        for i in range(1, 6):
            for j in range(1, 7):
                if (i + j) % 2 == 0:
                    self.b[i][j].configure(bg="#dbbb8a")
                else:
                    self.b[i][j].configure(bg="#b38349")
        return

    def change_part(self):              # смена игры из первой части во второую
        if self.count_figur == 12:
            self.win_X = 12
            self.win_O = 12
            self.count_figur = 0
            self.first_part = False
            self.lbl_part.configure(text='Сейчас идёт ВТОРОЙ этап игры')
        return

    def click(self, r, c):         # обработчик кнопок поля
        try:
            self.lbl_popup.configure(text='')
            if self.first_part:        # если идёт первый этап игры
                self.colour_change()
                if not self.check_three_on_line(r, c):
                    self.count += 1
                    self.b[r][c].configure(image=self.image2)
                    self.field[r][c] = 1
                if self.count == 2:
                    self.count = 0
                    self.player = 2
                    self.pc_move()
            else:                     # если не первый этап игры
                self.choice_cell(r, c)
            return
        except Exception as e:
            pass

    def choice_cell(self, r, c):       # второй этап игры
        if len(self.zeros) != 0:       # если несколько вариантов атаки
            for i in self.zeros:
                if i == (r, c):        # если выбранная игроком фишка противника подходит
                    self.b[r][c].configure(image=self.image3)
                    self.field[r][c] = 0
                    self.colour_change()
                    self.score += 50 * len(self.zeros)
                    self.lbl_score.configure(text=f'SCORE:{self.score}')
                    self.zeros = []
                    self.win_X -= 1
                    self.win()
                    self.player = 2
                    self.pc_move()
                    break
            else:
                self.lbl_popup.configure(text='Выберете выделенную фишку противника')
            return
        if not (self.choice):          # выбор своей фишки для хода ею
            if self.field[r][c + 1] != 0 and self.field[r][c - 1] != 0 and self.field[r + 1][c] != 0 \
                    and self.field[r - 1][c] != 0 and self.field[r][c] == 1:
                self.lbl_popup.configure(text='Выбирите другую свободную фишку')
            elif self.field[r][c] == 2:
                self.lbl_popup.configure(text='Это фишка противника.\nВыбирете свою фишку')
            elif self.field[r][c] == 1:
                self.colour_change()
                self.a, self.z = r, c
                self.b[r][c].configure(bg='yellow')
                self.choice = True
        elif self.a == r and self.z == c:   # отменить выбранную фишку
            self.choice = False
            self.colour_change()
        else:                # ход выбранной фишкой
            if (abs(r - self.a) + abs(c - self.z) == 1) and self.player == 1 and self.field[r][c] == 0:
                self.b[r][c].configure(image=self.image2)
                self.field[r][c] = 1
                self.b[self.a][self.z].configure(image=self.image3)
                self.colour_change()
                self.field[self.a][self.z] = 0
                self.zeros = self.check_attack(r, c)
                if len(self.zeros) == 1:         # если под атакой 1 вражеская фишка
                    self.b[self.zeros[0][0]][self.zeros[0][1]].configure(image=self.image3)
                    self.field[self.zeros[0][0]][self.zeros[0][1]] = 0
                    self.zeros = []
                    self.score += 50
                    self.lbl_score.configure(text=f'SCORE:{self.score}')
                    self.win_X -= 1
                    self.win()
                if len(self.zeros) == 0:         # если под атакой нет вражеских фишек
                    self.player = 2
                    self.pc_move()
                else:                            # если под атакой несколько вражеских фишек
                    for i in self.zeros:
                        self.b[i[0]][i[1]].configure(bg='red')
                self.choice = False
            else:
                self.b[self.a][self.z].configure(bg='yellow')
                self.lbl_popup.configure(text='Для передвижения фишки выберете соседнее'
                                              ' поле по вертикали или горизонтали')
        return

    def check_attack(self, r, c):        # проверка на атаку
        zero_nymnym = []
        cross_nymnym = []
        right = 0
        left = 0
        for i in range(c, c + 2):        # проверка наличия фишек игрока/противника справа
            if self.field[r][i + 1] == self.player:
                right += 1
            else:
                break
        for i in range(c, c - 2, -1):    # проверка наличия фишек игрока/противника слева
            if self.field[r][i - 1] == self.player:
                left += 1
            else:
                break
        if right + left >= 2 and self.player == 1:
            if self.field[r][c + right + 1] == 2:
                zero_nymnym.append((r, c + right + 1))
            if self.field[r][c - left - 1] == 2:
                zero_nymnym.append((r, c - left - 1))
        elif right + left >= 2 and self.player == 2:
            if self.field[r][c + right + 1] == 1:
                cross_nymnym.append((r, c + right + 1))
            if self.field[r][c - left - 1] == 1:
                cross_nymnym.append((r, c - left - 1))
        up = 0
        down = 0
        for i in range(r, r + 2):        # проверка наличия фишек игрока/противника снизу
            if self.field[i + 1][c] == self.player:
                down += 1
            else:
                break
        for i in range(r, r - 2, -1):    # проверка наличия фишек игрока/противника сверху
            if self.field[i - 1][c] == self.player:
                up += 1
            else:
                break
        if down + up >= 2 and self.player == 1:
            if self.field[r + down + 1][c] == 2:
                zero_nymnym.append((r + down + 1, c))
            if self.field[r - up - 1][c] == 2:
                zero_nymnym.append((r - up - 1, c))
        elif down + up >= 2 and self.player == 2:
            if self.field[r + down + 1][c] == 1:
                cross_nymnym.append((r + down + 1, c))
            if self.field[r - up - 1][c] == 1:
                cross_nymnym.append((r - up - 1, c))
        if self.player == 1:
            return zero_nymnym
        if self.player == 2:
            return cross_nymnym

    def check_three_on_line(self, r, c):          # проверка на три в ряд в первом этапе игры
        if self.field[r][c] == 0 and self.count < 2:
            if (self.field[r][c - 2] == self.player and self.field[r][c - 1] == self.player) or \
               (self.field[r][c + 1] == self.player and self.field[r][c + 2] == self.player) or \
               (self.field[r][c - 1] == self.player and self.field[r][c + 1] == self.player):     # по горизонтали
                if self.player == 1:            # исход для игрока
                    self.b[r][c].configure(bg="red")
                    self.lbl_popup.configure(text='На первом этапе игры нельзя собирать '
                                                  'три фишки в ряд по вертикали и горизонтали')
                    return True
                if self.player == 2:            # исход для компа
                    return [r, c]
            if (self.field[r + 1][c] == self.player and self.field[r + 2][c] == self.player) or \
               (self.field[r - 1][c] == self.player and self.field[r - 2][c] == self.player) or \
               (self.field[r - 1][c] == self.player and self.field[r + 1][c] == self.player):   # по вертикали
                if self.player == 1:
                    self.b[r][c].configure(bg="red")
                    self.lbl_popup.configure(text='На первом этапе игры нельзя собирать '
                                                  'три фишки в ряд по вертикали и горизонтали')
                    return True
                if self.player == 2:
                    return [r, c]
        elif self.field[r][c] != 0 and self.player == 1:    # если кликнул не на пустое поле
            return True
        elif self.player == 2:
            return
        elif self.player == 1:        # если поле пустое
            return False

    def pc_possiblemove(self):          # поиск фишек которыми может сходить комп
        possiblemove = []
        for i in range(1, 6):
            for j in range(1, 7):
                if self.field[i][j] == self.player and (self.field[i][j + 1] == 0 or self.field[i][j - 1] == 0 or
                                                self.field[i + 1][j] == 0 or self.field[i - 1][j] == 0):
                    possiblemove.append([i, j])
        return  possiblemove

    def pc_move(self):            # ход компьютера
        if self.first_part:       # если первый этап игры
            while self.count < 2:
                choice_field = self.pc_choice()
                if len(choice_field) != 0:     # комп перекрывать фишки игрока => игрок не может сделать тройку
                    move = random.choice(choice_field)
                    self.b[move[0]][move[1]].configure(image=self.image1)
                    self.field[move[0]][move[1]] = 2
                    self.count += 1
                    self.count_figur += 1
                    self.change_part()
                else:
                    if len(self.free_field) != 0:  # комп ставит фишки рядом со своими
                        move = random.choice(self.free_field)
                        self.b[move[0]][move[1]].configure(image=self.image1)
                        self.field[move[0]][move[1]] = 2
                        self.count += 1
                        self.count_figur += 1
                        self.change_part()
                    else:
                        if [3, 3] in self.other_field or [3, 4] in self.other_field:    # если перекрывать нечего и
                            if [3, 3] in self.other_field:
                                field = [[3, 3]]                                     # если нет свободных со своими
                            if [3, 4] in self.other_field:
                                field = [[3, 4]]
                            move = random.choice(field)
                        else:
                            move = random.choice(self.other_field)
                        self.b[move[0]][move[1]].configure(image=self.image1)
                        self.field[move[0]][move[1]] = 2
                        self.count += 1
                        self.count_figur += 1
                        self.change_part()
            else:
                self.player = 1
                self.count = 0
                return
        else:
            choice_usefulmove = self.pc_part_2()
            if len(choice_usefulmove) != 0:         # если есть ходы, которые заберут фишку игрока
                move = random.choice(choice_usefulmove)
                choice_direction = self.direction(move[0], move[1])
                while True:
                    direction = random.choice(choice_direction)     # выбор направления
                    self.field[move[0]][move[1]] = 0
                    if direction == 1 and len(self.check_attack(move[0], move[1] + 1)) != 0:
                        self.field[move[0]][move[1]] = 2
                        break
                    elif direction == 2 and len(self.check_attack(move[0] + 1, move[1])) != 0:
                        self.field[move[0]][move[1]] = 2
                        break
                    elif direction == 3 and len(self.check_attack(move[0], move[1] - 1)) != 0:
                        self.field[move[0]][move[1]] = 2
                        break
                    elif direction == 4 and len(self.check_attack(move[0] - 1, move[1])) != 0:
                        self.field[move[0]][move[1]] = 2
                        break
                self.direction_move(direction, move)        # ход компа
                if direction == 1:
                    cross_nymnym = self.check_attack(move[0], move[1] + 1)
                    self.pc_attack(cross_nymnym)
                    return
                elif direction == 3:
                    cross_nymnym = self.check_attack(move[0], move[1] - 1)
                    self.pc_attack(cross_nymnym)
                    return
                elif direction == 2:
                    cross_nymnym = self.check_attack(move[0] + 1, move[1])
                    self.pc_attack(cross_nymnym)
                    return
                elif direction == 4:
                    cross_nymnym = self.check_attack(move[0] - 1, move[1])
                    self.pc_attack(cross_nymnym)
                    return

            elif len(self.pc_possiblemove()) != 0:
                possiblemove = self.pc_possiblemove()
                move = random.choice(possiblemove)
                direction_choice = self.direction(move[0], move[1])
                direction = random.choice(direction_choice)
                self.direction_move(direction, move)
                self.player = 1
                return
            else:
                self.lbl_popup.configure(text='Противнику некуда ходить.\nХод противника пропускается')
                self.player = 1
                return

    def pc_choice(self):
        self.free_field = []        # поля рядом с фишкой компа
        self.other_field = []       # поля не рядом с фишкой компа и без перекрытия фишек игрока
        pc_choise_field = []        # поля для перекрытия фишек игрока
        for i in range(1, 6):
            for j in range(1, 7):
                if self.field[i][j] == self.field[i][j + 1] == 1:
                    if self.field[i][j - 1] == 0 and not(self.check_three_on_line(i, j - 1)):
                        pc_choise_field.append([i, j - 1])
                    if self.field[i][j + 2] == 0 and not(self.check_three_on_line(i, j + 2)):
                        pc_choise_field.append([i, j + 2])
                if self.field[i][j] == self.field[i + 1][j] == 1:
                    if self.field[i - 1][j] == 0 and not(self.check_three_on_line(i - 1, j)):
                        pc_choise_field.append([i - 1, j])
                    if self.field[i + 2][j] == 0 and not(self.check_three_on_line(i + 2, j)):
                        pc_choise_field.append([i + 2, j])
                if self.field[i][j - 1] == 1 and self.field[i][j + 1] == 1 and self.field[i][j] == 0 and\
                    not(self.check_three_on_line(i, j)):
                    pc_choise_field.append([i, j])
                if self.field[i - 1][j] == 1 and self.field[i + 1][j] == 1 and self.field[i][j] == 0 and\
                        not(self.check_three_on_line(i, j)):
                    pc_choise_field.append([i, j])
        for i in range(1, 6):
            for j in range(1, 7):
                if not([i, j] in pc_choise_field) and not(self.check_three_on_line(i, j)) \
                        and self.field[i][j] == 0 and (self.field[i][j + 1] == 2 or self.field[i][j - 1] == 2
                         or self.field[i + 1][j] == 2 or self.field[i - 1][j] == 2):
                    self.free_field.append([i, j])
                elif len(self.free_field) == 0 and not(self.check_three_on_line(i, j)) and self.field[i][j] == 0:
                    self.other_field.append([i, j])
        return pc_choise_field

    def pc_part_2(self):
        possiblemove = self.pc_possiblemove()   # все возможные ходы
        usefulmove = []                         # все полезные ходы
        left_move = []
        right_move = []
        up_move = []
        down_move = []
        for i in possiblemove:                  # проверка на полезный ход
            if i[1] > 1 and self.field[i[0]][i[1] - 1] == 0:
                self.field[i[0]][i[1]] = 0
                left_move = self.check_attack(i[0], i[1] - 1)
                self.field[i[0]][i[1]] = 2
            if i[1] < 6 and self.field[i[0]][i[1] + 1] == 0:
                self.field[i[0]][i[1]] = 0
                right_move = self.check_attack(i[0], i[1] + 1)
                self.field[i[0]][i[1]] = 2
            if i[0] > 1 and self.field[i[0] - 1][i[1]] == 0:
                self.field[i[0]][i[1]] = 0
                up_move = self.check_attack(i[0] - 1, i[1])
                self.field[i[0]][i[1]] = 2
            if i[0] < 5 and self.field[i[0] + 1][i[1]] == 0:
                self.field[i[0]][i[1]] = 0
                down_move = self.check_attack(i[0] + 1, i[1])
                self.field[i[0]][i[1]] = 2
            if len(left_move) != 0 or len(right_move) != 0 or len(up_move) != 0 or len(down_move) != 0:
                usefulmove.append([i[0], i[1]])
                left_move = right_move = up_move = down_move = []
        return usefulmove

    def direction(self, i, j):          # нахождение стороны направления хода
        choice_direction = []
        if self.field[i][j + 1] == 0:
            choice_direction.append(1)
        if self.field[i + 1][j] == 0:
            choice_direction.append(2)
        if self.field[i][j - 1] == 0:
            choice_direction.append(3)
        if self.field[i - 1][j] == 0:
            choice_direction.append(4)
        return choice_direction

    def direction_move(self, d, move):  # ход компа в выбранную сторону выбранной фишкой
        self.b[move[0]][move[1]].configure(bg="yellow")
        if d == 1:
            self.b[move[0]][move[1] + 1].configure(image=self.image1)
            self.field[move[0]][move[1] + 1] = 2
            self.b[move[0]][move[1] + 1].configure(bg="yellow")
            self.b[move[0]][move[1]].configure(image=self.image3)
            self.field[move[0]][move[1]] = 0
            return
        elif d == 3:
            self.b[move[0]][move[1] - 1].configure(image=self.image1)
            self.field[move[0]][move[1] - 1] = 2
            self.b[move[0]][move[1] - 1].configure(bg="yellow")
            self.b[move[0]][move[1]].configure(image=self.image3)
            self.field[move[0]][move[1]] = 0
            return
        elif d == 2:
            self.b[move[0] + 1][move[1]].configure(image=self.image1)
            self.field[move[0] + 1][move[1]] = 2
            self.b[move[0] + 1][move[1]].configure(bg="yellow")
            self.b[move[0]][move[1]].configure(image=self.image3)
            self.field[move[0]][move[1]] = 0
            return
        elif d == 4:
            self.b[move[0] - 1][move[1]].configure(image=self.image1)
            self.field[move[0] - 1][move[1]] = 2
            self.b[move[0] - 1][move[1]].configure(bg="yellow")
            self.b[move[0]][move[1]].configure(image=self.image3)
            self.field[move[0]][move[1]] = 0
            return

    def pc_attack(self, cross_nymnym):
        cross = random.choice(cross_nymnym)
        self.b[cross[0]][cross[1]].configure(image=self.image3)
        self.b[cross[0]][cross[1]].configure(bg='red')
        self.field[cross[0]][cross[1]] = 0
        if self.score >= 25:
            self.score -= 25
        self.lbl_score.configure(text=f'SCORE:{self.score}')
        self.win_O -= 1
        self.win()
        self.player = 1
        return

    def win(self):         # условия победы
        if self.win_X == 2:
            self.change_table_of_records()
            self.file_sourt()
            self.table_of_records()
            win = mb.askquestion('Игра окончена', f'  Вы выиграли!\n Ваш счет {self.score}\n Начать новую игру?')
            if win == 'yes':
                self.lbl_score.configure(text='0')
                self.reload()
            else:
                self.destroy()

        elif self.win_O == 2:
            self.change_table_of_records()
            self.file_sourt()
            self.table_of_records()
            win = mb.askquestion('Игра окончена', f'Компьютер выиграл\n Ваш счет {self.score}\n Начать новую игру?')
            if win == 'yes':
                self.lbl_score.configure(text='0')
                self.reload()
            else:
                self.destroy()

    def change_table_of_records(self):             # добавление нового результата в таблицу лидеров
        f2 = open("Bolotudu_Game/User.txt", "r")
        text2 = f2.read()
        if len(text2) != 0:
            f1 = open("Bolotudu_Game/Users.txt", "r+")
            text1 = f1.read().split()
            new_text = []
            for i in text1:
                if i.split(":")[0] == text2 and int(i.split(":")[2]) < self.score:
                    new_record = i.rstrip(i.split(":")[2]) + str(self.score)
                    new_text.append(new_record)
                else:
                    new_text.append(i)
            f1.seek(0)
            f1.truncate()
            f1.write('\n'.join(new_text) + '\n')
            f1.close()
            f2.close()
        return

    def file_sourt(self):                      # сортировка лидеров
        f = open('Bolotudu_Game/Users.txt', 'r+')
        text = f.read().split()
        sorted_text = sorted(text, key=lambda x: -int(x.split(':')[2]))
        sorted_text_str = "\n".join(sorted_text)
        f.seek(0)
        f.write(sorted_text_str)
        f.close()
        return

    def table_of_records(self):                  # вывод таблици лидеров
        f = open('Bolotudu_Game/Users.txt', 'r')
        text = f.read().split()
        name_users = [i.split(':')[0] for i in text]
        score_users = [i.split(':')[2] for i in text]
        name_users_str = "\n".join(name_users)
        score_users_str = "\n".join(score_users)
        self.lbl_table_1.configure(text=name_users_str)
        self.lbl_table_2.configure(text=score_users_str)
        f.close()
        return

menu = Menu()
menu.mainloop()
