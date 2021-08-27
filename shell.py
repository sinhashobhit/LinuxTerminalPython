#!/usr/bin/python
# Shobhit Sinha
# Assignment 2 for Operating Systems Class, IIIT Kalyani
'''
This is probably the most powerful Python code I have ever written
'''
import os
import commands,subprocess,sys
from os.path import expanduser
inpfrom = sys.stdin
def cd(a):
    cmd = a.split()
    if(len(cmd)==1 or cmd[1]=='~'): #only cd is typed and nothing else, transfer to home directory
       os.chdir(expanduser("~"))
    else:
        try:
             os.chdir(cmd[1])
        except OSError as e:
             print(e)

def findExec(command, paths = None):

    # I am checking in the location given by PATH,if executable exists there
    # Then I am searching in all the sub directories in the PATH, to find the executable    
    # Function return none if no Executable exist: Leads the program to print unknown command
    if paths is None:
        paths = os.environ.get('PATH','')

    if os.path.exists(command):
        return command

    if not paths:
        paths = os.defpath

    pathext = os.environ.get('PATHEXT', '').split(os.pathsep)

    for path in paths.split(os.pathsep):
        for ext in pathext:
            p = os.path.join(path, command + ext)
            if os.path.exists(p):
                return p
    return None
def execute(a):
        status  = 0
        cmd = a.split()
        if('<' in cmd):
            # Condition for redirected stdin
            temp = a.split('<')
            file = temp[1].lstrip()
            execcmd = temp[0]
            cmd = execcmd.split()
            try: 
                os.close(0) 
                status = 1    # to indicate if stdin is redirected
            except OSError as e: print e   
            try:
                 inpfrom = open(file,'r') 
            except OSError as e: print e   
        elif('>'in cmd):
            #Condition for redirected stdout
            temp = a.split('>')
            file = temp[1].lstrip()
            execcmd = temp[0]
            cmd = execcmd.split()
            try: 
                os.close(1) 
                status = 2    # to indicate if stdout is redirected
            except OSError as e: print e   
            try:
                os.open(file,os.O_WRONLY+os.O_CREAT)
            except OSError as e: print e
        try:
            chPID = os.fork() 
            if chPID > 0:
                if(cmd[-1]!='&'):
                    os.waitpid(chPID,0)
                    #print 'CHILD OVER'
            else:
                 if(findExec(cmd[0])==None):
                    print 'Unknown Command :'+ a
                 else:
                    execC = findExec(cmd[0]) 
                    try: 
                        os.execv(execC, cmd[0:])
                    except OSError as e: print e
        except OSError as e: print e
        return status
def main():  
   os.system('clear')
   a = 'void'
   while(a!='exit'):
      stdout_copy=os.dup(1)
      stdin_copy = os.dup(0)
      print '\33[32m'+ os.getcwd()+':'+'\033[0m',
      a = raw_input()
      execmd = a
      cmd = a.split()
      if(a == '' or a.isspace()):
        continue
      elif(cmd[0]=='cd'):
        cd(a)
      elif(cmd[0]=='exit'):
        break;
      else:
        log = execute(a)
        if(log==1):
            os.dup(stdin_copy)
            os.close(stdin_copy)

        elif(log==2):
            os.close(1)
            os.dup(stdout_copy)
            os.close(stdout_copy)   
main()
