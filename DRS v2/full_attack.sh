python gen_training.py $1 $2 0 10 
python gen_model.py $1 $2 0 10
python attack.py $1 $2 10 20
