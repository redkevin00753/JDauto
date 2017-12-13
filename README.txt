Jenkins Docker auto build tools

find ${WORKSPACE} -name *-ear*.ear
find ${WORKSPACE} -name *.war

find /var/lib/jenkins/workspace/kevinAuto -name *-ear*.ear
find /var/lib/jenkins/workspace/kevinAuto -name *.war

pscript=/root/scripts/JDauto/main.py

if [ -z "${CONTAINER_NAME}" ] ; then
		echo "Container name is blank !" 
        exit 1
fi
sudo /opt/python3.6/bin/python3 $pscript ${DOCKER_IMAGE} ${CONTAINER_NAME}

if [ -d "/tmp/${CONTAINER_NAME}" ]; then
		sudo find ${WORKSPACE} -name *.war -exec cp {} /tmp/${CONTAINER_NAME} \;
        echo "Deploy Done !"
else
		echo "Volume folder not there !"
fi 
