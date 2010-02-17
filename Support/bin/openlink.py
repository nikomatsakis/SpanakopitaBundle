#!/usr/bin/env python

import os, sys, urlparse, urllib, re, subprocess, os.path

filepath = os.environ["TM_FILEPATH"]
filedir = os.path.dirname(filepath)
current_line = os.environ["TM_CURRENT_LINE"]
current_index = int(os.environ["TM_LINE_INDEX"])
scope = os.environ["TM_SCOPE"]

# First we need to extract the link.  The current index
# will be located in the middle.  It should be either:
# [../some/relative/path] or
# [[...@../some/relative/path]]
# depending on the current scope.

def shell(str):
    subprocess.Popen(str, shell=True)

before = current_line[:current_index]
after = current_line[current_index:]

if scope.endswith("markup.underline.link.img.spanakopita"):
    prechar = "["
    postchar = "]"
else:
    prechar = "@"
    postchar = "]]"

(_, _, before1) = before.rpartition(prechar)
(after1, _, _) = after.partition(postchar)
openurl = before1 + after1

print "<body><pre>"

print "filepath", filepath
print "current_line", current_line
print "current_index", current_index
print "scope", scope
print "before", before
print "after", after
print "before1", before1
print "after1", after1
print "openurl", openurl

if not re.match(r"[a-z.]:", openurl):
    # Relative or absolute path: 
    linkedpath = os.path.normpath(os.path.join(filedir, openurl))
    
    # Create file if it does not already exist:
    if not os.path.exists(linkedpath):
        f = open(linkedpath, 'w')
        f.write("Insert text here.")
        f.close()        
        
        # Switch to Dock so that TextMate will refresh:
        shell("osascript -e 'tell application \"Dock\" to activate'")    	
        
    # Create text mate URL:
    openurl = "txmt://open?url=file://"+urllib.quote(linkedpath.strip())

print "openurl", openurl
shell("open "+openurl)

print "</pre></body>"
