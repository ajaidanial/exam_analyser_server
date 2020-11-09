"""
Contains initial fixture data. Used to load the database with initial data using the
management commands. The other necessary data can also be added later.
"""

EXAMS = [
    {"name": "Quarterly Exam"},
    {"name": "Half Yearly Exam"},
    {"name": "Annual Exam"},
]

SUBJECTS = [
    {"name": "Biology"},
    {"name": "Physics"},
    {"name": "Chemistry"},
    {"name": "Mathematics"},
    {"name": "Commerce"},
    {"name": "Economics"},
    {"name": "Accountants"},
    {"name": "Computer Science"},
]

QUESTION_CATEGORIES = [
    {"name": "Programming", "subject": "Computer Science"},
    {"name": "Logical Thinking", "subject": "Accountants"},
    {"name": "Problem Solving", "subject": "Accountants"},
    {"name": "Logical Reasoning", "subject": "Economics"},
    {"name": "Moral Values", "subject": "Economics"},
    {"name": "Tinkering", "subject": "Chemistry"},
    {"name": "Experimenting", "subject": "Chemistry"},
    {"name": "Plant Anatomy", "subject": "Biology"},
    {"name": "Zoology", "subject": "Biology"},
    {"name": "Animal Anatomy", "subject": "Biology"},
]

# main initial data creation config | used to create the data dynamically
# used in the custom management command to create the instances
INITIAL_DATA_CREATION_CONFIGURATION = [
    {"model": "examination.Exam", "data": EXAMS},
    {"model": "examination.Subject", "data": SUBJECTS},
    {"model": "examination.QuestionCategory", "data": QUESTION_CATEGORIES},
]
