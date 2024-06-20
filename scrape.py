""" Helper functions that scrapes the course data from the artsci website
"""
import requests
from bs4 import BeautifulSoup as BS
import csv
from courseclasses import Course


def scrape_courses() -> list:
    """Scrape the artsci website to get information on various courses"""

    course_list = []

    for i in range(170):
        URL = f"https://artsci.calendar.utoronto.ca/search-courses?page={i}"
        page = requests.get(URL)
        soup = BS(page.content, "html.parser")
        courses = soup.findAll(class_='views-row')

        print("Page:", i)

        for course in courses:
            if course.find('h3') is not None:
                title = course.find('h3').text
                # print(title[2:10], end="\n\n")
                if title[9] != '1':
                    continue

                desc = course.find(class_="views-field views-field-body")
                if desc is not None:
                    desc = " ".join(desc.text.split()).strip()
                else:
                    desc = None

                prereq = course.find(class_="views-field views-field-field-prerequisite")
                if prereq is not None:
                    prereq = " ".join(prereq.text.split())[14::].strip()
                else:
                    prereq = None

                coreq = course.find(class_="views-field views-field-field-corequisite")
                if coreq is not None:
                    coreq = " ".join(coreq.text.split())[13::].strip()
                else:
                    coreq = None

                exclusion = course.find(class_="views-field views-field-field-exclusion")
                if exclusion is not None:
                    exclusion = " ".join(exclusion.text.split())[11::].strip()
                else:
                    exclusion = None

                breadthreq = course.find(class_="views-field views-field-field-breadth-requirements")
                if breadthreq is not None:
                    breadthreq = " ".join(breadthreq.text.split())[22::].strip()
                else:
                    breadthreq = None
                # print("="*60)

                c = Course(title[2:10], title[13::],
                           desc,
                           breadthreq=breadthreq,
                           prereq=prereq,
                           coreq=coreq,
                           exclusions=exclusion)

                course_list.append(c)

    return course_list


def write_to_csv(course_list, filename="courses.csv"):
    """Writes Data from scrape_courses into a csv file using the pipe delimiter"""

    with open(filename, "w", newline="", encoding='utf-8') as f:
        writer = csv.writer(f, delimiter="|")

        for course in course_list:
            writer.writerow(course.to_list())


if __name__ == "__main__":
    pass
# DO NOT RUN FUNCTION: Will Replace all data in courses.csv
# write_to_csv(scrape_courses())
