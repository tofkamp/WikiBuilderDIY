def hole1()
	forward	18.00000000000091;
	rotate	-90.0;
	forward	53.999999999999886;
	rotate	-90.0;
	forward	18.00000000000091;
end
def main()
	hole hole1	at -1000.5000000000018,53.999999999999886;
	forward	18.0;
	rotate	90.0;
	connector 0,0,-18,54;
	forward	53.999999999999886;
	rotate	90.0;
	forward	18.0;
	rotate	-90.0;
	forward	30.000000000000114;
	rotate	90.0;
	forward	1710.000000000001;
	rotate	90.0;
	forward	30.000000000000114;
	rotate	90.0;
	forward	18.0;
	rotate	-90.0;
	connector 0,0,18,54;
	forward	53.999999999999886;
	rotate	-90.0;
	forward	18.0;
	rotate	90.0;
	forward	30.0;
	rotate	90.0;
	forward	1428.001000000001;
	rotate	90.0;
	connector 0,0,18,57;
	forward	57.00006399999995;
	rotate	-90.0;
	forward	17.998999999999796;
	rotate	-90.0;
	forward	57.00006399999995;
	rotate	90.0;
	forward	264.0;
end
