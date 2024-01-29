package donkeykongobj;

// All the objs that can have other objs staying "on top" of, including ladders, floors etc.
public class Climbables extends GameObj{

	//Which picture the obj uses to represent itself
	private int renderPic;
		
	public Climbables(int x, int y, int health, int renderPic) {
		super(x, y, health);
		this.renderPic = renderPic;
	}
	@Override
	public void kill() {
		// TODO: Method to add it to the remove list
		
	}
	@Override
	public void update() {
		// TODO: Method to update it
		
	}
	public void interact(GameObj obj) {
		//overloading the method 
		//implement to bounce off or whatever the desired interaction would be for the game
		//such as changing speed an direction of objs, calling to add them to the kill list etc.
	}
	@Override
	public void annouceSelf() {
		// TODO Auto-generated method stub
		System.out.println("I'm a floor or ladder");
	}
	
}
