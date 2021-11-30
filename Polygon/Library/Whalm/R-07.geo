def hole1()
	forward	17.99989999999991;
	rotate	90.0;
	forward	53.999999999999886;
	rotate	90.0;
	forward	17.99989999999991;
end
def hole2()
	rotate	90.0;
	forward	53.999999999999886;
	rotate	90.0;
	forward	17.99989000000005;
	rotate	90.0;
	forward	53.999999999999886;
end
def hole3()
	rotate	-90.0;
	forward	53.999999999999886;
	rotate	-90.0;
	forward	18.00000630000001;
	rotate	-90.0;
	forward	53.999999999999886;
end
def main()
	hole hole1	at -1161.3922200000002,-66.0;
	hole hole2	at -81.0003200000001,-66.0;
	hole hole3	at -1763.3923280000001,-12.000000000000114;
	rotate	90.0;
	forward	18.0;
	rotate	90.0;
	connector 0,0,-18,-54;
	forward	1833.39226;
	connector 0,0,-18,78;
	rotate	90.0;
	forward	18.0;
	rotate	-90.0;
	forward	39.000035239999995;
	rotate	90.0;
	forward	77.99997000000008;
	rotate	90.0;
	forward	39.000035239999995;
	rotate	-90.0;
	forward	18.000029999999924;
	rotate	90.0;
	connector 0,0,-18,-78;
	forward	1833.39226;
	rotate	90.0;
	forward	18.000029999999924;
	rotate	-90.0;
	connector 0,0,18,54;
	forward	53.999900000000025;
	rotate	-90.0;
	forward	18.000029999999924;
	rotate	90.0;
	forward	87.81277999999975;
	rotate	90.0;
	forward	114.0;
	rotate	90.0;
	forward	87.81277999999975;
	rotate	90.0;
	forward	18.0;
end
