ALLURE ADAPTOR FOR ROBOT FRAMEWORK

Allure is an open-spurce framework designed to represent clear test execution reports.

How to use it:
    - Just `import AllureLibrary` in the configuration file.
    - The output directory is the same as the output directory of RobotFramework.
    - One of the features is that a test may be connected to a jira issue. The ticket number of Jira startign with DIM should be specified as a tag in the test and the rest of the URL is given through command line `pybot -v ISSUE_TRACKER:http://jira.com/`
    - Different level of severities can be set through the tags through one of the states: critical, blocker, normal, minor, trivial.

         
DEVELOPMENT INFORMATION

Output Convention:
    - Every XML file should be named like this: {UUID}-testsuite.xml, where {UUID} is a universally unique identifier.
    - Every XML file should be valid when checked with the Allure schema.
    - The output result of an Allure adapter should store not only XML files with information about tests, but also copies of all attached files.
    - Every attachment file should be named like this: {HASH-SUM}-attachment.{EXT}, where {HASH-SUM} is the cryptographic hash sum of the file contents (e.g. MD5, SHA1, Whirlpool and so on), {EXT} is the file extension corresponding to the MIME type in the XML file. We require cryptographic hash sums in order to avoid storing files with duplicate content.
    - One xml file should contain one test suite.

Main features aligned with Robot Framework:
    - Steps in Allure Framework are aligned to Keyword in Robot Framework.
    - Test Suites and Test Cases are the same at both xml formats of Robot Framework and Allure.
    - Feature and Stories are implemented as labels.
    - Issues are labels and the url of them is given as a variable from the pybot.
    - The allure xml and attached file directory is the same as the output directory of robot framework.

Further development:
    - For the time being even the reports from Robot Framework are saved and not disabled. It can be done from the command line, but a solution is also to do it from Allure Library.
    - Screenshots are saved as a copy of the screenshoots generated from Robot Framework. It needs to be improved and some suggestions that needs to be discussed are:
            - Change the filename in `Capture Screenshot` keyword, so it is aligned with Allure requirements.
            - If the output files of Robot Framework are not needed any more than the screenshots can be renamed.
    - To specify issues, than the label should be unified by using the ticket number like: `DIM-234`.

Moreover extra information can be fetched through tags and a lot of allure features are implemented through label field in xml. One of the drawbacks is that the log messages do not provide a lot of information for the attachments.
