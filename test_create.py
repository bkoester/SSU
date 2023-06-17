'''Test the make_data.py file'''
import os
import pandas as pd
import make_data as md


def test_dummy():
    '''Create a test files, make sure they look ok, then delete them'''

    write_path='.tmp/'
    md.create_student_struct(100, write_path)

    #assert that the files were made
    assert os.path.isfile(write_path+'/students.csv')
    assert os.path.isfile(write_path+'courses.csv')
    assert os.path.isfile(write_path+'majors.csv')


    #now read in each file
    std = pd.read_csv('.tmp/students.csv')
    #print(std.head())
    print(f'Test student table dimensions{std.shape}')

    assert std.shape[0] == 100

    course = pd.read_csv('.tmp/courses.csv')
    #print(course.head())
    print(f'Test course table dimensions{course.shape}')

    majors = pd.read_csv('.tmp/majors.csv')
    #print(majors.head())
    print(f'Test majors table dimensions{majors.shape}')

    #now delete the files
    os.remove('.tmp/students.csv')
    os.remove('.tmp/courses.csv')
    os.remove('.tmp/majors.csv')