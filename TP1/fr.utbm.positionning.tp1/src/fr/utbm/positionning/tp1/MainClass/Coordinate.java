package fr.utbm.positionning.tp1.MainClass;

public class Coordinate {

	private double x;
	private double y;
	private double z;
	
	public Coordinate(double d, double e, double f) {
		this.x = d;
		this.y = e;
		this.z = f;
	}
	
	public double distance(Coordinate coo) {
		return Math.sqrt((Math.pow(this.x - coo.getX(),2) + Math.pow(this.y - coo.getY(),2) + Math.pow(this.z - coo.getZ(),2))); 
	}

	public double getX() {
		return x;
	}

	public double getY() {
		return y;
	}

	public double getZ() {
		return z;
	}

	@Override
	public String toString() {
		return "Coordinate [x=" + x + ", y=" + y + ", z=" + z + "]";
	}
	
}
