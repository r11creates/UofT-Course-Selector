
from CourseParse import parse_courses, CourseCollection
from typing import Optional

INTERESTS = ["chemistry", "christianity", "cinema", "cognitive_science", "computer_science", "drama", "economics",
             "english", "history", "linguistics", "math", "music", "other_languages", "philosophy", "physics",
             "psychology", "religion", "statistics"]


class Course:
    """
    Stores attributes for each course

    Instance Attributes:
        - course_id: Course Code of the Course
        - name: Name of the Course
        - description: Description of the Course
        - breadthreq: Breadth Category It belongs to
        - prereq: Prerequisites of the Course
        - coreq: Corequisites of the Course
        - exclusion: Exclusions of the Course

    Representation Invariants:
        - course_id != '' and len(course_id) >= 8
        - name != ''
        - description != ''
    """

    course_id: str
    name: str
    description: str
    breadthreq: Optional[str]
    prereq: Optional[str | CourseCollection]
    coreq: Optional[str | CourseCollection]
    exclusions: Optional[str | CourseCollection]

    def __init__(self, course_id: str, name: str, desc: str, breadthreq=None, prereq=None, coreq=None,
                 exclusions=None) -> None:
        """Initialize a Course"""
        self.course_id = course_id.strip()
        self.name = name.strip()
        self.description = desc.strip()
        self.breadthreq = breadthreq
        self.prereq = prereq
        self.coreq = coreq
        self.exclusions = exclusions

    def __str__(self) -> str:
        """String Representation of the Course"""
        s = self.course_id + ": " + self.name + "\n\n" + self.description + "\n\n"

        if self.breadthreq:
            s += "Breadth Requirements: " + self.breadthreq + "\n\n"

        if self.prereq:
            s += "Prerequisites: " + self.prereq + "\n\n"

        if self.coreq:
            s += "Corequisites: " + self.coreq + "\n\n"

        if self.exclusions:
            s += "Exclusions: " + self.exclusions + "\n\n"

        return s

    def to_list(self) -> list:
        """Converst course details to a list"""
        return [self.course_id, self.name, self.description, self.breadthreq, self.prereq, self.coreq, self.exclusions]


if __name__ == "__main__":

    import csv

    i = 0

    with open("courses.csv", "r", newline="", encoding='utf-8') as f:
        reader = csv.reader(f, delimiter="|")

        with open("check.txt", "w", encoding="utf-8") as tf:
            for row in reader:
                if row[4] != "":
                    print("COURSE CODE:", row[0])
                    # print(row[4])
                    # parse_courses(row[4])
                    # print("\n")

                    tf.write("COURSE CODE: " + row[0] + "\n")
                    tf.write(row[4] + "\n")
                    c = str(parse_courses(row[4]))
                    if "None" in c:
                        c = str(parse_courses(c))
                    tf.write(c + "\n\n")
