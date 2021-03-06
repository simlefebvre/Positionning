package fr.utbm.positionning.tp1.MainClass;

import java.util.ArrayList;
import java.util.List;

public class MainClass {

	public static void main(String[] args) {
		Emmetor E0 = new Emmetor(new Coordinate(0.5, 0.5, 0.5), 3);
		Emmetor E1 = new Emmetor(new Coordinate(4, 0, 0), 2);
		Emmetor E2 = new Emmetor(new Coordinate(4, 5, 5), 4.2);
		Emmetor E3 = new Emmetor(new Coordinate(3, 3, 3), 2.5);
		
		Receiver r = new Receiver();
		Coordinate coo = r.compute(E0,E1,E2,E3);
		
		System.out.println(coo.toString());
		
	}

}
