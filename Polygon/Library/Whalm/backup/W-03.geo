def hole1()
	rotate	-90.0;
	forward	99.99990400000007;
	rotate	-90.0;
	forward	18.000190000000202;
	rotate	-90.0;
	forward	99.99990400000007;
end
def hole2()
	rotate	-90.0;
	forward	100.00014199999998;
	rotate	90.0;
	forward	18.000190000000202;
	rotate	90.0;
	forward	100.00014199999998;
end
def hole3()
	forward	99.99990000000003;
	rotate	-90.0;
	forward	18.000007000000096;
	rotate	-90.0;
	forward	99.99990000000003;
end
def hole4()
	rotate	90.0;
	forward	100.00003600000002;
	rotate	90.0;
	forward	18.000190000000202;
	rotate	90.0;
	forward	100.00003600000002;
end
def hole5()
	rotate	180.0;
	forward	99.99990000000003;
	rotate	-90.0;
	forward	17.999887;
	rotate	-90.0;
	forward	99.99990000000003;
end
def main()
	hole hole1	at -52.0,-475.00002399999994;
	hole hole2	at -70.0001900000002,-274.999858;
	hole hole3	at -200.00007000000005,-825.000047;
	hole hole4	at -52.0,-774.999988;
	hole hole5	at -100.00017000000003,-224.999785;
	rotate	-90.0;
	forward	1050.000088;
	rotate	-90.0;
	forward	300.0002099999999;
	rotate	-90.0;
	forward	1050.000088;
end
