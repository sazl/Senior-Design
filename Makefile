
all: convert random-trips run

convert: import/map.sumocfg import/typemap.xml import/run.sh
	cd import && ./run.sh

random-trips: tollgate/data/map.net.xml
	cd tollgate/data/ && \
	../../sumo/tools/trip/randomTrips.py -n map.net.xml -e 50 -l -o map.trips.xml && \
	duarouter -n map.net.xml -t map.trips.xml -o map.rou.xml --ignore-errors --begin 0 --end 50.0 --no-step-log

run: tollgate/main.py
	cd tollgate && python main.py -g
