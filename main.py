"""This is the main file that runs the GUI. Run this file to try our the project!"""

import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from customizable_gui import initialize_new_window
from selector import CourseSelector, generate_graph_from_file
from programclasses import get_programs_list, get_program
from selector import course_list_combiner

g = generate_graph_from_file('courses.csv')


def generate_courses() -> list:
    """Generates all required courses for that program"""

    courses = []

    spec, major, major_alt, minor, minor_alt = (dropdown1.get(), dropdown2.get(), dropdown2_alt.get(),
                                                dropdown3.get(), dropdown3_alt.get())

    condition1 = (
            spec != 'None' and major == 'None' and major_alt == 'None' and minor == 'None' and minor_alt == 'None')
    condition2 = (
            major != 'None' and major_alt != 'None' and spec == 'None' and minor == 'None' and minor_alt == 'None')
    condition3 = (
            major != 'None' and minor != 'None' and minor_alt != 'None' and major_alt == 'None' and spec == 'None')

    p = []
    courses1 = []
    courses2 = []
    courses3 = []

    if not (condition1 or condition2 or condition3):
        return []

    if condition1 and 'Focus' not in spec:  # specialist

        specs = get_programs_list()['Specialist']

        for sp in specs:
            if sp[1] == spec:
                p.append(get_program(sp[0], sp[1]))

        for pr in p:
            courses = pr.get_required_courses(g)

    elif condition1 and 'Focus' in spec:  # focus

        # focus
        specs = get_programs_list()['Specialist']

        for sp in specs:
            if sp[1] == spec:
                p.append(get_program(sp[0], sp[1]))

        for pr in p:
            courses1 = pr.get_required_courses(g)

        p = []

        # specialist
        specs = get_programs_list()['Specialist']

        for sp in specs:
            if sp[1] == 'Computer Science Specialist':
                p.append(get_program(sp[0], sp[1]))

        for pr in p:
            courses2 = pr.get_required_courses(g)

        courses = course_list_combiner(courses1, courses2, False)

    elif condition2:  # double major

        # major_1
        specs = get_programs_list()['Major']

        for sp in specs:
            if sp[1] == major:
                p.append(get_program(sp[0], sp[1]))

        for pr in p:
            courses1 = pr.get_required_courses(g)

        p = []

        # major_2
        specs = get_programs_list()['Major']

        for sp in specs:
            if sp[1] == major_alt:
                p.append(get_program(sp[0], sp[1]))

        for pr in p:
            courses2 = pr.get_required_courses(g)

        courses = course_list_combiner(courses1, courses2, False)

    elif condition3:  # major + 2 minors

        # major
        specs = get_programs_list()['Major']

        for sp in specs:
            if sp[1] == major:
                p.append(get_program(sp[0], sp[1]))

        for pr in p:
            courses1 = pr.get_required_courses(g)

        p = []

        # minor_1
        specs = get_programs_list()['Minor']

        for sp in specs:
            if sp[1] == minor:
                p.append(get_program(sp[0], sp[1]))

        for pr in p:
            courses2 = pr.get_required_courses(g)

        courses = course_list_combiner(courses1, courses2, False)

        p = []

        # minor_2
        specs = get_programs_list()['Minor']

        for sp in specs:
            if sp[1] == minor_alt:
                p.append(get_program(sp[0], sp[1]))

        for pr in p:
            courses3 = pr.get_required_courses(g)

        courses = course_list_combiner(courses, courses3, False)

    return courses


def generate_programs() -> list:
    """Generates the programs"""

    spec, major, major_alt, minor, minor_alt = (dropdown1.get(), dropdown2.get(), dropdown2_alt.get(),
                                                dropdown3.get(), dropdown3_alt.get())

    condition1 = (
            spec != 'None' and major == 'None' and major_alt == 'None' and minor == 'None' and minor_alt == 'None')
    condition2 = (
            major != 'None' and major_alt != 'None' and spec == 'None' and minor == 'None' and minor_alt == 'None')
    condition3 = (
            major != 'None' and minor != 'None' and minor_alt != 'None' and major_alt == 'None' and spec == 'None')

    p = []

    if not (condition1 or condition2 or condition3):
        return []

    if condition1 and 'Focus' not in spec:  # specialist

        specs = get_programs_list()['Specialist']

        for sp in specs:
            if sp[1] == spec:
                p.append(get_program(sp[0], sp[1]))

    elif condition1 and 'Focus' in spec:  # focus

        # focus
        specs = get_programs_list()['Specialist']

        for sp in specs:
            if sp[1] == spec:
                p.append(get_program(sp[0], sp[1]))

        # specialist
        specs = get_programs_list()['Specialist']

        for sp in specs:
            if sp[1] == 'Computer Science Specialist':
                p.append(get_program(sp[0], sp[1]))

    elif condition2:  # double major

        # major_1
        specs = get_programs_list()['Major']

        for sp in specs:
            if sp[1] == major:
                p.append(get_program(sp[0], sp[1]))

        # major_2
        specs = get_programs_list()['Major']

        for sp in specs:
            if sp[1] == major_alt:
                p.append(get_program(sp[0], sp[1]))

    elif condition3:  # major + 2 minors

        # major
        specs = get_programs_list()['Major']

        for sp in specs:
            if sp[1] == major:
                p.append(get_program(sp[0], sp[1]))

        # minor_1
        specs = get_programs_list()['Minor']

        for sp in specs:
            if sp[1] == minor:
                p.append(get_program(sp[0], sp[1]))

        # minor_2
        specs = get_programs_list()['Minor']

        for sp in specs:
            if sp[1] == minor_alt:
                p.append(get_program(sp[0], sp[1]))

    return p


def click(interests_list: list) -> None:
    """Generates the course plan"""

    output_textbox.delete("1.0", "end")

    if not isinstance(interests_list[0], tuple):
        for i in range(len(interests_list)):
            interests_list[i] = (interests_list[i].cget("text"), checkbox_vars[i].get())

    p = generate_programs()

    if not p:
        return

    selector = CourseSelector(p, g)

    courses = selector.select_courses(interests_list)

    if not courses[0]:
        return

    for i in range(len(courses)):
        output_textbox.insert('end', f'Year {i + 1}: {str(courses[i]).replace("[", "").replace("]", "")}\n\n')

    return


def init_new_window_to_next_file(interests_list: list) -> None:
    """Opens new window to customize course plan"""

    if not isinstance(interests_list[0], tuple):
        for i in range(len(interests_list)):
            interests_list[i] = (interests_list[i].cget("text"), checkbox_vars[i].get())

    spec, major, major_alt, minor, minor_alt = (dropdown1.get(), dropdown2.get(), dropdown2_alt.get(),
                                                dropdown3.get(), dropdown3_alt.get())

    condition1 = (
            spec != 'None' and major == 'None' and major_alt == 'None' and minor == 'None' and minor_alt == 'None')
    condition2 = (
            major != 'None' and major_alt != 'None' and spec == 'None' and minor == 'None' and minor_alt == 'None')
    condition3 = (
            major != 'None' and minor != 'None' and minor_alt != 'None' and major_alt == 'None' and spec == 'None')

    if condition1 or condition2 or condition3:

        p = generate_programs()
        courses = generate_courses()

        root.destroy()

        initialize_new_window(interests_list, courses, p)


def help_button() -> None:
    """Instructions on how to use the program"""

    output_textbox.delete("1.0", "end")
    output_textbox.insert(END, """The top of this window will have the options for the user to select the
specialist, major, and minors of their choice from the dropdown list.
However, the user can only select one of the following combinations:

i) 1 specialist
ii) 2 majors
iii) 1 major and 2 minors

If none of these combinations are chosen, the program will not run.

The user has to leave the dropdown box untouched if they would not like to use it. That
is, if the user would like to select the first combination (just 1 specialist), then they
need not make any changes to the other dropdown lists. Similarly, if the user would like
to choose 2 majors, then they need not select from any of the dropdown lists except the major
dropdown and second major dropdown lists.

After selecting a combination, the user can choose his interests. This will be used in the
selection of his electives/breadth requirement courses.

After filling the dropdown boxes and the checkboxes, the user can either click the "Generate
Courses" button or the "Customize Courses" button.

If the "Generate Courses" button is clicked, the program will auto-generate a course plan based on
the combination and interests chosen by the user. It will be displayed in the text box.

If the "Customize Courses" button is clicked, it will prompt a new window to open. This new window
will have the options for the user to customize their own course plan. However, our program will give
them course recommendations in order to help them achieve their goal.

At the bottom of the window (below the text box), the user will have the option to input a course code
and give the course a rating by clicking the "Upload Rating" button.

In addition, we also display course descriptions and course ratings in the form of the 5 star rating syst
em in order to aid in the user's judgement of courses to pick.""")


def upload_review() -> None:
    """Adds review to the review data"""

    course_code = textbox4.get("1.0", "end-1c").upper()
    rating = dropdown.get()

    course_vertex = g.get_vertex(course_code)

    if course_vertex is None:
        return

    textbox4.delete("1.0", "end")

    course_vertex.add_course_rating(int(rating))


root = Tk()
root.title("UofT Course Selector")
root.geometry('900x900')

background = Image.open("bg.png")
background = background.resize((900, 900))
test = ImageTk.PhotoImage(background)
label1 = tk.Label(root, image=test)
label1.image = test
label1.place(x=0, y=0, relwidth=1, relheight=1)

top_label = Label(root, text='Generate Courses: ', fg='green', bg='white', font=('Calibri', 20))
top_label.place(x=50, y=10)

# ----
programs = get_programs_list()

first_label = Label(root, text='Specialist: ', fg='red', bg='white', font=('Calibri', 15))
first_label.place(x=50, y=50)

specialists = ['None']
specialists.extend([spec[1] for spec in programs['Specialist']])

selected_specialist = tk.StringVar(root)
selected_specialist.set(specialists[0])
dropdown1 = ttk.Combobox(root, textvariable=selected_specialist, values=specialists, width=50, height=10)
dropdown1.place(x=130, y=50)

second_label = Label(root, text='Major: ', fg='red', bg='white', font=('Calibri', 15))
second_label.place(x=50, y=100)
second_label_alt = Label(root, text='Second Major: ', fg='red', bg='white', font=('Calibri', 15))
second_label_alt.place(x=459, y=100)

majors = ['None']
majors.extend([major[1] for major in programs['Major']])

selected_major = tk.StringVar(root)
selected_major.set(majors[0])
selected_major_alt = tk.StringVar(root)
selected_major_alt.set(majors[0])
dropdown2 = ttk.Combobox(root, textvariable=selected_major, values=majors, width=32, height=10)
dropdown2_alt = ttk.Combobox(root, textvariable=selected_major_alt, values=majors, width=32, height=10)
dropdown2.place(x=130, y=100)
dropdown2_alt.place(x=570, y=100)

third_label = Label(root, text='Minor: ', fg='red', bg='white', font=('Calibri', 15))
third_label.place(x=50, y=150)
third_label_alt = Label(root, text='Second Minor: ', fg='red', bg='white', font=('Calibri', 15))
third_label_alt.place(x=459, y=150)

minors = ['None']
minors.extend([minor[1] for minor in programs['Minor']])

selected_minor = tk.StringVar(root)
selected_minor.set(minors[0])
selected_minor_alt = tk.StringVar(root)
selected_minor_alt.set(minors[0])
dropdown3 = ttk.Combobox(root, textvariable=selected_minor, values=minors, width=32, height=10)
dropdown3_alt = ttk.Combobox(root, textvariable=selected_minor_alt, values=minors, width=32, height=10)
dropdown3.place(x=130, y=150)
dropdown3_alt.place(x=570, y=150)

fourth_label = Label(root, text='Interests: ', fg='red', bg='white', font=('Calibri', 15))
fourth_label.place(x=50, y=200)

interests = []

# Checkbox
var1 = IntVar()
checkbox1 = Checkbutton(root, text="Psychology", variable=var1)
interests.append(checkbox1)
checkbox1.place(x=130, y=205)

var2 = IntVar()
checkbox2 = Checkbutton(root, text="Math", variable=var2)
interests.append(checkbox2)
checkbox2.place(x=230, y=205)

var3 = IntVar()
checkbox3 = Checkbutton(root, text="Computer Science", variable=var3)
interests.append(checkbox3)
checkbox3.place(x=291, y=205)

var4 = IntVar()
checkbox4 = Checkbutton(root, text="Statistics", variable=var4)
interests.append(checkbox4)
checkbox4.place(x=433, y=205)

var5 = IntVar()
checkbox5 = Checkbutton(root, text="English", variable=var5)
interests.append(checkbox5)
checkbox5.place(x=520, y=205)

var6 = IntVar()
checkbox6 = Checkbutton(root, text="Cognitive Science", variable=var6)
interests.append(checkbox6)
checkbox6.place(x=594, y=205)

var7 = IntVar()
checkbox7 = Checkbutton(root, text="Philosophy", variable=var7)
interests.append(checkbox7)
checkbox7.place(x=130, y=235)

var8 = IntVar()
checkbox8 = Checkbutton(root, text="Physics", variable=var8)
interests.append(checkbox8)
checkbox8.place(x=228, y=235)

var9 = IntVar()
checkbox9 = Checkbutton(root, text="Drama", variable=var9)
interests.append(checkbox9)
checkbox9.place(x=305, y=235)

var10 = IntVar()
checkbox10 = Checkbutton(root, text="Chemistry", variable=var10)
interests.append(checkbox10)
checkbox10.place(x=375, y=235)

var11 = IntVar()
checkbox11 = Checkbutton(root, text="History", variable=var11)
interests.append(checkbox11)
checkbox11.place(x=467, y=235)

var12 = IntVar()
checkbox12 = Checkbutton(root, text="Other Languages", variable=var12)
interests.append(checkbox12)
checkbox12.place(x=541, y=235)

var13 = IntVar()
checkbox13 = Checkbutton(root, text="Religion", variable=var13)
interests.append(checkbox13)
checkbox13.place(x=130, y=265)

var14 = IntVar()
checkbox14 = Checkbutton(root, text="Christianity", variable=var14)
interests.append(checkbox14)
checkbox14.place(x=210, y=265)

var15 = IntVar()
checkbox15 = Checkbutton(root, text="Linguistics", variable=var15)
interests.append(checkbox15)
checkbox15.place(x=310, y=265)

var16 = IntVar()
checkbox16 = Checkbutton(root, text="Economics", variable=var16)
interests.append(checkbox16)
checkbox16.place(x=405, y=265)

var17 = IntVar()
checkbox17 = Checkbutton(root, text="Cinema", variable=var17)
interests.append(checkbox17)
checkbox17.place(x=501, y=265)

var18 = IntVar()
checkbox18 = Checkbutton(root, text="Music", variable=var18)
interests.append(checkbox18)
checkbox18.place(x=577, y=265)

checkbox_vars = [var1, var2, var3, var4, var5, var6, var7, var8, var9, var10, var11, var12, var13, var14, var15, var16,
                 var17, var18]

button1 = Button(root, text="Generate Courses", command=lambda: click(interests), font=("Calibri", 15), fg="black",
                 bg="white")
button1.place(x=50, y=320)

button2 = Button(root, text="Customize Courses", command=lambda: init_new_window_to_next_file(interests),
                 font=("Calibri", 15), fg="black", bg="white")
button2.place(x=220, y=320)

helper_button = Button(root, text="Help", command=help_button, font=("Calibri", 15), fg="black", bg="white")
helper_button.place(x=800, y=12)

output_textbox = Text(root, bg='white', fg='black', font=("Calibri", 15), width=70, height=12)
output_textbox.place(x=50, y=370)

# ------------------------------------ Options for the dropdown

fourth_label = Label(root, text='Rate a Course: ', fg='green', bg='white', font=('Calibri', 20))
fourth_label.place(x=50, y=630)

fifth_label = Label(root, text='Course Code: ', fg='red', bg='white', font=('Calibri', 15))
fifth_label.place(x=50, y=670)

textbox4 = Text(root, bg='white', fg='black', font=("Calibri", 15), width=50, height=1)
textbox4.place(x=160, y=670)

sixth_lable = Label(root, text='Rating: ', fg='red', bg='white', font=('Calibri', 15))
sixth_lable.place(x=50, y=710)

options = ["5", "4", "3", "2", "1"]

# Variable to hold the selected option
selected_option = tk.StringVar(root)
selected_option.set(options[0])  # Setting the default option

# Creating the dropdown box
dropdown = ttk.Combobox(root, textvariable=selected_option, values=options, width=10, height=10)
dropdown.place(x=160, y=710)

review_button = Button(root, text="Upload Rating", command=upload_review, font=("Calibri", 15), fg="black", bg="white")
review_button.place(x=50, y=750)

root.mainloop()
