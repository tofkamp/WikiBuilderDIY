def hole2()
	connector 0,0,-18,54;
	rotate	90.0;
	forward	18.000169999999912;
	rotate	-90.0;
	forward	54.0;
	rotate	-90.0;
	forward	18.000169999999912;
end
def hole3()
	connector 0,0,-18,54;
	rotate	90.0;
	forward	17.999880999999988;
	rotate	-90.0;
	forward	54.0;
	rotate	-90.0;
	forward	17.999880999999988;
end
def main()
#	color "#FEB109";
	hole hole2	at -84.0003000000006,840.999719;
	hole hole3	at -84.0003000000006,41.00000800000001;
	forward	17.999699999999393;
	rotate	90.0;
	connector 0,0,-18,100;
	forward	100.00002299999997;
	rotate	90.0;
	forward	17.999699999999393;
	rotate	-90.0;
	forward	699.99981;
	rotate	-90.0;
	forward	17.999699999999393;
	rotate	90.0;
	connector 0,0,-18,100;
	forward	99.99990600000012;
	rotate	90.0;
	forward	17.999699999999393;
	rotate	-90.0;
	forward	150.00032999999985;
	rotate	90.0;
	forward	114.0002999999997;
	rotate	90.0;
	forward	150.00032999999985;
	rotate	-90.0;
	forward	17.99967000000015;
	rotate	90.0;
	connector 0,0,-18,100;
	forward	99.99990600000012;
	rotate	90.0;
	forward	17.99967000000015;
	rotate	-90.0;
	forward	699.99981;
	rotate	-90.0;
	forward	17.99967000000015;
	rotate	90.0;
	connector 0,0,-18,100;
	forward	100.00002299999997;
	rotate	90.0;
	forward	17.99967000000015;
	rotate	-90.0;
###
	forward	286;
	left	114,66;
#	left	220;

end
