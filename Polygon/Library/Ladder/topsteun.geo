def c73()
	forward	28;
	left	10;
	left	5;
	right	73 - 20;
	right	5;
	left	10;
	left	28;
	left	10;
	left	5;
	right	73 - 20;
	right	5;
#	left	10;
end

def main()
	hole	c73	at 16,20;
	hole	c73	at 16,425;

	forward	60;
	left	73;
	right	10;
	right	5;
	left	20;
	left	382;
	left	20;
	left	5;
	right	10;
	connector 5,0,5 + 18,60;
	connector 5 + 18, (60 - 18) / 2, 5 + 18 + 30, (60 - 18) / 2 + 18;
	right	73;

	left	60;
	left	73;
	right	10;
	right	5;
	left	27;
	left	141;
	connector 0,0,18,100;
	right	18;
	left	100;
	left	18;
	right	141;
	left	27;
	left	5;
	right	10;
	connector 5,0,5 + 18,60;
	connector 5 + 18, (60 - 18) / 2, 5 + 18 + 30, (60 - 18) / 2 + 18;
end
