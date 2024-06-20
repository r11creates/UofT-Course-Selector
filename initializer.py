from __future__ import annotations
from typing import Any, Optional
from CourseParse import CourseAnd, CourseOr, parse_courses
import csv
import networkx as nx
import pickle
import os

PRINT = False  # print for debug purposes
INTERESTS = [interest[:-4] for interest in os.listdir(os.curdir + '/keywords/')]


def changeType(course: str) -> str:
    """Changes course from H1 course to a Y1 course and vice versa"""
    if course[-2] == "H":
        return course[0:-2] + 'Y1'
    return course[0:-2] + 'H1'


def course_in_list(course: _Vertex, course_list: list[list[CourseVertex]]) -> bool:
    """Checks whether the course is in any year of the course_list"""

    if isinstance(course, CourseVertex):
        for year in course_list:
            for c in year:
                if str(course) == str(c):
                    return True

    elif isinstance(course, CourseAndVertex):
        return all([course_in_list(c, course_list) for c in course.get_neighbours()])

    elif isinstance(course, CourseOrVertex):
        return any([course_in_list(c, course_list) for c in course.get_neighbours()])

    return False


class Graph:
    """
    Graph that contains the Data of all Vertices.

    Instance Attributes:
        - _vertices: A dict containing the vertices

    """
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty Graph, with no vertices"""
        self._vertices = {}

    def add_vertex(self, v: _Vertex) -> None:
        """Add a Vertex to the Graph"""
        self._vertices[v.course_code] = v

    def get_vertex(self, course_code: str) -> Optional[_Vertex]:
        """ Just return the Vertex with the same course code"""
        if course_code in self._vertices:
            return self._vertices[course_code]

        return None

    def get_all_courses(self) -> list[CourseVertex]:
        """Return a list of all vertices of the Graph that are of type CourseVertex"""
        courses = []

        for c in self._vertices:
            if isinstance(self._vertices[c], CourseVertex):
                courses.append(self._vertices[c])

        return courses

    def get_course(self, course: Any) -> Optional[_Vertex]:
        """
        If the course is a str, return the CourseVertex with the same course_code
        If the course is a CourseAnd or CourseOr, then if the corresponding CourseAndVertex/CourseOrVertex
        exists return them, else create a new Vertex object and return it
        """

        if isinstance(course, str):
            if course in self:
                return self.get_vertex(course)

            elif changeType(course) in self:
                return self.get_vertex(changeType(course))

            else:
                if PRINT:
                    print(course, "is not an available course")
                return None
                # raise ValueError

        elif isinstance(course, CourseAnd):

            if course in self:
                return self.get_vertex(str(course))

            v = CourseAndVertex(str(course))
            for course in course.courses:
                c = self.get_course(course)
                if c is not None:
                    v.add_neighbours(c)
            self.add_vertex(v)
            return v

        elif isinstance(course, CourseOr):

            if course in self:
                return self.get_vertex(str(course))

            v = CourseOrVertex(str(course))
            for course in course.courses:
                c = self.get_course(course)
                if c is not None:
                    v.add_neighbours(c)
            self.add_vertex(v)
            return v

        else:
            print("Unidetified item:", str(course))

    def __contains__(self, val: _Vertex) -> bool:
        """Checks whether graph contains given _Vertex"""
        return val in self._vertices

    def to_networkx(self, max_v: int = 5000) -> nx.Graph:
        """Convert Graph into a networkx Graph and return it"""

        graph_nx = nx.Graph()
        for v in self._vertices.values():
            if isinstance(v, CourseVertex):
                graph_nx.add_node(v.course_code, kind='Course')
            elif isinstance(v, CourseOrVertex):
                graph_nx.add_node(v.course_code, kind='CourseOr')
            elif isinstance(v, CourseAndVertex):
                graph_nx.add_node(v.course_code, kind='CourseAnd')

            if isinstance(v, CourseVertex):
                for u in v.prereq_neighbours.values():
                    if graph_nx.number_of_nodes() < max_v:
                        if isinstance(u, CourseVertex):
                            graph_nx.add_node(u.course_code, kind='Course')
                        elif isinstance(u, CourseOrVertex):
                            graph_nx.add_node(u.course_code, kind='CourseOr')
                        elif isinstance(u, CourseAndVertex):
                            graph_nx.add_node(u.course_code, kind='CourseAnd')

                    if u.course_code in graph_nx.nodes:
                        graph_nx.add_edge(v.course_code, u.course_code, kind='prereq')

                for u in v.coreq_neighbours.values():
                    if graph_nx.number_of_nodes() < max_v:
                        if isinstance(u, CourseVertex):
                            graph_nx.add_node(u.course_code, kind='Course')
                        elif isinstance(u, CourseOrVertex):
                            graph_nx.add_node(u.course_code, kind='CourseOr')
                        elif isinstance(u, CourseAndVertex):
                            graph_nx.add_node(u.course_code, kind='CourseAnd')

                    if u.course_code in graph_nx.nodes:
                        graph_nx.add_edge(v.course_code, u.course_code, kind='coreq')

                for u in v.exclusions_neighbours.values():
                    if graph_nx.number_of_nodes() < max_v:
                        if isinstance(u, CourseVertex):
                            graph_nx.add_node(u.course_code, kind='Course')
                        elif isinstance(u, CourseOrVertex):
                            graph_nx.add_node(u.course_code, kind='CourseOr')
                        elif isinstance(u, CourseAndVertex):
                            graph_nx.add_node(u.course_code, kind='CourseAnd')

                    if u.course_code in graph_nx.nodes:
                        graph_nx.add_edge(v.course_code, u.course_code, kind='exclusion')

                if graph_nx.number_of_nodes() >= max_v:
                    break

            else:
                for u in v.neighbours.values():
                    if graph_nx.number_of_nodes() < max_v:
                        if isinstance(u, CourseVertex):
                            graph_nx.add_node(u.course_code, kind='Course')
                        elif isinstance(u, CourseOrVertex):
                            graph_nx.add_node(u.course_code, kind='CourseOr')
                        elif isinstance(u, CourseAndVertex):
                            graph_nx.add_node(u.course_code, kind='CourseAnd')

                    if u.course_code in graph_nx.nodes:
                        graph_nx.add_edge(v.course_code, u.course_code, kind='CourseOptions')

                if graph_nx.number_of_nodes() >= max_v:
                    break

        return graph_nx


class _Vertex:
    """
    A Parent class vertex, with basic functionality

    Instance Attributes:
        - neighbours: Dictionary containing all the neighbouring vertices
        - course_code: Contains the course code of a CourseVertex or a representation of CourseOrVertex or CourseAndVertex

    Representation Invariants:
        - self.course_code != ''
    """
    neighbours: dict[Any, _Vertex]
    course_code: str

    def __init__(self, course_code: str) -> None:
        """Initialize a basic Vertex with a course_code"""
        self.neighbours = {}
        self.course_code = course_code

    def add_neighbours(self, vertex: _Vertex) -> None:
        """Adds a Neighbour to the _Vertex"""
        assert isinstance(vertex, _Vertex)
        self.neighbours[vertex.course_code] = vertex

    def get_neighbours(self) -> list[_Vertex]:
        """Returns a list of _Vertex that are adjacent to self"""
        return list(self.neighbours.values())

    def course_is_connected(self, course: CourseVertex) -> bool:
        """Returns whether the course is connected to self"""

        for neighbour in self.get_neighbours():
            if isinstance(neighbour, CourseVertex):
                if neighbour == course:
                    return True
            elif isinstance(neighbour, _Vertex):
                if neighbour.course_is_connected(course):
                    return True

        return False

    def __str__(self) -> str:
        """String representation of the course"""
        return self.course_code

    def __repr__(self) -> str:
        """String representation of the course"""
        return self.course_code


class CourseOrVertex(_Vertex):
    """
    Sub-Class of _Vertex that represents an Option between multiple courses
    Neighbours of this Vertex are the Various options

    Instance Attributes:
        - neighbours: dict of all _Vertex that are adjacent to self
        - course_code: String representation of the Vertex as defined by CourseOr

    Representation Invariants:
        - self.course_code != ''
    """
    neighbours: dict[Any, _Vertex]
    course_code: str


class CourseAndVertex(_Vertex):
    """
    Sub-Class of _Vertex that represents a requirement to complete multiple courses at the same time
    Neighbours of this Vertex are the Various Requirements of the vertex

    Instance Attributes:
        - neighbours: dict of all _Vertex that are adjacent to self
        - course_code: String representation of the Vertex as defined by CourseAnd

    Representation Invariants:
        - self.course_code != ''
    """
    neighbours: dict[Any, _Vertex]
    course_code: str


class CourseVertex(_Vertex):
    """
    Sub-Class of _Vertex that represents a Course

    Instance Attributes:
        - coreq_neighbours: dict containing the Co-Requisites of self
        - prereq_neighbours: dict containing the Pre-Requisites of self
        - exclusion_neighbours: dict containing the Exclusions of self
        - course_code: Course code of the Course
        - course_name: Name of the Course
        - description: Description of the Course
        - breadth_req: Breadth Category of the Course
        - interest_scores: Dict containing the scores for each interest
        - rating: Rating of the Course

    Representation Invariants:
        - self.course_code != ''
        - self.course_name != ''
        - self.rating > 0
    """
    coreq_neighbours: dict[Any, _Vertex]
    prereq_neighbours: dict[Any, _Vertex]
    exclusions_neighbours: dict[Any, _Vertex]
    course_code: str
    course_name: str
    description: str
    breadthreq: str
    interest_scores: dict[str, float]
    rating: Optional[float]

    def __init__(self, course_code, name, desc, breadthreq, rating) -> None:
        """Initialize a course vertex"""
        self.course_code = course_code.strip()
        self.name = name.strip()
        self.description = desc.strip()
        self.breadthreq = breadthreq.strip()
        self.prereq_neighbours = {}
        self.coreq_neighbours = {}
        self.exclusions_neighbours = {}
        self.interest_scores = {}
        self.rating = rating
        self.generate_course_interest_scores()

    def verify_course_list(self, course_list: list[list[CourseVertex]], year: int) -> bool:
        """
        Verify whether the course_list contains the required pre-requisites
        Verify whether the course_list contains the required co-requisites
        Verify whether the course_list does not contain any exclusion
        """
        for prereqCourse in list(self.prereq_neighbours.values()):

            if not course_in_list(prereqCourse, course_list[:year + 1]):
                # print(self.course_code, prereqCourse, "p")
                return False

        for coreqCourse in list(self.coreq_neighbours.values()):

            if not course_in_list(coreqCourse, course_list[:year + 1]):
                # print(self.course_code, coreqCourse, "c")
                return False

        for exclusion in list(self.exclusions_neighbours.values()):

            if course_in_list(exclusion, course_list[:year + 1]):
                # print(self.course_code, exclusion, "e")
                return False

        return True

    def course_is_prereq(self, course: CourseVertex) -> bool:
        """
        Returns if given course is a prerequisite of self
        # self <--- Pre Requisite --- Course
        """

        for neighbour in self.prereq_neighbours.values():

            if isinstance(neighbour, CourseVertex):
                if course == neighbour:
                    return True
                continue

            elif isinstance(neighbour, _Vertex):

                if neighbour.course_is_connected(course):
                    return True

        return False

    def add_prereq(self, course_list: Any, graph: Graph) -> None:
        """
        Add prerequisite neighbours recursively

        >>> g = Graph()
        >>> v1 = CourseVertex('CSC110', 'Intro to CS', "It's an intro to CS!", "Math and Physical Sciences")
        >>> v3 = CourseVertex('MAT137', 'Intro to Calc', "Brain Pain", "Math and Physical Sciences")
        >>> v2 = CourseVertex('CSC111', 'Continuation to CSC110', "Intro to CS II", "Math and Physical Sciences")
        >>> v4 = CourseVertex('MAT157', 'Enhanced Intro to Calc', "It's an intro to Calc!", "Math and Physical Sciences")
        >>> g.add_vertex(v1)
        >>> g.add_vertex(v2)
        >>> g.add_vertex(v3)
        >>> g.add_vertex(v4)
        >>> v1.add_prereq(CourseAnd(['CSC110', CourseOr(['MAT137', 'MAT157'])]), g)
        >>> print(v1.prereq_neighbours)
        {'CSC110': CSC110, '( MAT137/ MAT157 )': ( MAT137/ MAT157 )}
        """

        if course_list is None:
            return

        elif isinstance(course_list, str):
            course_list = course_list.strip()
            if course_list in graph:
                c = graph.get_vertex(course_list)
                if c is not None:
                    self.prereq_neighbours = {course_list: c}

            elif changeType(course_list) in graph:
                c = graph.get_vertex(changeType(course_list))
                if c is not None:
                    self.prereq_neighbours = {course_list: c}

            elif course_list.strip() == "None":
                return

            else:
                if PRINT:
                    print(course_list, "is not an available course")
                return
                # raise ValueError

        elif isinstance(course_list, CourseAnd):
            for course in course_list.courses:
                c = graph.get_course(course)
                if c is not None:
                    self.prereq_neighbours[str(course)] = c

        elif isinstance(course_list, CourseOr):
            c = graph.get_course(course_list)
            if c is not None:
                self.prereq_neighbours = {str(course_list): graph.get_course(course_list)}

    def add_coreq(self, course_list: Any, graph: Graph) -> None:
        """
        Add corequisite neighbours recursively
        """

        if course_list is None:
            return

        elif isinstance(course_list, str):
            course_list = course_list.strip()
            if course_list in graph:
                c = graph.get_vertex(course_list)
                if c is not None:
                    self.coreq_neighbours = {course_list: c}

            elif changeType(course_list) in graph:
                c = graph.get_vertex(changeType(course_list))
                if c is not None:
                    self.coreq_neighbours = {course_list: c}

            elif course_list.strip() == "None":
                return

            else:
                if PRINT:
                    print(course_list, "is not an available course")
                return
                # raise ValueError

        elif isinstance(course_list, CourseAnd):
            for course in course_list.courses:
                c = graph.get_course(course)
                if c is not None:
                    self.coreq_neighbours[str(course)] = c

        elif isinstance(course_list, CourseOr):
            c = graph.get_course(course_list)
            if c is not None:
                self.coreq_neighbours = {str(course_list): graph.get_course(course_list)}

    def add_exclusions(self, course_list: Any, graph: Graph) -> None:
        """
        Add exclusion neighbours recursively
        """

        if course_list is None:
            return

        elif isinstance(course_list, str):
            course_list = course_list.strip()
            if course_list in graph:
                c = graph.get_vertex(course_list)
                if c is not None:
                    self.exclusions_neighbours = {course_list: c}

            elif changeType(course_list) in graph:
                c = graph.get_vertex(changeType(course_list))
                if c is not None:
                    self.exclusions_neighbours = {course_list: c}

            elif course_list.strip() == "None":
                return

            else:
                if PRINT:
                    print(course_list, "is not an available course")
                return
                # raise ValueError

        elif isinstance(course_list, CourseAnd):
            for course in course_list.courses:
                c = graph.get_course(course)
                if c is not None:
                    self.exclusions_neighbours[str(course)] = c

        elif isinstance(course_list, CourseOr):
            c = graph.get_course(course_list)
            if c is not None:
                self.exclusions_neighbours = {str(course_list): graph.get_course(course_list)}

    def add_course_rating(self, rating: int, filename: str = 'ratings.bin') -> None:
        """Add a Course Rating and Accordingly change the new Course Rating and Update the same"""
        with open(filename, 'rb') as f:
            ratingDict = pickle.load(f)
            ratingCount = ratingDict[self.course_code][1]
            if ratingCount > 0:
                newRating = (rating + (self.rating * ratingCount)) / (ratingCount + 1)
                ratingCount += 1
            else:
                ratingCount = 1
                newRating = rating

            ratingDict[self.course_code] = (newRating, ratingCount)
            self.rating = newRating

        with open(filename, 'wb') as f:
            pickle.dump(ratingDict, f)

    def generate_course_interest_scores(self) -> None:
        """Generates the score of each interest based on each course's description"""

        description_lower = self.description.lower()

        for interest in INTERESTS:

            self.interest_scores[interest] = 0

            path = "keywords/" + interest + '.txt'

            with open(path, "r") as interests_file:

                reader_interests = csv.reader(interests_file)

                for row_interest in reader_interests:
                    new_description = description_lower.replace(row_interest[0].strip(), "")
                    self.interest_scores[interest] += (len(description_lower) - len(new_description)) / len(interest)


def generate_graph_from_file(filename: str = 'courses.csv', ratingsFile='ratings.bin') -> Graph:
    """
    Generates a graph from the given csv file and ratings binary File

    CSV File Format (delimiter='|'):
        <Course Code>|<Course Name>|<Course Description>|<Breadth Requirement>|<Prerequisites>|<Corequisites>|<Exclusions>

    Ratings File Contains a serialized dict
        dict format: {<Course Code>: (<Course Rating>, <No. of Reviews>)}
    """
    import csv
    g = Graph()
    with open(ratingsFile, 'rb') as f:

        ratingsDict = pickle.load(f)

    with open(filename, "r", newline="", encoding='utf-8') as f:
        reader = csv.reader(f, delimiter="|")

        courses = {}
        for row in reader:

            if PRINT:
                print("COURSE CODE:", row[0])

            c = [parse_courses(row[4]), parse_courses(row[5]), parse_courses(row[6])]

            v = CourseVertex(row[0], row[1], row[2], row[3], ratingsDict[row[0]][0])
            g.add_vertex(v)
            courses[v] = c

        for v in courses:
            if False:
                print(v.course_code)
            v.add_prereq(courses[v][0], g)
            v.add_coreq(courses[v][1], g)
            v.add_exclusions(courses[v][2], g)

    return g


if __name__ == "__main__":
    # import doctest
    # doctest.testmod(verbose=True)

    # PRINT = True

    my_graph = generate_graph_from_file('courses.csv')
    from viewer import visualize_graph

    visualize_graph(my_graph, 'spring_layout')
