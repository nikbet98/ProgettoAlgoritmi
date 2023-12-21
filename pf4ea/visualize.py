#!/usr/bin/env python3Rect
from matplotlib.lines import Line2D
import yaml
import matplotlib

# matplotlib.use("Agg")
from matplotlib.patches import Circle, Rectangle, Arrow
from matplotlib.collections import PatchCollection
from utils import get_coordinates
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
import matplotlib.animation as manimation
import argparse
import math

COLORS = ["orange", "blue", "green","purple","cyan"]


class Animation:
    def __init__(self, grid, paths, solution):
        self.grid = grid
        rows,cols = grid.get_dim()
        obstacles = [get_coordinates(obstacle,cols) for obstacle in grid.get_obstacles()]
        self.solution = [get_coordinates(node,cols) for node in solution]
        self.myRobot_path = []
        self.paths = [[get_coordinates(node,cols) for node in path] for path in paths]
        self.robot_path = [get_coordinates(node,cols) for node in solution]
        
        aspect = rows / cols
        self.figure, self.axis = plt.subplots(figsize=(4 * aspect, 4))
        self.axis.set_aspect('equal')
        # plt.axis('off')

        # Lista di oggetti grafici
        self.patches = []
        # Lista di qualsiasi cosa possa essere disegnata su un asse
        self.artists = []
        self.agents = dict()
        self.agent_names = dict()
        self.myRobot = None
        self.myRobot_name = None

        # create boundary patch
        xmin = -0.5
        ymin = -0.5
        xmax = rows-0.5
        ymax = cols-0.5

        # self.ax.relim()

        # Imposto i limiti sugli assi x e y.
        self.draw_grid(rows,cols)
        
        # plt.axis('off')
        # self.ax.axis('tight')
        # self.ax.axis('off')
        
        # aggiungo un rettangolo alla lista degli oggetti grafici
        self.patches.append(
            Rectangle(
                (xmin-0.5, ymin-0.5),
                xmax - xmin,
                ymax - ymin,
                facecolor="none",
                edgecolor="red",
            )
        )
        for obstacle in obstacles:
            x, y = obstacle
            self.patches.append(
                Rectangle((x-0.5,y-0.5), 1,1, facecolor="black", edgecolor="black")
            )

        # Creo i percorsi degli agenti:
        self.T = 0
        # Disegna goal,start degli agenti e del myRobot
        x_goal, y_goal = self.robot_path[-1]
        x_init, y_init = self.robot_path[0]
        
        self.patches.append(
                Rectangle(
                    (x_goal-0.5 , y_goal-0.5),
                    1,
                    1,
                    facecolor=COLORS[4],
                    edgecolor="black",
                    alpha=0.5,
                )
        )
  
        self.myRobot = Circle(
                (x_init, y_init),
                0.35,
                facecolor=COLORS[4],
                edgecolor="black",
            )
        
        self.patches.append(self.myRobot)
        self.myRobot_name = self.axis.text(x_init, y_init, "😎")
        self.myRobot_name.set_horizontalalignment("center")
        self.myRobot_name.set_verticalalignment("center")
        self.artists.append(self.myRobot_name)

        x_coord_line, y_coord_line = zip(*self.robot_path)
        myRobot_path_line = Line2D(x_coord_line,y_coord_line,linewidth=3,linestyle='--')
        self.artists.append(myRobot_path_line)

        for agent_id, path in enumerate(self.paths):
            x_goal, y_goal = path[-1]
            self.patches.append(
                Rectangle(
                    (x_goal-0.5, y_goal-0.5),
                    1,
                    1,
                    facecolor=COLORS[0],
                    edgecolor="black",
                    alpha=0.5,
                )
            )

            x_start, y_start = path[0]
            self.agents[agent_id] = Circle(
                (x_start, y_start),
                0.35,
                facecolor=COLORS[0],
                edgecolor="black",
            )
            self.agents[agent_id].original_face_color = COLORS[0]
            self.patches.append(self.agents[agent_id])
            self.T = max(self.T, len(path))
            self.agent_names[agent_id] = self.axis.text(
                x_start, y_start, 'Agent {}'.format(agent_id)
          )
            self.agent_names[agent_id].set_horizontalalignment("center")
            self.agent_names[agent_id].set_verticalalignment("center")
            self.artists.append(self.agent_names[agent_id])

        # self.axes.set_axis_off()
        # self.figure.axes[0].set_visible(True)
        # self.figure.axes.get_yaxis().set_visible(True)

        self.figure.tight_layout()

        self.anim = animation.FuncAnimation(
            self.figure,
            self.animate_func,
            init_func=self.init_func,
            frames=len(self.robot_path)+1,
            interval=1000,
            blit=True,
            repeat_delay=3000,
        )

    def draw_grid(self, rows, cols):
        self.axis.set_xlim([-0.5, cols+0.5])
        self.axis.set_ylim([-0.5, rows+0.5])

        self.axis.set_xticks(np.arange(0, cols, 1))
        self.axis.set_yticks(np.arange(0, rows, 1))

        self.axis.grid(which='both', color='gray', linestyle='dotted', linewidth=0.5)

        plt.gca().invert_yaxis()  # Invert y axis
        plt.gca().xaxis.tick_top()  # Move x-axis to the top

    def save_as_video(self, file_name):
        self.anim.save(file_name, "ffmpeg", fps=1, dpi=200)
        # savefig_kwargs={"pad_inches": 0, "bbox_inches": "tight"})
    
    def save_as_image(self, file_name):
        self.figure.text(0.5, 0.02, "Istante di tempo iniziale: 0", ha='center')
        self.figure.savefig(file_name, bbox_inches='tight', pad_inches=1)
    def show(self):
        plt.show()

    def init_func(self):
        for p in self.patches:
            self.axis.add_patch(p)
        for a in self.artists:
            self.axis.add_artist(a)
        return self.patches + self.artists

    def animate_func(self, i):
        if i >= len(self.robot_path): self.anim.event_source.stop()
        pos = self.getState(i, self.robot_path)
        p = (pos[0], pos[1])
        self.myRobot.center = p
        self.myRobot_name.set_position(p)
        self.myRobot.set_facecolor(COLORS[4])
        

        for agent_id, path in enumerate(self.paths):
            pos = self.getState(i, path)
            p = (pos[0], pos[1])
            self.agents[agent_id].center = p
            self.agent_names[agent_id].set_position(p)

        # reset all colors
        for _, agent in self.agents.items():
            agent.set_facecolor(agent.original_face_color)

        # check drive-drive collisions
        # objects_array = [agent for _, agent in self.agents.items()] + [self.myRobot]
        # for i in range(0, len(objects_array)):
        #     for j in range(i + 1, len(objects_array)):
        #         d1 = objects_array[i]
        #         d2 = objects_array[j]
        #         pos1 = np.array(d1.center)
        #         pos2 = np.array(d2.center)
        #         if np.linalg.norm(pos1 - pos2) < 0.7:
        #             d1.set_facecolor("red")
        #             d2.set_facecolor("red")
        #             print("COLLISIONE tra oggetti!!! ({}, {})".format(i, j))

        return self.patches + self.artists
    
    # def draw_myRobot_path(self):
    #     # Disegna myRobot_path solo una volta, dopo che tutti gli altri elementi sono stati disegnati
    #     if len(self.myRobot_path) > 1:
    #         self.axis.plot(*zip(*self.myRobot_path), color=Colors[4])
  
    def getState(self, time, path):
      idx = 0
      while idx < len(path) and idx < time:
        idx += 1
      if idx == 0:
        x_pos, y_pos = path[0]
        return np.array([float(x_pos), float(y_pos)])
      elif idx < len(path):
        x_pos, y_pos = path[idx-1]
        x_pos_next, y_pos_next = path[idx]
        posLast = np.array([float(x_pos), float(y_pos)])
        posNext = np.array([float(x_pos_next), float(y_pos_next)])
      else:
        x_last_pos, y_last_pos = path[-1]
        x_pos, y_pos = path[idx-1]
        return np.array([float(x_last_pos), float(y_last_pos)])
      t = (time - (idx-1))
      pos = (posNext - posLast) * t + posLast
      return pos


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("map", help="input file containing map")
#     parser.add_argument("schedule", help="schedule for agents")
#     parser.add_argument(
#         "--video",
#         dest="video",
#         default=None,
#         help="output video file (or leave empty to show on screen)",
#     )
#     parser.add_argument("--speed", type=int, default=1, help="speedup-factor")
#     args = parser.parse_args()

#     with open(args.map) as map_file:
#         map = yaml.load(map_file, Loader=yaml.FullLoader)

#     with open(args.schedule) as states_file:
#         schedule = yaml.load(states_file, Loader=yaml.FullLoader)

#     # animation = Animation(map, schedule)
#     animation = Animation(grid, paths, solution)
#     if args.video:
#         animation.save(args.video, args.speed)
#     else:
#         animation.show()


# if __name__ == "__main__":
#     continue