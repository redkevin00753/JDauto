# coding: utf-8
import os
import socket
import json
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
    	print("deploy to exist done")
    	# docker run -d --name kevineee -p 9001:9080 -v /var/lib/jenkins/workspace/kevinAuto/projects/epricer-tool/target/epricertools.war:/config/dropins/docker.war websphere-liberty
    	# commandstr = "docker run -d --name "
    	# commandstr += cname
    	# commandstr += " -p " + port + ":9080"
    	# commandstr += " -v " + war +":/config/dropins/docker.war"
    	# commandstr += " " + imagename

    	# result = os.popen('docker images ' + imagename + '|wc -l')
    	# # count = int(result.read().strip())
    	# # if count > 1:
    	# # 	print('image %s Found' % imagename)
    	# # 	return True
    	# # else:
    	# # 	print('image %s Not Found' % imagename)
    	# # 	return False   
	##  deploy to new
    def deployToNew(war,imagename,port,cname):
    	popenlist = ['docker','run','-d','--name']
    	popenlist.append(cname)
    	popenlist.append('-p')
    	popenlist.append(port + ':9080')
    	popenlist.append('-v')
    	popenlist.append(war + ':/config/dropins/docker.war')
    	popenlist.append(imagename)

    	p = Popen(popenlist,stdout=PIPE,stderr=PIPE)
    	lines = p.stdout.readlines()
    	if len(lines) not 1:
    		print('Container create Failed')
    		sys.exit(1)
    	for line in lines:
    		linestr = bytes.decode(line)
    		result = os.popen('docker inspect ' + linestr)
    		jsonstr = result.read().strip()[1:-1]
    		jsonobj = json.loads(jsonstr)
    		print('Container %s start OK' % getName(jsonobj))
 

    def getContainerNamesPorts():
    	p = Popen(['docker', 'ps', '-aq'],stdout=PIPE,stderr=PIPE)
    	lines = p.stdout.readlines()
    	nameList=[]
    	portList=[]
    	for line in lines:
    		linestr = bytes.decode(line)
    		result = os.popen('docker inspect ' + linestr)
    		jsonstr = result.read().strip()[1:-1]
    		jsonobj = json.loads(jsonstr)
    		nameList.append(Docker.getName(jsonobj))
    		portList.extend(Docker.getPorts(jsonobj))
    	portList.sort()
    	return nameList,portList
    def getName(json):
    	return json['Name'][1:]
    def getPorts(json):
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
    	
