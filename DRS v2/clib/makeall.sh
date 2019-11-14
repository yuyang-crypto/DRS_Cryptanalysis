rm *.o *.so
 
for i in 16 24 32 48 64 80 96 112 128 160 192 256 512;
do
	g++ -fPIC -Ofast -mavx2 -funroll-loops -std=c++11 -c -Dnnn=$i signlib.cpp -o signlib$i.o
	g++ -shared -Ofast -mavx2 -funroll-loops -std=c++11 signlib$i.o -o signlib$i.so	
done
