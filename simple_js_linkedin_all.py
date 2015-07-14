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

class down_info(object):
  def __init__(self,du,sp,lv):
    self.down_url = du;
    self.save_path = sp;
    self.level = lv;

class HumanizedCrawler:  

  def __init__(self, urlFile, hosturl, down_path = '', preventFile = ''):
    self.hosturl = hosturl;
    self.urlFile = urlFile;
    self.down_path = down_path;
    if self.down_path == '':
      self.down_path = 'output/';
    if(not os.path.exists(self.down_path)):
      os.makedirs(self.down_path)

    if preventFile == '':
      preventFile = 'finish_url.dat'; 
    self.preventFile = open(preventFile, 'a');
    self.logFile = open('log.txt', 'a');
    self.mineUrlFile = open('newUrl.dat', 'a');

    self.prevent_list = {};
    self.driver = self.LoadDriver();
    self.idx = 0;
    self.countfinish = 0;

    if os.path.exists(self.preventFile):
      self.prevent_list = [line.strip() for line in file(preventFile)]

  def Close():
    self.driver.close()
    self.logFile.close();
    self.mineUrlFile.close();
    self.preventFile.close();

  def LoadDriver(self):
  # dcap = dict(DesiredCapabilities.PHANTOMJS)
  # dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ")
  # driver = webdriver.PhantomJS(desired_capabilities=dcap)
    self.driver = webdriver.Chrome()

  def finish_callback(self, url):
    self.countfinish += 1
    if self.countfinish % 30 == 0:
      print 'finish %d'%self.countfinish    
    self.preventFile.write(url + '\n')
    print '/////////finish url %s/////////'%url

  def write_log(self, info):  
    print datetime.datetime.now(), info
    self.logFile.write('%s %s\n'%(datetime.datetime.now(), info));

  def AddTargetUrl(self, url):
    self.mineUrlFile.write(url + '\n')
  
  def download_js(di,sec,isLeaf):
    if not di:
      return ""

    self.write_log("trying to download " + di.down_url);

    try:
      if (not isLeaf and di.down_url in self.prevent_list) or (isLeaf and os.path.isfile(di.save_path)):
        write_log("already download " + di.down_url)
        return di.down_url

      self.idx += 1
      if self.idx % 50 == 0:
        self.logFile.flush();
  #     driver.close()
  #     LoadDriver()

      self.driver.get(di.down_url)

      sleeptime = random.randint(1, sec)
      sleep(sleeptime)
      
      doc = self.driver.page_source.encode('utf-8');
      
      fobj = open(di.save_path , 'w')
      fobj.write(doc+"\n")
      fobj.close()
      
      self.finish_callback(di.down_url)
      
      if not isLeaf:
        self.AnalyzePage(doc, di.level);

      return di.down_url
    except:
      self.write_log("download error")
      raise Exception("Download Error")

  def AnalyzePage(self, doc, level):
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
        dj = down_info(href, down_path + href[href.rfind('/'):] + ".html", level + 1)
        self.download_js(dj, sec, False)
      else:
        self.AddTargetUrl(href)
    self.write_log('mining link %d in %s'%(count, di.down_url))

  def DownloadDirectory():
    rootlist = [line.strip() for line in file(self.urlFile)]
    for rooturl in rootlist:
      di =  down_info(rooturl, down_path + rooturl[rooturl.rfind('/'):] + ".html", 2)
      self.download_js(di, 5, False)

    print "total task url ", countfinish

  def DownloadPage():    
    rootlist = [line.strip() for line in file(self.urlFile)]
    for rooturl in rootlist:
      di =  down_info(rooturl, down_path + rooturl[rooturl.rfind('/'):] + ".html", 2)
      self.download_js(di,5, True)

    print "total task url ", countfinish



if __name__=="__main__" :
  main_page();
