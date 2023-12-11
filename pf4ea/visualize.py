#!/usr/bin/env python3
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

Colors = ["orange", "blue", "green","red","cyan"]


class Animation:
    def __init__(self, grid, paths, solution):
        self.grid = grid
        rows,cols = grid.get_dim()
        obstacles = [get_coordinates(obstacle,cols) for obstacle in grid.get_obstacles()]
        self.solution = [get_coordinates(node,cols) for node in solution]
        self.myRobot_path = []
        self.paths = [[get_coordinates(node,cols) for node in path] for path in paths]
        self.robot_path = [get_coordinates(node,cols) for node in solution]
        
        # self.combined_schedule.update(self.schedule["schedule"])

        # aspect = map["map"]["dimensions"][0] / map["map"]["dimensions"][1]
        aspect = rows / cols
        # Creo una nuova figura fig
        self.figure = plt.figure(frameon=False, figsize=(4 * aspect, 4))
        # Aggiungo un asse alla figure
        self.axis = self.figure.add_subplot(111, aspect="equal")
        # self.axis.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
        # Regolo lo spazio tra i subplot
        self.figure.subplots_adjust(
            left=0, right=1, bottom=0, top=1, wspace=None, hspace=None
        )
        # self.ax.set_frame_on(False)

        # Lista usata per memorizzare oggetti grafici
        self.patches = []
        # In Matplotlib un artist è qualsiasi cosa che possa essere disegnata
        # su un asse.
        self.artists = []

        self.agents = dict()
        self.agent_names = dict()
        self.myRobot = None
        self.myRobot_name = None
        # create boundary patch
        xmin = -0.5
        ymin = -0.5
        xmax = rows - 0.5
        ymax = cols - 0.5

        # self.ax.relim()

        # Imposto i limiti sugli assi x e y.
        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)
        
        self.axis.set_xticks([])
        self.axis.set_yticks([])
        # plt.axis('off')
        # self.ax.axis('tight')
        # self.ax.axis('off')
        
        # aggiungo un rettangolo alla lista degli oggetti grafici
        self.patches.append(
            Rectangle(
                (xmin, ymin),
                xmax - xmin,
                ymax - ymin,
                facecolor="none",
                edgecolor="red",
            )
        )
        for obstacle in obstacles:
            x, y = obstacle
            self.patches.append(
                Rectangle((x - 0.5, y - 0.5), 1, 1, facecolor="black", edgecolor="black")
            )

        # Creo i percorsi degli agenti:
        self.T = 0
        # Disegno i goal e gli start degli agenti e del nostro automa
        x_goal, y_goal = self.robot_path[-1]
        x_init, y_init = self.robot_path[0]
        
        self.patches.append(
                Rectangle(
                    (x_goal - 0.25, y_goal - 0.25),
                    0.5,
                    0.5,
                    facecolor=Colors[3],
                    edgecolor="black",
                    alpha=0.5,
                )
        )
  
        self.myRobot = Circle(
                (x_init, y_init),
                0.3,
                facecolor=Colors[4],
                edgecolor="black",
            )
        
        self.patches.append(self.myRobot)
        self.myRobot_name = self.axis.text(x_init, y_init, "😎")
        self.myRobot_name.set_horizontalalignment("center")
        self.myRobot_name.set_verticalalignment("center")
        self.artists.append(self.myRobot_name)

        for agent_id, path in enumerate(self.paths):
            x_goal, y_goal = path[-1]
            self.patches.append(
                Rectangle(
                    (x_goal - 0.25, y_goal - 0.25),
                    0.5,
                    0.5,
                    facecolor=Colors[0],
                    edgecolor="black",
                    alpha=0.5,
                )
            )

            x_start, y_start = path[0]
            self.agents[agent_id] = Circle(
                (x_start, y_start),
                0.3,
                facecolor=Colors[0],
                edgecolor="black",
            )
            self.agents[agent_id].original_face_color = Colors[0]
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
            frames=int(self.T + 1) * 10,
            interval=100,
            blit=True,
        )

    def save(self, file_name, speed):
        self.anim.save(file_name, "ffmpeg", fps=10 * speed, dpi=200),
        # savefig_kwargs={"pad_inches": 0, "bbox_inches": "tight"})

    def show(self):
        plt.show()

    def init_func(self):
        for p in self.patches:
            self.axis.add_patch(p)
        for a in self.artists:
            self.axis.add_artist(a)
        return self.patches + self.artists

    def animate_func(self, i):
        pos = self.getState(i / 10, self.robot_path)
        p = (pos[0], pos[1])
        self.myRobot.center = p
        self.myRobot_name.set_position(p)
        self.myRobot.set_facecolor(Colors[3])
        
        self.myRobot_path.append(p)


        for agent_id, path in enumerate(self.paths):
            pos = self.getState(i / 10, path)
            p = (pos[0], pos[1])
            self.agents[agent_id].center = p
            self.agent_names[agent_id].set_position(p)

        # reset all colors
        for _, agent in self.agents.items():
            agent.set_facecolor(agent.original_face_color)

        # check drive-drive collisions
        objects_array = [agent for _, agent in self.agents.items()] + [self.myRobot]
        for i in range(0, len(objects_array)):
            for j in range(i + 1, len(objects_array)):
                d1 = objects_array[i]
                d2 = objects_array[j]
                pos1 = np.array(d1.center)
                pos2 = np.array(d2.center)
                if np.linalg.norm(pos1 - pos2) < 0.7:
                    d1.set_facecolor("red")
                    d2.set_facecolor("red")
                    print("COLLISIONE tra oggetti!!! ({}, {})".format(i, j))

        self.draw_myRobot_path()

        return self.patches + self.artists
    
    def draw_myRobot_path(self):
        # Disegna myRobot_path solo una volta, dopo che tutti gli altri elementi sono stati disegnati
        if len(self.myRobot_path) > 1:
            self.axis.plot(*zip(*self.myRobot_path), color=Colors[4])
  
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