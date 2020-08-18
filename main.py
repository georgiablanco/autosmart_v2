#! /usr/bin/python
from bs4 import BeautifulSoup
import sys
import function as cdb
import HTML


if __name__=="__main__":
	
	diff = []

	print(cdb.get_value_from_para("cdb_report1.html", "number of campaigns"))
	print(cdb.get_value_from_row("cdb_report1.html", "CRTs", "101", "House_Count"))

	diff.append(cdb.get_value_from_row("cdb_report1.html", "CRTs", "102", "House_Count"))
	diff.append(cdb.get_value_from_row("cdb_report2.html", "CRTs", "102", "House_Count"))
	print(diff)


	# cdb.result_in_html("Number of Campaigns 1", cdb.get_value_from_row("cdb_report1.html", "Campaigns", "901", "House_Count"), cdb.get_value_from_row("cdb_report2.html", "Campaigns", "901", "House_Count"),2)
	# cdb.result_in_html("Number of Campaigns 2", cdb.get_value_from_row("cdb_report1.html", "Campaigns", "902", "House_Count"), cdb.get_value_from_row("cdb_report2.html", "Campaigns", "902", "House_Count"),3)
	# cdb.result_in_html("Number of Campaigns 3", cdb.get_value_from_row("cdb_report1.html", "Campaigns", "910", "House_Count"), cdb.get_value_from_row("cdb_report2.html", "Campaigns", "910", "House_Count"),4)

	
		