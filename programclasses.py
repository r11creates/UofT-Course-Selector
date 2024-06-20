""" Contains the Program Class, Credit Requirement Class and the Limit Class, that all help parse Program data
Also contains a plethora of helper functions
"""
from __future__ import annotations
from typing import Optional, Any, Union
from CourseParse import parse_courses, get_credits, CourseCollection, CourseOr
from initializer import Graph, generate_graph_from_file, CourseVertex, CourseOrVertex, CourseAndVertex, course_in_list
import csv
import os

PRINT = False  # bool to check whether to print during doctests


def get_full_courselist(filename: str = 'courses.csv') -> list[str]:
    """Get a list of all course codes"""

    courselist = []

    with open(filename, "r", newline="", encoding='utf-8') as f:
        reader = csv.reader(f, delimiter="|")

        for row in reader:
            courselist.append(row[0])

    return courselist


def get_keyword_courselist(keyword: str, filename: str = 'courses.csv') -> list[str]:
    """Get a list of all course codes given a keyword, ie. 300-level CSC courses by CSC3XX"""

    courselist = []

    with open(filename, "r", newline="", encoding='utf-8') as f:
        reader = csv.reader(f, delimiter="|")

        for row in reader:
            if row[0][:4] == keyword:
                courselist.append(row[0])

    return courselist


def get_courses_from_course_list(course_list: list[list[CourseVertex]]) -> list[CourseVertex]:
    """Get a list of Course Vertices from a given Course_list"""
    courses = []

    for year in course_list:
        for course in year:
            courses.append(course)

    return courses


def get_programs_list() -> dict[str, list[tuple]]:
    """Returns a Dict with Specialist, Major, Minor as keys
    and the values as Tuples including the name of the Program and the filepath
    """
    programs = {
        'Specialist': [],
        'Major': [],
        'Minor': []
    }

    for typeP in programs:
        progs = os.listdir(os.curdir + f"/Programs/{typeP}/")
        for p in progs:
            programs[typeP].append((os.curdir + f"/Programs/{typeP}/{p}", p.replace('_', ' ')[:-4]))

    return programs


def get_program(progFile: str, progName: str) -> Program:
    """Returns the program based on the progFile and program Name"""

    with open(progFile, 'r') as f:
        s = f.read()

    return Program(s, progName)


class Limit:
    """
    Limits on Credit Requirements, it may be a minimum or a maximum limit on given courses.

    Instance Attributes:
        - courses: list of courses that are part of the limit
        - credits: the number of credits it limits
        - typemin: Tells the type of the limit, max or min

    Representation Invariants:
        - self.credits > 0
    """

    courses: list[str]
    credits: float
    typemin: bool

    def __init__(self, credits: float, typemin: bool) -> None:
        """Initialize a Limit"""
        self.credits = credits
        self.typemin = typemin
        self.courses = []

    def add_courses(self, courses: str) -> None:
        """Add course options to self.courses
        if course is like CSC3XX, it will add all 300-level CSC courses"""

        if courses[4:6] == 'XX':
            self.courses.extend(get_keyword_courselist(courses[:4]))
            return

        c = parse_courses(courses)
        if isinstance(c, CourseCollection):
            self.courses.extend(c.courses)

        elif c is None:
            return

        else:
            self.courses.append(c)

    def check_limit(self, courses: list[str]) -> bool:
        """Makes sure all the limits are being adhered to by a given list of courses"""
        credit_count = 0

        if self.typemin:
            for course in courses:
                if course in self.courses:
                    credit_count += get_credits(course)

            return credit_count >= self.credits

        for course in courses:

            if course in self.courses:
                credit_count += get_credits(course)

        return credit_count <= self.credits

    def __str__(self) -> str:
        """String Representation of the limit"""
        return str(self.credits) + f"({'min' if self.typemin else 'max'}): " + str(self.courses)


class CreditRequirement:
    """
    Contains Data that helps pick a few courses from self.courses list within self.limits worth self.credits for 3rd and 4th year

    Instance Attributes:
        - courses: list of courses that are part of the Credit Requirement
        - credits: Number of credits that need to be completed
        - limits: Various limits applied on the Credit Requirement

    Representation Invariants:
        - self.credits > 0
    """
    courses: list[str]
    credits: float
    limits: list[Limit]

    def __init__(self, credits: float) -> None:
        """Initialize a Credit Requirement"""
        self.credits = credits
        self.courses = []
        self.limits = []

    def add_courses(self, courses: str) -> None:
        """Add a course option to the Credit Requirement
        If course is like CSC3XX, it will add all 300-level CSC courses
        """
        if courses[4:6] == 'XX':
            self.courses.extend(get_keyword_courselist(courses[:4]))
            return

        c = parse_courses(courses)
        if isinstance(c, CourseCollection):
            self.courses.extend(c.courses)

        else:
            self.courses.append(c)

    def add_exclusions(self, courses: str) -> None:
        """Add exclusion to the course options
        Removes Courses from the course list
        """
        for course in courses.split(', '):

            if course in self.courses:
                self.courses.remove(course.strip())

    def add_limit(self, courses: list[str], credits: float, limit_type: str = 'min'):
        """Add Limits to the Credit Requirements"""
        limit = Limit(credits, limit_type == 'min')

        for course in courses:
            limit.add_courses(course.strip())

        self.limits.append(limit)

    def check_validity(self, courses: list, debug: bool = False) -> bool:
        """Checks the validity of the courses and sees if they pass all the requirements and limits

        >>> cr = CreditRequirement(5.0)
        >>> courses = "CSC3XX, CSC4XX, MAT3XX, MAT4XX, STA3XX, STA4XX, BCB410H1, BCB420H1, BCB330Y1/​ BCB430Y1, MAT224H1/​ MAT247H1, MAT235Y1/​ MAT237Y1/​ MAT257Y1".split(', ')
        >>> for course in courses:
        ...     cr.add_courses(course)
        >>> cr.add_limit(["CSC4XX", "BCB4XX"], 1.5, 'min')
        >>> cr.add_limit("MAT3XX, STA4XX, STA3XX, STA4XX".split(", "), 2.0, 'max')
        >>> cr.add_limit("CSC490H1, CSC491H1, CSC494H1, CSC495H1, CSC494Y1, BCB330Y1/​ BCB430Y1".split(', '), 1.0, 'max')
        >>> cr.add_limit("CSC301H1, CSC302H1, CSC318H1, CSC404H1, CSC413H1, CSC417H1, CSC418H1, CSC419H1, CSC420H1, CSC428H1, CSC454H1, CSC485H1, CSC490H1, CSC491H1, CSC494H1, CSC495H1, CSC494Y1".split(', '), 0.5, 'min')
        >>> v = cr.check_validity("CSC301H1, CSC302H1, CSC318H1, CSC404H1, CSC413H1, CSC417H1, CSC428H1, CSC419H1, CSC420H1, CSC490H1".split(', '))
        >>> v2 = cr.check_validity("MAT354H1, MAT363H1, MAT367H1, MAT377H1, MAT382H1, CSC417H1, CSC428H1, CSC419H1, CSC420H1, CSC490H1".split(', '))
        >>> print(v)
        True
        >>> print(v2)
        False
        """

        # Check if every course in courses exists as an option
        credits = 0.0
        for course in courses:
            if course not in self.courses:
                continue

            elif isinstance(course, str):
                credits += get_credits(course)

        if credits < self.credits:
            if PRINT:
                print("Inadequate credits requirement:", credits, "/", self.credits)
            return False
            # raise ValueError

        for limit in self.limits:
            if not limit.check_limit(courses):
                if PRINT:
                    print("Does not pass limit-", str(limit))
                return False
                # raise ValueError

        return True

    def __str__(self) -> str:
        """String representation of the Credit Requirement"""
        s = str(self.credits) + ": " + str(self.courses)

        for limit in self.limits:
            s += '\n\t' + str(limit)

        return s


class Program:
    """
    Contains Data of all required courses in each year, along with all the Credit Requirements.

    Instance Attributes:
        - y1: Contains all the courses required by the program in year 1
        - y2: Contains all the courses required by the program in year 2
        - y3: Contains all the courses required by the program in year 3
        - y4: Contains all the courses required by the program in year 4
        - credReqs: Contains all the Credit Requirements for the course
        - name: Name of the Program

    Representation Invariants:
        - self.name != ''
    """
    y1: Optional[Union[CourseCollection, str]]
    y2: Optional[Union[CourseCollection, str]]
    y3: Optional[Union[CourseCollection, str]]
    y4: Optional[Union[CourseCollection, str]]
    creditReqs: list[CreditRequirement]
    name: str

    def __init__(self, programtxt: str, fname: str = 'Unamed Program') -> None:
        """
        Intialize a Program by parsing the programtxt in the following manner:

            Line 1: Required Courses in Year 1
            Line 2: Required Courses in Year 2
            Line 3: Required Courses in Year 3
            Line 4: Required Courses in Year 4
            Line 4+: Contains Credit Requirements

                IF line N is not indented: - New Credit Requirement, with given Credits and Courses at line N
                                           - line N+1 is the exclusions of the Credit Requirement
                                           - indented lines till the next Credit Requirements contain the Limits

                IF line is indented: - Line is either exclusion or Limit

            Format of Credit Requirement: <No. of Credits>: <List of Courses>
            Format of exclusion: exclusion: <List of Courses>
            Format of Limit: <No. of Credits>(<Type of Limit>):<List of Courses>
        """
        programlst = programtxt.split('\n')

        self.y1 = parse_courses(programlst[0])
        self.y2 = parse_courses(programlst[1])
        self.y3 = parse_courses(programlst[2])
        self.y4 = parse_courses(programlst[3])
        self.creditReqs = []
        self.name = fname

        reqs = []

        for i, line in enumerate(programlst[4::]):
            if not line[0].isspace():
                reqs.append(i + 4)

        for j in range(len(reqs)):

            rlst = programlst[reqs[j]:reqs[j + 1]] if j + 1 < len(reqs) else programlst[reqs[j]:]

            colon = rlst[0].index(':')
            credits = float(rlst[0][0:colon])
            courses = rlst[0][colon + 1:].split(', ')

            cr = CreditRequirement(credits)
            for course in courses:
                cr.add_courses(course.strip())

            for line in rlst[1:]:
                colon = line.index(':')
                if line[:colon].strip() == 'exclusion':
                    exclusion = line[colon + 1:]
                    cr.add_exclusions(exclusion)
                    continue

                limit_credits = float(line[:colon - 5].strip())
                limit_type = line[colon - 4: colon - 1]
                limit_courses = line[colon + 1:].split(', ')

                cr.add_limit(limit_courses, limit_credits, limit_type)

            self.creditReqs.append(cr)

    def __str__(self) -> str:
        """String Representation of Programs"""
        s = 'Year 1: ' + str(self.y1) + '\n'
        s += 'Year 2: ' + str(self.y2) + '\n'
        s += 'Year 3: ' + str(self.y3) + '\n'
        s += 'Year 4: ' + str(self.y4) + '\n'

        for cr in self.creditReqs:
            s += str(cr) + '\n'

        return s

    def get_required_courses(self, g: Graph) -> list[list[CourseVertex]]:
        """Returns a list of Required Course vertices for each year for self.program"""

        if isinstance(self.y1, CourseOr) or isinstance(self.y1, str):
            y1 = [g.get_course(self.y1)]
        else:
            y1 = [g.get_course(c) for c in self.y1.courses if c is not None] if self.y1 is not None else []

        if isinstance(self.y2, CourseOr) or isinstance(self.y2, str):
            y2 = [g.get_course(self.y2)]
        else:
            y2 = [g.get_course(c) for c in self.y2.courses if c is not None] if self.y2 is not None else []

        if isinstance(self.y3, CourseOr) or isinstance(self.y3, str):
            y3 = [g.get_course(self.y3)]
        else:
            y3 = [g.get_course(c) for c in self.y3.courses if c is not None] if self.y3 is not None else []

        if isinstance(self.y4, CourseOr) or isinstance(self.y4, str):
            y4 = [g.get_course(self.y4)]
        else:
            y4 = [g.get_course(c) for c in self.y4.courses if c is not None] if self.y4 is not None else []

        return [y1, y2, y3, y4]

    def isComplete(self, course_list: list[list[CourseVertex]], g: Graph) -> bool:
        """
        Checks whether all required Courses are completed
        Checks if all Credit Requirements are completed
        Checks if all Limits are adhered to
        """
        required = self.get_required_courses(g)

        for year in required:
            for c in required:
                if isinstance(c, CourseVertex):
                    if not course_in_list(c, course_list):
                        return False
                elif isinstance(c, CourseOrVertex):
                    if not any([course_in_list(course, course_list) for course in c.get_neighbours()]):
                        return False
                elif isinstance(c, CourseAndVertex):
                    if not all([course_in_list(course, course_list) for course in c.get_neighbours()]):
                        return False

        for credReq in self.creditReqs:
            if not credReq.check_validity([str(course) for course in get_courses_from_course_list(course_list)]):
                return False

        return True


if __name__ == "__main__":
    # cr = CreditRequirement(5.0)
    # courses = "CSC3XX, CSC4XX, MAT3XX, MAT4XX, STA3XX, STA4XX, BCB410H1, BCB420H1, BCB330Y1/​ BCB430Y1,
    # MAT224H1/​ MAT247H1, MAT235Y1/​ MAT237Y1/​ MAT257Y1".split(', ')
    # for course in courses:
    #     cr.add_courses(course)

    # cr.add_limit(["CSC4XX", "BCB4XX"], 1.5, 'min')
    # cr.add_limit("MAT3XX, STA4XX, STA3XX, STA4XX".split(", "), 2.0, 'max')
    # cr.add_limit("CSC490H1, CSC491H1, CSC494H1, CSC495H1, CSC494Y1, BCB330Y1/​ BCB430Y1".split(', '), 1.0, 'max')
    # cr.add_limit("CSC301H1, CSC302H1, CSC318H1, CSC404H1, CSC413H1, CSC417H1, CSC418H1, CSC419H1, CSC420H1,
    # CSC428H1, CSC454H1, CSC485H1, CSC490H1, CSC491H1, CSC494H1, CSC495H1, CSC494Y1".split(', '), 0.5, 'min')

    # v = cr.check_validity("CSC301H1, CSC302H1, CSC318H1, CSC404H1, CSC413H1, CSC417H1, CSC428H1, CSC419H1, CSC420H1,
    # CSC490H1".split(', '))

    # v2 = cr.check_validity("MAT354H1, MAT363H1, MAT367H1, MAT377H1, MAT382H1, CSC417H1, CSC428H1, CSC419H1, CSC420H1,
    # CSC490H1".split(', '))
    # print(v2)

    g = generate_graph_from_file('courses.csv')

    CSspec = Program("""CSC110Y1, CSC111H1, (MAT137Y1/​ MAT157Y1)
CSC207H1, CSC209H1, (STA237H1/ STA247H1/ STA255H1/ STA257H1), CSC236H1, CSC258H1, CSC263H1/​ CSC265H1, MAT223H1/​
MAT240H1; STA247H1/​ STA237H1/​ STA255H1/​ STA257H1
CSC369H1, CSC373H1

5.0: CSC3XX, CSC4XX, MAT3XX, MAT4XX, STA3XX, STA4XX, BCB410H1, BCB420H1, BCB330Y1/​ BCB430Y1, MAT224H1/​ MAT247H1,
 MAT235Y1/​ MAT237Y1/​ MAT257Y1
    exclusion: MAT329Y1, MAT390H1, MAT391H1, STA248H1,​ STA238H1,​ STA261H1
    1.5(min): CSC4XX, BCB4XX
    2.0(max): MAT3XX, STA4XX, STA3XX, STA4XX
    1.0(max): CSC490H1, CSC491H1, CSC494H1, CSC495H1, CSC494Y1, BCB330Y1/​ BCB430Y1
    0.5(min): CSC301H1, CSC302H1, CSC318H1, CSC404H1, CSC413H1, CSC417H1, CSC418H1, CSC419H1, CSC420H1, CSC428H1,
    CSC454H1, CSC485H1, CSC490H1, CSC491H1, CSC494H1, CSC495H1, CSC494Y1""")

    print(CSspec.get_required_courses(g))

    # import doctest

    # PRINT = False
    # doctest.testmod(verbose=True)
    # PRINT = True
