# autosmart_v2

Automation solution for placement project to improve test coverage. The brief for this project was to create a program
that is able to run stream tests by following test steps within a specific test but without replication of code. 
It outputs a pass or fail per step allowing the program to determine whether the overall test has passed or not.

The main task for this project was to automate the 4 key procedures that are used in any
AdSmart test:
• Play out the specific stream needed for the test. This was done using a service
• Remote control commands
• Extract the reports from the box. This was also done using a service
• Verification from the reports that the box has recorded the correct information in
its html report

Once the procedures had been automated, I then adapted the script to allow for more
than one box to run at a time. Allowing the 4 STB platforms to run in parallel. Which is a
local set up for a tester; AutoSmart was then able to run in addition to the
manual Testers and was integrated in to the current automation framework.



Front end
Where you select the test’s you want to run and the boxes (HUB/RACK)

Test Script
Each test has an individual test script with a unique order of test procedures. 
These procedures are called from a template script that has all of test procedures that is needed for any AdSmart test. 
These templates are input dependent from the arguments in the test script.

Servers
The majority of the procedures are services which allows them to be accessed remotely meaning they can be accessed not only from your local computer set up.
Stream player – used to control the stream playout and status.
VNC remote 
STB Extractor – being able to extract from a box using its unique IP

STBS
The services talk with the STBs to complete each test step. 
The PASS/FAIL steps are mostly from verification stages. Once the extractor server extracts the AdSmart report, the test script calls the verification process to see if the information on the report matches what is expected. And a pass or fail is submitted. This is then shown on the front end.

