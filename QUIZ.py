from tkinter import *
import random
import time
from functools import partial
from tkinter import messagebox
import string

questions = []
options = []
answers = []

root = Tk()
root.geometry("800x600")
root.title("QUIZ")
windowWidth = root.winfo_screenwidth()
windowHeight = root.winfo_screenheight()
positionRight = int(root.winfo_screenwidth() / 2 - 800 / 2)
positionDown = int(root.winfo_screenheight() / 2 - 600 / 2)
root.geometry("+{}+{}".format(positionRight, positionDown))
root.configure(background="white")
root.resizable(height=False, width=False)

with open("Questions.txt") as filehandle:
    for i in filehandle:
        questions.append(i)
with open("Options.txt") as filehandle:
    for i in filehandle:
        options.append(i.capitalize())
with open("Answers.txt") as filehandle:
    for i in filehandle:
        answers.append(i.capitalize())

show_question = StringVar()
show_option1 = StringVar()
show_option2 = StringVar()
show_option3 = StringVar()
show_option4 = StringVar()
show_score = StringVar()
var = IntVar()

question_variable = ""
option1_variable = ""
option2_variable = ""
option3_variable = ""
option4_variable = ""
get_answer = ""
get_question = ""

save_questions = []
get_options = []
check_answer = []

question_count = 0
check_button_status = 0
score = 0
status = 0

show_score.set(score)


def check_question():
    global get_question, save_questions, status, question_count
    get_question = random.choice(questions)
    if (len(save_questions) != 0):
        for i in range(len(save_questions)):
            if (get_question == save_questions[i]):
                get_question = ""
                check_question()
            else:
                save_questions.append(get_question)
                show_question.set(get_question)
                status = 1
                break
    elif (len(save_questions) == 0):
        save_questions.append(get_question)
        status = 1
    question_count += 1


def get_question_options():
    global get_options, get_answer, save_questions, get_question, show_option1, show_option2, show_option3, show_option4, status, x
    for i in range(len(questions)):
        if (questions[i] == get_question):
            x = questions.index(questions[i])
            get_answer = answers[i]
            question_variable = questions[i]
            show_question.set(question_variable)
            break
    x = x + 1
    x = (x * 4) - 1
    get_options.clear()
    for i in range(4):
        get_options.append(options[x - i])
    random.shuffle(get_options)
    option1_variable = get_options[0]
    option2_variable = get_options[1]
    option3_variable = get_options[2]
    option4_variable = get_options[3]
    show_option1.set(option1_variable)
    show_option2.set(option2_variable)
    show_option3.set(option3_variable)
    show_option4.set(option4_variable)
    x = 0


def next_button_click():
    global status, option1, option2, option3, option4, var, x, get_options, get_question, get_answer
    get_options.clear()
    get_question = ""
    get_answer = ""
    check_question()
    if (status == 1):
        get_question_options()
        option1.configure(bg="white")
        option2.configure(bg="white")
        option3.configure(bg="white")
        option4.configure(bg="white")
        option1.deselect()
        option2.deselect()
        option3.deselect()
        option4.deselect()
        var.set(0)
        check_button.configure(state=NORMAL)
        status = 0
        next_button.configure(state=DISABLED)


def home_exit_button_click():
    home_exit_status = messagebox.askquestion("Confirm", "Do you really want to Exit ?")
    if (home_exit_status == "yes"):
        root.destroy()


def starting_window():
    global head_label, play_button, score_button, exit_button, score
    head_label = Label(root, text="QUIZ", font=(None, 35, "bold"), bg="white", width=6)
    head_label.place(x=289, y=45)
    play_button = Button(root, text="Play", relief="flat", font=(None, 15), bg="black", fg="white",
                         command=home_play_click, height=1, width=5)
    play_button.place(x=360, y=328)
    exit_button = Button(root, text="Exit", relief="flat", font=(None, 15), bg="black", fg="white", width=5,
                         command=home_exit_button_click, height=1)
    exit_button.place(x=360, y=392)


def destroy_home():
    global head_label, play_button, score_button, exit_button
    head_label.destroy()
    play_button.destroy()
    exit_button.destroy()


def destroy_quiz():
    global question_label, option1, option2, option3, option4, check_button, home_button, next_button, score_label, score_name_label, question_count, var, get_question, get_options, get_answer
    question_label.destroy()
    option1.destroy()
    option2.destroy()
    option3.destroy()
    option4.destroy()
    check_button.destroy()
    home_button.destroy()
    next_button.destroy()
    score_label.destroy()
    score_name_label.destroy()
    var.set(0)
    score = 0
    show_score.set(score)
    question_count = 0
    get_options.clear()
    get_question = ""
    get_answer = ""


def home_play_click():
    destroy_home()
    question_widgets()
    check_question()
    get_question_options()


def assign_option_values():
    global check_answer
    for i in range(4):
        if (get_options[i] == get_answer):
            check_answer = get_options.index(get_options[i]) + 1


def question_count_check():
    global question_count, var
    if (question_count > 4):
        check_button.configure(state=DISABLED)
        next_button.configure(state=DISABLED)
        messagebox.showinfo("Max Reached", "You have completed all the questions")
        score_home_status = messagebox.askquestion("Exit", "Do you want to go home")
        if (score_home_status == "yes"):
            score = 0
            show_score.set(score)
            question_count = 0
            get_options.clear()
            get_question = ""
            get_answer = ""
            option1.deselect()
            option2.deselect()
            option3.deselect()
            option4.deselect()
            var.set(0)
            destroy_quiz()
            starting_window()


def check_button_click():
    global selected_option, check_answer, option1, option2, option3, option4, score
    assign_option_values()
    selected_option = var.get()
    if (selected_option == 1 or selected_option == 2 or selected_option == 3 or selected_option == 4):
        check_button.configure(state=DISABLED)
        next_button.configure(state=NORMAL)
        if (selected_option == 1):
            if (selected_option == check_answer):
                option1.configure(bg="green")
                score = score + 10
                show_score.set(score)
            else:
                option1.configure(bg="red")
                if (check_answer == 2):
                    option2.configure(bg="green")
                if (check_answer == 3):
                    option3.configure(bg="green")
                if (check_answer == 4):
                    option4.configure(bg="green")
            question_count_check()
        if (selected_option == 2):
            if (selected_option == check_answer):
                option2.configure(bg="green")
                score = score + 10
                show_score.set(score)
            else:
                option2.configure(bg="red")
                if (check_answer == 1):
                    option1.configure(bg="green")
                if (check_answer == 3):
                    option3.configure(bg="green")
                if (check_answer == 4):
                    option4.configure(bg="green")
            question_count_check()
        if (selected_option == 3):
            if (selected_option == check_answer):
                option3.configure(bg="green")
                score = score + 10
                show_score.set(score)
            else:
                option3.configure(bg="red")
                if (check_answer == 1):
                    option1.configure(bg="green")
                if (check_answer == 2):
                    option2.configure(bg="green")
                if (check_answer == 4):
                    option4.configure(bg="green")
            question_count_check()
        if (selected_option == 4):
            if (selected_option == check_answer):
                option4.configure(bg="green")
                score = score + 10
                show_score.set(score)
            else:
                option4.configure(bg="red")
                if (check_answer == 1):
                    option1.configure(bg="green")
                if (check_answer == 2):
                    option2.configure(bg="green")
                if (check_answer == 3):
                    option3.configure(bg="green")
            question_count_check()
    else:
        messagebox.showwarning("Select an option", "Please Select an Option")


def home_button_click():
    global var, get_options, get_question, get_answer
    home_status = messagebox.askquestion("Home", "Your score will be lost, Are You Sure ?")
    if (home_status == "yes"):
        var.set(0)
        get_options.clear()
        get_question = ""
        get_answer = ""
        destroy_quiz()
        starting_window()


def question_widgets():
    global question_label, option1, option2, option3, option4, check_button, home_button, next_button, score_label, score_name_label
    question_label = Label(root, textvariable=show_question, font=(None, 12), bg="white", wraplength=670, height=4,
                           width=69)
    question_label.place(x=20, y=64)
    option1 = Radiobutton(root, textvariable=show_option1, variable=var, value=1, font=(None, 11), bg="white", height=2)
    option1.place(x=80, y=174)
    option2 = Radiobutton(root, textvariable=show_option2, variable=var, value=2, font=(None, 11), bg="white", height=2)
    option2.place(x=80, y=240)
    option3 = Radiobutton(root, textvariable=show_option3, variable=var, value=3, font=(None, 11), bg="white", height=2)
    option3.place(x=80, y=306)
    option4 = Radiobutton(root, textvariable=show_option4, variable=var, value=4, font=(None, 11), bg="white", height=2)
    option4.place(x=80, y=372)
    check_button = Button(root, text="Check", relief="flat", font=(None, 15), fg="white", bg="black", height=1, width=6,
                          command=check_button_click)
    check_button.place(x=240, y=450)
    home_button = Button(root, text="Home", relief="flat", font=(None, 15), bg="black", fg="white", height=1, width=6,
                         command=home_button_click)
    home_button.place(x=120, y=450)
    next_button = Button(root, text="Next", relief="flat", font=(None, 15), bg="black", fg="white", height=1, width=5,
                         state=DISABLED, command=next_button_click)
    next_button.place(x=550, y=450)
    score_name_label = Label(root, text="Score:", font=(None, 11, "bold"), bg="white")
    score_name_label.place(x=80, y=530)
    score_label = Label(root, textvariable=show_score, font=(None, 11), bg="white", fg="black")
    score_label.place(x=155, y=530)


starting_window()
root.mainloop()
