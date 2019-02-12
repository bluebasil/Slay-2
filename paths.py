import const
import math

def find(start,end):
	result = A_Star(start,end)
	#print(result,flush = True)
	out = []
	for t in result:
		out.append(t.tid)
	return out

def test():
	paths = [[start]]
	while len(paths[0]) < 100:
		#print(f"depth {len(paths[0])}",flush = True)
		paths = breth_first(paths,end)
		#print(paths,flush = True)
		for p in paths:
			if p[-1] == end:
				#print("DONE",flush = True)
				out = []
				for t in p:
					out.append(t.tid)
				return out
	return []

def breth_first(start_list,end):
	next_layer = []
	for s in start_list:
		for t in s[-1].adjacent.values():
			#print(s[-1].adjacent,flush = True)
			if t != None:
				#if t == end:
					#print("FOUDN IT",flush = True)
				out = s.copy()
				out.append(t)
				next_layer.append(out)
	return next_layer

def heuristic_cost_estimate(start, goal):
	x = abs(start.x-goal.x)
	y = abs(start.y-goal.y)
	x = min(x,const.BOARD_WIDTH-x)
	y = min(y,const.BOARD_HEIGHT-y)
	return math.sqrt(x**2+y**2)

def reconstruct_path(cameFrom, current):
	total_path = [current]
	while current in cameFrom:
		current = cameFrom[current]
		total_path.append(current)
	return total_path

def A_Star(start, goal):
	# The set of nodes already evaluated
	closedSet = set()

	# The set of currently discovered nodes that are not evaluated yet.
	# Initially, only the start node is known.
	openSet = set([start])

	# For each node, which node it can most efficiently be reached from.
	# If a node can be reached from many nodes, cameFrom will eventually contain the
	# most efficient previous step.
	cameFrom = {}

	# For each node, the cost of getting from the start node to that node.
	gScore = {}
	#map with default value of Infinity

	# The cost of going from start to start is zero.
	gScore[start] = 0

	# For each node, the total cost of getting from the start node to the goal
	# by passing by that node. That value is partly known, partly heuristic.
	fScore = {}
	#= map with default value of Infinity

	# For the first node, that value is completely heuristic.
	fScore[start] = heuristic_cost_estimate(start, goal)

	while len(openSet) > 0:
		lowest_val = math.inf
		current = None
		for n in openSet:
			if fScore[n] < lowest_val:
				lowest_val = fScore[n]
				current = n

		#current = the node in openSet having the lowest fScore[] value
		
		if current == goal:
			return reconstruct_path(cameFrom, current)

		if current not in openSet:
			print("No route found (1)",flush = True)
			return []
		openSet.remove(current)
		closedSet.add(current)

		for neighbor in current.adjacent.values():
			if neighbor == None:
				continue
			if neighbor in closedSet:
				continue		# Ignore the neighbor which is already evaluated.

			# The distance from start to a neighbor
			tentative_gScore = gScore[current] + neighbor.terrain.movement_cost#dist_between(current, neighbor)

			if not neighbor in openSet:	# Discover a new node
				openSet.add(neighbor)
			elif tentative_gScore >= gScore[neighbor]:
				continue

			# This path is the best until now. Record it!
			cameFrom[neighbor] = current
			gScore[neighbor] = tentative_gScore
			fScore[neighbor] = gScore[neighbor] + heuristic_cost_estimate(neighbor, goal)

	print("No route found (2)",flush = True)
	return []