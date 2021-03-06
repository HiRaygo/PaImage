#-------------------------------------------------------------------------------
# -*- coding:  UTF-8
# Purpose:
# Author:      Raygo
# Created:     07/03/2015
# Copyright:   (c) Raygo 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import urllib
import urllib2
import re
import os
import random
import string
import time
from threading import Thread


RE_IMAGELINKA = r'<img class="PhotoPostImage" src="http:.*alt'
RE_IMAGELINK = r'http:.*jpg'
RANDOMSTRING = "abcdefghijklmnopqrstuvwxyzQWERTYUIOPKJLHGFDSAZXCVBNM0987654321"

class request():
    def __init__(self,baseurl,savepath):
        self.baseURL = baseurl
        self.filePath = savepath

    def getPage(self,pagen):
        try:
            url = self.baseURL + str(pagen)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print "Connect error: ",e.reason
                return None

    def getImglinks(self,page):
        if page is None:
            return None
        try:
            result = re.findall(RE_IMAGELINKA,page)
            if result:
                links = []
                for res in result:
                    link = re.findall(RE_IMAGELINK,res)
                    if link:
                        links.append(link[0])
                return links
            else:
                return None
        except:
            return None

    def downloadImage(self,Imglinks, threadNo):
        if Imglinks is None:
            return
        try:
            if not os.path.exists(self.filePath) :
                os.mkdir(self.filePath)
            for item in Imglinks:
                jpgfile = self.filePath + string.join(random.sample(RANDOMSTRING, 8)).replace(" ", "") +'.jpg'
                print jpgfile
                with open(jpgfile, 'wb') as jpg:
                    jpg.write(urllib2.urlopen(url=item, timeout =10).read())
            print('Thread %d finish.\n' %threadNo)
        except Exception, ex:
            print ex

    def GetImages(self, pageNum):
        for i in range(1, pageNum+1):
            pg= self.getPage(i)
            lks = self.getImglinks(pg)
            downThread = Thread(group =None, target= self.downloadImage, args = (lks,i))
            downThread.setDaemon(True)
            downThread.start()
            print('Thread %d start.\n' %i)
            time.sleep(1)
