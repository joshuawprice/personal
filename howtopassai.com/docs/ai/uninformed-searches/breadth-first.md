# Breadth-first search (BFS)

1. Root node is expanded first.
2. All the successors of the root node are expanded next.
3. Then their successors
4. and so on…

All the nodes are expanded at a given depth in the search tree before any nodes at the next level are expanded.

General graph-search algorithm in which the shallowest unexpanded node is chosen for expansion.
- Implemented by using a FIFO queue for the frontier.
- So new nodes (deeper than their parents) go to the back of the queue.
- And old nodes (shallower than the new nodes) get expanded first.

### Performance

- Complete: if the shallowest goal node is at some finite depth d, breadth-first search will eventually find it after generating all shallower nodes (provided the branching factor b is finite).
- Non-Optimal: the shallowest goal node is not necessarily the optimal one; BFS is optimal if the path cost is a nondecreasing function of the depth of the node (e.g. all actions have the same cost).
- Time Complexity: searching a uniform tree where every state has $b$ successors. The root of the search tree generates $b$ nodes at the first level, each of which generates b more nodes, for a total of $b^2$ at the second level. Each of these generates $b$ more nodes, yielding $b^3$ nodes at the third level, and so on.

    Now suppose that the solution is at depth d. In the worst case, it is the last node generated at that level. Then the total number of nodes generated is

	$$b + b^2 + b^3 + · · · + b^d = \mathcal{O}(b^d)$$

- Space Complexity: for any kind of graph search, which stores every expanded node in the explored set, the space complexity is always within a factor of $b$ of the time complexity. Every node generated remains in memory.

    There will be $\mathcal{O}(b^d−1)$ nodes in the explored set and $\mathcal{O}(b^d)$ nodes in the frontier, so the space complexity is $\mathcal{O}(b^d)$, i.e., it is dominated by the size of the frontier.