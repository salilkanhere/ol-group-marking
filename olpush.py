#!/usr/bin/env python2

# based on code written by Alex Hixon
# https://github.com/ahixon/openlearning-offline

import urllib
import urllib2
import json
import time
import sys
import os
import cookielib
import csv
import BeautifulSoup
import datetime
import cgi
import random
from time import gmtime, strftime

import olsettings

SESSIONID = None

def read_json (f):
	#f = opener.open(req)
	return json.loads (f.read ())

def main ():
	random.seed()

	global SESSIONID

	if len(sys.argv) != 2:
		print "Usage: %s <report-directory>" % (sys.argv[0])
		return

	SESSIONID = olsettings.SESSIONID
	reportDirectory = sys.argv[1]

	cj = cookielib.CookieJar()

	cj.set_cookie (cookielib.Cookie (version=0, name='sessionid', value=SESSIONID, port=None, port_specified=False, domain='www.openlearning.com', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=True, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False))
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

	if not os.path.isdir (reportDirectory):
		print "Report directory does not exist"
		return

	for reportFilename in os.listdir (reportDirectory):

		print "Uploading %s..." % (reportFilename)

		reportFilenameWithoutExt = os.path.splitext(reportFilename)[0]

		reportSource = open("%s/%s" % (reportDirectory, reportFilename)).read()

		reportSource = reportSource.replace("\n", "")

		reportRelativeUrl = "courses/99luftballons/Cohorts/ClassOf2014/Groups/Tutors/MagicalMarkingPages/%s" % (reportFilenameWithoutExt)

		# testing
		# reportRelativeUrl = "courses/99luftballons/Cohorts/ClassOf2014/Groups/Tutors/MagicalMarkingPages/%s" % ("Test")

		content_url = 'https://www.openlearning.com/%s' % reportRelativeUrl
		commentpage = opener.open (content_url).read()
		soup = BeautifulSoup.BeautifulSoup(commentpage)
		commentcontainer = soup.find (id='comments-container-main')
		commentdoc = commentcontainer['data-document']

		randomNumber = random.randint(0,20)
		randomNumber2 = random.randint(0,25)
		randomLetter = chr(65 + randomNumber2)

		comment_content = "This page was automatically updated at %s. Brought to you by Alex, Rupert, the number %d and the letter '%s'." % (strftime("%Y-%m-%d %H:%M:%S"), randomNumber, randomLetter)
		comment_content = comment_content.replace ("\n", "<br />")

		export_data = {
			'document': commentdoc,
			'parentComment': '',
			'content': comment_content
		}

		# do some csrf bs
		csrf = None
		for cookie in cj:
			if 'csrf' in cookie.name:
				csrf = cookie.value
				break

		opener.addheaders = [
			('Referer', content_url),
			('X-CSRFToken', csrf),
			('X-Requested-With', 'XMLHttpRequest')
		]

		http_data =  urllib.urlencode (export_data.items())
		resp = opener.open ('https://www.openlearning.com/commenting/add/', data=http_data).read()
		jcomment = json.loads (resp)
		if jcomment['success'] != True:
			print "Failed to post comment, skipping."
			continue

		# do some csrf bs (again?)
		csrf = None
		for cookie in cj:
			if 'csrf' in cookie.name:
				csrf = cookie.value
				break

		componentData = '{"HTMLData":{"pageHTML":"%s"}}' % (
			reportSource
		)

		editData = {
			'method': 'saveComponents',
   			'componentData': componentData
		}

		http_data = urllib.urlencode (editData.items())

		editPageUrl = content_url + "?action=edit&editor=html"

		resp = opener.open (editPageUrl, data=http_data)

	print "Finished updating stats - hooray!"
		
if __name__ == "__main__":
	main ()
