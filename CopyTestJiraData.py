# Go through source project Zephyr Squad test cases and copy all normal Jira fields to matching target project Test case
# (using source project test case summary as find key)
# mika.nokka1@gmail.com 15.9.2021



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
 
    parser = argparse.ArgumentParser(description=" Copy test case normal jira data to target project (and matching test case)",
    
    
    epilog="""
    
    EXAMPLE:
    
    CopyTestJiraData.py  -u MYUSERNAME -w MYPASSWORD -s https://MYOWNJIRA.fi/ """

    
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

            TARGETTEST="NA"
            SUMMARY=issue.fields.summary.encode("utf-8")
            DESCRIPTION=issue.fields.description
            if (DESCRIPTION!=None):
                DESCRIPTION=issue.fields.description.encode("utf-8")
            COMPONENT=issue.fields.components
            REPORTER=issue.fields.reporter
            PRIORITY=issue.fields.priority 
            LABELS=issue.fields.labels 
            AUTOMATION=issue.get_field("customfield_11801") #TBD field numbers in data structure
            #TEAM=issue.get_field("customfield_13402") 
            TEAM2=issue.get_field("customfield_12500") 
            REPORTEDBYSI=issue.get_field("customfield_12200") 
            SAUTOMATION=issue.get_field("customfield_20205")
            CLIENTU=issue.get_field("customfield_11802")
            CLIENTREQ=issue.get_field("customfield_11472")
         
            print ("SOURCE PROJECT ISSUE:{0}-->{1}".format(COUNTER,issue))
            print("SUMMARY:{0}".format(SUMMARY))
            print("DESCRIPTION:{0}".format(DESCRIPTION))
            print ("COMPONENTS:{0}".format(COMPONENT))
            print ("REPORTER:{0}".format(REPORTER))
            print ("PRIORITY:{0}".format(PRIORITY))
            print ("AUTOMATION:{0}".format(AUTOMATION))
            #print ("TEAM:{0}".format(TEAM))
            print ("TEAM2:{0}".format(TEAM2))
            print ("REPORTEDBYSI:{0}".format(REPORTEDBYSI))
            print ("SAUTOMATION:{0}".format(SAUTOMATION))
            print ("CLIENTU:{0}".format(CLIENTU))
            print ("CLIENTREQ:{0}".format(CLIENTREQ))
            
            C=0
            for label in LABELS:
                C=C+1
                print ("LABEL {0} : {1}".format(C,label))
         

            #Find Test case from target project, using summary as key
            SUMMARY=SUMMARY.decode()
            EDITEDSUMMARY=SUMMARY.replace('[','')
            EDITEDSUMMARY=EDITEDSUMMARY.replace(']','')
            EDITEDSUMMARY=EDITEDSUMMARY.replace('}','')
            EDITEDSUMMARY=EDITEDSUMMARY.replace('\'','\\\'')
            jql_query="Project = \'{0}\' and summary ~ \'{1}\' and issuetype = Test ".format(TARGETPROJECT,EDITEDSUMMARY) 
            print ("Used query:{0}".format(jql_query))                        
            issue_list=jira.search_issues(jql_query, maxResults=4000)
        
            z=len(issue_list)                    
            if (z > 1):
      
                    print ("DUPLICATE ERROR Found several:{0} matching same TARGET project test cases".format(z))
                    print ("Use another tool to delete duplicates.SKIPPING THIS ISSUE...")
                    continue
                            
            elif (z==1):
                    TARGETSUMMARY=issue.fields.summary.encode("utf-8")
                    TARGETSUMMARY=TARGETSUMMARY.decode()
                    TARGETEDITEDSUMMARY=TARGETSUMMARY.replace('[','')
                    TARGETEDITEDSUMMARY=EDITEDSUMMARY.replace(']','')
                    TARGETEDITEDSUMMARY=EDITEDSUMMARY.replace('}','')
                    TARGETEDITEDSUMMARY=EDITEDSUMMARY.replace('\'','\\\'')
                    
                    print("OK: Found single:{0} matching TARGET project test case".format(z))
                    TARGETTEST=issue_list[0]
                    print ("Matching target test case --> {0}".format(TARGETTEST))
                    print ("Target summary: {0}".format(TARGETEDITEDSUMMARY))
                    print ("Target-Source pair: {0} --> {1} ".format(issue,TARGETTEST))
                    

                    
                    if (SKIP==1):
                                print("DRY RUN MODE ON. Not doing Jira data copying")
                    else:
                        print ("REAL OPERATING MODE. CURRENTLY DOING NOTHING:{0}".format(issue))               
                          
            else:
                    print ("ERROR: NO TARGET TEST CASE FOUND")          
            print ("****************************************************************************************************************")

            COUNTER=COUNTER+1
            
                
            
            if (TARGETTEST != "NA"):
                
                if (SKIP==1):
                    print("DRY RUN MODE ON. NOT DOING ANYTHING")
                   
                else:
                    print ("REAL OPERATION MODE. DRY RUN MODE OFF. Doing the data copy operation") 
                    CopyData (DESCRIPTION,COMPONENT,REPORTER,PRIORITY,LABELS,AUTOMATION,TEAM2,REPORTEDBYSI,SAUTOMATION,CLIENTU,CLIENTREQ,TARGETTEST)   
                    #time.sleep(0.3) # prevent jira crash when creating issues in a row
                
               
                if (COUNTER>=1):
                    print ("FORCE TESTING  STOP!!!")
                    sys.exit(5)    
                
                
                
            print ("xxxxxxxxxx END OF ISSUE HANDLING xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print ("")
            
            

            
    else:
        print ("No test case found")
 
############################################################################################
# copy source project test case normal Jira data to target project found matching test case    
# TBD: data in dictionary     
        
def CopyData (DESCRIPTION,COMPONENT,REPORTER,PRIORITY,LABELS,AUTOMATION,TEAM2,REPORTEDBYSI,SAUTOMATION,CLIENTU,CLIENTREQ,TARGETTEST):        
        print ("Data copy operations TO:{0}".format(TARGETTEST))
        print ("..............................................")
        
        if (DESCRIPTION != None):
            print ("DESCRIPTION available")
            TARGETTEST.update(notify=False, description=str(DESCRIPTION))
            time.sleep(0.3) 
        
        if (COMPONENT != None):
            NAME=COMPONENT[0]
      
            print ("COMPONENT available -->{0}".format(NAME))
            #TARGETTEST.update(notify=False, components=str(NAME))
            #values = [{'value':str(NAME)}]
            #TARGETTEST.update(notify=False,components={ values})
            #TARGETTEST.update(notify=False,fields={'components': {'value':str(COMPONENT)}})
            TARGETTEST.update(notify=False,update={"components": [{"add": {"name": str(NAME),}}],},)
            #'components' : [{'name' : 'FCS'}],
            time.sleep(0.3)

        
        if (REPORTER != None):
            print ("REPORTER available")
            
            NAME = TARGETTEST.fields.reporter.name
            print ("NAME:{0}".format(NAME))
            TARGETTEST.update(notify=False,reporter={'name': str(NAME)})
            #TARGETTEST.update(notify=False, reporter=str(REPORTER))
            time.sleep(0.3)        
            
        if (PRIORITY != None):
            print ("PRIORITY available")
            TARGETTEST.update(notify=False,priority={'name': str(PRIORITY)})
            #TARGETTEST.update(notify=False, priority=str(PRIORITY))
            time.sleep(0.3) 
        
        if (LABELS != None):
            print ("LABELS available")
            for label in LABELS:
                print ("  -->{0}".format(label))
                TARGETTEST.fields.labels.append(label)
                TARGETTEST.update(fields={"labels": TARGETTEST.fields.labels})
                time.sleep(0.3)
        
        if (AUTOMATION != None):
            print ("AUTOMATION available")
            TARGETTEST.update(notify=False,fields={'customfield_11801': {'value':str(AUTOMATION)}})
            #TARGETTEST.update(notify=False, customfield_11801=AUTOMATION)
            time.sleep(0.3)
        
        if (TEAM2 != None):
            print ("TEAM2 available")
            TARGETTEST.update(notify=False,fields={'customfield_12500': {'value':str(TEAM2)}})
            #TARGETTEST.update(notify=False, customfield_12500=TEAM2)
            time.sleep(0.3)
        
        if (REPORTEDBYSI != None):
            print ("REPORTEDBYSI available")
            TARGETTEST.update(notify=False,fields={'customfield_12200': {'value':str(REPORTEDBYSI)}})
            time.sleep(0.3)

        if (SAUTOMATION != None):
            print ("SAUTOMATION available")
            TARGETTEST.update(notify=False,fields={'customfield_20205': {'value':str(SAUTOMATION)}})
            time.sleep(0.3)
            
        if (CLIENTU != None):
            print ("CLIENTU available")
            TARGETTEST.update(notify=False,fields={'customfield_11802': {'value':str(CLIENTU)}})
            time.sleep(0.3)
            
        if (CLIENTREQ != None):
            print ("CLIENTREQ available")
            TARGETTEST.update(notify=False,fields={'customfield_11472': {'value':str(CLIENTREQ)}})
            time.sleep(0.3)


#########################################################################

if __name__ == "__main__":
    main(sys.argv[1:]) 
 