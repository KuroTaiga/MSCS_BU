package donkeykongobj;

public class Enemy extends GameObj{
	static int counter = 0;
	
	private int id;
	private int dmg;
	private int speedX;
	private int speedY;
	//acceleration in either axis
	private int accX;
	private int accY;
	private int size;
	
	public Enemy(int x, int y,int health, int dmg,int speedX, int speedY,int accX, int accY, int size) {
		super(x, y,health);
		this.id = counter;
		this.dmg = dmg;
		this.speedX = speedX;
		this.speedY = speedY;
		this.accX = accX;
		this.accY = accY;
		this.size = size;
	}
	//record enemy id
	static int setId() {
		counter ++;
		return counter;
	}
	
	//getters and setters
	public int getDmg() {return this.dmg;}
	public int getSpeedX() {return this.speedX;}
	public int getSpeedY() {return this.speedY;}
	public int getAccX() {return this.accX;}
	public int getAccY() {return this.accY;}
	public int getSize() {return this.size;}
	
	public void setDmg(int newDmg) {this.dmg = newDmg;}
	
	
	@Override
	//Method to update enemy obj during each cycle
	public void update() {
	}

	@Override
	//Method to set enemy to be killed during next update
	public void kill() {		
	}

	@Override
	public void annouceSelf() {
		System.out.println("I'm enmey! No. "+this.id);
	}
	@Override
	public void interact(GameObj obj) {
		// TODO implement how emeny interact with other obj in game
		
	}

}
