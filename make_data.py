'''Create university synthetic data for testing'''
# write python code to create synthetic college
# transcript table with about 30 courses per student,
# and about 4 courses a term, with a single student
# course per row, and unique student ID for each student,
# and a second table that contains graduating majors and
# synthetic ACT scores, and first and last terms.
#
# write python code to create synthetic student
# demographic table with about 30 students per row,
# and about 4 courses a term, with a single student
# course per row, and unique student ID for each student,
# and a second table that contains graduating majors and
# synthetic ACT scores, and first and last terms.
#
# will this run?
# create a student class

import sys
import random
import pandas as pd
import requests

class Student:
    """Class representing a student"""
    def __init__(self):
        gint = ['g1', 'g2']
        eth = ['white', 'black', 'hispanic', 'asian', 'other','twoplus']
        majors = ['CS', 'BIO', 'MATH', 'PHYS', 'CHEM', 'ECON',
                  'ENG', 'HIST', 'POLI', 'PSYC', 'SOC', 'OTHER']
        self.student_id = random.randint(1,100)
        self.gender = random.choice(gint)
        self.act = random.randint(20, 36)
        self.race = random.choice(eth)
        self.first_term = random.randint(1, 10)
        self.last_term = random.randint(4, 14) + self.first_term
        self.major = random.choice(majors)
        self.hsgpa = random.randint(20, 40)/10.
        self.courses = []

    def add_course(self, course):
        '''Function to add a course to the student's course list'''
        self.courses.append(course)


def course_list():
    '''Function to create a list of courses to draw from'''

    courses = ['MATH 100','MATH 200','MATH 300','MATH 400','MATH 500',
                   'CHEM 100', 'CHEM 200', 'CHEM 300', 'CHEM 400', 'CHEM 500',
                    'PHYS 100','PHYS 200', 'PHYS 300', 'PHYS 400', 'PHYS 500',
                    'SOC 100', 'SOC 200', 'SOC 300', 'SOC 400', 'SOC 500',
                    'HIST 100', 'HIST 200', 'HIST 300', 'HIST 400', 'HIST 500']
    return courses

class Course:
    """Class representing a course"""
    def __init__(self,student_id,hsgpa,term,course_models,omit_previous_courses=None):
        # generate a list of 20 courses to draw from:
        # 10 lower division, 10 upper division,from 5 departments
        # 5 math, 5 science, 5 social science, 5 humanities, 5 other

        # remove course from the courses vector if the course
        # is in the omit_previous_courses vector
        course_names = [x for x in course_models['course']
                        if x not in omit_previous_courses]

        course_title = course_names[random.randint(0,len(course_names)-1)]
        index = course_models.index[course_models['course'] ==
                                    course_title].tolist()[0]
        grade_interp = (course_models['coeff1'][index] +
                       course_models['coeff2'][index]*hsgpa +
                       course_models['coeff3'][index]*hsgpa**2)
        self.letter = letter_grade(grade_interp)
        self.grade = grade_interp
        self.name = course_title
        self.credits = random.randint(3,4)
        self.student_id = student_id
        self.term = term

# for Course object, create a columns that converts the grade
# to a letter grade
def letter_grade(grade):
    '''Function to convert a grade to a letter grade'''
    if grade >= 3.5:
        letter = 'A'
    elif grade >= 3.0:
        letter = 'B'
    elif grade >= 2.5:
        letter = 'C'
    elif grade >= 2.0:
        letter = 'D'
    elif grade >= 1.0:
        letter = 'W'
    else:
        letter = 'E'
    return letter

# create a function that maps terms to years for Fall and Winter for
# terms 1-16 up to 2020
def term_to_year(term):
    '''Function to map terms to years'''
    if term <= 3:
        year = 2016
    elif term <= 6:
        year = 2017
    elif term <= 9:
        year = 2018
    elif term <= 12:
        year = 2019
    else:
        year = 2019

    seas = 'FA'

    if term % 2 == 0:
        seas = 'WN'
    elif term % 3 == 0:
        seas = 'SP'

    term_short_des = seas + ' ' + str(year)

    return term_short_des

# create a lookup table for courses that includes with a
# course name, a functional form for predicted grade vs. input GPA
# (linear, quadratic), and random coefficients
# for the functional form.
# this should only be run once and saved so that all
# students in a a course have the same grade function.
def course_grade_function():
    '''Function to create a lookup table for courses'''

    courses = course_list()

    #create a dataframe of courses and their grade functions
    # that will be filled in the loop
    df_cmodel = pd.DataFrame(columns=
                             ['course','form','coeff1','coeff2','coeff3'])

    for course in courses:
        # randomly select a functional form for the grade vs. GPA curve
        # 0 is linear, 1 is quadratic
        form = random.randint(1,2)
        # randomly select coefficients for the functional form
        if form == 1:
            coeff1 = random.randint(4,14)/10.
            coeff2 = random.randint(2,9)/10.
            coeff3 = 0
        if form == 2:
            coeff1 = random.randint(4,14)/10
            coeff2 = random.randint(2,9)/10.
            coeff3 = random.randint(1,5)/10.

        # add the course and the grade function to the dataframe
        df_cmodel = df_cmodel.append({'course':course,
                                      'form':form,'coeff1':coeff1,
                                      'coeff2':coeff2,'coeff3':coeff3},
                                      ignore_index=True)
    return df_cmodel


# create a class that uses the assigns a major for
# every term in the course table
class Major:
    """Class representing a major"""
    def __init__(self,student_id,term):
        # for each student_id-term pair in the course table , create a major
        # use the majors already in the student class
        majors = ['CS', 'BIO', 'MATH', 'PHYS', 'CHEM', 'ECON',
                  'ENG', 'HIST', 'POLI', 'PSYC', 'SOC', 'OTHER']
        self.major = random.choice(majors)
        self.student_id = student_id
        self.term=term


#assign courses to students, then write out a dataframe
# of coures taken by each student

def create_student_struct(n_student,write_path):
    '''The main function that creates the student data structures'''
    # create a data frame of students and
    # another dataframe
    # of courses taken by each student
    # create a dataframe of students

    course_models = course_grade_function()

    students = []
    for i in range(n_student):
        students.append(Student())

    # do the same thing but now save as a pandas dataframe
    df_students = pd.DataFrame([vars(s) for s in students])

    # create a dataframe of courses taken by each student
    courses = []
    for student in students:
        # randomly select a number of courses to take each term
        # between 1-4 and let n_crse be the
        # total number of courses each term. create a vector that
        # contains the term number for of n_crse and append
        # the vector for each term
        n_crse = 0
        full_term_vec = []

        for term in range(student.first_term,student.last_term):
            n_crse = n_crse+random.randint(1,4)
            term_vec = [term for i in range(n_crse)]
            full_term_vec = full_term_vec + term_vec

        omit_previous_courses = []

        #this can't be any larger than the number of courses in
        # the courses vector for now
        if n_crse > 25:
            n_crse = 25

        for i in range(n_crse):
            course = Course(student.student_id,student.hsgpa,
                            full_term_vec[i],course_models,
                            omit_previous_courses)
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

    #now use the term_to_year function to create a term_short_des column
    df_students['first_term_short_des'] = df_students['first_term'].apply(term_to_year)
    df_students['last_term_short_des'] = df_students['last_term'].apply(term_to_year)
    df_courses['term_short_des'] = df_courses['term'].apply(term_to_year)
    df_majors['term_short_des'] = df_majors['term'].apply(term_to_year)

    # write out the dataframes to csv files in the home directory
    #home = '~/' #/home/ec2-user/environment/'

    #drop the courses column from df_students
    df_students = df_students.drop('courses',axis=1)

    #now rename the columns to match the database
    df_students,df_courses,df_majors = rename_columns(df_students,df_courses,df_majors)


    #write out the dataframes to csv files but don't write out the index
    df_students.to_csv(write_path+"students.csv",index=False)
    df_courses.to_csv(write_path+"courses.csv",index=False)
    df_majors.to_csv(write_path+"majors.csv",index=False)
    #return df_students,df_courses,df_majors


# a function to rename the columns in the dataframe to match the database
# column names
def rename_columns(df_students,df_courses,df_majors):
    '''Function to rename the columns in the dataframes to match the database'''
    #create a dictionary of old and new column names
    student_dict = {'student_id':'STDNT_ID',
                    'gender':'STDNT_SEX_SHORT_DES',
                    'act':'MAX_ACT_MATH_SCR',
                    'race':'STDNT_ETHNC_GRP_SHORT_DES',
                    'first_term': 'FIRST_TERM_ATTND_CD',
                    'last_term': 'LAST_TERM_ATTND_CD',
                    'first_term_short_des':'FIRST_TERM_ATTND_SHORT_DES',
                    'last_term_short_des':'LAST_TERM_ATTND_SHORT_DES',
                    'major':'UM_DGR_1_MAJOR_1_DES',
                    'hsgpa':'HS_GPA'}

    courses_dict = {'grade':'GRD_PTS_PER_UNIT_NBR',
                    'letter':'CRSE_GRD_OFFCL_CD',
                    'name':'CRSE_ID_CD',
                    'credits':'UNITS_ERND_NBR',
                    'student_id':'STDNT_ID',
                    'term':'TERM_CD',
                    'term_short_des':'TERM_SHORT_DES'}

    majors_dict = {'major':'UM_DGR_1_MAJOR_1_DES',
                   'student_id':'STDNT_ID',
                   'term':'TERM_CD',
                   'term_short_des':'TERM_SHORT_DES'}


    #rename the columns
    df_students.rename(columns=student_dict,inplace=True)
    df_courses.rename(columns=courses_dict,inplace=True)
    df_majors.rename(columns=majors_dict,inplace=True)

    return df_students,df_courses,df_majors

# create a function to read the median income by zipcode from the american
# community survey data website.
def fetch_median_incomes():
    '''Function to fetch the median incomes by zipcode 
    from the american community survey data website'''
    base_url = "https://api.census.gov/data/2019/acs/acs5/profile"
    variables = "DP03_0062E"  # Median Income: DP03_0062E

    # fetch all the median incomes for all zipcodes in the US
    incomes = requests.get(f"{base_url}?get={variables}&\
                           for=zip%20code%20tabulation%20area:*",\
                           timeout=20)

    # add some error handling at some point
    #convert the json object to a pandas dataframe
    df_incomes = pd.DataFrame(incomes.json()[1:],columns=incomes.json()[0])

    return df_incomes



# this is needed to run the script from the command line
if __name__ == '__main__':
    create_student_struct(int(sys.argv[1]),sys.argv[2])
