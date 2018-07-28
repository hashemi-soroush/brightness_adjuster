#!/bin/bash

src_file=`readlink -f $0`
src_dir=`dirname $src_file`
cd $src_dir

pid_file_path=".pid"

case "${1}" in
	"install" ) 
		sudo apt-get install ffmpeg python3-pip
		sudo python3 -m pip install -r requirements.txt
		;;
	"on" )
		if [ ! -e "${pid_file_path}" ] ; then
			python3 brightness_adjuster.py 2> /dev/null &
			echo $! > "${pid_file_path}"
		fi
		;;
	"off" )
		if [ -e "${pid_file_path}" ] ; then
			pid=`cat "${pid_file_path}"`
			kill ${pid}
			rm "${pid_file_path}"
		fi
		;;
	* )
		echo "wrong command. try: on, off, install"
		echo "ex: brightness_adjuster_ui on"
		;;
esac
