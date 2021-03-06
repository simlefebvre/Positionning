package fr.utbm.positionning.tp1.MainClass;

import java.util.Random;

public class Receiver {
	
	public Receiver() {
		
	}
	
	public Coordinate compute(Emmetor...emmetors) {
		double temp = 0.7;
		int nbiter = 99999;
		double pas = 0.95;
		double bestdist = 999999;
		
		Coordinate bestcoo =  new Coordinate(Math.random() * 10 - 5, Math.random()* 10 - 5, Math.random()* 10 - 5);
		
		while(temp > 0.0000007) {
			for(int i = 0; i<nbiter;i++) {
				
				Coordinate cootemp = new Coordinate(bestcoo.getX() + (Math.random() * 2 - 1), bestcoo.getX() + (Math.random() * 2 - 1),bestcoo.getX() + (Math.random() * 2 - 1));
				
				double distance = 0;
				
				for(Emmetor emmetor : emmetors) {
					distance = distance +Math.abs(emmetor.getCoo().distance(cootemp) - emmetor.getDist());
				}
				
				double delta = -bestdist + distance;
				
				
				if(delta<0) {
					bestdist = distance;
					bestcoo = cootemp;
				}else {
					if(Math.random() < Math.exp(-delta/temp)) {
						bestdist = distance;
						bestcoo = cootemp;
					}
				}
			}
			temp = pas*temp;
		}
		System.out.println(bestdist);
		return bestcoo;
	}
}
