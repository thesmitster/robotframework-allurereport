from setuptools import setup

setup(
    name = 'robotframework_allure',
    packages = ['AllureLibrary'],
    version = '0.1.0',
    description = 'Allure for Robot Framework',
    author = 'qatoe1991',
    author_email = 'qatoeltjona@gmail.com',
    url = 'https://github.com/qatoe1991/robotframework_allure',
    keywords = ['allure', 'robotframework', 'reporting'],
    classifiers = [],
    install_requires=[
        "lxml>=3.2.0",
        "namedlist",
        "py",
        "six>=1.9.0"
    ]
)
