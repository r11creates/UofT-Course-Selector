
from typing import Any, Optional


def is_course_code(code: str) -> bool:
    """Returns whether the given code is a course code or not"""
    try:
        return code[:3].isalpha() and code[0:3].isupper() and code[3:6].isnumeric() and code[6] in "YH" and code[
            7] == "1" and len(code) == 8
    except IndexError:
        print("Tried", code)
        raise IndexError


def contains_course_code(txt: str) -> tuple[bool, Optional[int]]:
    """Returns a tuple consisting of whether a course code exists in the given txt and its index"""

    for i in range(len(txt) - 7):
        if is_course_code(txt[i: i + 8]):
            return True, i
    return False, None


def get_credits(course_code: str) -> float:
    """Returns credits of that particular course"""

    credits = {'H': 0.5, 'Y': 1.0}

    if course_code[0] in '([':
        crs = 0.0
        for course in course_code[1:-1].strip().replace('/', ",").split(','):
            crs += get_credits(course)
        return crs

    return credits[course_code[-2]]


class CourseCollection:
    """
    A Parent class, that represents a collection of Course Codes and/or CourseCollections

    Instance Attributes:
        - courses: list of course codes and/or CourseCollections

    Representation Invariants:
        - self.courses != []
    """
    courses: list

    def __init__(self, courses: list) -> None:
        """Initialize a CourseCollection"""
        self.courses = courses


class CourseAnd(CourseCollection):
    """
    A Sub-Class of CourseCollection, that represents a collection of Course Codes and/or CourseCollections,
    in which all are compulsory.

    Instance Attributes:
        - courses: list of course codes and/or CourseCollections

    Representation Invariants:
        - self.courses != []
    """

    def __str__(self) -> str:
        """String Representation of CourseAnd"""
        if len(self.courses) == 0:
            return ''

        s = f'[ {str(self.courses[0])}'
        for c in self.courses[1::]:
            s += f", {str(c)}"

        s += ' ]'

        return s


class CourseOr(CourseCollection):
    """
    A Sub-Class of CourseCollection, that represents a collection of Course Codes and/or CourseCollections,
    in which any one of them is required.

    Instance Attributes:
        - courses: list of course codes and/or CourseCollections

    Representation Invariants:
        - self.courses != []
    """

    def __str__(self) -> str:
        """String Representation of CourseOr"""

        if len(self.courses) == 0:
            return ''

        s = f'( {str(self.courses[0])}'
        for c in self.courses[1::]:
            s += f"/ {str(c)}"

        s += ' )'

        return s


def psplit(s: str, char: str) -> list[str]:
    """
    Splits the string with char as the delimiter without breaking up brackets
    >>> psplit('CSC110, (MAT137, MAT223), CSC111')
    ['CSC110', ' (MAT137, MAT223)', ' CSC111']
    """

    split = []
    left_i = 0
    for i in get_indices(char, s):

        if get_level(i, s) == 0:
            split.append(s[left_i:i])
            left_i = i + 1

    split.append(s[left_i::])
    return split


def parse_commas(courses: str) -> Any:
    """Unpacks a string of courses separated by commas"""

    course_list = []
    lst = psplit(courses, ',')
    for course in lst:
        has_course, i = contains_course_code(course)
        if has_course:
            c = parse_courses(course.strip())
            if c is not None:
                course_list.append(c)

    if len(course_list) > 1:
        return CourseAnd(course_list)
    return course_list[0] if len(course_list) == 1 else None


def parse_slashes(courses: str) -> Any:
    """Unpacks a string of course options separated by slashes"""

    course_list = []
    lst = psplit(courses, '/')
    for course in lst:
        has_course, i = contains_course_code(course)
        if has_course:
            c = parse_courses(course.strip())
            if c is not None:
                course_list.append(c)

    if len(course_list) > 1:
        return CourseOr(course_list)
    return course_list[0] if len(course_list) == 1 else None


def parse_brackets(courses: str) -> Any:
    """Unpacks a string of courses from a bracket"""

    left_index = courses.index('(')
    right_index = courses.index(')')

    while courses.count('(', left_index, right_index + 1) != courses.count(')', left_index, right_index + 1):
        right_index = courses.index(')', right_index + 1)

    return parse_courses(courses[left_index + 1:right_index])


def get_level(index: int, s: str) -> int:
    """
    Returns the level of an index in a string, ie. under how many brackets is the index
    >>> get_level(2, '((c))')
    2
    >>> get_level(2, 'abcde')
    0
    """

    string = s.replace('[', '(').replace(']', ')')

    return string.count('(', 0, index) - string.count(')', 0, index)


def get_indices(char: str, s: str) -> list[int]:
    """Returns the indices of a particular character in a string s"""

    indices = []
    prev = 0

    while char in s[prev::]:
        i = s.index(char, prev)
        indices.append(i)
        prev = i + 1

    return indices


def parse_courses(courses: str) -> Any:
    """
    Unpacks a string of courses into a list of the course names
    >>> parse_courses('CSC209H1,  CSC258H1,  CSC263H1/  CSC265H1,  STA247H1/  STA255H1/  STA257H1/  STA237H1/  ECO227Y1')
    ['CSC209H1', 'CSC258H1', {'CSC263H1', 'CSC265H1'},  {'STA247H1', 'STA255H1', 'STA257H1', 'STA237H1', 'ECO227Y1'}]
    """

    # Remove Extra whitespaces
    courses = " ".join(courses.split())
    # Reformat
    courses = courses.replace(".", ",").replace(";", ',').replace('+', ",").replace(" or", "/").replace(' Or',
                                                                                                        "/").replace(
        " OR", "/").replace(" And", ",").replace(" AND", ",").replace(" and", ',').replace('[', "(").replace(']', ')')

    if ',' in courses and min([get_level(i, courses) for i in get_indices(',', courses)]) == 0:
        # Check if comma is the highest priority
        # print("Highest Priority: ','")

        course_list = parse_commas(courses)
        return course_list

    elif '/' in courses and min([get_level(i, courses) for i in get_indices('/', courses)]) == 0:
        # Check if / has the highest priority
        # print("Highest Priority: '/'")

        course_list = parse_slashes(courses)
        return course_list

    elif '(' in courses:
        # Brackets have the highest priority
        # print("Highest Priority: '()'")

        course_list = parse_brackets(courses)

        if course_list is None and contains_course_code(courses):
            return parse_courses(courses[0:courses.index('('):])
        return course_list

    # Does not contain ',' or '(' or '/'
    else:
        has_course, i = contains_course_code(courses)
        if has_course:
            return courses[i:i + 8:]


if __name__ == "__main__":
    print(parse_courses(
        'CSC207H1, CSC209H1, (STA237H1/ STA247H1/ STA255H1/ STA257H1), CSC236H1, CSC258H1, CSC263H1/​ CSC265H1, '
        'MAT223H1/​ MAT240H1; STA247H1/​ STA237H1/​ STA255H1/​ STA257H1'))
