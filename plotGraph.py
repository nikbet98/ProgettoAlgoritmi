import matplotlib.pyplot as plt
import numpy as np


def graphPlotter(graph):
	row, col = graph.getDim()

	n = row*col
	data = np.ones((row, col))*255

	for i in range(row):
		for j in range(col):
			node = (j+1) + i*col
			if graph.getAdjList(node) == {}:
				data[i,j] = 0
	
	fig, ax = plt.subplots()
	ax.imshow(data)

	# draw gridlines
	ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
	ax.set_xticks(np.arange(-.5, col, 1));
	ax.set_yticks(np.arange(-.5, row, 1));
	ax.xaxis.set_ticklabels([])
	ax.yaxis.set_ticklabels([])
	plt.show()	
