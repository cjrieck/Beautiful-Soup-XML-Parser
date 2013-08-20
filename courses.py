from bs4 import BeautifulSoup
from datetime import *

import plistlib, urllib2

def main():

	courseNames = {}
	output = {}

	semester = ""
	currentYear = date.today().year
	currentDate = date.today() #datetime.strptime("11/2/12", "%m/%d/%y")
	

	fallDate = "3/1/" + str(currentYear)
	fallDate = fallDate.replace("20", "")
	
	springDate = "09/01/" + str(currentYear)
	springDate = springDate.replace("20", "")

	fallSemesterStart = datetime.strptime(fallDate, "%m/%d/%y")
	springSemesterStart = datetime.strptime(springDate, "%m/%d/%y")

	if (currentDate > fallSemesterStart.date()) and (currentDate < springSemesterStart.date()):
		semester = "F"

	else:
		semester = "S"

	if(semester == "S"):
		url = "http://apollo/schedule/schedule_xml.php?semester="+semester+"+"+str(currentYear+1)+"&btn_simple_search=Search"

	else:
		url = "http://apollo/schedule/schedule_xml.php?semester="+semester+"+"+str(currentYear)+"&btn_simple_search=Search"

	opener = urllib2.build_opener()	
	url_opener = opener.open(url)
	page = url_opener.read()

	html = BeautifulSoup(page, "xml")

	courses = html.findAll("course")

	i = 2 # Course section counter
	p = 1 # Lab Section counter

	temp = ""

	for course in courses:

		information = []

		title = course.findAll("title",text=True)[0].renderContents()
		department = course.findAll("department",text=True)[0].renderContents()
		days = course.findAll("days",text=True)[0].renderContents()
		beginTime = course.findAll("begin_time",text=True)[0].renderContents()
		endTime = course.findAll("end_time",text=True)[0].renderContents()
		professor = course.findAll("professor",text=True)[0].renderContents()
		crn = course.findAll("crn",text=True)[0].renderContents()

		typeOfClass = course.findAll("type", text=True)[0].renderContents()

		title = title.replace("&amp;","&")
		information.append(department)
		information.append(days)
		information.append(beginTime)
		information.append(endTime)
		information.append(professor)
		information.append(crn)

		temp2 = title

		if title in courseNames:

			if typeOfClass == "lab":

				if p == 1:
					title = title + " Lab"
					p = p + 1

				else:
					title = title + " Lab " + str(p)
					p = p + 1

			else:
				title = title + " (Sect " + str(i) + ")"
				i = i + 1

		elif temp != title:
			p = 1
			i = 2

		courseNames[title] = information

		temp = temp2

	output = {"Courses" : courseNames}
	plistlib.writePlist(courseNames, "courses.plist")
main()