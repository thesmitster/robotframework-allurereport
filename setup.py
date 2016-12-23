from setuptools import setup

setup(
    name = 'robotframework_allure',
    packages = ['AllureLibrary'],
    version = '1.0.1',
    description = 'Allure for Robot Framework',
    author = 'Eltjona Qato', 'Anne Kootstra', 
    author_email = 'qatoeltjona@gmail.com', 'kootstra@hotmail.com'
    url = 'https://github.com/kootstra/robotframework_allure',
    keywords = ['allure', 'robotframework', 'reporting'],
    classifiers = [],
    install_requires=[
        "lxml>=3.2.0",
        "namedlist",
        "py",
        "six>=1.9.0"
    ]
)
