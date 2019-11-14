PREFLAG = -fPIC -Ofast -mavx2 -funroll-loops -std=c++11
PREFLAGSO = -shared -Ofast -mavx2 -funroll-loops -std=c++11
OBJ = signlib.o

all: signlib

signlib: signlib.cpp
	g++ ${PREFLAG} -c signlib.cpp -o signlib.o
	g++ ${PREFLAGSO} signlib.o -o signlib.so
