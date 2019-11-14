expo=$2

for i in {0..10}; do
	bash full_attack_one.sh $1 $expo
	expo=$((expo+2))
done
