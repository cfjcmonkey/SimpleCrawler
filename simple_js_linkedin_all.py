# -*- coding: gbk -*-
from time import ctime,sleep
import time
import os
import errno
import fnmatch
import threading
from random import choice
import random
import re
import urllib2
from subprocess import call
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from multiprocessing import Pool
import sys
import datetime


prevent_list = {};
down_list = [];
unzip_list = [];
treate_list = [];
down_path = '';
treate_path_part = '';
keep_path = '';
idx = 0;
driver = ""
countfinish = 0
hosturl = "http://www.linkedin.com"
logFile = open('log.txt', 'a');

def LoadDriver():
	global driver
#	dcap = dict(DesiredCapabilities.PHANTOMJS)
#	dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ")
#	driver = webdriver.PhantomJS(desired_capabilities=dcap)
	driver = webdriver.Chrome()

class down_info(object):
	def __init__(self,du,sp,lv):
		self.down_url = du;
		self.save_path = sp;
		self.level = lv;
#self.context = ""

def finish_callback(url):
	global countfinish
	countfinish += 1
	if countfinish % 30 == 0:
		print 'finish %d'%countfinish
	fobj = open("finishurl_linkedin_dir.dat","a")
	fobj.write(url + '\n')
	fobj.close()
	print '/////////finish url %s/////////'%url

def AddTargetUrl(url):
	fobj = open("url_linkedIn_com_all.txt", "a")
	fobj.write(url + '\n')
	fobj.close()
	
def download_js(di,sec,isLeaf):
	if not di:
		return ""

	write_log("trying to download " + di.down_url);
	global prevent_list;
	global down_path;
	global idx;
	global driver
	global logFile

	try:
		if (not isLeaf and di.down_url in prevent_list) or (isLeaf and os.path.isfile(di.save_path)):
			write_log("already download " + di.down_url)
			return di.down_url
		idx += 1
		if idx % 50 == 0:
			logFile.flush();
#			driver.close()
#			LoadDriver()

		driver.get(di.down_url)

		sleeptime = random.randint(1, sec)
		sleep(sleeptime)
		
		doc = driver.page_source.encode('utf-8');
		
		fobj = open(di.save_path , 'w')
		fobj.write(doc+"\n")
		fobj.close()
		
		finish_callback(di.down_url)
		
		if not isLeaf:
			bg = doc.find("<ul class=\"column dual-column\">")
			ed = doc.find("</ul>", bg)
			dircnt = doc[bg:ed]
			count = 0
			for m in re.finditer(r'\shref="(.+?)"\s', dircnt):
				count += 1
				href = m.group(1)
				if href.startswith('http') == False:
					href = hosturl + href
				if '/directory/' in href:
					dj = down_info(href, down_path + href[href.rfind('/'):] + ".html", di.level + 1)
					download_js(dj, sec, False)
				else:
					AddTargetUrl(href)
			write_log('mining link %d in %s'%(count, di.down_url))
		return di.down_url
	except:
		write_log("download error")
		raise Exception("Download Error")

def write_log(info):
	global logFile
	
	print datetime.datetime.now(), info
	logFile.write('%s %s\n'%(datetime.datetime.now(), info));

def main_dir():
	global down_path;
	global prevent_list;
	global countfinish;
	global driver
	global logFile

	keep_path = os.getcwd()+'/'
	down_path = keep_path + 'linkedin/'
	if(not os.path.exists(down_path)):
		os.makedirs(down_path)

	LoadDriver()
	prevent_list = [line.strip() for line in file("finishurl_linkedin_dir.dat")]

#	rooturl = "http://www.linkedin.com/directory/companies?trk=hb_ft_companies_dir"	
#	di =  down_info(rooturl, down_path + rooturl[rooturl.rfind('/'):] + ".html", 2)
#	download_js(di, 3, False)

	rootlist = [line.strip() for line in file('url_linkedIn_root.txt')]
	for rooturl in rootlist:
		di =  down_info(rooturl, down_path + rooturl[rooturl.rfind('/'):] + ".html", 2)
		download_js(di, 5, False)

	print "total task url ", countfinish
	driver.close()
	logFile.close();

def main_page():
	global down_path;
	global prevent_list;
	global countfinish;
	global driver
	global logFile

	keep_path = os.getcwd()+'/'
	down_path = keep_path + 'linkedin/'
	if(not os.path.exists(down_path)):
		os.makedirs(down_path)
	LoadDriver()
	
	rootlist = [line.strip() for line in file('url_linkedIn_com_all.txt')]
	for rooturl in rootlist:
		di =  down_info(rooturl, down_path + rooturl[rooturl.rfind('/'):] + ".html", 2)
		download_js(di,5, True)

	print "total task url ", countfinish
	driver.close()
	logFile.close()


if __name__=="__main__" :
	main_page();




