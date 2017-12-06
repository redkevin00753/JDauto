# coding: utf-8
import os
import socket
import json
import sys
import re
from subprocess import Popen, PIPE

class Docker(object):
    """ Docker metheds """
    ##  check if image exist
    def checkImageNames(imagename):
    	result = os.popen('docker images ' + imagename + '|wc -l')
    	count = int(result.read().strip())
    	if count > 1:
    		print('-> image %s OK' % imagename)
    		return True
    	else:
    		print('-> image %s Not Found' % imagename)
    		return False
	##  deploy to exist
    def deployToExist(war,cname):
    	Docker.killAndRmContainer(cname)
    	image = Docker.getImage(cname)
    	port = Docker.getPorts(cname)[0]
    	Docker.deployToNew(war,image,port,cname)

	##  deploy to new
    def deployToNew(war,imagename,port,cname):
    	popenlist = ['docker','run','-d','--name']
    	popenlist.append(cname)
    	popenlist.append('-p')
    	popenlist.append(str(port) + ':9080')
    	popenlist.append('-v')
    	popenlist.append(war + ':/config/dropins/docker.war')
    	popenlist.append(imagename)
    	p = Popen(popenlist,stdout=PIPE,stderr=PIPE)
    	lines = p.stdout.readlines()
    	if len(lines) != 1:
    		print('Container create Failed')
    		sys.exit(1)
    	for line in lines:
    		linestr = bytes.decode(line)
    		print('Container %s Build OK on Port %s ' % (Docker.getName(linestr),Docker.getPorts(linestr)[0]))
    		
    # Kill and Remove container
    def killAndRmContainer(cname):
    	os.popen('docker kill ' + cname)
    	os.popen('docker rm ' + cname)

    # Get Container name inspect as json object 
    def getCinspect2JsonObj(cname):
    	result = os.popen('docker inspect ' + cname)
    	jsonstr = result.read().strip()[1:-1]
    	jsonobj = json.loads(jsonstr)
    	return jsonobj

    # Get Depolyed URLs from log
    def getDeployURLs(host,port,cname):
    	urllist = []
    	p = Popen(['docker','logs','-f',cname],stdout=PIPE,stderr=PIPE)
    	flag = True
    	while flag:
    		line = p.stdout.readline()
    		linestr = bytes.decode(line)
    		urlstr = re.match('.*Web application available \(default_host\).*:[0-9]*/(.*)/\n',linestr,re.S)
    		if urlstr:
    			urllist.append(host+':'+str(port)+'/'+urlstr.group(1))
    		if re.search(r'The server defaultServer is ready to run a smarter planet',linestr):
    			flag = False
    	s = set(urllist)
    	for a in s:
    		print(a)

    def getContainerNamesPorts():
    	p = Popen(['docker', 'ps', '-aq'],stdout=PIPE,stderr=PIPE)
    	lines = p.stdout.readlines()
    	nameList=[]
    	portList=[]
    	for line in lines:
    		linestr = bytes.decode(line)
    		nameList.append(Docker.getName(linestr))
    		portList.extend(Docker.getPorts(linestr))
    	portList.sort()
    	return nameList,portList
    def getImage(cname):
    	json = Docker.getCinspect2JsonObj(cname)
    	return json['Image']
    def getName(cname):
    	json = Docker.getCinspect2JsonObj(cname)
    	return json['Name'][1:]
    def getPorts(cname):
    	json = Docker.getCinspect2JsonObj(cname)
    	items = json['HostConfig']['PortBindings']
    	plist = []
    	for item in items:
    		subitems = items[item]
    		for subitem in subitems:
    			plist.append(int(subitem['HostPort']))
    	return plist

class OS(object):
	def IsNotUse(port,ip='127.0.0.1'):
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		try:
			s.connect((ip,int(port)))
			s.shutdown(2)
			# print('Port %d is used' % port)
			return False
		except:
			# print('Port %d is not used' % port)
			return True
	def IsWarThere(path):
		isexists = os.path.exists(path)
		# os.path.isfile(path)
		if isexists:
			print('-> war %s OK' % path)
			return True
		else:
			print('-> war %s missing' % path)
			return False
    	
