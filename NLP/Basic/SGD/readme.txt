#-c:dataset(1:mnist, 2:covertype) -m:method(1:Adagrad, 2:Momentum)   -e:epochs   -b:batch_size   -a:learning rate -p:pemalate

D:
cd D:\AllCode\PyCode\NLP\Basic\SGD
activate tensorflow

#run
python run.py -c mnist -m adagrad -e 1000 -b 1000 -a 0.01 -p 0.1 >mni_ada_0.1.txt 2>&1 &
python run.py -c mnist -m momentum -e 1000 -b 1000 -a 0.1 -p 0.1  >mni_mom_0.1.txt 2>&1 &

#run
python run.py -c mnist -m momentum -e 200 -b 1000 -a 0.1 -p 0.01 >mni_mom_0.01.txt 2>&1 &
python run.py -c mnist -m momentum -e 200 -b 1000 -a 0.1 -p 1 >mni_ada_1.txt 2>&1 &

#run
python run.py -c covertype -m adagrad -e 1000 -b 1000 -a 0.01 -p 0.1   >cov_ada_0.1.txt 2>&1 &
python run.py -c covertype -m momentum -e 200 -b 1000 -a 0.1 -p 0.1   >cov_mom_0.1.txt 2>&1 &
python run.py -c covertype -m momentum -e 200 -b 1000 -a 0.1 -p 0.01 >cov_mom_0.01.txt 2>&1 &

python run.py -c covertype -m momentum -e 200 -b 1000 -a 0.1 -p 1     >cov_mom_1.txt 2>&1 &