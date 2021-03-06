#!/usr/bin/env bash

project=proxy_server
config=gun.config.py

start() {
	status
	if [  $? = 1 ]; then
		echo "${project} is already running.."
		return 1
	fi

    mkdir -p log
    pip install virtualenv
    virtualenv .venv -p python2
    .venv/bin/pip install -U pip
    .venv/bin/pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
    .venv/bin/gunicorn -c ${config} wsgi:application

    echo "${project} start success..."
}

stop() {
	status
	if [ $? = 0 ]; then
	    echo "${project} not running.."
	    return 0
	fi

    ps -ef | grep -v grep | grep 'wsgi:application' | awk '{print $2}' | xargs kill -9
    rm -rf ${project}.pid

	echo "${project} stop success..."
	return 1
}

restart() {
    stop
    sleep 1
    start
}

status() {
    pid=`ps -ef | grep -v grep | grep 'wsgi:application' | awk '{print $2}'`
    if [ -z "${pid}" ]; then
        return 0
    fi
    echo ${pid}
    return 1
}

clean() {
    rm -rf log/*.log
    rm -rf log/*.pid
}

case "$1" in
	start|stop|restart|status|clean)
  		$1
		;;
	*)
		echo $"Usage: $0 {start|stop|status|restart|clean}"
		exit 1
esac
