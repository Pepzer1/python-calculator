import customtkinter
import re
import tkinter


import re


class Calculate:
    def __init__(self):
        # Сопоставление операторов с функциями
        self.operations = {
            "+": self.add,
            "-": self.sub,
            "*": self.mul,
            "/": self.div,
            "^": self.pows,
        }
        self.history = []

    # История выражений и результатов
    def add_to_history(self, expr, result):
        self.history.insert(0, (expr, result))

    def get_last_ans(self):
        return self.history[0][1] if self.history else "empty"

    # Операции
    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

    def mul(self, a, b):
        return a * b

    def div(self, a, b):
        if b == 0:
            raise ZeroDivisionError("division by zero")
        return a / b

    def pows(self, a, b=None):
        return a**a if b is None else a**b

    # ------------------------------------------
    # 🔹 Разбор выражения: превращение строки в токены
    # ------------------------------------------
    def parse_expr(self, expr: str) -> list[str]:
        # Разделяем на числа и операторы
        tokens = re.findall(r"\d+(?:\.\d+)?|[+\-*/^]", expr)
        parsed_tokens = []
        i = 0

        # Обработка унарного минуса в начале
        if tokens and tokens[0] == "-":
            parsed_tokens.append(str(-float(tokens[1])))
            i = 2

        # Основной цикл разбора выражения
        while i < len(tokens):
            if (
                tokens[i] in self.operations
                and i + 2 < len(tokens)
                and tokens[i + 1] == "-"
            ):
                # Обработка унарного минуса после оператора
                parsed_tokens.append(tokens[i])
                parsed_tokens.append(str(-float(tokens[i + 2])))
                i += 3
            else:
                parsed_tokens.append(tokens[i])
                i += 1
        return parsed_tokens

    # ------------------------------------------
    # 🔹 Степени (самый высокий приоритет)
    # ------------------------------------------
    def parse_pow(self, tokens: list[str]) -> list[str]:
        output = []
        i = len(tokens) - 1

        while i >= 0:
            token = tokens[i]
            if token.replace(".", "", 1).isdigit():
                base = float(token)
                # Объединяем цепочку степеней справа налево
                while i - 2 >= 0 and tokens[i - 1] == "^":
                    exp = float(tokens[i - 2])
                    base = self.operations["^"](exp, base)
                    i -= 2
                output.insert(0, str(base))
            else:
                output.insert(0, token)
            i -= 1
        return output

    # ------------------------------------------
    # 🔹 Умножение и деление (средний приоритет)
    # ------------------------------------------
    def parse_mul_div(self, tokens: list[str]) -> list[str]:
        output = []
        i = 0

        while i < len(tokens):
            token = tokens[i]
            if token.replace(".", "", 1).isdigit():
                value = float(token)
                # Объединяем цепочку *, /
                while i + 2 < len(tokens) and tokens[i + 1] in ("*", "/"):
                    op = tokens[i + 1]
                    next_val = float(tokens[i + 2])
                    value = self.operations[op](value, next_val)
                    i += 2
                output.append(str(value))
            else:
                output.append(token)
            i += 1
        return output

    # ------------------------------------------
    # 🔹 Сложение и вычитание (низший приоритет)
    # ------------------------------------------
    def parse_add_sub(self, tokens: list[str]) -> float:
        result = float(tokens[0])
        i = 1
        while i + 1 < len(tokens):
            op = tokens[i]
            value = float(tokens[i + 1])
            result = self.operations[op](result, value)
            i += 2
        return result

    # ------------------------------------------
    # 🔹 Финальная обработка выражения
    # ------------------------------------------
    def calc(self, expr: str) -> float:
        tokens = self.parse_expr(expr)

        if "^" in tokens:
            tokens = self.parse_pow(tokens)

        if "*" in tokens or "/" in tokens:
            tokens = self.parse_mul_div(tokens)

        return self.parse_add_sub(tokens)

    # ------------------------------------------
    # 🔹 Обработка скобок и замена ans
    # ------------------------------------------
    def simplify(self, expr: str) -> str:
        if "ans" in expr:
            expr = expr.replace("ans", str(self.get_last_ans()))

        # Рекурсивная замена скобок на значения
        while "(" in expr:
            open_indices = []
            for i, char in enumerate(expr):
                if char == "(":
                    open_indices.append(i)
                elif char == ")":
                    start = open_indices.pop()
                    inner = expr[start + 1 : i]
                    result = str(float(self.calc(inner)))

                    # Обработка минуса перед скобкой: -(...)
                    if start > 0 and expr[start - 1] == "-":
                        result = str(-float(result))
                        expr = expr[: start - 1] + result + expr[i + 1 :]
                    else:
                        expr = expr[:start] + result + expr[i + 1 :]
                    break
        return expr


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__(fg_color="#2B2D31")
        self.sidebar_width = 200
        self.main_width = 400
        self.height = 550

        self.title("Calculator")
        self.geometry(f"{self.main_width}x{self.height}")
        self.calc_engine = Calculate()

        # 🔹 Новый контейнер для всех "основных" фреймов
        self.main_panel = customtkinter.CTkFrame(self, fg_color="#2B2D31")
        self.main_panel.pack(side="left", fill="both", expand=True)
        self.display_frame = DisplayFrame(self.main_panel)
        # 🔹 Отдельно боковая панель, пока скрыта
        self.display_frame.pack(pady=10, fill="x")
        self.sidebar_frame = SidebarPanel(
            self,
            self.display_frame,
            self.calc_engine,
        )  # self — это CTk-окно (родитель)
        # не вызываем pack здесь — будет вызываться при нажатии на кнопку

        self.control_frame = ControlFrame(
            self.main_panel, self.display_frame, self.sidebar_frame, self
        )
        self.control_frame.pack(pady=5, fill="x")

        self.buttons_frame = ButtonsFrame(
            self.main_panel,
            self.display_frame,
            self.calc_engine,
            self.sidebar_frame,
            self,
        )
        self.buttons_frame.pack(pady=5, fill="x")

        self.bind("<Key>", self.buttons_frame.handle_keypress)


class DisplayFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, height=100, fg_color="#2B2D31")
        self.result_displayed = False

        self.expression = customtkinter.StringVar()
        self.entry = customtkinter.CTkEntry(
            self,
            placeholder_text="Enter smth...",
            textvariable=self.expression,
            font=("JetBrains Mono", 24),
            justify="right",
            height=100,
            text_color="#D0BCFF",
            fg_color="#464850",
        )
        self.entry.pack(fill="x", padx=10)
        self.entry.configure(state="readonly")

        self.entry.bind("<FocusIn>", lambda e: self.focus())  # снимаем фокус
        self.entry.bind("<Button-1>", lambda e: "break")  # блок клика
        self.entry.bind("<Key>", lambda e: "break")  # блок клавиш

    def get_expression(self):
        return self.expression.get()

    def append_expression(self, value):
        operators = set("+-*/^")  # перечень операторов, можно расширить
        if self.result_displayed:
            if value in operators:
                # если ввод оператор — добавляем к результату, флаг сбрасывать не надо
                self.expression.set(self.expression.get() + value)
            else:
                # если ввод не оператор (число, точка и т.п.) — очищаем и начинаем новое число
                self.expression.set(value)
            self.result_displayed = False
        else:
            current = self.expression.get()
            self.expression.set(current + value)

    def some_clear(self):
        current_val = self.expression.get()
        current_val = current_val[:-1]
        self.expression.set(current_val)

    def clear_expression(self):
        self.expression.set("")

    def set_result_displayed(self, val: bool):
        self.result_displayed = val


class ButtonsFrame(customtkinter.CTkFrame):

    def __init__(self, parent, display_frame, calc_engine, sidebar_frame, app):
        super().__init__(parent, fg_color="#2A2B31")
        self.display = display_frame
        self.calc_engine = calc_engine
        self.sidebar_frame = sidebar_frame
        self.app = app
        buttons = [
            "7",
            "8",
            "9",
            "/",
            "4",
            "5",
            "6",
            "*",
            "1",
            "2",
            "3",
            "+",
            "ans",
            "0",
            ".",
            "-",
            "(",
            ")",
            "=",
            "^",
        ]
        for i in range(len(buttons)):
            btn_text = buttons[i]
            button = customtkinter.CTkButton(
                self,
                command=lambda t=btn_text: self.on_button_click(t),
                text=btn_text,
                fg_color="#3E4C5A",
                width=90,
                height=60,
                border_color="#3E4C5A",
                hover_color="#2D3B4F",
                text_color="#D0BCFF",
                font=("JetBrains Mono", 24),
            )
            button.grid(row=i // 4, column=i % 4, padx=5, pady=5)

    def handle_keypress(self, event):
        allowed_chars = set("0123456789.+-*/^")
        keysym_to_char = {
            "0": "0",
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4",
            "5": "5",
            "6": "6",
            "7": "7",
            "8": "8",
            "9": "9",
            "KP_1": "1",
            "KP_2": "2",
            "KP_3": "3",
            "KP_4": "4",
            "KP_5": "5",
            "KP_6": "6",
            "KP_7": "7",
            "KP_8": "8",
            "KP_9": "9",
            "KP_0": "0",
            "period": ".",
            "KP_Decimal": ".",
            "plus": "+",
            "KP_Add": "+",
            "minus": "-",
            "KP_Subtract": "-",
            "slash": "/",
            "KP_Divide": "/",
            "asterisk": "*",
            "KP_Multiply": "*",
            "asciicircum": "^",
            "parenleft": "(",
            "parenright": ")",
            "KP_Enter": "=",
            "Return": "=",
            "Delete": "clear",
            "BackSpace": "sclear",
            "Escape": "quit",
        }
        key = keysym_to_char.get(event.keysym)
        match key:
            case k if k in allowed_chars:
                self.display.append_expression(k)
            case "=":
                self.on_button_click("=")
            case "sclear":
                self.display.some_clear()
            case "clear":
                self.display.clear_expression()
            case "quit":
                self.app.destroy()

    def on_button_click(self, text):
        if text == "=":
            try:
                expr = self.display.get_expression()
                simplified_expr = self.calc_engine.simplify(expr)
                result = self.calc_engine.calc(simplified_expr)  # убираем int()

                if result.is_integer():
                    result = int(result)
                if abs(result) > 1_000_000_000_000:
                    result = "{:.6e}".format(result)

                self.calc_engine.add_to_history(expr, str(result))

                self.display.expression.set(str(result))
                self.display.result_displayed = True
                self.sidebar_frame.print_history()

            except Exception as e:
                self.display.expression.set(f"Error: {e}")
                self.display.result_displayed = True

        elif text == "ans":
            last_ans = self.calc_engine.get_last_ans()
            if last_ans != "empty":
                self.display.append_expression(str(last_ans))
        else:
            self.display.append_expression(text)


class SidebarPanel(customtkinter.CTkFrame):
    def __init__(
        self,
        app,
        display_frame,
        calc_engine,
        width=200,
    ):
        super().__init__(app, width=width, fg_color="#2A2B31")

        self.app = app
        self.sidebar_visible = False
        self.calc_engine = calc_engine
        self.pack_propagate(False)
        self.display = display_frame
        # Контейнер для свитча и лейбла
        top_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        top_frame.pack(pady=10, fill="x", padx=10)
        self.switch_var = tkinter.BooleanVar(value=False)
        # Переключатель
        self.switch = customtkinter.CTkSwitch(
            top_frame,
            text="Result",
            text_color="#D0BCFF",
            progress_color="#B69DF8",
            variable=self.switch_var,
            command=self.switch_callback,
        )
        self.switch.pack(side="bottom", padx=(30, 0))

        # Лейбл "История"
        self.history_label = customtkinter.CTkLabel(
            top_frame,
            text="History",
            font=customtkinter.CTkFont(size=14, weight="bold"),
            text_color="#D0BCFF",
        )
        self.history_label.pack(side="top", padx=10)
        self.scrollable_history = customtkinter.CTkScrollableFrame(
            self,
            fg_color="#3A3B41",
        )
        self.scrollable_history.pack(fill="both", expand=True)

    def print_history(self):
        # Очистка предыдущих записей
        for widget in self.scrollable_history.winfo_children():
            widget.destroy()

        # Добавляем новые записи истории
        if self.calc_engine.history:
            for expr, result in self.calc_engine.history:
                copy_hist_btn = customtkinter.CTkButton(
                    self.scrollable_history,
                    text=f"{expr} = {result}",
                    text_color="#D0BCFF",
                    font=customtkinter.CTkFont(size=18),
                    command=lambda e=expr, r=result, s=self.switch_var: self.expr_onclick(
                        e, r, s
                    ),
                    fg_color="#3A3B41",
                    hover_color="#3A3B41",
                )
                copy_hist_btn.pack(anchor="w", pady=2)

    def expr_onclick(self, expr, result, switch):
        if switch.get():
            self.display.expression.set(expr)

        else:
            self.display.expression.set(result)

        self.display.set_result_displayed(False)

    def switch_callback(
        self,
    ):
        if self.switch_var.get():
            self.switch.configure(text="Expression")
        else:
            self.switch.configure(text="Result")

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.pack_forget()
        else:
            self.pack(side="left", fill="y")
        self.sidebar_visible = not self.sidebar_visible
        self.update_window_size()

    def update_window_size(self):
        width = self.app.main_width
        if self.sidebar_visible:
            width += self.app.sidebar_width
        self.app.geometry(f"{width}x{self.app.height}")


class ControlFrame(customtkinter.CTkFrame):
    def __init__(self, parent, display_frame, sidebar_frame, app):
        super().__init__(parent, fg_color="#2A2B31")
        self.app = app
        self.display = display_frame
        self.sidebar_frame = sidebar_frame
        history_btn = customtkinter.CTkButton(
            self,
            text="📜 history",
            fg_color="#3E4C5A",
            width=67,
            height=60,
            text_color="#D0BCFF",
            command=self.sidebar_frame.toggle_sidebar,
            hover_color="#2D3B4F",
            font=customtkinter.CTkFont(size=17),
        )
        history_btn.pack(side="right", padx=5)

        exit_btn = customtkinter.CTkButton(
            self,
            text="❌ Exit",
            command=self.app.destroy,
            fg_color="#3E4C5A",
            hover_color="#732027",
            width=67,
            height=60,
            text_color="#D0BCFF",
            font=customtkinter.CTkFont(size=17),
        )

        exit_btn.pack(side="left", padx=5)

        copy_btn = customtkinter.CTkButton(
            self,
            text="📋 Copy",
            fg_color="#3E4C5A",
            width=67,
            height=60,
            text_color="#D0BCFF",
            command=self.copy_entry_text,
            hover_color="#2D3B4F",
            font=customtkinter.CTkFont(size=16),
        )
        copy_btn.pack(side="left", padx=5)

        back_btn = customtkinter.CTkButton(
            self,
            text="⌫",
            fg_color="#3E4C5A",
            width=67,
            height=60,
            text_color="#D0BCFF",
            command=self.display.some_clear,
            hover_color="#2D3B4F",
            font=customtkinter.CTkFont(size=25),
        )
        back_btn.pack(side="right", padx=5)

        clear_btn = customtkinter.CTkButton(
            self,
            text="🧹 ",
            fg_color="#3E4C5A",
            width=67,
            height=60,
            text_color="#D0BCFF",
            command=self.display.clear_expression,
            hover_color="#2D3B4F",
            font=customtkinter.CTkFont(size=25),
        )
        clear_btn.pack(side="right", padx=5)

    def copy_entry_text(self, event=None):
        text = self.display.get_expression()
        app.clipboard_clear()
        app.clipboard_append(text)
        app.update()


app = App()
app.mainloop()
