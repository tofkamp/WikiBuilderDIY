def c60()
	connector 0,5,-60,23;
#	connector 5,0,23,60;
	forward	28;
	left	10;
	left	5;
	right	40;
	right	5;
	left	10;
	left	28;
	left	10;
	left	5;
	right	40;
	right	5;
end

def ahole()
	forward	253;
	left	512,-90;
	left	73;
end

def tredegat(delta)
    	left	58.5 - delta;
    	left	5;
    	right	10;
    	right	28;
    	right	10;
    	right	5;
	connector 10,0, -60,18;
#	connector 0,10, -18,-60;
    	left	58.5 + delta;
end

def main()
	hole ahole 	at 226,418;
	hole c60 	at 339,338;
	hole c60	at 339,987;
	hole c60	at 339,1509;

	forward	152;
	left	318,56;
	right	289;
	right	318,-56;
	left	152;
	left	318,-56;
	tredegat(-1.5);
	left	243,-43;
	tredegat(-1.5);
	left	243,-43;
	tredegat(-1.5);
	left	243,-43;
	tredegat(-1.5);
	left	243,-43;
	tredegat(-1.5);
	left	244,-43;
	left	30;
	connector 0,0, -18,73;
	left	23;
	right	10;
	right	5;
	left	53;
	left	5;
	right	10;
	right	23;
	left	30;
	left	244,43;
	tredegat(1.5);
	left	243,43;
	tredegat(1.5);
	left	243,43;
	tredegat(1.5);
	left	243,43;
	tredegat(1.5);
	left	243,43;
	tredegat(1.5);

end