# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import glob
from django.core.management import setup_environ
from settings import settings
setup_environ(settings)
from classhelper.models import Subject, Grades


files = glob.glob('grades_data/*.html')
for file in files:
    filereader = open(file, 'r')
    html = filereader.read()
    soup = BeautifulSoup(html, 'html5')
    tables = soup.find_all('table')

    # Semester info
    table_info = tables[len(tables) -4]
    rows_info = table_info.find_all('tr')
    td_info = rows_info[1].find_all('td')
    temp = td_info[1].string.split('-')
    semester_code = '%s%s' % (temp[0].strip(), temp[1].strip()[0])
    print "processing %s" % (semester_code)


    # Grade info
    rows_grades = soup.find_all(class_="tableRow")
    # row 5 and down is subjects
    for i in range(0, len(rows_grades) -1):
        td_grades = rows_grades[i].find_all('td')
        subject_code = td_grades[0].string.split('-')
        subject_code = subject_code[0].strip()
        subject = Subject.objects.filter(subject_code=subject_code)
        if subject:
            grades = Grades.objects.filter(subject = subject[0], semester_code=semester_code)
            if not grades:
                grades = Grades()
                grades.subject = subject[0]
                grades.semester_code = semester_code
                grades.f = int(td_grades[6].string.strip())
                grades.a = int(td_grades[13].string.strip())
                grades.b = int(td_grades[14].string.strip())
                grades.c = int(td_grades[15].string.strip())
                grades.d = int(td_grades[16].string.strip())
                grades.e = int(td_grades[17].string.strip())
                grades.save()
                print "%s - %s added" % (subject[0], semester_code)
