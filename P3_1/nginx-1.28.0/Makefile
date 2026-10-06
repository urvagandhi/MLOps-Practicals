
default:	build

clean:
	rm -rf Makefile objs

.PHONY:	default clean

build:
	$(MAKE) -f objs/Makefile

install:
	$(MAKE) -f objs/Makefile install

modules:
	$(MAKE) -f objs/Makefile modules

upgrade:
	/home/urva/Downloads/Academics/Semester - 7/MLOps/Practicals/P3_1/nginx-1.28.0/sbin/nginx -t

	kill -USR2 `cat /home/urva/Downloads/Academics/Semester - 7/MLOps/Practicals/P3_1/nginx-1.28.0/logs/nginx.pid`
	sleep 1
	test -f /home/urva/Downloads/Academics/Semester - 7/MLOps/Practicals/P3_1/nginx-1.28.0/logs/nginx.pid.oldbin

	kill -QUIT `cat /home/urva/Downloads/Academics/Semester - 7/MLOps/Practicals/P3_1/nginx-1.28.0/logs/nginx.pid.oldbin`

.PHONY:	build install modules upgrade
