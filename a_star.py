import math

"""
    Find the shortest path from one map node to another.

    The below uses A* search to implement a "Google-maps" style route planning algorithm

    Assistance from the following resources:
    - Udacity Data Structures and Algorithms course material
    - https://www.geeksforgeeks.org/a-search-algorithm/
    - https://www.w3schools.com/python/trypython.asp?filename=demo_list_copy2

    """

class heap_node:
    #things you need to track for frontier entries

    def __init__(self, distance = float("inf"), intersection = None, path = []):
        self.distance = distance   # sum of distance up to point
        self.int_num = intersection   # intersection num up to point
        self.path = path    # list of path intersections up to point

class minheap:

    def __init__(self,size = 10):
        self.cbt = [None for _ in range(size)]
        self.next_idx = 0

    def insert(self, distance = float("inf"), intersection = None, path = []):
        print("in insert",self.print_heap(), "size:", self.next_idx)
        if self.is_empty():
            temp_node = heap_node(distance, intersection, path)
            self.cbt.append(temp_node)
            self.next_idx += 1
            print("should have added 1")

        else:
            self.cbt[self.next_idx] = heap_node(distance, intersection, path)

            self.up_heapify()

            self.next_idx += 1


        if self.next_idx >= len(self.cbt):
            temp = self.cbt
            self.cbt = [None for _ in range(2*len(self.cbt))]

            for x in range(self.next_idx):
                self.cbt[x] = temp[x]

        print("post insert",self.print_heap(), "size:", self.next_idx)
        for x in self.print_heap():
            print("u- ", x)


    def remove(self):
        print("in remove, size:", self.size(), "to rem", self.cbt[0].int_num)
        if self.is_empty():
            return None

        if self.size() == 1:
            print("removing size 1")
            to_remove = self.cbt[0]
            self.cbt = []
            self.next_idx -= 1

        else:
            self.next_idx -= 1

            to_remove = self.cbt[0]
            last_elem = self.cbt[self.next_idx]

            self.cbt[0] = last_elem
            self.cbt[self.next_idx] = to_remove

            print("removing", to_remove.int_num)
            self.down_heapify()

        for x in self.print_heap():
            print("d- ", x)

        return to_remove

    def size(self):
        return self.next_idx

    def is_empty(self):
        return self.size() == 0

    def up_heapify(self):
        if self.is_empty():
            return

        child_idx = self.next_idx

        while child_idx >= 1:
            print("in upheap while")
            parent_idx = (child_idx - 1) // 2
            parent_elem = self.cbt[parent_idx].distance
            child_elem = self.cbt[child_idx].distance

            print("up heap nums, parent[",parent_idx, self.cbt[parent_idx].int_num, parent_elem, "]  child: [", child_idx, self.cbt[child_idx].int_num, child_elem,"]")
            if parent_elem > child_elem:
                parent_node_hold = self.cbt[parent_idx]
                child_node_hold = self.cbt[child_idx]
                self.cbt[parent_idx] = child_node_hold
                self.cbt[child_idx] = parent_node_hold

                child_idx = parent_idx
            else:
                break

    def down_heapify(self):
        print("start down heap")
        parent_idx = 0

        while parent_idx < self.next_idx:
            print("in down heap while")
            left_child_idx = 2 * parent_idx + 1
            right_child_idx = 2 * parent_idx + 2

            parent = self.cbt[parent_idx]
            left_child = None
            right_child = None

            min_elem = parent.distance
            print("dh min elem",min_elem)

            if left_child_idx < self.next_idx:
                left_child = self.cbt[left_child_idx]

            if right_child_idx < self.next_idx:
                right_child = self.cbt[right_child_idx]

            if left_child is not None:
                min_elem = min(parent.distance, left_child.distance)

            if right_child is not None:
                min_elem = min(right_child.distance, min_elem)

            if min_elem == parent.distance:
                return
            print("min elem in Down Heap", parent_idx, self.next_idx, min_elem)

            if min_elem == left_child.distance and left_child is not None:
                print("left", min_elem)
                self.cbt[left_child_idx] = parent
                self.cbt[parent_idx] = left_child
                parent_idx = left_child_idx

            elif right_child is not None and min_elem == right_child.distance:
                print("right", min_elem)
                self.cbt[right_child_idx] = parent
                self.cbt[parent_idx] = right_child
                parent_idx = right_child_idx

    def get_minimum(self):
        if self.size == 0:
            return None
        return self.cbt[0].distance

    def print_heap(self):
        lyst = []
        for i in self.cbt:
            if self.size == 0:
                lyst = []
            elif i is None:
                lyst.append(None)
            else:
                lyst.append([i.int_num, i.distance, i.path])

        return lyst


def shortest_path(M, start, goal):
    explored = set()
    frontier = minheap(0)

    #use M.intersections for points
    #use M.roads for edges

    #things you need to track for frontier
        # intersection num up to point
        # sum of distance up to point
        # list of path intersections up to point

    start_hold = float("inf")
    frontier.insert(start_hold, start,[start])

    while frontier.size() > 0:
        print("\n-------start main while-------")

        print("frontier:", frontier.print_heap())
        print("explored:", explored)

        node = frontier.remove()      # 'pop'ing out node
        print("removed node dist:", node.distance)
        explored.add(node.int_num)    # marking as visited

        # if most recently removed min distance's starting node is == goal, return
        if node.int_num == goal:
            return node.path

        for child_int_num in M.roads[node.int_num]:
            if child_int_num not in explored:
                print("\n---in for, node:", node.int_num, "child", child_int_num)

                # Update distance
                if node.distance == float("inf"):
                    temp_dist = 0
                else:
                    temp_dist = node.distance
                f_value = temp_dist + f(M.intersections[node.int_num],
                                      M.intersections[child_int_num])
                print("f",f_value)

                h_value = h(M.intersections[child_int_num], M.intersections[goal])

                print("h",h_value)

                new_dist = f_value + h_value
                print("node, child, dist", node.int_num, child_int_num, new_dist)


                # Update intersection number
                new_int_num = child_int_num

                # Update path list
                new_path = []
                new_path = list(node.path)
                new_path.append(child_int_num)
                print("node path",node.path)

                frontier.insert(new_dist, new_int_num, new_path)

            print("frontier2:", frontier.print_heap())
            print("explored2:", explored)

    print("shortest path called")
    return

def f(current, target):

    f = math.sqrt(((target[0] - current[0])**2) + ((target[1] - current[1])**2))

    return f

def h(current, goal):
    # Function to return estimated distance using euclidean distance heuristic
    # created with help from https://www.geeksforgeeks.org/a-search-algorithm/

    h = math.sqrt(((goal[0] - current[0])**2) + ((goal[1] - current[1])**2))

    return h
