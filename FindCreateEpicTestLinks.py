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

    jql_query="Project = \'{0}\' and issuetype =\'Test\' ".format(SOURCEJIRAPROJECT) # by default only 1000 results given
    
    # some splitting queries by create date
    #1
    #jql_query="Project = \'{0}\' and issuetype =\'Test\' and createdDate > \"2019-01-01\" and createdDate <\"2020-5-21 15:08\"".format(SOURCEJIRAPROJECT)
    #2
    #jql_query="Project = \'{0}\' and issuetype =\'Test\' and createdDate > \"2020-5-21 15:08\" and createdDate <\"2020-5-21 20:09\"".format(SOURCEJIRAPROJECT)
    #3
    #jql_query="Project = \'{0}\' and issuetype =\'Test\' and createdDate > \"2020-5-21 20:09\" and createdDate <\"2020-5-21 20:21\"".format(SOURCEJIRAPROJECT)
    #4
    #jql_query="Project = \'{0}\' and issuetype =\'Test\' and createdDate > \"2020-5-21 20:21\" and createdDate <\"2020-5-21 20:40\"".format(SOURCEJIRAPROJECT)
    #5
    #jql_query="Project = \'{0}\' and issuetype =\'Test\' and createdDate > \"2020-5-21 20:40\" and createdDate <\"2020-7-30 20:40\"".format(SOURCEJIRAPROJECT)
    #6
    #jql_query="Project = \'{0}\' and issuetype =\'Test\' and createdDate > \"2020-7-30 20:40\" and createdDate <\"2021-3-30 20:40\"".format(SOURCEJIRAPROJECT)
    #7
    #jql_query="Project = \'{0}\' and issuetype =\'Test\' and createdDate > \"2021-3-30 20:40\"".format(SOURCEJIRAPROJECT)
    
    print ("Used query:{0}".format(jql_query))
                        
    issue_list=jira.search_issues(jql_query, maxResults=6000)
    
       
                     
    nbr=len(issue_list)                    
    if nbr >= 1:
        COUNTER=1
        print ("Found:{0} Tests".format(nbr)) # iterate over all found Test issues
        for issue in issue_list:
            print ("")
            print ("")
            print ("xxxxxxxxxxxxxxxxxxxxx {0} xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx".format(issue))
            TARGETEPIC="NA"
            TARGETTEST="NA"
            SUMMARY=issue.fields.summary.encode("utf-8")
            DESCRIPTION=issue.fields.description
            if (DESCRIPTION!=None):
                 DESCRIPTION=issue.fields.description.encode("utf-8")
            EPICLINK=issue.raw["fields"]["customfield_10006"]  # find ocrrect epic link id from ui
            print ("SOURCE PROJECT ISSUE:{0}-->{1}".format(COUNTER,issue))
            print("SUMMARY:{0}".format(SUMMARY))
            print("DESCRIPTION:{0}".format(DESCRIPTION))
            print("SOURCE PROJECT EPICLINK:{0}".format(EPICLINK))
            


 
            
            
        
            if (EPICLINK != None): # Test case has linked EPIC
                
                print ("****************** EPIC LINKS SECTION ********************************************************************")
                
                
                # fail this issue handling if source project test case linked EPIC is outside source project (in another project)
                REGEXPR=r"("+SOURCEJIRAPROJECT+r")(-)(.*)"
                x = re.search(str(REGEXPR), str(EPICLINK))       
                if (x and x.group(1)==SOURCEJIRAPROJECT):
                    print ("OK. source project Epic is inside source project:{0}".format(x.group(1)))                            
                else:
                    print ("ERROR: SOURCE PROJECT LINKED EPIC IS OUTSIDE OF SOURCE PROJECT!!!!!!!")
                    print ("STOPPING ANALYZING THIS TEST CASE. YOU MIGHT WANT CHECK THIS LINKAGE MANUALLY") 
                    continue
                
                
                linkedissue = jira.issue(EPICLINK)
                LINKEDSUMMARY=linkedissue.fields.summary
                print("LINKED SOURCE EPIC SUMMARY:{0}".format(LINKEDSUMMARY))
                print ("Linked Source Test case: {0}-->  Source Epic:{1}".format(issue,linkedissue))
                print ("{0} --> {1}".format(SUMMARY,LINKEDSUMMARY))


                #Find Epic from target project, using source Epic summary as key for JQL
                #get rid of some JQL command chars first
                EDITEDLINKEDSUMMARY=LINKEDSUMMARY.replace('[','')
                EDITEDLINKEDSUMMARY=EDITEDLINKEDSUMMARY.replace(']','')
                EDITEDLINKEDSUMMARY=EDITEDLINKEDSUMMARY.replace('\'','\\\'')
                EDITEDSUMMARY=EDITEDLINKEDSUMMARY.replace('\'','\\\'')
                jql_query="Project = \'{0}\' and summary ~ \'{1}\' and issuetype = Epic ".format(TARGETPROJECT,EDITEDLINKEDSUMMARY) 
                print ("Used query:{0}".format(jql_query))                        
                issue_list=jira.search_issues(jql_query, maxResults=4000)
              
                            
                z=len(issue_list)                    
                if z >= 1:
                    print ("Found name matching TARGET project Epic:{0}".format(z))
                    for issue in issue_list: # assume only one Epic has been linked 
                        TARGETEPIC=issue
                        print ("TARGET EPIC:{0}".format(TARGETEPIC))
                elif (z>1): # in case many epics, fails this issue handling
                    print ("ERROR: TOO MANY LINKED EPICS FOUND.MAYBE EPIC SUMMARY MATCHES TOO MANY EPICS. CHECK MANUALLY!!")
                    continue            
                else:
                    print ("ERROR: NO TARGET PROJECT EPIC FOUND. IT MIGHT BE OUTSIDE IN ANOTHER PROJECT!!!!!!!!!")
                    print ("STOPPING ANALYZING THIS CASE. YOU MIGHT WANT CHECK THIS LINKAGE MANUALLY") 
                    continue   
                
                
                #Find Test case from target project, using summary as key
                SUMMARY=SUMMARY.decode()
                EDITEDSUMMARY=SUMMARY.replace('[','')
                EDITEDSUMMARY=EDITEDSUMMARY.replace(']','')
                EDITEDSUMMARY=EDITEDSUMMARY.replace('\'','\\\'')
                jql_query="Project = \'{0}\' and summary ~ \'{1}\' and issuetype = Test ".format(TARGETPROJECT,EDITEDSUMMARY) 
                print ("Used query:{0}".format(jql_query))                        
                issue_list=jira.search_issues(jql_query, maxResults=4000)
              
                
                #create target project to be created pic->test link information  
                # collect information to be deleted duplicates          
                z=len(issue_list)                    
                if (z > 1):
                    duplicates=[]
                    print ("DUPLICATE ERROR Found several:{0} matching same TARGET project test cases".format(z))
                    COUNTER2=0
                    for issue in issue_list: # assume only one Test 
                        COUNTER2=COUNTER2+1
                        if (COUNTER2<=1): # use first as test case, delete rest of the duplicates
                            TARGETTEST=issue
                            print ("TARGET EPIC:{0} -> LINKED TEST:{1}".format(TARGETEPIC,TARGETTEST))
                            print ("TODO Duplicates to be removed:")
                        else:
                            duplicates.append(issue)
                    if (COUNTER2>1):
                        print ("Duplicate test issues to be deleted: {0}".format(duplicates))
                        for issue in duplicates:
                            print ("TBD Deleted issue: {0}".format(issue))
                            if (SKIP==1):
                                print("DRY RUN MODE ON. Not doing anything")
                            else:
                                print ("REAL OPERATING MODE. DELETING ISSUE:{0}".format(issue))
                                #issue.delete()
                            
                            
                    else:
                        print ("ERROR: This line should not be executed")    
                            
                elif (z==1):
                    print("OK: Found single:{0} matching TARGET project test case".format(z))
                    TARGETTEST=issue_list[0]
                    print ("TARGET EPIC:{0} -> LINKED TEST:{1}".format(TARGETEPIC,TARGETTEST))
                    EPICLINK=TARGETTEST.raw["fields"]["customfield_10006"]  # find ocrrect epic link id from ui
                    print ("Target Issue Epic Link:{0}".format(EPICLINK))
                    
                    
                    if (SKIP==1):
                                print("DRY RUN MODE ON. Not doing Epic-Test linking")
                    else:
                        print ("REAL OPERATING MODE. Creating Target Epic-Target Test link:{0}".format(issue))               
                        TARGETTEST.update(fields={'customfield_10006': str(TARGETEPIC)})
                        #print("FORCE EXIT. CHECK RESULTS")
                    
                               
                else:
                    print ("ERROR: NO TARGET TEST CASE FOUND")          
                print ("****************************************************************************************************************")

            COUNTER=COUNTER+1
            if (SKIP==1):
                print("DRY RUN MODE ON. Not doing anything")
            else:
                print ("REAL OPERATION MODE. DRY RUN MODE OFF. Doing the deed. NOTHING AT TME MOMENT")    
                #CreateEpic(jira,SUMMARY,DESCRIPTION,TARGETPROJECT)
            
                #time.sleep(0.5) # prevent jira crash when creating issues in a row
            print ("xxxxxxxxxx END OF ISSUE HANDLING xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print ("")
            
    else:
        print ("NO Epics found")


#########################################################################

if __name__ == "__main__":
    main(sys.argv[1:]) 
 