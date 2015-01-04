
all: run

run: tollgate/main.py
	cd tollgate && python main.py -g
