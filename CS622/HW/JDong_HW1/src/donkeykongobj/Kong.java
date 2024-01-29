package donkeykongobj;

public class Kong extends GameObj{
	
	public Kong(int x, int y, int health) {
		super(x, y,health);
	}

	@Override
	public void kill() {
		// TODO Logic for adding DK to kill list
		
	}
	@Override
	public void update() {
		// TODO Logic for updating DK
		
	}
	@Override
	public void interact(GameObj obj) {
		// Kong should only be interacting with barrels, I think?
		// TODO: implement logic for how kong interact with other barrels
		System.out.println("DK throws");
		obj.annouceSelf();
	}

	@Override
	public void annouceSelf() {
		System.out.println("I'm the badest Kongs!");
		
	}

}
