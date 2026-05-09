Yes, 11 minutes is too long for a class video unless the professor specifically wants that. Here’s a tighter version that should land around **7:30–8:00**, but still keeps enough detail for you to implement the Manim scenes cleanly.

# CVRP Video Script, 7–8 Minute Version

## Scene 1 — Hook: One Depot, Many Customers

**Runtime:** 0:00–0:30

### Narration

“Imagine you run a delivery company. You have one depot, a group of customers, and a fleet of trucks.”

“Each customer needs a delivery, but every truck can only carry so much.”

“So the question is: how should the trucks be routed so everyone is served, no truck is overloaded, and the total driving distance is as small as possible?”

“That problem is called the Capacitated Vehicle Routing Problem, or CVRP.”

### Visualization

Start on a dark background.

Show title:

```text
The Capacitated Vehicle Routing Problem
```

Subtitle:

```text
How do delivery trucks choose their routes?
```

After a few seconds, fade the title out.

Then show:

* yellow square = depot
* purple dots = customers
* small demand labels above/below customers: `d=2`, `d=3`, `d=4`
* maybe one thin route line briefly tries to visit many customers, then fades

Optional speech bubble:

```text
One depot.
Many customers.
Limited truck space.
```

---

## Scene 2 — What CVRP Is

**Runtime:** 0:30–1:10

### Narration

“In CVRP, we model the system as a graph. The depot is one node, customers are the other nodes, and edges represent travel distance or cost.”

“Each customer has a demand, and each vehicle has a capacity, usually written as (Q).”

“A valid solution is a set of routes. Every route starts at the depot, visits some customers, and returns to the depot.”

### Visualization

Keep the depot/customers on screen.

Add a large capacity box in the upper-right:

```text
Vehicle Capacity: Q = 8
```

Then show rules one by one:

```text
1. Visit every customer exactly once
2. Start and end at the depot
3. Do not exceed vehicle capacity
4. Minimize total travel distance
```

Implementation idea:

* Use `FadeIn` for each rule.
* Use small check marks next to each rule.
* Keep rules on the left or lower-left, not too close to the bottom.

Speech bubble:

```text
A route is valid only if it follows the rules.
```

---

## Scene 3 — Why Capacity Makes It Hard

**Runtime:** 1:10–1:50

### Narration

“If we had one vehicle with unlimited capacity, this would look more like the Traveling Salesman Problem: one route through every customer.”

“But CVRP adds a second decision. We have to decide which customers go on the same truck, and then decide the order in which each truck visits them.”

“So CVRP is both grouping and routing.”

### Visualization

Draw one big red route through all customers.

Show the total demand:

[
2 + 3 + 4 + 2 + 3 + 2 + 4 = 20 > Q = 8
]

Make the route pulse red.

Add label:

```text
Infeasible
```

Then show simple comparison:

Left:

```text
TSP
One route
```

Right:

```text
CVRP
Multiple routes + capacity
```

On the right, show several colored routes.

Speech bubble:

```text
Shortest is not enough.
The truck still has to fit.
```

---

## Scene 4 — Feasible vs. Optimal

**Runtime:** 1:50–2:25

### Narration

“A useful way to think about CVRP is to separate feasibility from optimality.”

“A feasible solution follows the rules. No customer is missed, and no truck is overloaded.”

“An optimal solution is the best feasible one, usually meaning the one with the smallest total travel cost.”

### Visualization

Fade out the red infeasible route.

Show three feasible routes:

```text
Route 1: 2 + 3 + 3 = 8 ≤ 8
Route 2: 4 + 2 = 6 ≤ 8
Route 3: 2 + 4 = 6 ≤ 8
```

Place those route labels in the **left-middle** of the screen, not at the bottom, so video controls don’t block them.

Then briefly show two feasible route plans side by side:

```text
Feasible but longer
```

and

```text
Feasible and shorter
```

Highlight the shorter one.

Speech bubble:

```text
Feasible first.
Optimal second.
```

---

## Scene 5 — Objective Function

**Runtime:** 2:25–2:50

### Narration

“The objective is to minimize total travel cost.”

“If (c_{ij}) is the cost of traveling from node (i) to node (j), then every edge we use adds to the total.”

“So the goal is to choose routes that satisfy capacity while minimizing the sum of all route costs.”

### Visualization

Keep the colored routes visible.

Show:

[
\min \sum_{\text{routes}} \sum_{(i,j)} c_{ij}
]

Highlight a few edges one at a time and label them:

```text
c_ij
```

Then show a total cost counter:

```text
Total Cost = 142
```

Speech bubble:

```text
Every edge we use adds cost.
```

---

## Scene 6 — Main Ways CVRP Is Solved

**Runtime:** 2:50–3:15

### Narration

“There are many ways to solve CVRP, but most fall into a few categories.”

“Exact methods try to prove the best solution. Heuristics try to build good routes quickly. Local search and metaheuristics improve solutions, and newer learning-based methods can help guide the search.”

“In this video, we’ll focus on two visual examples: branch-and-bound and Clarke-Wright Savings.”

### Visualization

Show a clean method map:

```text
Ways to Solve CVRP

Exact Methods
  → Branch-and-Bound

Constructive Heuristics
  → Clarke-Wright Savings

Improvement Methods
  → Local Search / Metaheuristics

Learning-Based Methods
```

Highlight **Branch-and-Bound** and **Clarke-Wright Savings** because those are the two main examples.

Speech bubble:

```text
One exact example.
One fast heuristic.
```

---

## Scene 7 — Branch-and-Bound: Search Tree

**Runtime:** 3:15–4:05

### Narration

“Branch-and-bound is an exact method. It is designed to search for the optimal solution and prove that no better solution exists.”

“The idea is to organize possible routing decisions as a tree.”

“At the root, nothing has been decided yet. Then the solver branches by fixing choices, like whether to use a certain edge or whether to avoid it.”

“Each branch represents a smaller version of the original problem.”

### Visualization

Clear most of the screen.

Left side: small CVRP graph with 4 or 5 customers.

Right side: search tree.

Root node:

```text
All route plans possible
```

Branch into:

```text
Use edge A-B
```

and:

```text
Do not use edge A-B
```

Then branch each of those once more.

Keep the tree simple: 2–3 levels only.

Animation directions:

* Use circles or rounded rectangles for tree nodes.
* Use `Line` objects for branches.
* As each decision appears, highlight the corresponding edge on the graph.
* The graph and tree should visually communicate that the tree is exploring route choices.

Speech bubble:

```text
Each branch fixes one decision.
```

---

## Scene 8 — Branch-and-Bound: Bounds and Pruning

**Runtime:** 4:05–4:55

### Narration

“The bound is what makes branch-and-bound powerful.”

“At each tree node, the solver computes a best-case estimate for that branch. For a minimization problem, this is usually a lower bound.”

“Suppose the best complete solution found so far has cost 120.”

“If another branch has a lower bound of 135, then even in the best case, that branch cannot beat 120.”

“So the solver prunes it. It stops searching that branch completely.”

### Visualization

Show text at top:

```text
Best solution so far: 120
```

Add bound labels to tree nodes:

```text
Lower bound = 95
Lower bound = 118
Lower bound = 135
```

For the node with `135`:

* turn it red
* draw an X through it
* label it:

```text
Pruned
```

For the node with `95`:

* keep it blue/green
* expand it further

Then show a complete solution node:

```text
Complete solution: 112
```

Update top text:

```text
Best solution so far: 112
```

Speech bubble:

```text
If a branch cannot win,
we stop searching it.
```

---

## Scene 9 — Exact Methods: Quick Extension

**Runtime:** 4:55–5:15

### Narration

“In practice, CVRP exact solvers often strengthen branch-and-bound.”

“Branch-and-cut adds extra constraints to remove invalid route structures. Branch-and-price generates useful full routes as needed.”

“So branch-and-bound is the core idea, but stronger exact solvers build on it.”

### Visualization

Show a simple transformation stack:

```text
Branch-and-Bound
= search tree + bounds
```

Transform into:

```text
Branch-and-Cut
= add cutting constraints
```

Then:

```text
Branch-and-Price
= generate routes as columns
```

For branch-and-price, briefly show a route card:

```text
Route: Depot → A → C → Depot
Demand = 6
Cost = 31
```

Keep this short. This is just a conceptual bridge.

Speech bubble:

```text
Same tree idea,
stronger tools.
```

---

## Scene 10 — Clarke-Wright Savings: Starting Point

**Runtime:** 5:15–5:55

### Narration

“Now let’s switch to a heuristic: the Clarke-Wright Savings algorithm.”

“A heuristic does not usually prove the optimal solution, but it can find good routes quickly.”

“Clarke-Wright starts with a simple feasible solution: every customer gets their own route from the depot and back.”

“This is feasible, but very inefficient.”

### Visualization

Return to depot/customer graph.

Show one route per customer:

[
0 \to i \to 0
]

Visually:

* depot to customer A and back
* depot to customer B and back
* depot to customer C and back

To avoid clutter:

* animate 3 representative routes strongly
* show the rest as faint gray lines

Label:

```text
Initial solution:
one route per customer
```

Speech bubble:

```text
Feasible, but wasteful.
```

---

## Scene 11 — Clarke-Wright Savings: Merge Rule

**Runtime:** 5:55–6:45

### Narration

“The algorithm then asks: what if two customers are served on the same route instead of separately?”

“If connecting customer (i) directly to customer (j) saves distance, then merging their routes might be a good idea.”

“The savings value is”

[
s_{ij} = c_{i0} + c_{0j} - c_{ij}
]

“Large savings mean a merge is attractive, but only if the combined route still respects capacity.”

### Visualization

Zoom into depot, customer (i), and customer (j).

Show separate routes:

```text
0 → i → 0
0 → j → 0
```

Then transform into:

```text
0 → i → j → 0
```

Show the formula:

[
s_{ij} = c_{i0} + c_{0j} - c_{ij}
]

Highlight terms as narration says them.

Then show two candidate merges.

Accepted merge:

```text
Demand: 3 + 4 = 7 ≤ 8
Accept
```

Use green check. Draw merged route in green.

Rejected merge:

```text
Demand: 5 + 6 = 11 > 8
Reject
```

Use red X. Make the attempted merge line appear red, shake slightly, then fade out.

Speech bubble:

```text
Save distance,
but don't overload.
```

---

## Scene 12 — Local Search and Metaheuristics

**Runtime:** 6:45–7:30

### Narration

“After building an initial route plan, solvers often improve it with local search.”

“Local search makes small changes, like removing crossed edges with 2-opt, moving one customer somewhere better, or swapping two customers.”

“But local search can get stuck in a local optimum.”

“That is why metaheuristics search more broadly. For example, large neighborhood search removes part of a solution and then repairs it in a better way.”

### Visualization

Part A: local search.

Show a route with crossing edges.

Label:

```text
2-opt
```

Animate the crossed edges uncrossing.

Show:

```text
Cost: 142 → 128
```

Then briefly show:

```text
Relocate
```

A customer dot moves from one route to another.

Then:

```text
Swap
```

Two customer dots trade positions.

Part B: metaheuristic.

Show text:

```text
Large Neighborhood Search
Destroy → Repair → Improve
```

Visual:

* start with route solution
* gray out/remove 3 customers
* reinsert them in better positions
* cost decreases again

Speech bubble:

```text
Small moves improve.
Big moves escape.
```

---

## Scene 13 — Learning-Based Methods and Final Comparison

**Runtime:** 7:30–8:00

### Narration

“More recently, machine learning has also been used to help with routing.”

“A model might predict promising edges, good customer clusters, or useful improvement moves.”

“But the big picture is this: different methods serve different goals.”

“Exact methods can prove optimality. Heuristics are fast. Local search and metaheuristics improve solutions. Learning-based methods can help guide the search.”

### Visualization

Very brief GNN-style animation:

* nodes pulse
* edges glow
* a few promising edges become highlighted

Text:

```text
ML can suggest:
promising edges
clusters
initial routes
improvement moves
```

Then switch to compact comparison table:

```text
Method              Main idea                 Strength
Branch-and-Bound    Search tree + pruning      Exact
Clarke-Wright       Merge routes by savings    Fast
Local Search        Small improvements         Practical
Metaheuristics      Broader exploration         Strong
Learning-Based      Predict useful patterns    Smart guidance
```

Highlight one row at a time as you say it.

Speech bubble:

```text
Most real solvers combine ideas.
```

---

## Scene 14 — Closing Takeaway

**Runtime:** 8:00–8:20 max, optional if you want a clean ending

If you need to stay under 8 minutes, make this only 10 seconds.

### Narration

“CVRP is simple to state, but hard to solve.”

“It combines grouping, routing, and capacity into one optimization problem.”

“And that is why a basic delivery question becomes a powerful mathematical problem.”

### Visualization

Return to final depot/customer graph.

Show clean final routes.

Final equation:

[
\text{CVRP} = \text{Grouping} + \text{Routing} + \text{Capacity}
]

Final text:

```text
Simple to state.
Hard to solve.
Very useful.
```

Fade out.

---

# Final Runtime

This version should land around:

```text
Scene 1: 0:00–0:30
Scene 2: 0:30–1:10
Scene 3: 1:10–1:50
Scene 4: 1:50–2:25
Scene 5: 2:25–2:50
Scene 6: 2:50–3:15
Scene 7: 3:15–4:05
Scene 8: 4:05–4:55
Scene 9: 4:55–5:15
Scene 10: 5:15–5:55
Scene 11: 5:55–6:45
Scene 12: 6:45–7:30
Scene 13: 7:30–8:00
Scene 14: 8:00–8:20 optional
```

So the core video is **about 8 minutes**, and if you trim the closing or speak a little faster, it becomes **7:45–8:00**.

The two main examples are still:

```text
1. Branch-and-Bound
2. Clarke-Wright Savings
```

Everything else is a quick but visual overview.


haracter Guide System

Use the characters like little “guide cameos,” not full subtitles.

Basic rule:

M = Main explainer / setup moments
I = Interrupts / points out constraints or problems
T = Transition / moves us into the next method

They should appear in different corners and sometimes rotated so it feels playful:

M: usually lower-right or lower-left, normal orientation
I: sometimes upside down in upper-left, like it dropped in
T: tilted in upper-right or peeking from a corner

Speech bubbles should be short, like 1–2 lines max.

Character Directions Added to the Script
Scene 1 — Hook

Character: M
Position: lower-right corner
Orientation: normal
Bubble:

One depot.
Many customers.
Limited truck space.

Visual role: M introduces the problem, then fades out before the full graph gets busy.

Scene 2 — What CVRP Is

Character: M
Position: lower-left corner
Orientation: slight tilt, maybe rotate(5 * DEGREES)
Bubble:

A route is valid
only if it follows
the rules.

Visual role: M points toward the rules list as each rule appears.

Scene 3 — Why Capacity Makes It Hard

Character: I
Position: upper-left corner
Orientation: upside down, rotate(PI)
Bubble:

Wait...
that truck is
overloaded.

Visual role: I appears right when the one big route turns red and the demand sum becomes 20>8. This makes the capacity violation feel like a “caught mistake” moment.

Scene 4 — Feasible vs. Optimal

Character: I
Position: upper-right corner
Orientation: slightly tilted
Bubble:

Feasible first.
Optimal second.

Visual role: I stays briefly while the red route becomes feasible colored routes. Then fade it out before the objective equation.

Scene 5 — Objective Function

Character: T
Position: lower-right corner
Orientation: peeking from the corner, maybe partially off-screen
Bubble:

Every edge we use
adds cost.

Visual role: T appears while edge labels c
ij
	​

 pop up. T can look toward the highlighted edges.

Scene 6 — Main Ways CVRP Is Solved

Character: T
Position: upper-right corner
Orientation: tilted, rotate(-12 * DEGREES)
Bubble:

One exact example.
One fast heuristic.

Visual role: T introduces the transition from defining the problem to solving the problem.

Scene 7 — Branch-and-Bound: Search Tree

Character: M
Position: lower-left corner
Orientation: normal
Bubble:

Each branch fixes
one decision.

Visual role: M appears next to the search tree, not the graph. It helps explain that each tree node represents a partial routing decision.

Scene 8 — Bounds and Pruning

Character: I
Position: upper-left corner
Orientation: upside down or sideways
Bubble:

If it cannot win,
we stop searching it.

Visual role: I appears right when a branch with lower bound 135 gets crossed out. This is a good “aha” moment for the character.

Scene 9 — Exact Methods Quick Extension

Character: none or very quick T
Position: lower-right
Orientation: normal
Bubble:

Same tree idea,
stronger tools.

Visual role: Optional. This scene is short, so the character may be unnecessary. The screen may already have enough text with branch-and-cut and branch-and-price.

Scene 10 — Clarke-Wright Starting Point

Character: M
Position: lower-right corner
Orientation: normal
Bubble:

Feasible,
but wasteful.

Visual role: M appears as one route per customer is drawn. The joke is that the solution technically works, but it is obviously inefficient.

Scene 11 — Clarke-Wright Merge Rule

Character: T
Position: upper-right corner
Orientation: tilted
Bubble:

Save distance,
but don't overload.

Visual role: T appears during the accepted/rejected merge examples. This is probably one of the best places for the guide character.

Scene 12 — Local Search and Metaheuristics

Character: I then T

For local search:

Character: I
Position: upper-left
Orientation: slight tilt
Bubble:

Small moves
can improve routes.

For LNS/metaheuristics:

Character: T
Position: lower-right
Orientation: peeking from corner
Bubble:

Big moves help
escape.

Visual role: I introduces small improvements like 2-opt. T introduces the broader destroy-repair idea.

Scene 13 — Learning-Based Methods and Final Comparison

Character: M, I, and T together briefly
Position: bottom of screen or three different small corners
Orientation:

M normal
I upside down
T tilted

Bubble:

Most real solvers
combine ideas.

Visual role: This is where the full cast can appear briefly, because the video is summarizing all method types.

Scene 14 — Closing

Character: M, I, and T together
Position: bottom-right or around the final equation
Orientation: playful but not too chaotic
Bubble:

That's CVRP.

Visual role: The final routes appear, then the three letters pop in around the final takeaway:

CVRP=Grouping+Routing+Capacity
Best Character Usage Pattern

I’d keep the letters to about 8–10 appearances total, not every single scene.

Best scenes to definitely include them:

Scene 1: M introduces the problem
Scene 3: I catches the capacity violation
Scene 6: T transitions into solution methods
Scene 7–8: M/I explain branch-and-bound
Scene 10–11: M/T explain Clarke-Wright
Scene 13–14: all three appear for summary

That way they feel like a recurring YouTube-style guide system, but they don’t cover the animation or make the video too childish.