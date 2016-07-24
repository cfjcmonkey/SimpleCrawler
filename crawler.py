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

class DownInfo:
	def __init__(self, url, path, level):
		self.url = url;
		self.path = path;
		self.level = level;

class Crawler:
	def __init__(self, outputPath = 'output/', ignoreFile = 'ignoreurl.dat'):
		self.outputPath = outputPath;
		self.ignoreFile = open(ignoreFile, 'a');
		
		self.ignoreList = [line.strip() for line in file(ignoreFile)];
		self.logFile = open('log.txt', 'a');		
		self.driver = webdriver.Chrome();
		self.idx = 0;
		self.finishCount = 0;
		
	def Close(self):
		self.driver.close();
		self.logFile.close();
		self.ignoreFile.close();
	
	def Download(self, info, maxsleep):
		if not info:
			return "";			
		if info.url in self.ignoreList:
			self.Log("already download " + info.url);
			return info.url;
		
		self.Log("trying to download " + info.url);		
		try:
			self.idx += 1
			if self.idx % 50 == 0:
				self.logFile.flush();
			#     driver.close()
			#     LoadDriver()

			self.driver.get(info.url)

			sleeptime = random.randint(1, maxsleep)
			sleep(sleeptime)

			doc = self.driver.page_source.encode('utf-8');
			self.Log("finish download, begin save to " + info.path);
			
			fobj = open(info.path , 'w')
			fobj.write(doc + "\n")
			fobj.close();
			
			self.Log("finish " + info.url);
			self.FinishCallback(info);
			return info.url;
		except:
			self.Log("Download Error in " + info.url);
		
	def Log(self, message):
		print datetime.datetime.now(), message;
		self.logFile.write('%s %s\n'%(datetime.datetime.now(), message));

	def FinishCallback(self, info):
		self.finishCount += 1
		if self.finishCount % 30 == 0:
			print 'finish %d'%self.finishCount    
		self.ignoreFile.write(info.url + '\n')
		self.ignoreList.append(info.url);
	
	def DownloadBatchPage(self, urlFile):    
		rootlist = [line.strip() for line in file(urlFile)]
		for rooturl in rootlist:
			di =  DownInfo(rooturl, self.outputPath + rooturl[rooturl.rfind('/'):] + ".html", 2)
			self.Download(di, 10)
	
	def DownloadPage(self, url):
		di =  DownInfo(url, self.outputPath + url[url.rfind('/'):] + ".html", 2)
		self.Download(di, 10)
		
def main_page():
	crawler = Crawler('urlList.dat', 'http://xxx/', "output/");
	crawler.DownloadPage();
	crawler.Close();

if __name__=="__main__" :
	main_page();
