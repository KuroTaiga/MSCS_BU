package donkeykongobj;

import java.util.List;

class Map {
    private Mario mario;
    private Enemy enemy;
    private List<Climbables> obstacles;

    public Map() {
        // Initialize the map, player, enemy, and obstacles
    }

    // Method to update the entire game state
    public void update() {
    	mario.update();
        enemy.update();
        for (Climbables obstacle : obstacles) {
            obstacle.update();
        }
    }

    // Overloaded method example: adding obstacles
    public void addObstacle(Climbables obstacle) {
        obstacles.add(obstacle);
    }

    // Overloading the addObstacle method to add multiple obstacles at once
    public void addObstacle(List<Climbables> newObstacles) {
        obstacles.addAll(newObstacles);
    }
}