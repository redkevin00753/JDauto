# coding: utf-8
import sys
from settings import Config
from utils import Docker,OS


def main():
	if not checkArgs(sys.argv):
		sys.exit(1)
	# get params
	WAR_PATH = sys.argv[1]
	IMAGE_NAME = sys.argv[2]
	CONTAINER_NAME = sys.argv[3]

	namelist,portlist = Docker.getContainerNamesPorts()
	print('Exists Container names : %s ' % namelist)
	print('Exists Container ports : %s ' % portlist)
	if CONTAINER_NAME in namelist:
		if not OS.IsWarThere(WAR_PATH):
			sys.exit(1)
		Docker.deployToExist(WAR_PATH,CONTAINER_NAME)
		sys.exit(0)
	else:
		if Docker.checkImageNames(IMAGE_NAME) and OS.IsWarThere(WAR_PATH):
			Docker.deployToNew(WAR_PATH,IMAGE_NAME,getAvailablePort(),CONTAINER_NAME)
		else:
			sys.exit(1)

def getAvailablePort():
	print("check port from " + str(Config.FROM_PORT) + " to " + str(Config.TO_PORT))
	for port in range(Config.FROM_PORT,Config.TO_PORT):
		if port not in portlist:
			if OS.IsNotUse(port):
				return(port)
				break
	print("can not get a available port !!!")
	sys.exit(0)

def checkArgs(list):
	if len(list) == 4:
		return True
	else:
		print("Params Wrong")
		return False

if __name__ == '__main__':
    print("*******************************************************")
    print("*              DOCKER python for Jekin                *")
    print("*                      (c) 2017 - KEVIN               *")
    print("*******************************************************")
    main()