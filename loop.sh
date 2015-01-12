HOSTS=6
TESTRUN=2
rm -rf logs-example/$HOSTS/
mkdir -p logs-example/$HOSTS

for i in `seq 1 $TESTRUN`;
do
   	#$temp=$RANDOM
   	NOW=$(date +"%F")
   	NOWT=$(date +"%T")
   	BAK="/logs-example/$NOW"
   	sudo python sch4.py >> logs-example/$HOSTS/$NOW.$NOWT.$i.log
   	sleep 1
done    

mv logs-example/log.* logs-example/$HOSTS/
chmod -R 777 logs-example/
