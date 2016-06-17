from disutils.core import setup
setup(
    name = 'robotframework_allure',
    packages = ['robotframework_allure'],
    version = '0.1',
    description = 'Allure for Robot Framework',
    author = 'Eltjona Qato',
    author_email = 'qatoeltjona@gmail.com',
    url = 'https://github.com/qatoe1991/robotframework_allure',
    download_url = '',
    keywords = ['allure', 'robotframework', 'reporting'],
    classifiers = [],
    install_requires=[
        'lxml>=3.6.0',
        'py>=1.4',
        'namedlist>=1.7',
    ]
)
