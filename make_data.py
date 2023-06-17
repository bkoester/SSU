#!/usr/bin/
# write python code to create synthetic college transcript table with about 30 courses per student,
# and about 4 courses a term, with a single student course per row, and unique student ID for each student,
# and a second table that contains graduating majors and synthetic ACT scores, and first and last terms.
#
# write python code to create synthetic student demographic table with about 30 students per row,
# and about 4 courses a term, with a single student course per row, and unique student ID for each student,
# and a second table that contains graduating majors and synthetic ACT scores, and first and last terms.
#

# will this run?
# create a student class
class Student:
    def __init__(self):
        import random
        gint = ['g1', 'g2']
        eth = ['white', 'black', 'hispanic', 'asian', 'other','twoplus']
        majors = ['CS', 'BIO', 'MATH', 'PHYS', 'CHEM', 'ECON', 'ENG', 'HIST', 'POLI', 'PSYC', 'SOC', 'OTHER']
        self.student_id = random.randint(1,100)
        self.gender = random.choice(gint)
        self.act = random.randint(20, 36)
        self.race = random.choice(eth)
        self.first_term = random.randint(1, 10)
        self.last_term = random.randint(4, 14) + self.first_term
        self.major = random.choice(majors)
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)


class Course:
    def __init__(self,student_id,act,term,omit_previous_courses=[]):
        import random
        import numpy as np

        # generate a list of 20 courses to draw from: 10 lower division, 10 upper division,from 5 departments
        # 5 math, 5 science, 5 social science, 5 humanities, 5 other
        courses = ['MATH 100','MATH 200','MATH 300','MATH 400','MATH 500',
                   'CHEM 100', 'CHEM 200', 'CHEM 300', 'CHEM 400', 'CHEM 500',
                    'PHYS 100','PHYS 200', 'PHYS 300', 'PHYS 400', 'PHYS 500',
                    'SOC 100', 'SOC 200', 'SOC 300', 'SOC 400', 'SOC 500',
                    'HIST 100', 'HIST 200', 'HIST 300', 'HIST 400', 'HIST 500']

        #remove course from the courses vector if the course is in the omit_previous_courses vector
        courses = [x for x in courses if x not in omit_previous_courses]

        grades = [0,0.7,1.0,1.3,1.7,2.0,2.3,2.7,3.0,3.3,3.7,4.0]
        # map the act score to an index between 0 and 11 plus gaussian noise, then use that index to select a grade
        # from the grades list
        index = round(np.interp(act, [20, 36], [0, 11])+np.random.normal(0,2))

        if index < 0:
            index = 0
        if index > 11:
            index = 11

        self.grade = grades[index]
        self.name = random.choice(courses)
        self.grade = grades[index]
        self.credits = random.randint(3,4)
        self.student_id = student_id
        self.term = term

# create a class that uses the assigns a major for every term in the course table
class Major:
    def __init__(self,student_id,term):
        import random
        # for each student_id-term pair in the course table , create a major
        # use the majors already in the student class
        majors = ['CS', 'BIO', 'MATH', 'PHYS', 'CHEM', 'ECON', 'ENG', 'HIST', 'POLI', 'PSYC', 'SOC', 'OTHER']
        self.major = random.choice(majors)
        self.student_id = student_id
        self.term=term


#assign courses to students, then write out a dataframe of coures taken by each student

def create_student_struct(N):

    import pandas as pd
    import random
    # create a data frame of students and another dataframe of courses taken by each student
    # create a dataframe of students
    students = []
    for i in range(N):
        students.append(Student())

    # do the same thing but now save as a pandas dataframe
    df_students = pd.DataFrame([vars(s) for s in students])

    # create a dataframe of courses taken by each student
    courses = []
    for student in students:

        n_term = student.last_term-student.first_term+1

        # randomly select a number of courses to take each term between 1-4 and let n_crse be the
        # total number of courses each term. create a vector that contains the term number for of n_crse and append
        # the vector for each term
        n_crse = 0
        full_term_vec = []

        for term in range(student.first_term,student.last_term):
            n_crse = n_crse+random.randint(1,4)
            term_vec = [term for i in range(n_crse)]
            full_term_vec = full_term_vec + term_vec

        omit_previous_courses = []

        #this can't be any larger than the number of courses in the courses vector for now
        if n_crse > 25:
            n_crse = 25

        for i in range(n_crse):
            course = Course(student.student_id,student.act,full_term_vec[i],omit_previous_courses)
            student.add_course(course)
            courses.append(course)
            omit_previous_courses.append(course.name)

    # do the same thing but now save as a pandas dataframe
    df_courses = pd.DataFrame([vars(c) for c in courses])

    # now create a dataframe of majors for each student from the major class
    majors = []
    for student in students:
        for term in range(student.first_term,student.last_term):
            major = Major(student.student_id,term)
            majors.append(major)

    df_majors = pd.DataFrame([vars(m) for m in majors])

    home = '/home/ec2-user/environment/'
    df_students.to_csv(home+"students.csv")
    df_courses.to_csv(home+"courses.csv")
    df_majors.to_csv(home+"majors.csv")
    
    #return df_students,df_courses,df_majors

if __name__ == '__main__':
    create_student_struct(10)