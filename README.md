# JiraCopyEpics
Copy one projects Epics (summary+description) to another project. For Jira Data Center usage
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
Browse source project and find Epic-Test case linkage pairs. Remove possible copies of of matched test case (fixing Zephyr Squad importer errors)

Note:source and target projects hardcoded   
EXAMPLE: FindCreateEpicTestLinks.py -u MYUSERNAME -w MYPASSWORD -s https://MYOWNJIRA.fi/ 