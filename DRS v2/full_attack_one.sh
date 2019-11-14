export MKL_NUM_THREADS=1

echo "Gen Training $1 $2"
python gen_training.py $1 $2 0 5  &>> log/$1_$2.log
echo "Gen Model $1 $2"
python gen_model.py $1 $2 0 5  &>> log/$1_$2.log
echo "Gen attack $1 $2"
python attack.py $1 $2 5 10   &>> log/$1_$2.log
rm -r training/$1_$2
echo "Done with $1 $2"
