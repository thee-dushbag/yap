CC=g++ -Wall -std=c++23

main: main.o libnodes.so
	${CC} -o $@ main.o -Wl,-rpath,"`pwd`" -L. -lnodes

main.o: main.cpp

libnodes.so: nodes.o visitors.o
	${CC} -o $@ -fPIC -shared $^

nodes.o: nodes.cpp
	${CC} -fPIC -c -o $@ $^

visitors.o: visitors.cpp
	${CC} -fPIC -c -o $@ $^

clean:
	rm -rfv *.o

clean_all: clean
	rm *.so
	rm main
