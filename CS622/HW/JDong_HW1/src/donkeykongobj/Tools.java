package donkeykongobj;

public class Tools extends GameObj{
	// health is how many times tools can be used
	public Tools(int x, int y, int health) {
		super(x, y, health);
	}

	@Override
	public void update() {
	}

	@Override
	public void kill() {
	}

	@Override
	public void annouceSelf() {
	}

	@Override
	public void interact(GameObj obj) {
		//TODO implement how tool interact with obj
	}
	
	

}
