import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
import os
from quiz_data import quiz_data

username = ""
leaderboard_file = "leaderboard.txt"
current_question = 0
score = 0

def save_score():
    global username, score
    with open(leaderboard_file, "a") as file:
        file.write(f"{username}: {score}/{len(quiz_data)}\n")

def show_leaderboard():
    root.withdraw()
    leaderboard_window = tk.Toplevel()
    leaderboard_window.title("Leaderboard")
    leaderboard_window.geometry("400x400")
    style = Style(theme="flatly")

    title_label = ttk.Label(
        leaderboard_window,
        text="Leaderboard",
        font=("Helvetica", 20),
        anchor="center",
    )
    title_label.pack(pady=10)

    if os.path.exists(leaderboard_file):
        with open(leaderboard_file, "r") as file:
            scores = file.readlines()
    else:
        scores = ["No scores available yet.\n"]

    global leaderboard_text
    leaderboard_text = tk.Text(
        leaderboard_window,
        height=15,
        width=40,
        font=("Helvetica", 12),
    )
    leaderboard_text.pack(pady=10)
    leaderboard_text.insert("1.0", "".join(scores))
    leaderboard_text.config(state="disabled")

    clear_btn = ttk.Button(
        leaderboard_window,
        text="Clear Leaderboard",
        command=clear_leaderboard,
        style="danger.TButton",
    )
    clear_btn.pack(pady=10)

    close_btn = ttk.Button(
        leaderboard_window,
        text="Close",
        command=lambda: (leaderboard_window.destroy(), root.deiconify()),
    )
    close_btn.pack(pady=10)

def clear_leaderboard():
    if os.path.exists(leaderboard_file):
        with open(leaderboard_file, "w") as file:
            pass
        messagebox.showinfo("Leaderboard Cleared", "All scores have been cleared!")
        leaderboard_text.config(state="normal")
        leaderboard_text.delete("1.0", "end")
        leaderboard_text.insert("1.0", "No scores available yet.\n")
        leaderboard_text.config(state="disabled")
    else:
        messagebox.showwarning("Error", "No leaderboard file found!")

def login_screen():
    login_window = tk.Toplevel()
    login_window.title("Login")
    login_window.geometry("400x300")
    style = Style(theme="flatly")

    title_label = ttk.Label(
        login_window,
        text="Enter your name:",
        font=("Helvetica", 18),
        anchor="center",
    )
    title_label.pack(pady=20)

    name_entry = ttk.Entry(
        login_window,
        font=("Helvetica", 14),
        justify="center",
    )
    name_entry.pack(pady=10)

    def start_quiz():
        global username
        username = name_entry.get()
        if username.strip():
            login_window.destroy()
            show_question()
        else:
            messagebox.showwarning("Input Error", "Please enter your name!")

    start_btn = ttk.Button(
        login_window,
        text="Start Quiz",
        command=start_quiz,
    )
    start_btn.pack(pady=20)

def show_question():
    global current_question, score

    question = quiz_data[current_question]
    qs_label.config(text=question["question"])

    choices = question["choices"]
    for i in range(4):  # Only 4 choices per question
        choice_btns[i].config(text=choices[i], state="normal")

    feedback_label.config(text="")
    next_btn.config(state="disabled")

    score_label.config(text=f"Score: {score}/{len(quiz_data)}")

def check_answer(choice):
    global score
    question = quiz_data[current_question]
    selected_choice = choice_btns[choice].cget("text")

    if selected_choice == question["answer"]:
        score += 1
        feedback_label.config(text="Correct!", foreground="green")
    else:
        feedback_label.config(text="Incorrect!", foreground="red")

    for button in choice_btns:
        button.config(state="disabled")
    next_btn.config(state="normal")

def next_question():
    global current_question
    current_question += 1
    if current_question < len(quiz_data):
        show_question()
    else:
        save_score()
        messagebox.showinfo("Quiz Completed", f"Your final score is {score}/{len(quiz_data)}.")
        show_leaderboard()

root = tk.Tk()
root.title("Quiz App")
root.geometry("600x500")
style = Style(theme="flatly")

qs_label = ttk.Label(root, font=("Helvetica", 20), anchor="center", wraplength=500)
qs_label.pack(pady=20)

choice_btns = []
for i in range(4):
    button = ttk.Button(
        root,
        command=lambda i=i: check_answer(i),
        style="info.TButton",
        width=30,  
    )
    button.pack(pady=5)
    choice_btns.append(button)

feedback_label = ttk.Label(root, font=("Helvetica", 16), anchor="center")
feedback_label.pack(pady=10)

score_frame = tk.Frame(root, bg="black")
score_frame.pack(fill="x", pady=10)
score_label = ttk.Label(
    score_frame,
    text=f"Score: {score}/{len(quiz_data)}",
    font=("Helvetica", 16),
    foreground="white",
    background="black",
)
score_label.pack()

next_btn = ttk.Button(root, text="Next", command=next_question, state="disabled", style="success.TButton")
next_btn.pack(pady=10)

login_screen()

root.mainloop()
