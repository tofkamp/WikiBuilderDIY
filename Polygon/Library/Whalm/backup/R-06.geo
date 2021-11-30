def hole1()
	forward	18.00000630000001;
	rotate	90.0;
	forward	53.999999999999886;
	rotate	90.0;
	forward	18.00000630000001;
end
def hole2()
	rotate	180.0;
	forward	17.99989000000005;
	rotate	-90.0;
	forward	53.999999999999886;
	rotate	-90.0;
	forward	17.99989000000005;
end
def hole3()
	rotate	90.0;
	forward	53.999999999999886;
	rotate	-90.0;
	forward	17.99989999999991;
	rotate	-90.0;
	forward	53.999999999999886;
end
def main()
	hole hole1	at -1760.3919543000002,30.0;
	hole hole2	at -59.99994000000015,30.0;
	hole hole3	at -1140.3918400000002,30.0;
	rotate	180.0;
	forward	1812.3918800000001;
	rotate	-90.0;
	forward	18.000029999999924;
	rotate	90.0;
	forward	39.000035239999995;
	rotate	-90.0;
	forward	77.99997000000008;
	rotate	-90.0;
	forward	39.000035239999995;
	rotate	90.0;
	forward	18.0;
	rotate	-90.0;
	forward	1812.3918800000001;
end
