# Go through source project Zephyr Squad test cases and find Epic(s) linked to them
# Then find this test->epic pairs from target project using summaries as JQL query and 
# create link between them (test cases and epics have been copied to new project, missing the linkage) 
# 
# mika.nokka1@gmail.com 1.9.2021



#from __future__ import unicode_literals

import sys, logging
import argparse
#import re
from collections import defaultdict
from Authorization import Authenticate  # no need to use as external command
from Authorization import DoJIRAStuff

import glob
import re
import os
import time
import unidecode
from jira import JIRA, JIRAError
from collections import defaultdict
from time import sleep
import keyboard
import math


__version__ = u"0.1"



logging.basicConfig(level=logging.DEBUG) # IF calling from Groovy, this must be set logging level DEBUG in Groovy side order these to be written out



def main(argv):
    
    JIRASERVICE=u""
    JIRAPROJECT=u""
    PSWD=u''
    USER=u''
  
    #hardcoded Jira source (of the epics) and target project (place where epics are copied) IDs
    TARGETPROJECT="GRA12"  
    SOURCEJIRAPROJECT="GRAP"
  
    logging.debug (u"--Created date field copier starting --") 
    start = time.perf_counter()
 
    parser = argparse.ArgumentParser(description=" Copy Jira JQL result issues attachments to given directory",
    
    
    epilog="""
    
    EXAMPLE:
    
    CopyEpics.py  -u MYUSERNAME -w MYPASSWORD -s https://MYOWNJIRA.fi/ """

    
    )
    
    
    parser.add_argument('-v', help='Show version&author and exit', action='version',version="Version:{0}   mika.nokka1@gmail.com ,  MIT licenced ".format(__version__) )
    
    parser.add_argument("-w",help='<JIRA password>',metavar="password")
    parser.add_argument('-u', help='<JIRA user account>',metavar="user")
    parser.add_argument('-s', help='<JIRA service>',metavar="server_address")
    parser.add_argument('-r', help='<DryRun - do nothing but emulate. On by default>',metavar="on|off",default="on")
 

    args = parser.parse_args()
       
    JIRASERVICE = args.s or ''
    PSWD= args.w or ''
    USER= args.u or ''

    if (args.r=="on"):
        SKIP=1
    else:
        SKIP=0    

    
    # quick old-school way to check needed parameters
    if (JIRASERVICE=='' or  PSWD=='' or USER==''):
        logging.error("\n---> MISSING ARGUMENTS!!\n ")
        parser.print_help()
        sys.exit(2)
        
     
    Authenticate(JIRASERVICE,PSWD,USER)
    jira=DoJIRAStuff(USER,PSWD,JIRASERVICE)
    
    #print ("FORCE EXIT..!!")
    #sys.exit(5)
   
    if (SKIP==1):
        print("DRY RUN MODE ON")
    else:
        print ("REAL OPERATION MODE. DRY RUN MODE OFF") 
   
   

    GetSourceTests(SOURCEJIRAPROJECT,jira,SKIP,TARGETPROJECT)


    end = time.perf_counter()
    totaltime=end-start
    #seconds=totaltime.total_seconds()
    print ("Operation time taken:{0} seconds".format(totaltime))

############################################################################################################################################
# Create Epic issue. Using fixed task issuetype
#
# https://zzzzz.atlassian.net/rest/api/2/field to fiend Epic name custom field ID
# in used example Jira, it was customfield_10004
# In server check Issues/Epic ID using UI
#

def CreateEpic(jira,SUMMARY,DESCRIPTION,TARGETPROJECT):

    start = time.perf_counter()
    system.exit(5)
    try:    

            newissue=jira.create_issue(fields={
            'project': {'key': TARGETPROJECT},
            'issuetype': {
                "name": "Epic"
            },
            'summary': SUMMARY,
            'description': DESCRIPTION,
            'customfield_10005': SUMMARY   # only needed for Epic issuetype, "Epic Name", check your own Jira ID
            })
    
    except JIRAError as e: 
            logging.error(" ********** JIRA ERROR DETECTED: ***********")
            #logging.error("Tried create issue:{0}".format(newissue))
            
            logging.error(" ********** Statuscode:{0}    Statustext:{1} ************".format(e.status_code,e.text))
            if (e.status_code==400):
                logging.error("400 error dedected") 
    else:
        logging.info("All OK")
        logging.info("Issue created:{0}".format(newissue))
  
        
    end = time.perf_counter()
    totaltime=end-start
    print ("Operation time taken:{0} seconds".format(totaltime))
       
            
    print ("*************************************************************************")
    
logging.debug ("--Python exiting--")

#################################################
# Get source project Zephyr Squa Test cases, hardcoded JQL
#
# Check every Test case if there exists Epic (requirements) linked to it
#

def GetSourceTests(SOURCEJIRAPROJECT,jira,SKIP,TARGETPROJECT):

    jql_query="Project = \'{0}\' and issuetype =\'Test\' ".format(SOURCEJIRAPROJECT) 
    print ("Used query:{0}".format(jql_query))
                        
    issue_list=jira.search_issues(jql_query, maxResults=4000)
    
       
                     
    nbr=len(issue_list)                    
    if nbr >= 1:
        COUNTER=1
        print ("Found:{0} Tests".format(nbr)) # iterate over all found Test issues
        for issue in issue_list:
            print ("..............................................................................................................")
            TARGETEPIC="NA"
            TARGETTEST="NA"
            SUMMARY=issue.fields.summary
            DESCRIPTION=issue.fields.description
            EPICLINK=issue.raw["fields"]["customfield_10006"]  # find ocrrect epic link id from ui
            print ("SOURCE PROJECT ISSUE:{0}-->{1}".format(COUNTER,issue))
            print("SUMMARY:{0}".format(SUMMARY))
            print("DESCRIPTION:{0}".format(DESCRIPTION))
            print("SOURCE PROJECT EPICLINK:{0}".format(EPICLINK))
            
            if (EPICLINK != None): # Test case has linked EPIC
                
                print ("********************************************************************************************************")
                linkedissue = jira.issue(EPICLINK)
                LINKEDSUMMARY=linkedissue.fields.summary
                print("LINKED SOURCE EPIC SUMMARY:{0}".format(LINKEDSUMMARY))
                print ("Linked Source Test case: {0}-->  Source Epic:{1}".format(issue,linkedissue))
                print ("{0} --> {1}".format(SUMMARY,LINKEDSUMMARY))


                #Find Epic from target project, using summary as key
                
                
                EDITEDLINKEDSUMMARY=LINKEDSUMMARY.replace('[','')
                EDITEDLINKEDSUMMARY=EDITEDLINKEDSUMMARY.replace(']','')
                EDITEDLINKEDSUMMARY=EDITEDLINKEDSUMMARY.replace('\'','\\\'')
                jql_query="Project = \'{0}\' and summary ~ \'{1}\' and issuetype = Epic ".format(TARGETPROJECT,EDITEDLINKEDSUMMARY) 
                print ("Used query:{0}".format(jql_query))                        
                issue_list=jira.search_issues(jql_query, maxResults=4000)
              
                            
                z=len(issue_list)                    
                if z >= 1:
                    print ("Found name matching TARGET project Epic:{0}".format(z))
                    for issue in issue_list: # assume only one Epic has been linked 
                        TARGETEPIC=issue
                        print ("TARGET EPIC:{0}".format(TARGETEPIC))
                else:
                    print ("ERRIR: NO TARGET PROJECT EPIC FOUND")        
                
                
                #Find Test case from target project, using summary as key
                EDITEDSUMMARY=SUMMARY.replace('[','')
                EDITEDSUMMARY=EDITEDSUMMARY.replace(']','')
                EDITEDSUMMARY=EDITEDSUMMARY.replace('\'','\\\'')
                jql_query="Project = \'{0}\' and summary ~ \'{1}\' and issuetype = Test ".format(TARGETPROJECT,EDITEDSUMMARY) 
                print ("Used query:{0}".format(jql_query))                        
                issue_list=jira.search_issues(jql_query, maxResults=4000)
              
                
                #create target project to be credted pic->test link information  
                # collect information to be deleted duplicates          
                z=len(issue_list)                    
                if z >= 1:
                    print ("Found:{0} matching TARGET project test case(s)".format(z))
                    for issue in issue_list: # assume only one Test 
                        TARGETTEST=issue
                        print ("TARGET EPIC:{0} -> LINKED TEST:{1}".format(TARGETEPIC,TARGETTEST))
                else:
                    print ("ERRIR: NO TARGET TEST FOUND")          
                print ("****************************************************************************************************************")

            COUNTER=COUNTER+1
            if (SKIP==1):
                print("DRY RUN MODE ON. Not doing anythin")
            else:
                print ("REAL OPERATION MODE. DRY RUN MODE OFF. Doing the deed")    
                #CreateEpic(jira,SUMMARY,DESCRIPTION,TARGETPROJECT)
            
            #time.sleep(0.5) # prevent jira crash when creating issues in a row
            print ("..............................................................................................................")
            
    else:
        print ("NO Epics found")


#########################################################################

if __name__ == "__main__":
    main(sys.argv[1:]) 
 