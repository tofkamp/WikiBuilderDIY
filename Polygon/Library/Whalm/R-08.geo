def hole1()
	forward	18.000000000000455;
	rotate	-90.0;
	forward	53.999999999999886;
	rotate	-90.0;
	forward	18.000000000000455;
end
def hole2()
	rotate	-90.0;
	forward	53.999999999999886;
	rotate	90.0;
	forward	17.999550000000454;
	rotate	90.0;
	forward	53.999999999999886;
end
def main()
	hole hole1	at -923.4360000000006,65.99996999999996;
	hole hole2	at -109.00855000000047,65.99996999999996;
	rotate	90.0;
	forward	77.99997000000008;
	rotate	90.0;
	forward	39.0;
	rotate	-90.0;
	forward	18.0;
	rotate	90.0;
	connector 0,0,-18,-78;
	forward	965.4457900000007;
	rotate	90.0;
	forward	18.0;
	rotate	-90.0;
	connector 0,0,18,54;
	forward	53.9998999999998;
	rotate	-90.0;
	forward	18.0;
	rotate	90.0;
	forward	87.8128999999999;
	rotate	90.0;
	forward	114.0;
	rotate	90.0;
	forward	87.8128999999999;
	rotate	90.0;
	forward	18.000029999999924;
	rotate	-90.0;
	connector 0,0,18,54;
	forward	53.9998999999998;
	rotate	-90.0;
	forward	18.000029999999924;
	rotate	90.0;
	forward	965.4457900000007;
	connector 0,0,-18,78;
	rotate	90.0;
	forward	18.000029999999924;
end
