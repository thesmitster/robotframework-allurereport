from setuptools import setup

setup(
    name = 'robotframework_allure',
    packages = ['robotframework_allure'],
    version = '0.1.2',
    description = 'Allure for Robot Framework',
    author = 'Eltjona Qato',
    author_email = 'qatoeltjona@gmail.com',
    url = 'https://github.com/qatoe1991/robotframework_allure',
    download_url = '',
    keywords = ['allure', 'robotframework', 'reporting'],
    classifiers = [],
    install_requires=[
        'lxml',
        'py',
        'namedlist',
    ]
)
