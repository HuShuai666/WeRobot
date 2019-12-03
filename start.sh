#!/usr/bin/env bash

SHELL_FOLDER=$(cd `dirname ${0}`; pwd)
PROCESS=run.py
PYTHON='python'

PORTS=(6060)

function help()
{
	echo ""
	echo "	Usage: sh ${SHELL_FOLDER}/`basename ${0}` <start | stop | restart | status>"
	echo ""
}

function check_process_exists()
{
    PROCESS_NUM=`ps aux | grep ${PYTHON} | grep $1 | grep -v grep | wc -l`
    if [ 0 -eq ${PROCESS_NUM} ]
    then
        return 0 # 不存在
    else
        return 1 # 存在
    fi
}

function start()
{
    for PORT in ${PORTS[@]};
    do
        check_process_exists ${PORT}
        if [ $? -eq 1 ];
        then
            echo "process is running on port: "${PORT}
        else
            ${PYTHON} ${PROCESS} ${PORT} >> /dev/null 2>&1 &
            echo "process start successed on port: "${PORT}
        fi
	done
}

function stop()
{
    for PORT in ${PORTS[@]};
    do
        check_process_exists ${PORT}
        if [ $? -eq 0 ];
        then
            echo "process already stopped on port: "${PORT}
        else
            kill -9 $(ps aux | grep ${PYTHON} | grep ${PORT} | grep -v grep |awk '{print $2}')
            echo "process stop successed on port: "${PORT}
        fi
	done
}

function status()
{
    for PORT in ${PORTS[@]};
    do
        check_process_exists ${PORT}
        if [ $? -eq 0 ];
        then
            echo "process already stopped on port: "${PORT}
        else
            echo "process is running on port: "${PORT}
        fi
	done
}


if [ $# -ne 1 ]
then
	help
	exit 0
fi

ACTION=$1
if [ ${ACTION} == "start" ];
then
	start
elif [ ${ACTION} == "stop" ];
then
	stop
elif [ ${ACTION} == "restart" ];
then
	stop
	start
elif [ ${ACTION} == "status" ];
then
	status
else
	help
fi


