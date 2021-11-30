def topplankhole()
	connector -5,0,-5 - 18, 80 + 10 + 10;
	forward	10;
	left	5;
	right	80;
	right	5;
	left	10;
	left	28;

	left	10;
	left	5;
	right	80;
	right	5;
	left	10;
#	left	28;
end


def main()
	hole topplankhole at 141,53;
	forward	382;
	left	20;
	left	5;
	right	10;
	connector 5,0,5 + 18,73;
	right	23;
	left	73;
	left	23;
	right	10;
	right	5;
	left	20;

	left	382;
	left	20;
	left	5;
	right	10;
	connector 5,0,5 + 18,73;
	right	23;
	left	73;
	left	23;
	right	10;
	right	5;

end
