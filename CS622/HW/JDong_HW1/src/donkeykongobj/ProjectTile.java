package donkeykongobj;

public class ProjectTile extends Enemy{

	public ProjectTile(int x, int y, int health, int dmg, int speedX, int speedY, int accX, int accY,int size) {
		super(x, y, health, dmg, speedX, speedY, accX, accY,size);
	}
	@Override
	public void kill() {
		//Check for contact with other game obj, and update itself to be removed in the next update of the game
	}
}
