package donkeykongobj;

//this class implement the Mario

class Mario extends GameObj{

	private int speed;
	private int size;
	private boolean hasWeapon;
	
	public Mario(int x, int y, int health, int speed, int size) {
		super(x, y,health);
		this.speed = speed;
		this.size = size;
		this.hasWeapon = false;
	}
	
	//setters and getters for Mario's private variables
	public int getSpeed() {return this.speed;}
	public int getSize() {return this.size;}
	public boolean getWeaponState() {return this.hasWeapon;}
	public void setSpeed(int newSpeed) {this.speed = newSpeed;}
	public void setSize(int newSize) {this.size = newSize;}
	public void setWeaponState(boolean newWeapon) {this.hasWeapon = newWeapon;}
	
	public void jump() {
		//TODO: add logic for Mario jumping
	}
	
	public void attack() {
		//TODO: add logic for Mario attacking
	}
	
	//the method for updating player position is probably different
	@Override
	public void update() {
		//TODO: add logic for updating Mario
	}
	//the method for killing Mario
	public void kill() {
		//TODO: add logic for killing Mario 
	}
	@Override
	public void annouceSelf() {
		System.out.println("I'm Mario!");		
	}

	@Override
	public void interact(GameObj obj) {
		// TODO single obj interaction
		
	}
	public void interact(Tools tool, GameObj target) {
		// TODO when Mario use the tool to interact with another obj. 
		try {
			// TODO change this logic based on requirements for tools
			tool.interact(target);
		}catch(Exception e) {
			System.out.println("Can't use this tool in this way");
		}
	}
	
}
