def hole1()
	connector 0,0,18,-100;
	rotate	180.0;
	forward	100.00014999999985;
	rotate	90.0;
	forward	18.000080000000025;
	rotate	90.0;
	forward	100.00014999999985;
end
def hole2()
	connector 0,0,18,-100;
	rotate	-90.0;
	forward	17.99976000000015;
	rotate	-90.0;
	forward	100.00014999999985;
	rotate	-90.0;
	forward	17.99976000000015;
end
def main()
	hole hole1	at 207.00001999999995,56.0;
	hole hole2	at 207.00001999999995,1124.0;
	rotate	90.0;
	forward	56.0;
	rotate	-90.0;
	forward	81.00011999999992;
	rotate	90.0;
	forward	74.9998599999999;
	rotate	-90.0;
	forward	17.999860000000126;
	rotate	90.0;
	connector 0,0,-18,100;
	forward	100.0001400000001;
	rotate	90.0;
	forward	17.999860000000126;
	rotate	-90.0;
	forward	100.00014999999985;
	rotate	-90.0;
	forward	17.999860000000126;
	rotate	90.0;
	connector 0,0,-18,100;
	forward	99.9998499999997;
	rotate	90.0;
	forward	17.999860000000126;
	rotate	-90.0;
	forward	100.00000000000045;
	rotate	-90.0;
	forward	17.999860000000126;
	rotate	90.0;
	connector 0,0,-18,100;
	forward	99.9998599999999;
	rotate	90.0;
	forward	17.999860000000126;
	rotate	-90.0;
	forward	99.99990000000025;
	rotate	-90.0;
	forward	17.999860000000126;
	rotate	90.0;
	connector 0,0,-18,100;
	forward	99.99990999999955;
	rotate	90.0;
	forward	17.999860000000126;
	rotate	-90.0;
	forward	100.00032999999985;
	rotate	-90.0;
	forward	17.999860000000126;
	rotate	90.0;
	connector 0,0,-18,100;
	forward	100.00000000000045;
	rotate	90.0;
	forward	17.999860000000126;
	rotate	-90.0;
	forward	75.00023999999985;
	rotate	90.0;
	forward	81.00011999999992;
	rotate	-90.0;
	forward	55.99976000000015;
	rotate	108.43494404827493;
	forward	37.94734140885364;
	rotate	-108.43494404827493;
	forward	30.999999999999545;
	rotate	-90.0;
	connector 0,0,75,37;
	forward	324.0001299999999;
	rotate	-90.0;
	forward	1199.9999999999995;
	rotate	-90.0;
	forward	324.0001299999999;
	connector 0,0,75,-37;

	rotate	-90.0;
	forward	30.999899999999798;
end
