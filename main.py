# -*- encoding: utf-8 -*-
#!/usr/bin/env python

""" Script for bulk delete files in slack. """

import httplib2
import json
import calendar
import urllib
import sys
from datetime import datetime, timedelta

TOKEN = 'xoxp-292869156659-292426721345-512707621991-6447f58d0d0a92f54424dbddacbc0c7f'

h = httplib2.Http()
(response, content) = h.request(
    'https://slack.com/api/files.list?token={}'.format(TOKEN),
    "GET",
    headers={'Content-type': 'application/x-www-form-urlencoded'})

def check_error(error_message, answer, error_code = 1):
    if not answer["ok"]:
        print >> sys.stderr, '%s : %s' % (error_message, answer['error'])
        sys.exit(error_code)

answer = json.loads(content)
check_error('Could not get file list', answer)
files = answer["files"]
paging = answer["paging"]

while paging["page"] < paging["pages"]:
    newPage = paging["page"] + 1

    params["page"] = newPage
    data = urllib.urlencode(params)

    h = httplib2.Http()

    (response, content) = h.request(
        'https://slack.com/api/files.list',
        "POST",
        body=data,
        headers={'Content-type': 'application/x-www-form-urlencoded'})

    answer = json.loads(content)
    check_error('Could not get page of file', answer)
    files = files + answer["files"]
    paging = answer["paging"]

if len(files) < 1:
    print "No files to delete."
else:
    print "Total Files to delete: " + str(len(files)) + "\n Start deleting files."

for f in files:
    try:
        print "Deleting file " + str(f["id"]) + ": " + f["name"].encode('utf-8') + "...",

        timestamp = str(calendar.timegm(datetime.now().utctimetuple()))
        url = "https://slack.com/api/files.delete?t=" + timestamp

        params = {
            "token": TOKEN,
            "file": f["id"],
            "set_active": "true",
            "_attempts": "1"}

        data = urllib.urlencode(params)

        h = httplib2.Http()

        (resp, content) = h.request(url,
            "POST",
            body=data,
            headers={'Content-type': 'application/x-www-form-urlencoded'})

        print "[{}]".format("\033[92m {}\033[00m" .format(json.loads(content)["OK"]))

    except Exception as e:
        print e
