# Course Selector UofT

A program that suggests university courses based on your program and provides a custom GUI to customize your course
plan. Created to help UofT students in Python using graphs and Tkinter.

<img width="892" alt="Screenshot 2024-04-04 at 2 28 06 AM" src="https://github.com/Jai0212/Course-Selector-UofT/assets/86296165/804570e1-5fc5-4b1d-bf5d-365facbecdde">

Selecting courses for new students based on your program and breadth requirements (electives) can be a cumbersome task,
especially
for first years. With the availability of so many courses and so many breadth requirement options, it is quite
overwhelming for someone to decide on courses. It also takes a lot of time. Wouldn’t it be easier if you just have a
program that recommends you courses based on your program and interests?

Using graphs, we created a UofT course recommender based on your program and interests. It takes into
account for the prerequisites, co-requisites, and exclusions of each course.
On the interactive GUI (created in Tkinter) that we use to run our program, the user inputs the specialist, major, and
minor
combination of their choice. Then, they are presented with the option to auto-generate a course plan or alternatively,
customize their own plan.

In the case of customizing their own plan, the program recommends courses to fulfill program requirements and breadth
requirements based on the interests the user selects as well. It displays specific course recommendations for custom
specialist, major, and minor combinations of the given subset of UofT programs. The user gets to manually choose
the course they want to add to the plan.

**NOTE:** The GUI is specially designed for MacOS so it might look weird on other OSs


## Features

- Personalized course recommendations based on interests selected
- Auto generates a course plan for all 4 years of university
- Interactive user-friendly GUI to customize courses
- Course ratings and descriptions available for each course to make the right choice when choosing courses
- Arrow indicators to understand which course is a prerequisite for what
- Ability to make any choice of specialist, major or minor programs
- Ability to search for courses
- Ability to give course ratings
- Indications for breadth requirement (elective), program and degree completion

<img width="1391" alt="Screenshot 2024-04-04 at 1 02 53 AM" src="https://github.com/Jai0212/Course-Selector-UofT/assets/86296165/aa0d6645-6c88-4c04-920b-b519f2a09669">

## Technical Aspects

Packages Used:

- requests: Make GET requests to websites to get their response.
- BeautifulSoup: Parse the response from the request and scrape the required Data.
- pickle: Serialize and Unserialize Python objects using pickle.load and pickle.dump, in order to make ratings.bin to store all rating Data.
- CSV: Format Data and Store Data. Used to store Course Details.
- networkx: Format the graph and retrieve Position values that can be used to plot the graph.
- plotly: Visualize a given Graph, with customization.
- random: Generate Pseudo-Random Integers (random.randint). Used to generate Placeholder Ratings for Courses.
- os: Get files in a given directory (os.listdir) and the current directory (os.curdir). Used to find the Interests keywords and Program Files.
- pillow: Used to display images on the Tkinter window
- tkinter: Used to create an interactive GUI
- tkmacosx: Similarly, used to create an interactive GUI. However, this library is optimized for MacOS devices.


Graphs were used to design all algorithms. Computations performed on Graphs:

- Scraping Courses
- Parsing Courses
- Generating Graph
- Creating CourseVertex
- Creating CourseAndVertex and CourseOrVertex
- Generating Programs
- Verifying Course List
- Visualize Graph
- Auto Generating Course List
- Recommending Courses

Below is a more detailed explanation of some of the algorithms we created:

- Auto Generating Course List:
  - Given a list of Programs, Auto Generates Course List Based on Program requirements and Breadth Requirements. Optionally takes in a pre-filled course list if the user has already completed certain courses.
  - Whenever a course is added, we must make sure the resulting course list is valid.
  - First, we add all the required courses of all the programs, choices between multiple courses are made by picking the
  a course that would interest the student more, based on the given interests.
  - Second, we fill up Year 1 and Year 2 trying to complete all the Breadth Requirements, by picking courses interesting to the user.
  - Next, we Fill up Year 3 and Year 4, with courses from the Credit Requirements of each Program. Courses picked for completing Credit Requirement are first picked by the minimum limits. We then add the rest of the Courses for each Credit Requirement, making sure we do not cross any maximum limits.
  - Then we fill up the rest of the course list with courses that would interest the user.

- Recommending Courses:
  - Gives a list of Courses that when added to the course list will be valid, and it is ordered in descending order of interest to the user.
  - Optionally takes in Breadth Requirements, which filters the Courses and only picks the Courses that complete the breadth requirement.
  - Created a special list of files that stores keywords to match a particular score with a type of interest based on the course description.

<img width="1276" alt="Screenshot 2024-04-04 at 4 12 34 AM" src="https://github.com/Jai0212/Course-Selector-UofT/assets/86296165/5270bb17-cb36-49d8-8b7b-d0eaae612d92">


## Usage

In order to successfully run the program, the user has to install the libraries listed in the “requirements.txt” file
by entering the line below in the terminal:

pip install -r requirements.txt

**NOTE:** The GUI is specially designed for MacOS so it might look weird on other OSs

After having done this, the user should run “main.py” to start the program. Upon running this file, the user
can expect to see a window pop up titled “UofT Course Recommender” pop up.
The top of this window will have options for the user to select the specialist, major, and minor of their choice from
the dropdown list. However, the user can only select one of the following combinations:
i) 1 specialist
ii) 2 majors
iii) 1 major and 2 minors

If none of these combinations are chosen, the program will not run.

The user has to leave the dropdown box untouched if they would not like to use it. That is, if the user would like to select the first combination (just 1 specialist), then they need not make any changes to the other dropdown lists (i.e. all the other dropdowns should be ’None’). Similarly, if the user would like to choose 2 majors, then they need not select from any of the dropdown lists except the major dropdown and second major dropdown lists.

After selecting a combination, the user can choose his interests by clicking on the checkbox. This will be used in the selection of his electives/breadth requirement courses.

After filling in the dropdown boxes and the checkboxes, the user can either click the 'Generate Courses' button or the "Customize Courses" button.

If the "Generate Courses" button is clicked, the program will auto-generate a course plan based on the combination and interests chosen by the user. It will be displayed in the text box.

At the bottom of the window (below the text box), the user will have the option to input a course code and give the course a rating by clicking the “Upload Rating” button.There is also a 'Help' button on the top right which when pressed will tell you how to use the program.

If the "Customize Courses" button is clicked, it will close the current window and open a new window. This window will initially display all the courses that are required for that program. The courses that are already selected and are required for the program have a background colour of white. There will also be buttons named ’Choose’ which are light brown in colour. These are courses that are required but have a choice. For example, either one of MAT137Y1 or MAT157Y1 is required for CS but there is a choice. So, this will come in brown colour. Once you click on ’Choose’, on the right of the window, a choice will pop up between the courses. You can click on a course to select that course and then press the ’Select Course’ button on the bottom right to select that course (The ’Select Course’ button will change to ’Select MAT137Y1’ if MAT137 was selected). Sometimes no course will be displayed on the right even after pressing the brown button because it means you have to fill in the other brown buttons before coming on to this one because it needs to fulfill the prerequisites.

Once you have filled all the required courses (brown buttons), a lot of blue buttons will pop up. These buttons are for choosing all the other courses that you would need to fulfill breadth requirements or other program requirements. Once you click on a blue button, recommended courses will open up on the right which we generated based on the interests the user had input. There is also a search option available at the top right so you can search for custom courses and add them to your
courses. Just type the course code in the textbox and hit the 'Go' button. If that course satisfies all requirements and is not part of any exclusions, it will pop up and you will be able to select it (by clicking on the course button and then clicking the ’Select Course’ button on the bottom right).

You can also click on any course button and its description and rating (in stars, out of 5) will appear at the bottom so you can know more about the course and make a choice accordingly.

On the bottom left, all the breadth requirements and program requirements are mentioned and whether they have been fulfilled or not (indicated by a small coloured square, green if it is completed.)

You will also notice red arrows all around the GUI. If an arrow points to a course, it means the course at the origin of the arrow is a prerequisite to the course at the tip of the arrow. For example, CSC110 will point to CSC111 since CSC110 is a prerequisite for CSC111. This allows the user to graphically understand what courses he is choosing and which course is a prerequisite for which course.

Thus, we have created a visually pleasing and interactive GUI so that the user can customize and make his own course plan based on his program.
Lastly, you can run the 'initializer.py' file to visualize the graph that stores all the course vertices and edges.

**NOTE:** When entering the course code in the search bar or when entering the course code to rate a course, enter it in the format ’MAT137Y1’.

An example of how to run the project:

Run the 'main.py' file. A window will pop up. In the dropdown box next to 'Specialist', select 'Computer Science Specialist'. Select your interests by clicking on the checkboxes. Click 'Generate Courses' and you should see a sample list of courses displayed in the textbox based on each year. You can enter 'MAT137Y1' in the textbox next to the rating option and give the course a rating by selecting a value from the dropdown box. You can then click 'Customize Courses' and a new window should pop up. You can then click on the brown buttons and choose courses from the panel on the right. Once all brown-coloured courses are chosen, the blue-coloured buttons will appear and you can choose courses for those as well by either searching or selecting the recommended courses. Throughout the process, you can click on any course button and that course’s description and rating will appear at the bottom. While selecting the courses, you might also see the breadth or program requirement indicators changing on the bottom left.


## Acknowledgements

This project was created by Rithvik Sunil, Ashish Ajin Thomas and Jai Joshi.

The datasets used were:
 - Course Information: Obtained by web scraping using BeautifulSoup on UofT’s Arts and Sciences Website
 - Program Information:
Obtained by manual parsing based on Program information from UofT’s Programs Directory. This contains the program
requirements for the specialists, majors, and minors.
 - Ratings Information:
Obtained by randomized placeholder Values, generated by Python script. This is for the course
ratings.
 - Keywords Information:
Obtained by manual input. These keywords are related to the interests we displayed to the user.
