def hole1()
	rotate	90.0;
	forward	53.999999999999886;
	rotate	-90.0;
	forward	17.999539999999797;
	rotate	-90.0;
	forward	53.999999999999886;
end
def hole2()
	rotate	90.0;
	forward	53.999999999999886;
	rotate	-90.0;
	forward	18.000130000000354;
	rotate	-90.0;
	forward	53.999999999999886;
end
def hole3()
	forward	17.99999999999909;
	rotate	-90.0;
	forward	53.999999999999886;
	rotate	-90.0;
	forward	17.99999999999909;
end
def main()
	hole hole1	at 1691.58565,30.0;
	hole hole2	at 52.0000399999999,30.0;
	hole hole3	at 672.0296500000004,83.99999999999989;
	connector 0,0,-18,-78;
	forward	1769.5913300000002;
	rotate	90.0;
	forward	114.0;
	rotate	90.0;
	forward	1769.5906800000002;
	connector 0,0,-18,78;
	rotate	90.0;
	forward	18.0;
	rotate	-90.0;
	forward	39.00068999999985;
	rotate	90.0;
	forward	77.99997000000008;
	rotate	90.0;
	forward	39.0000399999999;
end
