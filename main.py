# coding: utf-8
import sys
from settings import Config
from utils import Docker,OS


def main():
	if not checkArgs(sys.argv):
		sys.exit(1)
	# get params
	IMAGE_NAME = sys.argv[1]
	CONTAINER_NAME = sys.argv[2]
	VOLUME_FOLDER = VOLUME_BASE + CONTAINER_NAME

	namelist,portlist = Docker.getContainerNamesPorts()
	if CONTAINER_NAME in namelist:
		print("Will deploy to exist container %s" % CONTAINER_NAME)
		if Docker.checkImageName(IMAGE_NAME) and OS.ContainerFolder(VOLUME_FOLDER):
			Docker.deployToExist(IMAGE_NAME,CONTAINER_NAME,VOLUME_FOLDER)
		else:
			sys.exit(1)
	else:
		print("Will deploy to new container %s" % CONTAINER_NAME)
		if Docker.checkImageName(IMAGE_NAME) and OS.ContainerFolder(VOLUME_FOLDER):
			Docker.deployToNew(IMAGE_NAME,getAvailablePort(portlist),CONTAINER_NAME,VOLUME_FOLDER)
		else:
			sys.exit(1)
	print("Container Create done , pelase put Xars to Volume")


def getAvailablePort(portlist):
	print("-> check ports from %d to %d" % (Config.FROM_PORT,Config.TO_PORT))
	for port in range(Config.FROM_PORT,Config.TO_PORT):
		if port not in portlist:
			if OS.IsNotUse(port):
				print('-> Got one available Port %d' % port)
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
    print("******************************************************* ")
    print("*              DOCKER python for Jekin                * ")
    print("*                      (c) 2017 - KEVIN               * ")
    print("******************************************************* ")
    main()
