import tkinter as tk
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Calculator")
        self.root.geometry("420x620")
        self.root.resizable(False, False)
        self.dark = True
        self.history = []
        self.display_var = tk.StringVar()
        self.create_ui()
        self.root.bind("<Key>", self.keyboard)

    def colors(self):
        if self.dark:
            return {"bg":"#202124","display":"#303134","button":"#3c4043",
                    "special":"#5f6368","operator":"#8ab4f8",
                    "text":"#ffffff","operator_text":"#202124"}
        return {"bg":"#f5f5f5","display":"#ffffff","button":"#e0e0e0",
                "special":"#bdbdbd","operator":"#4285f4",
                "text":"#202124","operator_text":"#ffffff"}

    def create_ui(self):
        c = self.colors()
        self.root.configure(bg=c["bg"])

        header = tk.Frame(self.root, bg=c["bg"])
        header.pack(fill="x", padx=12, pady=10)
        tk.Label(header, text="PYTHON CALCULATOR", font=("Arial",16,"bold"),
                 bg=c["bg"], fg=c["text"]).pack(side="left")
        tk.Button(header, text="☀" if self.dark else "🌙",
                  command=self.toggle_theme, font=("Arial",12),
                  bg=c["special"], fg=c["text"], relief="flat",
                  width=3).pack(side="right")

        self.display = tk.Entry(self.root, textvariable=self.display_var,
                                font=("Arial",28), justify="right",
                                bg=c["display"], fg=c["text"],
                                insertbackground=c["text"], bd=0)
        self.display.pack(fill="x", padx=12, pady=10, ipady=18)

        self.history_label = tk.Label(
            self.root, text="History: No calculations yet",
            font=("Arial",9), anchor="w", bg=c["display"], fg=c["text"])
        self.history_label.pack(fill="x", padx=12, pady=(0,10), ipady=6)

        frame = tk.Frame(self.root, bg=c["bg"])
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        buttons = [
            ["C","⌫","(",")","÷"],
            ["sin","cos","√","%","×"],
            ["7","8","9","x²","−"],
            ["4","5","6","π","+"],
            ["1","2","3",".","="],
            ["0","00","log","ln","AC"]
        ]

        for r in range(6):
            frame.rowconfigure(r, weight=1)
        for col in range(5):
            frame.columnconfigure(col, weight=1)

        for r, row in enumerate(buttons):
            for col, value in enumerate(row):
                if value in ("C","AC","⌫"):
                    bg, fg = c["special"], c["text"]
                elif value in ("÷","×","−","+","=","%","x²"):
                    bg, fg = c["operator"], c["operator_text"]
                else:
                    bg, fg = c["button"], c["text"]

                tk.Button(frame, text=value, font=("Arial",14,"bold"),
                          bg=bg, fg=fg, relief="flat",
                          command=lambda v=value: self.click(v)
                          ).grid(row=r, column=col, sticky="nsew",
                                 padx=3, pady=3)

    def click(self, v):
        if v in ("C","AC"):
            self.display_var.set("")
        elif v == "⌫":
            self.display_var.set(self.display_var.get()[:-1])
        elif v == "=":
            self.calculate()
        else:
            mapping = {"÷":"/","×":"*","−":"-","x²":"**2",
                       "√":"sqrt(","sin":"sin(","cos":"cos(",
                       "log":"log(","ln":"ln(","π":"pi","%":"/100"}
            self.display_var.set(self.display_var.get() + mapping.get(v, v))

    def calculate(self):
        original = self.display_var.get().strip()
        if not original:
            return
        try:
            expr = original.replace("sqrt","math.sqrt")
            expr = expr.replace("sin","math.sin")
            expr = expr.replace("cos","math.cos")
            expr = expr.replace("log","math.log10")
            expr = expr.replace("ln","math.log")
            expr = expr.replace("pi","math.pi")
            result = eval(expr, {"__builtins__": {}}, {"math": math})
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.history.insert(0, f"{original} = {result}")
            self.history = self.history[:3]
            self.display_var.set(str(result))
            self.history_label.config(text="History: " + " | ".join(self.history))
        except ZeroDivisionError:
            self.display_var.set("Cannot divide by 0")
        except Exception:
            self.display_var.set("Error")

    def keyboard(self, event):
        if event.char in "0123456789.+-*/()":
            self.display_var.set(self.display_var.get() + event.char)
        elif event.keysym in ("Return","KP_Enter"):
            self.calculate()
        elif event.keysym == "BackSpace":
            self.display_var.set(self.display_var.get()[:-1])
        elif event.keysym == "Escape":
            self.display_var.set("")

    def toggle_theme(self):
        expression = self.display_var.get()
        self.dark = not self.dark
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_ui()
        self.display_var.set(expression)

root = tk.Tk()
Calculator(root)
root.mainloop()
