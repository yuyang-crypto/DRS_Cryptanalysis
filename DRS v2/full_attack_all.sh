 
for i in 16 24 32 48 64 80 96 112 128 192 256 512;
do
	bash full_attack_core.sh $i 10 &
	bash full_attack_core.sh $i 11 &
done
