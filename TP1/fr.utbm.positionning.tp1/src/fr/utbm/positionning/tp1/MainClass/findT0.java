package fr.utbm.positionning.tp1.MainClass;

import java.util.ArrayList;
import java.util.List;

public class findT0 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Emmetor E0 = new Emmetor(new Coordinate(0.5, 0.5, 0.5), 3);
		Emmetor E1 = new Emmetor(new Coordinate(4, 0, 0), 2);
		Emmetor E2 = new Emmetor(new Coordinate(4, 5, 5), 4.2);
		Emmetor E3 = new Emmetor(new Coordinate(3, 3, 3), 2.5);
		
		Emmetor emmetors[] = {E0,E1,E2,E3};
		
		List dists = new ArrayList<Double>();
		double sumbis = 0;
		for (int j = 0;j<1000;j++) {
			
			Coordinate init =  new Coordinate(Math.random() * 10 - 5, Math.random()* 10 - 5, Math.random()* 10 - 5);
			double initdist = 0;
			for(Emmetor emmetor : emmetors) {
				initdist = initdist +Math.abs(emmetor.getCoo().distance(init) - emmetor.getDist());
				}
			
			double sum = 0;
			for (int i = 0;i<9999999;i++) {
				Coordinate newCoo = new Coordinate(init.getX() + (Math.random() * 2 - 1), init.getX() + (Math.random() * 2 - 1),init.getX() + (Math.random() * 2 - 1));
				
				double distance = 0;
				
				for(Emmetor emmetor : emmetors) {
					distance = distance +Math.abs(emmetor.getCoo().distance(newCoo) - emmetor.getDist());
				}
				
				sum = sum + (initdist - distance);
			}
			sumbis = sumbis + sum/9999999;
			System.out.println(j + " ; " + sumbis);
			sum = 0;
		}
		System.out.println(sumbis);
		
	}

}
