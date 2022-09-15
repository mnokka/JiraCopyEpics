# Jira Zephyr Squad tests from one project to another 
  
Zephyr Squad own test export does zillions of duplicates for each testcases, it also does not copy issue descriptions. 
Commercial Better Excel export plugin does better job, but must be limited 1000 issues max at the rxporttime (otherwise it crashes Jira due memory binge usage).  1000 tests can be JQL queried by using test case creation time (including minutes) as fetch criteria. 
  
If source project uses Epic as definition for test area (test cases are linked to some defining Epic), Epics must be copied to target project. (Script Runner project copy nor clone cant not handle test case steps)

Finally source project Epics-test case links must be recreated in target project (and remove possible test case duplicates) 
<br />
<br />
<br />   
### Copy one projects Epics (summary+description) to another project. For Jira Data Center usage
<br />
<br />
<br />

Install Python libraries:  
pip install -r requirements.txt    
<br />
<br />

    
usage: CopyEpics.py [-h] [-v] [-w password] [-u user] [-s server_address] [-r on|off]  
<br />
<br />


options:  
  -h, --help         show this help message and exit  
  -v                 Show version&author and exit  
  -w password        <JIRA password>  
  -u user            <JIRA user account>  
  -s server_address  <JIRA service>  
  -r on|off          <DryRun - do nothing but emulate. On by default>
  
  
Note: source and target projects hardcoded  

EXAMPLE: CopyEpics.py -u MYUSERNAME -w MYPASSWORD -s https://MYOWNJIRA.fi/  
<br />
<br />
<br />
<br />
###Browse source project and find Epic-Test case linkage pairs. Remove possible copies of of matched test case (fixing Zephyr Squad importer errors). Recreating links to target project

Note:source and target projects hardcoded   

EXAMPLE: FindCreateEpicTestLinks.py -u MYUSERNAME -w MYPASSWORD -s https://MYOWNJIRA.fi/   

<br />
<br />
<br />
<br />

### Copy source project components to target project  
  
Note:source and target projects hardcoded 
  
EXAMPLE: CopyComponents.py -u MYUSERNAME -w MYPASSWORD -s https://MYOWNJIRA.fi/   