# Artificial Intelligence

## Agents

An agent is anything that can be viewed as perceiving its environment through sensors and acting upon that environment through actuators.

### What is an intelligent agent?

A rational agent is one that does the right thing…

For each possible percept sequence, a rational agent should select an action that is expected to maximize its performance measure, given the evidence provided by the percept sequence and whatever built-in knowledge the agent has.

Types of Intelligent Agents:
- Simple reflex agents (example: a horn, a doorbell)
- Model-based reflex agents (example: wipers of a car)
- Goal-based agents (example: cruise control, a kettle)
- Utility-based agents (example: eco-mode in cars to save fuel)
- Learning agents (example: self-driving cars, predictive text)


## What is a well-defined problem?

Five components:
1. The initial state that the agent starts in.
2. A description of the possible actions available to the agent.
	- Given a particular state $s$, $\text{ACTIONS}(s)$ returns the set of actions that can be executed in $s$.
3. A description of what each action does; the formal name for this is the transition model.
	- Specified by a function $\text{RESULT}(s,\ a)$ that returns the state that results from doing action $a$ in state $s$.
4. The goal test, which determines whether a given state is a goal state.
	- Sometimes there is an explicit set of possible goal states, and the test simply checks whether the given state is one of them.
5. A path cost function that assigns a numeric cost to each path.
	- The problem-solving agent chooses a cost function that reflects its own performance measure.


## What is a Solution?

- A solution to a problem is an action sequence that leads from the initial state to a goal state.
- Solution quality is measured by the path cost function.
- An optimal solution has the lowest path cost among all solutions.

How do we measure the performance of a specific search algorithm?
- Completeness: Is the algorithm guaranteed to find a solution when there is one?
- Optimality: Does the strategy find the optimal solution?
- Time complexity: How long does it take to find a solution?
- Space complexity: How much memory is needed to perform the search?

How do we measure complexity?

Generally, a measure of the difficulty of the problem

In AI, complexity is expressed in terms of three quantities:
- $b$, the branching factor or maximum number of successors of any node;
- $d$, the depth of the shallowest goal node (i.e., the number of steps along the path from the root);
- $m$, the maximum length of any path in the state space.


## Uninformed Searches (a.k.a. Blind Searches)

- Strategies with no additional information about states beyond that provided in the problem definition.
- All they can do is generate successors and distinguish a goal state from a non-goal state.
- Search strategies are distinguished by the order in which nodes are expanded.

Types:
- [Breadth-first search (BFS)](./uninformed-searches/breadth-first)
- [Uniform-cost search (UCS)](./uninformed-searches/uniform-cost)
- Depth-first search (DFS)
- Depth-limited search
- Iterative deepening depth-first search
- Bidirectional search




Depth-first search (DFS)

It expands the deepest node in the frontier.

Search proceeds immediately to the deepest level of the search tree, where nodes have no successors.

Then the search “backs up” to the next deepest node that still has unexplored successors.

Implemented by using a LIFO queue for the frontier.

The most recently generated node is chosen for expansion.

This must be the deepest unexpanded node because it is one deeper than its parent.

Performance

Complete: in finite state spaces because it will eventually expand every node. In infinite state spaces, it will fail if an infinite non-goal path is encountered.

Non-Optimal: longer, potentially more expensive paths cost solutions will be returned first if their subtree happen to be expanded first.

Time Complexity: DFS will visit all states once, so the complexity is bounded by the size of the state space (which can be infinite!).

The tree version, with no checks for duplicate states, can generate all of the O(bm) nodes in the search tree, where m is the maximum depth of any node; this can be much greater than the size of the state space.

Space Complexity: no advantage for the graph version, as all nodes will be kept in the explored set.

But for the tree version, DFS needs to store only a single path from the root to a leaf node, along with the remaining unexpanded sibling nodes for each node on the path. For a state space with branching factor b and maximum depth m, depth-first search requires storage of only O(bm) nodes.



Depth-limited search

Solves the problem of infinite state spaces by  supplying depth-first search with a predetermined depth limit l.

Any nodes at depth l are treated as if they had
no successors.

DFS is a special case of depth-limited search where l = ∞.

Recursive algorithm for depth-limited search

Remember that DFS is a special case with l = ∞.

Performance

Incomplete: if d > l, where d is the depth of the shallowest goal state node.

Non-Optimal: for any values of l. Just as for DFS, longer, potentially more expensive paths cost solutions will be returned first if their subtree happen to be expanded first.

Time Complexity: as the maximum depth is limited to l, the time complexity is odes in O(bl), where b is the branching factor.

Space Complexity: similarly, the space complexity for the tree version of depth-limited search is O(bl).



Iterative Deepening DFS

Like depth-limited search, but with increasingly larger values for l (0, then 1, then 2, etc.)

Combines the benefits of DFS and BFS.

Like DFS, its memory requirements are O(bd).

Like BFS, it is complete when the branching factor is finite and optimal when the path cost is a nondecreasing function of the depth of the node.

In general, iterative deepening is the preferred uninformed search method when the search space is large and the depth of the solution is not known.

Bidirectional Search

Search forward from initial state node and backward from a goal state node.

Instead of checking for a goal state, check for the intersection of the two frontiers.

Time complexity using BFS in both directions is O(bd/2). The space complexity is also O(bd/2).

Bidirectional search requires a method for computing the predecessors of a state x: i.e.
all those states that have x as a successor.