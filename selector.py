"""File Contains the Selector Class and some helper functions
Selector class helps pick interested courses, pick required courses,
recommend courses and even auto generate course lists, based on program requirements.
"""
from programclasses import Program, get_program, get_courses_from_course_list
from initializer import CourseVertex, Graph, CourseOrVertex, CourseAndVertex, generate_graph_from_file, course_in_list
from CourseParse import get_credits
from random import randint
from typing import Optional, Any

PRINT = False


def course_list_combiner(course_list1: list[list[CourseVertex]], course_list2: list[list[CourseVertex]],
                         limit: bool = True) -> list[list[CourseVertex]]:
    """Takes in 2 course_lists and combines them"""

    combined_course_list = [[], [], [], []]
    for year in range(4):
        combined_course_list[year].extend(course_list1[year])
        combined_course_list[year].extend(course_list2[year])

        if limit and sum([get_credits(course.course_code) for course in combined_course_list[year]]) > 6.0:
            print("Too Many Courses, in year:", year + 1)
            raise ValueError

    return combined_course_list


def verify_course_list(course_list: list[list[CourseVertex]]) -> bool:
    """Checks each course in course_list and makes sure they are valid with given course_list"""
    for year in range(4):
        for course in course_list[year]:
            if not course.verify_course_list(course_list, year):
                return False
    return True


def get_breadth_req(course_list: list[list[CourseVertex]]) -> dict[str, float]:
    """Returns a Dict with the number of credits completed in each breadth requirement category"""

    breadth_reqs = {
        'Creative and Cultural Representations (1)': 0.0,
        'Thought, Belief and Behaviour (2)': 0.0,
        'Society and its Institutions (3)': 0.0,
        'Living Things and Their Environment (4)': 0.0,
        'The Physical and Mathematical Universes (5)': 0.0
    }

    for year in course_list:
        for course in year:
            if course.breadthreq != '' or course.breadthreq is not None:
                if course.breadthreq in breadth_reqs:
                    breadth_reqs[course.breadthreq] += get_credits(course.course_code)
                for br in course.breadthreq.split(', '):
                    if br.strip() in breadth_reqs:
                        breadth_reqs[br.strip()] += get_credits(course.course_code)

    return breadth_reqs


def verify_breadth_req(course_list: list[list[CourseVertex]]) -> bool:
    """Verifies whether the given course_list has completed the Breadth Requirements"""

    breadth_reqs = get_breadth_req(course_list)

    completed = 0
    half_complete = 0
    for breadth_req in breadth_reqs:
        if breadth_reqs[breadth_req] >= 1.0:
            completed += 1
        else:
            half_complete += 1

    if completed >= 4:
        return True

    elif completed == 3 and half_complete == 2:
        return True

    if PRINT:
        print(breadth_reqs)
    return False


def get_credits_year(course_list: list[list[CourseVertex]]) -> list[float]:
    """Returns a list of credits completed in each year"""
    creds = []

    for year in course_list:
        c = 0.0
        for course in year:
            c += get_credits(course.course_code)

        creds.append(c)

    return creds


def deep_copy_course_list(course_list: list[list[CourseVertex]]) -> list[list[CourseVertex]]:
    """Creates a Deep copy of the course list and returns it"""
    copy = [[], [], [], []]

    for year in range(4):
        for course in course_list[year]:
            copy[year].append(course)

    return copy


def calculate_interest_score(course: CourseVertex, interests: list[tuple[Any]]) -> float:
    """Calculates a heuristic score based on user preferences and weighted interests"""
    total = 0
    total_weight = 0

    for interest_name, interest_weight in interests:
        total += course.interest_scores[interest_name.lower().replace(' ', '_')] * interest_weight
        total_weight += interest_weight

    return total / total_weight if total_weight > 0 else 0


class CourseSelector:
    """
    A Selector that helps picks courses

    Instance Attributes:
        - programs: List of the various programs the selector must take into account
        - graph: Graph of the courses

    Representation Invariants:
        - self.programs != []
        - self.g._vertices != {}
    """

    programs: list[Program]
    graph: Graph

    def __init__(self, programs: list[Program], g: Graph) -> None:
        """Initialises a CourseSelector"""
        self.programs = programs
        self.graph = g

    def get_from_collection(self, course_collection: CourseAndVertex | CourseOrVertex,
                            course_list: list[list[CourseVertex]]) -> list[CourseVertex]:
        """Returns a list of valid courses that can be added to the course_list from a course collection"""
        courses = []

        if isinstance(course_collection, CourseAndVertex):
            c_list = deep_copy_course_list(course_list)
            for c in course_collection.get_neighbours():

                if isinstance(c, CourseVertex):
                    courses.append(c)
                    c_list[0].append(c)
                elif c is None:
                    if PRINT:
                        print("Course is None")
                    raise ValueError
                else:
                    courses.extend(self.get_from_collection(c, c_list))

        elif isinstance(course_collection, CourseOrVertex):

            options = course_collection.get_neighbours()

            for c in options:
                if isinstance(c, CourseVertex):
                    c_list = deep_copy_course_list(course_list)
                    c_list[3].append(c)
                    if verify_course_list(c_list):
                        courses.append(c)
                        return courses

                elif c is None:
                    if PRINT:
                        print("Course is None")
                    raise ValueError
                else:
                    if len(self.get_from_collection(c, course_list)) > 0:
                        courses.extend(self.get_from_collection(c, course_list))
                        return courses

        return courses

    def retrieve_available_courses(self, maxlevel: int, breadth_reqs: list[str] = None) -> list[CourseVertex]:
        """Returns a list of courses based on the maxlevel and breadth requirements"""
        courses = self.graph.get_all_courses()
        available_courses = []

        for course in courses:
            if int(course.course_code[-5]) <= maxlevel and (breadth_reqs is None or course.breadthreq in breadth_reqs):
                available_courses.append(course)

        return available_courses

    def get_an_interest_course(self, course_list: list[list[CourseVertex]],
                               year: int,
                               interests: list[str],
                               course_options: list[CourseVertex] = None,
                               breadth_req: list[str] = []) -> CourseVertex:
        """Returns a Course Vertex that will interest the user and is valid for the given course_list"""

        courses = self.retrieve_available_courses(year, breadth_req if len(
            breadth_req) > 0 else None) if course_options is None else [c for c in course_options if c is not None]
        courses = sorted(courses, key=lambda x: calculate_interest_score(x, interests), reverse=True)

        r = 0

        c_list = deep_copy_course_list(course_list)
        c_list[year - 1].append(courses[r])
        # courses[r].verify_course_list(course_list, year-1)

        run = 0
        while (not verify_course_list(c_list)) or courses[r] in get_courses_from_course_list(
                course_list):  # course_in_list(courses[r], course_list):

            run += 1

            if run > 100:
                return None
            # print(courses[r].course_code)
            if r == len(courses) - 1:
                if PRINT:
                    print(len(courses), courses)
            r += 1

            c_list = deep_copy_course_list(course_list)
            c_list[year - 1].append(courses[r])

        return courses[r]

    def select_courses(self, interests: list, c_list: Optional[list[list[CourseVertex]]] = None) -> Optional[
        list[list[CourseVertex]]]:
        """
        First Pick all the first year required courses, then Second year
        then Third year and Fourth Year.
        """

        course_list = [[], [], [], []] if c_list is None else deep_copy_course_list(c_list)

        # Go through every selected Programs and then add in the required courses of each year
        for program in self.programs:
            course_list = course_list_combiner(course_list, self.select_required_courses(program, course_list))

        run = 0
        # Keep trying until you get a valid course list
        while not verify_course_list(course_list):

            run += 1
            course_list = [[], [], [], []] if c_list is None else deep_copy_course_list(c_list)

            if run > 20:
                return course_list

            for program in self.programs:
                course_list = course_list_combiner(course_list, self.select_required_courses(program, course_list))

        # Find the credits already fulfilled in year 1 and year 2
        total_credits = get_credits_year(course_list)
        y1credits = total_credits[0]
        y2credits = total_credits[1]

        # Keep adding courses to year 1 until it has atleast 5.0 credits
        while y1credits < 5.0:

            # Keep track of all breadth requirements that have less than 1.0 credit in the breadth
            breadth_reqs = []

            if not verify_breadth_req(course_list):
                brs = get_breadth_req(course_list)
                for br in brs:
                    if brs[br] < 1:
                        breadth_reqs.append(br)

            # Find courses interesting to the user and add it to the course_list at year 1
            c = self.get_an_interest_course(course_list, 1, interests, None, breadth_reqs)
            if c is None:
                return course_list
            course_list[0].append(c)
            y1credits = get_credits_year(course_list)[0]

        # Keep adding courses to year 2 until it has atleast 5.0 credits
        while y2credits < 5.0:

            # Keep track of all breadth requirements that have less than 1.0 credit in the breadth
            breadth_reqs = []

            if not verify_breadth_req(course_list):
                brs = get_breadth_req(course_list)
                for br in brs:
                    if brs[br] < 1:
                        breadth_reqs.append(br)

            # Find courses interesting to the user and add it to the course_list at year 2
            c = self.get_an_interest_course(course_list, 2, interests, None, breadth_reqs)
            if c is None:
                return course_list
            course_list[1].append(c)
            y2credits = get_credits_year(course_list)[1]

        for program in self.programs:

            # Check and complete all credit requirements for each program
            for credreq in program.creditReqs:
                # Get all course options to pick from
                course_opt = [self.graph.get_course(c) for c in credreq.courses]
                # Add completed credits or start with 0 credits if no course is already completed
                credreq_credits = sum(
                    [get_credits(c.course_code) for c in course_opt if course_in_list(c, course_list)])
                # Remove courses that are already part of the course_list
                course_opt = [c for c in course_opt if not course_in_list(c, course_list)]

                # Go through all the minimum requirements of the credit requirement
                for limit in credreq.limits:

                    # Skip if it is a maximum type requirement
                    if not limit.typemin:
                        continue

                    # Similar to what we did for credit requirements
                    limit_credits = sum([get_credits(c.course_code)
                                         for c in get_courses_from_course_list(course_list)
                                         if c.course_code in limit.courses])
                    limit_course_opt = [self.graph.get_course(c) for c in limit.courses]
                    limit_course_opt = [c for c in limit_course_opt if not course_in_list(c, course_list)]

                    # Keep adding courses till the minimum requirement is fulfilled
                    while limit_credits < limit.credits:

                        if get_credits_year(course_list)[2] < 5.0:
                            c = self.get_an_interest_course(course_list, 3, interests, limit_course_opt)
                            if c is None:
                                return course_list
                            course_list[2].append(c)
                            credreq_credits += get_credits(c.course_code)
                            limit_credits += get_credits(c.course_code)
                            limit_course_opt.remove(c)
                            course_opt.remove(c)

                        else:
                            c = self.get_an_interest_course(course_list, 4, interests, limit_course_opt)
                            if c is None:
                                return course_list
                            course_list[3].append(c)
                            credreq_credits += get_credits(c.course_code)
                            limit_credits += get_credits(c.course_code)
                            limit_course_opt.remove(c)
                            course_opt.remove(c)

                # Keep adding courses until it fulfills credit requirement
                while credreq_credits < credreq.credits:

                    if get_credits_year(course_list)[2] < 5.0:
                        c = self.get_an_interest_course(course_list, 3, interests, course_opt)
                        if c is None:
                            return course_list
                        course_list[2].append(c)
                        credreq_credits += get_credits(c.course_code)
                        course_opt.remove(c)

                    else:
                        c = self.get_an_interest_course(course_list, 4, interests, course_opt)
                        if c is None:
                            return course_list
                        course_list[3].append(c)
                        credreq_credits += get_credits(c.course_code)
                        course_opt.remove(c)

        # Keep adding courses until it fulfills the minimum 20.0 credits to recieve undergrad degree
        while sum(get_credits_year(course_list)) < 20.0:

            if get_credits_year(course_list)[2] < 5.0:
                c = self.get_an_interest_course(course_list, 3, interests)
                if c is None:
                    return course_list
                course_list[2].append(c)

            else:
                c = self.get_an_interest_course(course_list, 4, interests)
                if c is None:
                    return course_list
                course_list[3].append(c)

        # FOR DEBUG PURPOSES: Checking whether all credits requirements have been fulfilled and are valid
        courses_list_str = [str(c) for c in get_courses_from_course_list(course_list)]
        for program in self.programs:
            for credreq in program.creditReqs:
                if PRINT:
                    print(credreq.check_validity(courses_list_str, debug=True))

        return course_list

    def select_required_courses(self, program: Program, c_list: Optional[list[list[CourseVertex]]]) -> list[
        list[CourseVertex]]:
        """Returns a list of list of required courses for each year
        based on the program"""

        courses = program.get_required_courses(self.graph)

        course_list = [[], [], [], []]

        for year in range(4):

            for c in courses[year]:

                if isinstance(c, CourseVertex):

                    if not course_in_list(c, c_list):
                        course_list[year].append(c)

                elif c is None:
                    continue

                elif isinstance(c, CourseAndVertex):
                    if all([course_in_list(self.graph.get_vertex(course), c_list) for course in c.neighbours]):
                        continue
                    test_list = course_list_combiner(course_list, c_list)
                    course_list[year].extend(self.get_from_collection(c, test_list))

                elif isinstance(c, CourseOrVertex):
                    if any([course_in_list(self.graph.get_vertex(course), c_list) for course in c.neighbours]):
                        continue
                    test_list = course_list_combiner(course_list, c_list)
                    course_list[year].extend(self.get_from_collection(c, test_list))

                else:
                    test_list = course_list_combiner(course_list, c_list)
                    course_list[year].extend(self.get_from_collection(c, test_list))

        return course_list

    def recomend_courses(self, course_list: list[list[CourseVertex]], year: int, interests: list[tuple[Any]],
                         breadth_req: list[str] = [], course_options: list[CourseVertex] = None) -> list[CourseVertex]:
        """Recommends a list of Courses based on a given course_list for the given year, interests, breadth requirements.
        It also optionally takes in course options to recommend from
        """
        courses = self.retrieve_available_courses(year, breadth_req if len(
            breadth_req) > 0 else None) if course_options is None else [c for c in course_options if c is not None]
        courses = sorted(courses, key=lambda x: calculate_interest_score(x, interests), reverse=True)
        recomended_courses = []

        r = 0

        # courses[r].verify_course_list(course_list, year-1)

        for r in range(len(courses)):

            c_list = deep_copy_course_list(course_list)
            c_list[year - 1].append(courses[r])

            if verify_course_list(c_list) and (courses[r] not in get_courses_from_course_list(course_list)):
                recomended_courses.append(courses[r])

        return recomended_courses


if __name__ == "__main__":
    print('Loading Graph')
    g = generate_graph_from_file('courses.csv')
    print('Graph Loaded')

    program = Program(get_program('Economics_Minor.txt'))
    focus = Program(get_program('Computer_Science_Minor.txt'))
    selector = CourseSelector([program, focus], g)
    course_list = [
        [g.get_vertex('CSC110Y1'), g.get_vertex('CSC111H1'), g.get_vertex('MAT137Y1'), g.get_vertex('AST199H1'),
         g.get_vertex('ESS105H1'), g.get_vertex('HPS205H1'), g.get_vertex('HPS120H1'), g.get_vertex('MAT223H1')], [],
        [], []]
    interests = [('economics', 2), ('computer_science', 1)]
    # print(selector.recomend_courses(course_list, 2, interests))

    cl = selector.select_courses(interests)
    print(program.isComplete(cl, g))
    print(cl)
    print(verify_course_list(cl))
    print(verify_breadth_req(cl))

    print("YAAAAAAAAAAAAAAYYYYY")
