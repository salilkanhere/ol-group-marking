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

import olsettings

SESSIONID = None

def read_json (f):
	#f = opener.open(req)
	return json.loads (f.read ())

def main ():
	global SESSIONID

	if len(sys.argv) != 2:
		print "Usage: %s <report-directory>" % sys.argv[0]
		return

	SESSIONID = olsettings.SESSIONID
	reportDirectory = sys.argv[1]

	cj = cookielib.CookieJar()

	cj.set_cookie (cookielib.Cookie (version=0, name='sessionid', value=SESSIONID, port=None, port_specified=False, domain='www.openlearning.com', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=True, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False))
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

	if not os.path.isdir (reportDirectory):
		print "Report directory does not exist"
		return

	for report in os.listdir (reportDirectory):

		print "Uploading %s..." % (report)

		reportSource = open(%s/%s' % (reportDirectory, report))

		# todo fix this
		reportRelativeUrl = "courses/99luftballons/Cohorts/ClassOf2014/Groups/Tutors/MagicalMarkingPages/Test"

		content_url = 'https://www.openlearning.com/%s' % reportRelativeUrl
		commentpage = opener.open (content_url).read()
		soup = BeautifulSoup.BeautifulSoup(commentpage)
		commentcontainer = soup.find (id='comments-container-main')
		commentdoc = commentcontainer['data-document']

		comment_content = "Test comment\n New \n Line \n Line"
		comment_content = comment_content.replace ("\n", "<br />")

		export_data = {
			'document': commentdoc,
			'parentComment': '',
			'content': comment_content
		}

		# do some csrf bullshit
		csrf = None
		for cookie in cj:
			print cookie
			if 'csrf' in cookie.name:
				csrf = cookie.value

		opener.addheaders = [('Referer', content_url),
			('X-CSRFToken', csrf),
			('X-Requested-With', 'XMLHttpRequest')]

		http_data =  urllib.urlencode (export_data.items())
		resp = opener.open ('https://www.openlearning.com/commenting/add/', data=http_data).read()
		jcomment = json.loads (resp)
		if jcomment['success'] != True:
			print "Failed to post comment, skipping."
			continue

		#print "\t\tMarking task as complete..."
		#mark_data = {
		#	'activityId': (activityId),
		#	'userId': stu[username]['userId'],
		#	'completed': 'true',
		#	'cohortId': (cohortId),
		#	'groupPath': ''
		#}

		#grade_page = "https://www.openlearning.com/api/mark/?action=setMarkComplete"
		#print grade_page
		#http_data =  urllib.urlencode (mark_data.items())
		#opener.open (grade_page, data=http_data)

	print "Finished uploading"
		
if __name__ == "__main__":
	main ()
