# coding: utf-8
import os
import socket
import json
import sys
import shutil
import re
from subprocess import Popen, PIPE

class Docker(object):
    """ Docker metheds """
    ##  check if image exist
    def checkImageName(imagename):
    	imagelist = os.popen('docker images | awk \'{print($1":"$2)}\'')
    	line = imagelist.readline().strip()
    	while line:
    		notag = ""
    		print(line)
    		if line[-6:] == "latest":
    			notag = line[:-7]
    			if imagename == line or imagename == notag:
    				print('-> image %s OK ' % imagename)
    				return True
    		line = imagelist.readline().strip()
    	print('-> image %s Not Found ' % imagename)
    	return False
	##  deploy to exist
    def deployToExist(imagename,cname,voloum):
    	port = Docker.getPorts(cname)[0]
    	Docker.killAndRmContainer(cname)
    	print('-> will reuse port %d ' % port)
    	Docker.deployToNew(imagename,port,cname,voloum)

	##  deploy to new
    def deployToNew(imagename,port,cname,voloum):
    	popenlist = ['docker','run','-d','--name']
    	popenlist.append(cname)
    	popenlist.append('-p')
    	popenlist.append(str(port) + ':9080')
    	popenlist.append('-v')
    	popenlist.append(voloum + ':/config/dropins/')
    	popenlist.append(imagename)
    	p = Popen(popenlist,stdout=PIPE,stderr=PIPE)
    	lines = p.stdout.readlines()
    	if len(lines) != 1:
    		print('Container create Failed ')
    		sys.exit(1)
    	for line in lines:
    		linestr = bytes.decode(line)
    		print('Container %s Build OK ' % Docker.getName(linestr))
    		
    # Kill and Remove container
    def killAndRmContainer(cname):
    	p = Popen(['docker','rm','-f',cname],stdout=PIPE,stderr=PIPE)
    	p.wait()

    # Get Container name inspect as json object 
    def getCinspect2JsonObj(cname):
    	result = os.popen('docker inspect ' + cname)
    	jsonstr = result.read().strip()[1:-1]
    	jsonobj = json.loads(jsonstr)
    	return jsonobj

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

	def ContainerFolder(folder):
		isexists = os.path.exists(folder)
		# os.path.isfile(path)
		if isexists:
			print('-> Folder OK ')
			return True
		else:
			result = os.mkdir(folder)
			print('-> Folder created')
			return True
		print('-> Folder check failed ')
		return False
    	
