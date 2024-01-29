package donkeykongobj;

public class Barrel extends GameObj{
	private int speed;
	//damage each barrel deals to Mario
	private int dmg;
	// 0 - going left, 1 - going right
	private boolean direction;
	
	public Barrel(int x, int y, int health,int speed, int dmg,boolean direction) {
		super(x, y, health);
		this.speed = speed;
		this.dmg = dmg;
		this.direction = direction;
	}

	//Getters and Setters
	public int getSpeed() {return this.speed;}
	public int getDmg() {return this.dmg;}
	public boolean getDirection() {return this.direction;}
	public void setSpeed(int newSpeed) {this.speed = newSpeed;}
	public void setDmg(int newDmg) {this.dmg = newDmg;}
	// setter for direction is just flipping from one direction to the other
	public void flip() {this.direction = !this.direction;}
	
	@Override
	public void update() {
		// TODO: Implement logic for updating barrels, rolling animation could be handled here
		
	}
	public void kill() {
		// TODO: Implement logic for killing barrels
		
	}

	@Override
	public void annouceSelf() {
		System.out.println("I'm a barrel");		
	}

	@Override
	public void interact(GameObj obj) {
		// TODO Implement how barrel interacts with other obj in game
		
	}

}
