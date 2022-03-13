package fr.utbm.positionning.tp1.MainClass;

public class Emmetor {
	
	private Coordinate coo;
	private double dist;
	
	public Emmetor(Coordinate coo,double d) {
		this.coo = coo;
		this.dist = d;
	}

	public Coordinate getCoo() {
		return coo;
	}

	public double getDist() {
		return dist;
	}
	
	

}
