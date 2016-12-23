#Allure Adaptor for Robot Framework

##Introduction

The Allure Adaptor for Robot Framework is a Library that can be included in the Robot scripts to generate [Allure] (http://allure.qatools.ru/) compatible XML files which can then be used to generate the Allure HTML reports. These reports are functionally comparable to the standard Robot Framework Report and Log, but integrated and more dynamic.

## Features

* Steps in Allure Framework are aligned to Keyword in Robot Framework.
* Test Suites and Test Cases are the same at both xml formats of Robot Framework and Allure.
* Feature and Stories are implemented as labels.
* Issues are labels and the url of them is given as a variable from the pybot.
* The allure xml and attached file directory is the same as the output directory of robot framework.

##Installation

Clone the project repository from GitHub_. After that you can install the framework with::

    python setup.py install

##Example

Below is a simple example test case for testing login to some system. In this example the AllureLibrary is added via::

    Library           AllureLibrary

You can find more examples with links to related demo projects from
http://robotframework.org.

    *** Settings ***
    Documentation     A test suite with a single test for valid login.
    ...
    ...               This test has a workflow that is created using keywords in
    ...               the imported resource file.
    Resource          resource.robot
    Library           AllureLibrary

    *** Test Cases ***
    Valid Login
        Open Browser To Login Page
        Input Username    demo
        Input Password    mode
        Submit Credentials
        Welcome Page Should Be Open
        [Teardown]    Close Browser

## Notes
Output Convention:

* Generated XML files are named like: {UUID}-testsuite.xml, where {UUID} is a universally unique identifier.
* Generated XML complies with the Allure schema.
* The output result of an Allure adapter are not only XML files with information about tests, but also copies of all attached files.
* Every attachment files are named like: {HASH-SUM}-attachment.{EXT}, where {HASH-SUM} is the cryptographic hash sum of the file contents (e.g. MD5, SHA1, Whirlpool and so on), {EXT} is the file extension corresponding to the MIME type in the XML file. Cryptographic hash sums are required to avoid storing files with duplicate content.
* One xml file contains one test suite.

## Further development

* For the time being even the reports from Robot Framework are saved and not disabled. It can be done from the command line, but a solution is also to do it from Allure Library.
* Screenshots are saved as a copy of the screenshoots generated from Robot Framework. It needs to be improved and some suggestions that needs to be discussed are:
* Change the filename in `Capture Screenshot` keyword, so it is aligned with Allure requirements.
* If the output files of Robot Framework are not needed any more than the screenshots can be renamed.
* To specify issues, than the label should be unified by using the ticket number like: `DIM-234`.
* Extra information can be fetched through tags and a lot of allure features are implemented through label field in xml. One of the drawbacks is that the log messages do not provide a lot of information for the attachments.
