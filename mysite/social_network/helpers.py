from social_network.models import User, FriendList
from collections import deque
from typing import List


def get_friends_ids(pk):
    """Function return the list of friends ids, related to the specified user"""
    user = User.objects.filter(id=pk).first()
    if user:
        friends = user.friends.values_list("id", flat=True)
        return friends
    return []


def get_list_of_ids(start_id: int, end_id: int, parents_dict: dict) -> List[int]:
    """Function restores the order of ids based on the parents relationships,
    passed in parents_dict"""
    result_ids = []
    current_id = end_id
    while True:
        parent_id = parents_dict.get(current_id)
        if parent_id == start_id:
            break
        result_ids.insert(0, parent_id)
        current_id = parent_id
    return result_ids


def shortest_path_search(start_vertex: int, end_vertex: int) -> List[int]:
    """Function implements the search for the shortest path between
    specified vertexes in oriented unweighted graph
    and returns the list of intermediate vertices on the shortest path"""
    q = deque([start_vertex])
    used_vertexes = set()
    parents = {}

    while q:
        current_vertex = q.popleft()
        # stop the search in case of reaching the end vertex
        if current_vertex == end_vertex:
            break
        # if the current vertex is not reviewed, looking for the neighbours and adding to the queue
        if current_vertex not in used_vertexes:
            used_vertexes.add(current_vertex)
            neighbours = get_friends_ids(current_vertex)
            for neighbour in neighbours:
                if neighbour not in used_vertexes:
                    q.append(neighbour)
                    # add the founded neighbour and its parent (the previous linked vertex)
                    # to the parent's dict, if it is not exists
                    if not parents.get(neighbour):
                        parents[neighbour] = current_vertex
    if not parents.get(end_vertex):
        return None
    vertexes_list = get_list_of_ids(start_vertex, end_vertex, parents)
    return vertexes_list

