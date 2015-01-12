for i in `seq 1 10`;
do
   #$temp=$RANDOM
   NOW=$(date +"%F")
   NOWT=$(date +"%T")
   BAK="/logs-example/$NOW"
   sudo python sch4.py >> logs-example/$NOW.$NOWT.log
   sleep 1
done    
