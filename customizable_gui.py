"""The Customizable Menu of the GUI"""

import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from initializer import CourseOrVertex, _Vertex, CourseAndVertex
from selector import CourseSelector, generate_graph_from_file, course_in_list
from programclasses import get_programs_list, get_program
from selector import get_credits_year, verify_breadth_req, get_breadth_req
from tkmacosx import Button

selected_course_text = ""
selected_course = None
curr_select_course_button_i_j = (-1, -1)

course_recs = []

g = generate_graph_from_file('courses.csv')

final_courses = {0: {0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None},
                 1: {0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None},
                 2: {0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None},
                 3: {0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None}}


def click(i_f: int, j_f: int, textbox1: Text, root: Tk) -> None:
    """Performed when any course button is clicked and performs the necessary operations"""

    display_description(i_f, j_f, textbox1, root)


def display_description(i_f: int, j_f: int, textbox1: Text, root: Tk) -> None:
    # switched parameters here
    """Displays course name, description and details when course button is clicked"""

    # course code
    course_name_label = Label(root, text=final_courses[i_f][j_f].course_code, fg='black', bg='white',
                              font=('Calibri', 20), width=8)
    course_name_label.place(x=490, y=460)

    # description
    textbox1.delete("1.0", "end")
    textbox1.insert(END, final_courses[i_f][j_f].description)  # switch here, i and j cuz of matrix indexing

    # stars
    canvas_star = Canvas(root, width=250, height=50, bg="white")
    canvas_star.place(x=620, y=700)

    number_of_int_stars = int(final_courses[i_f][j_f].rating)

    full_star = Image.open("full_star.png")
    full_star = full_star.resize((50, 50))
    full_star_image = ImageTk.PhotoImage(full_star)

    half_star = Image.open("half_star.png")
    half_star = half_star.resize((50, 50))
    half_star_image = ImageTk.PhotoImage(half_star)

    star_x_coordinate = 0

    for _ in range(number_of_int_stars):
        canvas_star.create_image(star_x_coordinate, 0, anchor=NW, image=full_star_image)
        star_x_coordinate += 50

    canvas_star.image = full_star_image

    if (round(final_courses[i_f][j_f].rating * 2) / 2) - 0.5 == number_of_int_stars:
        canvas_half_star = Canvas(root, width=50, height=50, bg="white", highlightthickness=0)
        canvas_half_star.place(x=620 + star_x_coordinate, y=703)

        canvas_half_star.create_image(1, 0, anchor=NW, image=half_star_image)
        canvas_half_star.image = half_star_image


def initialize_new_window(interests: list, courses: list, p: list) -> None:
    """Initializes the window"""

    root = Tk()
    root.title("UofT Customize Courses")
    root.geometry('1400x900')

    background = Image.open("bg.png")
    background = background.resize((2000, 9000))
    test = ImageTk.PhotoImage(background)
    label1 = tk.Label(root, image=test)
    label1.image = test
    label1.place(x=0, y=0, relwidth=1, relheight=1)

    canvas = Canvas(root, width=1400, height=900, bg="white")  # Create a canvas
    canvas.pack()

    # Draw a line to divide the window into two parts
    canvas.create_line(1220, 0, 1220, 900, fill="black", width=2)  # main vertical line
    canvas.create_line(0, 445, 1220, 445, fill="black", width=2)  # main horizontal line

    textbox1 = Text(root, bg='white', fg='black', font=("Calibri", 15), width=79, height=9, highlightthickness=0)

    top_label_3 = Label(root, text='Requirements: ', fg='green', bg='white', font=('Calibri', 20))
    top_label_3.place(x=25, y=460)

    breadth_canvas = Canvas(canvas, width=250, height=280, bg='white')
    breadth_canvas.place(x=25, y=510)

    br1 = Label(root, text='1) Creative and Cultural Representations', fg='black', bg='white', font=('Calibri', 11))
    br1.place(x=32, y=520)

    rectangle1 = tk.Canvas(root, width=9, height=9, bg='red', highlightthickness=0)
    rectangle1.place(x=257, y=526)

    br2 = Label(root, text='2) Thought, Belief, and Behavior', fg='black', bg='white', font=('Calibri', 11))
    br2.place(x=32, y=550)

    rectangle2 = tk.Canvas(root, width=9, height=9, bg='red', highlightthickness=0)
    rectangle2.place(x=257, y=556)

    br3 = Label(root, text='3) Society and its Institutions', fg='black', bg='white', font=('Calibri', 11))
    br3.place(x=32, y=586)

    rectangle3 = tk.Canvas(root, width=9, height=9, bg='red', highlightthickness=0)
    rectangle3.place(x=257, y=592)

    br4 = Label(root, text='4) Living Things and their Environment', fg='black', bg='white', font=('Calibri', 11))
    br4.place(x=32, y=622)

    rectangle4 = tk.Canvas(root, width=9, height=9, bg='red', highlightthickness=0)
    rectangle4.place(x=257, y=628)

    br5 = Label(root, text='5) Physical and Mathematical Universes', fg='black', bg='white', font=('Calibri', 11))
    br5.place(x=32, y=658)

    rectangle5 = tk.Canvas(root, width=9, height=9, bg='red', highlightthickness=0)
    rectangle5.place(x=257, y=664)

    br6 = Label(root, text='Progam Requirements', fg='black', bg='white', font=('Calibri', 11))
    br6.place(x=32, y=694)

    rectangle6 = tk.Canvas(root, width=9, height=9, bg='red', highlightthickness=0)
    rectangle6.place(x=257, y=700)

    degree_canvas = Canvas(canvas, width=150, height=60, bg='white')
    degree_canvas.place(x=73, y=720)

    degree_label = Label(root, text='Degree Completed?', fg='black', bg='white', font=('Calibri', 13))
    degree_label.place(x=90, y=725)

    degree_label_1 = Label(root, text='Not Yet', fg='red', bg='white', font=('Calibri', 11))
    degree_label_1.place(x=90, y=755)

    degree_label_2 = Label(root, text='Completed', fg='grey', bg='white', font=('Calibri', 11))
    degree_label_2.place(x=150, y=755)

    rectangles = [rectangle1, rectangle2, rectangle3, rectangle4, rectangle5, rectangle6]

    course_code = "pholder"

    top_label_4 = Label(root, text='Course Details: ', fg='green', bg='white', font=('Calibri', 20))
    top_label_4.place(x=350, y=460)

    review_canvas = Canvas(canvas, width=800, height=280, bg='white')
    review_canvas.place(x=350, y=510)

    textbox1.place(x=354, y=515)
    textbox1.insert(END, "")

    # line to divide the section
    canvas.create_line(1220, 200, 1500, 200, fill="black", width=2)

    select_course_button = Button(canvas, text="Select Course", bg='white', fg='black', font=('Calibri', 12), width=168)

    select_course_button.place(x=1225, y=775)

    # -------------------------------LINE 1-------------------------------

    button_1_line_1 = Button(root, text=course_code, command=lambda: click(0, 0, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white", width=90, height=50)
    # button_1_line_1.place(x=30, y=30)

    button_2_line_1 = Button(root, text=course_code, command=lambda: click(0, 1, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_2_line_1.place(x=150, y=30)

    button_3_line_1 = Button(root, text=course_code, command=lambda: click(0, 2, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_3_line_1.place(x=270, y=30)

    button_4_line_1 = Button(root, text=course_code, command=lambda: click(0, 3, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_4_line_1.place(x=390, y=30)

    button_5_line_1 = Button(root, text=course_code, command=lambda: click(0, 4, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_5_line_1.place(x=510, y=30)

    # -------

    button_6_line_1 = Button(root, text=course_code, command=lambda: click(0, 5, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_6_line_1.place(x=630, y=30)

    button_7_line_1 = Button(root, text=course_code, command=lambda: click(0, 6, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_7_line_1.place(x=750, y=30)

    button_8_line_1 = Button(root, text=course_code, command=lambda: click(0, 7, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_8_line_1.place(x=870, y=30)

    button_9_line_1 = Button(root, text=course_code, command=lambda: click(0, 8, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_9_line_1.place(x=990, y=30)

    button_10_line_1 = Button(root, text=course_code, command=lambda: click(0, 9, textbox1, root),
                              font=("Calibri", 15), fg="black", bg="white",
                              width=90, height=50)
    # button_10_line_1.place(x=1110, y=30)

    line_1_buttons = [button_1_line_1, button_2_line_1, button_3_line_1, button_4_line_1, button_5_line_1,
                      button_6_line_1, button_7_line_1, button_8_line_1, button_9_line_1, button_10_line_1]

    line_1_button_coordinates = [(30, 30), (150, 30), (270, 30), (390, 30), (510, 30),
                                 (630, 30), (750, 30), (870, 30), (990, 30), (1110, 30)]

    # -------------------------------LINE 2-------------------------------

    button_1_line_2 = Button(root, text=course_code, command=lambda: click(1, 0, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_1_line_2.place(x=30, y=140)

    button_2_line_2 = Button(root, text=course_code, command=lambda: click(1, 1, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_2_line_2.place(x=150, y=140)

    button_3_line_2 = Button(root, text=course_code, command=lambda: click(1, 2, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_3_line_2.place(x=270, y=140)

    button_4_line_2 = Button(root, text=course_code, command=lambda: click(1, 3, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_4_line_2.place(x=390, y=140)

    button_5_line_2 = Button(root, text=course_code, command=lambda: click(1, 4, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_5_line_2.place(x=510, y=140)

    # -------

    button_6_line_2 = Button(root, text=course_code, command=lambda: click(1, 5, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_6_line_2.place(x=630, y=140)

    button_7_line_2 = Button(root, text=course_code, command=lambda: click(1, 6, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_7_line_2.place(x=750, y=140)

    button_8_line_2 = Button(root, text=course_code, command=lambda: click(1, 7, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_8_line_2.place(x=870, y=140)

    button_9_line_2 = Button(root, text=course_code, command=lambda: click(1, 8, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_9_line_2.place(x=990, y=140)

    button_10_line_2 = Button(root, text=course_code, command=lambda: click(1, 9, textbox1, root),
                              font=("Calibri", 15), fg="black", bg="white",
                              width=90, height=50)
    # button_10_line_2.place(x=1110, y=140)

    line_2_buttons = [button_1_line_2, button_2_line_2, button_3_line_2, button_4_line_2, button_5_line_2,
                      button_6_line_2, button_7_line_2, button_8_line_2, button_9_line_2, button_10_line_2]

    line_2_button_coordinates = [(30, 140), (150, 140), (270, 140), (390, 140), (510, 140),
                                 (630, 140), (750, 140), (870, 140), (990, 140), (1110, 140)]

    # -------------------------------LINE 3-------------------------------

    button_1_line_3 = Button(root, text=course_code, command=lambda: click(2, 0, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_1_line_3.place(x=30, y=250)

    button_2_line_3 = Button(root, text=course_code, command=lambda: click(2, 1, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_2_line_3.place(x=150, y=250)

    button_3_line_3 = Button(root, text=course_code, command=lambda: click(2, 2, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_3_line_3.place(x=270, y=250)

    button_4_line_3 = Button(root, text=course_code, command=lambda: click(2, 3, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_4_line_3.place(x=390, y=250)

    button_5_line_3 = Button(root, text=course_code, command=lambda: click(2, 4, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_5_line_3.place(x=510, y=250)

    # -------

    button_6_line_3 = Button(root, text=course_code, command=lambda: click(2, 5, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_6_line_3.place(x=630, y=250)

    button_7_line_3 = Button(root, text=course_code, command=lambda: click(2, 6, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_7_line_3.place(x=750, y=250)

    button_8_line_3 = Button(root, text=course_code, command=lambda: click(2, 7, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_8_line_3.place(x=870, y=250)

    button_9_line_3 = Button(root, text=course_code, command=lambda: click(2, 8, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_9_line_3.place(x=990, y=250)

    button_10_line_3 = Button(root, text=course_code, command=lambda: click(2, 9, textbox1, root),
                              font=("Calibri", 15), fg="black", bg="white",
                              width=90, height=50)
    # button_10_line_3.place(x=1110, y=250)

    line_3_buttons = [button_1_line_3, button_2_line_3, button_3_line_3, button_4_line_3, button_5_line_3,
                      button_6_line_3, button_7_line_3, button_8_line_3, button_9_line_3, button_10_line_3]

    line_3_button_coordinates = [(30, 250), (150, 250), (270, 250), (390, 250), (510, 250),
                                 (630, 250), (750, 250), (870, 250), (990, 250), (1110, 250)]

    # -------------------------------LINE 4-------------------------------

    button_1_line_4 = Button(root, text=course_code, command=lambda: click(3, 0, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_1_line_4.place(x=30, y=360)

    button_2_line_4 = Button(root, text=course_code, command=lambda: click(3, 1, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_2_line_4.place(x=150, y=360)

    button_3_line_4 = Button(root, text=course_code, command=lambda: click(3, 2, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_3_line_4.place(x=270, y=360)

    button_4_line_4 = Button(root, text=course_code, command=lambda: click(3, 3, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_4_line_4.place(x=390, y=360)

    button_5_line_4 = Button(root, text=course_code, command=lambda: click(3, 4, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_5_line_4.place(x=510, y=360)

    # -------

    button_6_line_4 = Button(root, text=course_code, command=lambda: click(3, 5, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_6_line_4.place(x=630, y=360)

    button_7_line_4 = Button(root, text=course_code, command=lambda: click(3, 6, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_7_line_4.place(x=750, y=360)

    button_8_line_4 = Button(root, text=course_code, command=lambda: click(3, 7, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_8_line_4.place(x=870, y=360)

    button_9_line_4 = Button(root, text=course_code, command=lambda: click(3, 8, textbox1, root),
                             font=("Calibri", 15), fg="black", bg="white",
                             width=90, height=50)
    # button_9_line_4.place(x=990, y=360)

    button_10_line_4 = Button(root, text=course_code, command=lambda: click(3, 9, textbox1, root),
                              font=("Calibri", 15), fg="black", bg="white",
                              width=90, height=50)
    # button_10_line_4.place(x=1110, y=360)

    line_4_buttons = [button_1_line_4, button_2_line_4, button_3_line_4, button_4_line_4, button_5_line_4,
                      button_6_line_4, button_7_line_4, button_8_line_4, button_9_line_4, button_10_line_4]

    line_4_button_coordinates = [(30, 360), (150, 360), (270, 360), (390, 360), (510, 360),
                                 (630, 360), (750, 360), (870, 360), (990, 360), (1110, 360)]

    # ----------------------------------------

    line_buttons = [line_1_buttons, line_2_buttons, line_3_buttons, line_4_buttons]
    line_button_coordinates = [line_1_button_coordinates, line_2_button_coordinates,
                               line_3_button_coordinates, line_4_button_coordinates]

    all_after_j = []

    for i in range(len(courses)):

        after_j = 0

        for j in range(len(courses[i])):

            after_j = j

            if isinstance(courses[i][j], CourseOrVertex):

                chk = False

                for k in courses[i][j].neighbours:

                    if isinstance(courses[i][j].neighbours[k], CourseAndVertex):

                        chk = True

                        all_course_and_vertices = []

                        course_and_vertex = courses[i][j].neighbours[k].neighbours

                        for m in course_and_vertex:

                            course_code = m

                            final_courses[i][j] = g.get_vertex(course_code)

                            line_buttons[i][j].configure(text=course_code)

                            line_buttons[i][j].place(x=line_button_coordinates[i][j][0],
                                                     y=line_button_coordinates[i][j][1])

                            all_course_and_vertices.append(course_and_vertex[m])

                            after_j += 1
                            j += 1

                        j -= 1
                        break

                if chk:
                    continue

                line_buttons[i][j].configure(text="Choose")
                line_buttons[i][j].configure(bg='#D2B48C')

                line_buttons[i][j].place(x=line_button_coordinates[i][j][0], y=line_button_coordinates[i][j][1])
                line_buttons[i][j].configure(
                    command=lambda i_f=i, j_f=j: make_course_choice(root, i_f, j_f, courses, textbox1,
                                                                    select_course_button, interests, p))

            else:

                course_code = courses[i][j].course_code

                final_courses[i][j] = g.get_vertex(course_code)

                line_buttons[i][j].configure(text=course_code)

                line_buttons[i][j].place(x=line_button_coordinates[i][j][0], y=line_button_coordinates[i][j][1])

            after_j += 1

        all_after_j.append(after_j)

    if check_if_required_courses_completed(courses):
        display_rest_of_buttons(root, all_after_j, line_buttons, line_button_coordinates, textbox1,
                                select_course_button, interests, p)

    find_pre_req_and_draw_line(line_button_coordinates, canvas)

    update_requirements(rectangles, degree_label_1, degree_label_2, p)

    cover_canvas = Canvas(root, width=175, height=755, bg="white", highlightthickness=0)
    cover_canvas.create_line(0, 200, 180, 200, fill="black", width=2)
    cover_canvas.place(x=1221, y=0)

    (select_course_button.configure
     (command=lambda: return_selected_course(select_course_button, line_buttons, courses, textbox1, root, rectangles,
                                             degree_label_1, degree_label_2, line_button_coordinates,
                                             canvas, all_after_j, interests, p)))

    root.mainloop()


def draw_dotted_line(start_x: int, start_y: int, end_x: int, end_y: int, canvas: Canvas) -> None:
    """Draws the dotted line to indicate pre-requisites"""

    if start_y == end_y:
        canvas.create_line(start_x + 90, start_y + 25, end_x, end_y + 25, dash=(5, 5), width=2, fill='red',
                           arrow=tk.LAST)
    elif start_x == end_x:
        canvas.create_line(start_x + 44, start_y, end_x + 44, end_y, dash=(5, 5), width=2, fill='red', arrow=tk.LAST)

    else:
        canvas.create_line(start_x + 39, start_y + 39, end_x, end_y, dash=(5, 5), width=2, fill='red', arrow=tk.LAST)


def make_course_choice(root: Tk, i_f: int, j_f: int, courses: list, textbox1: Text,
                       select_course_button: Button, interests: list, p: list) -> None:
    """Calls all the required functions to choose between multiple courses"""

    cover_canvas = Canvas(root, width=175, height=755, bg="white", highlightthickness=0)
    cover_canvas.create_line(0, 200, 180, 200, fill="black", width=2)
    cover_canvas.place(x=1221, y=0)

    global selected_course

    if not courses:
        important_display_function(root, {}, i_f + 1, textbox1, select_course_button, i_f, j_f, interests, p)
    else:
        important_display_function(root, courses[i_f][j_f].neighbours, i_f + 1, textbox1, select_course_button, i_f,
                                   j_f, interests, p)


def important_display_function(root: Tk, lst: dict, year: int, textbox1: Text, select_course_button: Button,
                               i_f: int, j_f: int, interests: list, p: list) -> None:
    """Displays the recommended courses and all the buttons to select a course"""

    selector = CourseSelector(p, g)

    global course_recs

    if 'course_recs' in globals():
        for btn in course_recs:
            btn.destroy()
    course_recs = []

    if lst == {}:

        rec_course_label = Label(root, text='Recommended Courses:', fg='green', bg='white', font=('Calibri', 14))
        rec_course_label.place(x=1223, y=210)

        search_course_label = Label(root, text='Search Course:', fg='green', bg='white', font=('Calibri', 15))
        search_course_label.place(x=1250, y=10)

        course_text_box = tk.Text(root, height=1, width=10, bg='white', fg='black')
        course_text_box.place(x=1230, y=43)

        go_button = Button(root, text="Go", bg='white', fg='black', font=('Calibri', 11), width=60,
                           command=lambda: course_button(root, course_text_box, textbox1,
                                                         select_course_button, i_f, j_f))
        go_button.place(x=1320, y=40)

        temp = 0

        y_pos = 250

        for vertex_obj in selector.recomend_courses(dict_to_list(), year, interests):

            if temp > 7:
                break

            course_rec = Button(root, text=vertex_obj.course_code,
                                command=lambda vertex=vertex_obj: new_click(root, vertex, textbox1,
                                                                            select_course_button, i_f, j_f),
                                font=("Calibri", 15), fg="black", bg="white", width=90, height=50)

            course_rec.place(x=1270, y=y_pos)
            course_recs.append(course_rec)
            y_pos += 65
            temp += 1

    else:
        rec_course_label = Label(root, text='Select Course:', fg='green', bg='white', font=('Calibri', 15))
        rec_course_label.place(x=1223, y=210)

        y_pos = 250

        copy_of_lst = lst.copy()

        for c in lst:
            if not lst[c].verify_course_list(dict_to_list(), year - 1):
                del copy_of_lst[c]

        for c, vertex_obj in copy_of_lst.items():
            course_rec = Button(root, text=c, command=lambda vertex=vertex_obj: new_click(root, vertex, textbox1,
                                                                                          select_course_button,
                                                                                          i_f, j_f),
                                font=("Calibri", 15), fg="black", bg="white", width=90, height=50)

            course_rec.place(x=1270, y=y_pos)
            course_recs.append(course_rec)
            y_pos += 65


def course_button(root: Tk, txt_box: Text, textbox1: Text, select_course_button: Button, i_f: int,
                  j_f: int) -> None:
    """Displays button that appears when searching for a course"""

    txt = txt_box.get("1.0", "end-1c")

    if (g.get_vertex(txt.upper()) is not None and g.get_vertex(txt.upper()).verify_course_list(dict_to_list(), i_f)
            and not course_in_list(g.get_vertex(txt.upper()), dict_to_list())):
        course_searched = Button(root, text=txt.upper(),
                                 command=lambda: new_click(root, g.get_vertex(txt.upper()), textbox1,
                                                           select_course_button, i_f, j_f),
                                 font=("Calibri", 15), fg="black", bg="white", width=90, height=50)

        course_searched.place(x=1270, y=100)


def new_click(root: Tk, vertex_obj: _Vertex, textbox1: Text, select_course_button: Button, i_f: int, j_f: int) -> None:
    """If the selected button course is clicked"""

    global curr_select_course_button_i_j

    # course code
    course_name_label = Label(root, text=vertex_obj.course_code, fg='black', bg='white', font=('Calibri', 20))
    course_name_label.place(x=490, y=460)

    # description
    textbox1.delete("1.0", "end")
    textbox1.insert(END, vertex_obj.description)  # switch here, i and j cuz of matrix indexing

    # stars
    canvas_star = Canvas(root, width=250, height=50, bg="white")
    canvas_star.place(x=620, y=700)

    number_of_int_stars = int(vertex_obj.rating)

    full_star = Image.open("full_star.png")
    full_star = full_star.resize((50, 50))
    full_star_image = ImageTk.PhotoImage(full_star)

    half_star = Image.open("half_star.png")
    half_star = half_star.resize((50, 50))
    half_star_image = ImageTk.PhotoImage(half_star)

    star_x_coordinate = 0

    for _ in range(number_of_int_stars):
        canvas_star.create_image(star_x_coordinate, 0, anchor=NW, image=full_star_image)
        star_x_coordinate += 50

    canvas_star.image = full_star_image

    if (round(vertex_obj.rating * 2) / 2) - 0.5 == number_of_int_stars:
        canvas_half_star = Canvas(root, width=50, height=50, bg="white", highlightthickness=0)
        canvas_half_star.place(x=620 + star_x_coordinate, y=703)

        canvas_half_star.create_image(1, 0, anchor=NW, image=half_star_image)
        canvas_half_star.image = half_star_image

    new_str = 'Select ' + vertex_obj.course_code

    select_course_button.configure(text=new_str)

    curr_select_course_button_i_j = (i_f, j_f)


def return_selected_course(select_course_button: Button, line_buttons: list, courses: list, textbox1: Text, root: Tk,
                           rectangles: list, degree_label_1: Label, degree_label_2: Label,
                           line_button_coordinates: list,
                           canvas: Canvas, all_after_j: list, interests: list, p: list) -> None:
    """If we select the chosen course, update it in the original selected courses"""

    global selected_course_text
    global selected_course
    global curr_select_course_button_i_j

    if curr_select_course_button_i_j[0] == -1 or curr_select_course_button_i_j[1] == -1:
        return

    selected_course_text = select_course_button['text'][7:]

    selected_course = g.get_vertex(selected_course_text)

    i_f = curr_select_course_button_i_j[0]
    j_f = curr_select_course_button_i_j[1]

    if selected_course.verify_course_list(dict_to_list(), i_f):

        final_courses[i_f][j_f] = selected_course
        line_buttons[i_f][j_f].configure(text=selected_course.course_code)
        line_buttons[i_f][j_f].configure(command=lambda: click(i_f, j_f, textbox1, root))

        update_requirements(rectangles, degree_label_1, degree_label_2, p)
        find_pre_req_and_draw_line(line_button_coordinates, canvas)

        cover_canvas = Canvas(root, width=175, height=755, bg="white", highlightthickness=0)
        cover_canvas.create_line(0, 200, 180, 200, fill="black", width=2)
        cover_canvas.place(x=1221, y=0)

        if check_if_required_courses_completed(courses):
            display_rest_of_buttons(root, all_after_j, line_buttons, line_button_coordinates,
                                    textbox1, select_course_button, interests, p)

        selected_course = None

    curr_select_course_button_i_j = (-1, -1)
    select_course_button.configure(text="Select Course")


def dict_to_list() -> list:
    """Converts the dictionary of final_courses to a list"""

    lst = [[], [], [], []]

    for i in final_courses:
        for j in final_courses[i]:

            if final_courses[i][j] is not None:
                lst[i].append(final_courses[i][j])

    return lst


def update_requirements(rectangles: list, degree_label_1: Label, degree_label_2: Label, p: list) -> None:
    """Keeps checking whether the breath and program requiremets are fulfilles and keeps updating in the GUI"""

    breadth_req = get_breadth_req(dict_to_list())

    if breadth_req['Creative and Cultural Representations (1)'] >= 1:
        rectangles[0].configure(bg='green')

    if breadth_req['Thought, Belief and Behaviour (2)'] >= 1:
        rectangles[1].configure(bg='green')

    if breadth_req['Society and its Institutions (3)'] >= 1:
        rectangles[2].configure(bg='green')

    if breadth_req['Living Things and Their Environment (4)'] >= 1:
        rectangles[3].configure(bg='green')

    if breadth_req['The Physical and Mathematical Universes (5)'] >= 1:
        rectangles[4].configure(bg='green')

    if verify_breadth_req(dict_to_list()) and sum(get_credits_year(dict_to_list())) >= 20:
        degree_label_1.configure(fg='grey')
        degree_label_2.configure(fg='green')

    if all(program.isComplete(dict_to_list(), g) for program in p):
        rectangles[5].configure(bg='green')


def find_pre_req_and_draw_line(line_button_coordinates: list, canvas: Canvas) -> None:
    """Draws line by finding if courses are pre-requisites of each other"""

    for i in final_courses:

        for m in final_courses:

            for j in final_courses[i]:

                for k in final_courses[i]:

                    if (final_courses[i][j] is not None and final_courses[m][k] is not None
                            and final_courses[m][k].course_is_prereq(final_courses[i][j])):
                        draw_dotted_line(line_button_coordinates[i][j][0], line_button_coordinates[i][j][1],
                                         line_button_coordinates[m][k][0], line_button_coordinates[m][k][1], canvas)


def display_rest_of_buttons(root: Tk, all_after_j: list, line_buttons: list,
                            line_button_coordinates: list, textbox1: Text, select_course_button: Button,
                            interests: list, p: list) -> None:
    """Displays the rest of the optional buttins once all the program requirements are fulfilled"""

    for i in range(len(final_courses)):

        after_j = all_after_j[i]
        curr_credits = 0

        while curr_credits < 5.0 and after_j <= 9:
            line_buttons[i][after_j].configure(text="Choose")
            line_buttons[i][after_j].configure(bg="#ADD8E6")

            (line_buttons[i][after_j].configure
             (command=lambda i_f=i, j_f=after_j: make_course_choice(root, i_f, j_f, [], textbox1, select_course_button,
                                                                    interests, p)))

            line_buttons[i][after_j].place(x=line_button_coordinates[i][after_j][0],
                                           y=line_button_coordinates[i][after_j][1])

            curr_credits += 0.5
            after_j += 1


def check_if_required_courses_completed(courses: list) -> bool:
    """Checks if the user has chosen all the program required courses"""

    len_of_courses = sum([len(x) for x in courses])

    len_of_final_courses = sum([len(x) for x in dict_to_list()])

    return len_of_courses == len_of_final_courses


if __name__ == '__main__':

    specs = get_programs_list()['Specialist']

    p_main = []
    courses_main = []
    interests_main = []

    for sp in specs:
        if sp[1] == 'Computer Science Specialist':
            p_main.append(get_program(sp[0], sp[1]))

    for pr in p_main:
        courses_main = pr.get_required_courses(g)

    initialize_new_window(interests_main, courses_main, p_main)
