# Da cancellare
import numpy as np
import matplotlib.pyplot as plt

def graphPlotter(graph):
	row, col = graph.get_dim()
	data = np.ones((row, col))*255

	for i in range(row):
		for j in range(col):
			node = j + i*col
			if graph.get_adj_list(node) == {}:
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
