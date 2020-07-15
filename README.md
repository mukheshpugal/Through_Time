# Through Time

A simulator that aims to simulate a world based on [Dark's](https://www.netflix.com/title/80100172) concept of time travel.

## Premises and constraints

For the sake of simplicity, let us consider a finite two-dimensional space where the time and space are quantised. That is, the world is a two-dimensional grid, where beings can move only along the grid. Let us also consider that an being is of the size of a grid (a being cannot be in the middle of two grids). For each step in time, a being can either stay in place, or move in one of the available directions. Also, two beings cannot overlap.
<p align="center"><img src="assets/positions.png" /><br/>Each being in the grid can move to one of the shown possible positions in the next time step</p>

### Qualities of beings

Each being has a set of inputs and performs actions based on those inputs. In this case the input could be the status of each grid. *For example, a 100 element array of numbers, one element for each grid where 0 is for empty, 1 for green, 2 for blue etc.* Based on this, decisions are made at each time step by a definitive process given to us before simulation. <br/>
Each being has a fixed life time above which it will cease to exist.

### The time portal

There is a specific location in the world if reached by beings, enable them to travel through time.
<p align="center"><img src="assets/portal.png" /><br/>A black hole at the end of the world.</p>

Whenever a being lands on the black hole, it has two more choices. It can travel to the past by 10 steps (variable) or to the future by 10 steps. Again, all these decisions can be exactly predicted given the decision mechanism. We also prohibit travel beyond the origin to negative time.

#### Time travel mechanics

Whenever someone travels to the future for 10 frames, the being dissapears on the next time step and reappears after 10 time steps with the same age.
<br/>
Whenever someone travels to the past for 10 frames, their presence is mandatory in the (n - 10)th frame. That is, in the (n - 10)th frame, there are two beings who are the same, but one 10 frames older than the other. The future causes the present.

#### Destination post travel

In order to avoid ambiguities regarding the physical destination, after travel, the being ends up at the top left corner of the world. If the position is occupied, they are placed one block to the right and so on. 

## Aim

Our aim is to simulate this 10x10 world for a given initial configuration for a given amount of time steps. The concept of time travel introduces a lot of degrees of freedom. There are a lot of solutions for a given initial configuration. We should be abled to simulate at least one of them if not all. Remember that the brains of the beings are unaltered at any given time and each decision can be accutarely predicted given the current state of the world.

Please feel free to post issues for suggestions / for a better understanding of the concept.