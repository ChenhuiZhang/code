all: coredump crash

coredump: main.c
	gcc -ggdb -o coredump main.c -lcurl

crash: crash.c
	gcc -o crash crash.c

