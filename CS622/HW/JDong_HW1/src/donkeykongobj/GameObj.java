package donkeykongobj;

// overall generic class for all in game objects
// not making it public, only subclasses of GameObj shall be implemented in game
abstract class GameObj {
	
	//coordination of the object in game
	private int x,y,health;
	
	//Construction method 
	public GameObj(int x, int y,int health) {
		this.x = x;
		this.y = y;
		this.health = health;
	}
	
	//getter and setter for coordination
	public int getX() {
		return this.x;
	}
	public int getY() {
		return this.y;
	}
	public void setX(int newX) {
		//To-Do: perhaps we can return a boolean in the future, depending on the detailed implementation
		this.x = newX;
	}
	public void setY(int newY) {
		this.y = newY;
	}
	public void setHealth(int newHealth) {this.health = newHealth;}
	public int getHealth() {return this.health;}
	//method for losing health based on damage taken
	public void loseHealth(int dmg) {
		if (health>0) {
			health --;
		}
		else {
			this.kill();
		}
	}
	//method for gaining health
	public void gainHealth(int heal) {
		this.health = this.health+heal;
	}
	
	// method for checking collation
	public boolean detectCollation(GameObj obj) {
		if ((this.x == obj.getX()) && (this.y == obj.getY())){
			return true;
		}
		return false;
	}
	
	//generic update method to refresh the game objs
	// moving can be handled here
	public abstract void update();
	
	//everything should be able to be "killed" in game
	public abstract void kill();
	
	// method to announce basic info about the obj
	public abstract void annouceSelf(); 
	
	// method for interacting with other objs
	public abstract void interact(GameObj obj);
	
	
}