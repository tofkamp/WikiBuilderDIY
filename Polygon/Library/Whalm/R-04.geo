def hole1()
	rotate	180.0;
	forward	18.000000000000114;
	rotate	90.0;
	forward	53.999999999999886;
	rotate	90.0;
	forward	18.000000000000114;
end
def hole2()
	rotate	90.0;
	forward	53.999999999999886;
	rotate	90.0;
	forward	18.000006900000002;
	rotate	90.0;
	forward	53.999999999999886;
end
def main()
	hole hole1	at -808.00011,65.99996999999996;
	hole hole2	at -52.00004609999999,11.999970000000076;
	connector 0,0,18,78;
	forward	39.000034;
	rotate	90.0;
	forward	77.99997000000008;
	rotate	90.0;
	forward	39.000034;
	rotate	-90.0;
	forward	18.0;
	rotate	90.0;
	connector 0,0,-18,-78;
	forward	1090.00003;
	rotate	90.0;
	forward	30.000000000000114;
	rotate	-90.0;
	forward	18.000009999999975;
	rotate	90.0;
	connector 0,0,-18,54;
	forward	53.999999999999886;
	rotate	90.0;
	forward	18.000009999999975;
	rotate	-90.0;
	forward	30.0;
	rotate	90.0;
	forward	1090.00003;
end
