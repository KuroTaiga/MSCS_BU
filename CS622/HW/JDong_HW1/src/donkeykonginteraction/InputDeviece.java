package donkeykonginteraction;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;


public class InputDeviece implements KeyListener {
	private boolean left,right,up,down,click;
	private int cursorX, cursorY;
	public void setInput(int portNumber) {
		//TODO set input device. I'm not sure at this point what type of parameter we want to use
		// portNumber is just a place holder for which device to use
		System.out.println("device port: "+portNumber);
	}
	
	public void updateInput() {
		//TODO update the left, right, up, down, click, cursorX and cursorY based on the input device
		//not quite sure how we implement it
	}

	@Override
	public void keyTyped(KeyEvent e) {
		// TODO probably a useful method
	}

	@Override
	public void keyPressed(KeyEvent e) {
		// TODO probably a useful method
	}

	@Override
	public void keyReleased(KeyEvent e) {
		// TODO probably a useful method
	}
}
