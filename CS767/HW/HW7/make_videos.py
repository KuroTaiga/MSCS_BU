import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle


def create_animation(filename, speed, size, shape, color):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')  # Turn off the axis
    
    if shape == 'ball':
        moving_item = Circle((1, 5), size, color=color)
    else:
        moving_item = Rectangle((9, 9), size, size, color=color)
    ax.add_patch(moving_item)

    def update(frame):
        x_new = 1+np.mod(frame * speed,9)
        if shape == 'ball':
            moving_item.center = (x_new, 5)
        else:
            moving_item.set_x(10-x_new)
            moving_item.set_y(10-x_new)
            moving_item.set_height(size+frame*speed*0.6)
            moving_item.set_width(size+frame*speed*0.6)
        return moving_item,

    ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 900), blit=True)
    ani.save(filename, writer='pillow', fps=30)
    plt.close()

if __name__ == "__main__":
    create_animation('./fastsmallball.gif', 0.05, 1, 'ball', 'blue')
    create_animation('./slowbigball.gif', 0.01, 1.5, 'ball', 'blue')
    create_animation('./different.gif', 0.025, 5, 'rect', 'red')
