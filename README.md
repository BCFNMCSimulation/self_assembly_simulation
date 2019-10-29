# Hard-Sphere-Monte-Carlo

## Introduction

This repository is set up for the computational nanoscience course by Paddy Royall. Fergus and Yushi wrote some basic Monte-Carlo simulations code mentioned in the course.

The code is written in a way that anyone without prior programming experiences could ~~easily~~ understand it. We deliberately avoided any [advanced python features](https://docs.python.org/3/tutorial/classes.html) and [libraries](https://docs.scipy.org/doc/scipy/reference/spatial.distance.html). If you are looking for good and pythonic code, please take a look at [Josh's repository](https://github.com/tranqui/monte_carlo), which performs the same Monte-Carlo simulation.

## What to Do

There are four steps towards a successful Monte-Carlo simulation  of hard spheres.

1. Simulating a ideal gas with the periodic boundary condition (PBC).
2. Simulating hard spheres with PBC.
3. Simulating attracting hard spheres with PBC.
4. Change the parameters and observe different behaviours.

You are expected to write you own code in the class, and we will upload our version to this repository after each course as a reference.

## What is ideal gas

Essentally you want to randomly generate many (x, y, z) coordinates. Being "ideal" means gas molecules **would not** interact with each other and they can overlap.

You can use the `random` library comes with python to get random numbers, like this

```
import random

x = random.uniform(0, 10)  # generate a random number from 0 to 10
y = random.uniform(0, 10)
z = random.uniform(0, 10)
```

## What is Periodic boudnary condition

The particles (xyz coordinates) we generated are assumend to be in a **box**. If a particle moves out of the box from left side, it comes back from the right side.

Implementing periodic boundary condition means you have to check is a paritcle is moving out of our box. You write something like this

```
box_left_x = 0
box_right_x = 10

if x < box_left_x:
  x = x + box_right_x
```

PBC also affects the **distance** between two coordinates. If distance between `A` and `B` are greater than half of the box, the actual distance is `box_size - distance`. So you would write something like this

```
distance_A_B_X = abs(A_X - B_X)
if distance_A_B_X > box_size / 2:
  distance_A_B_X = box_size - distance_A_B_X
```

## What is hard sphere

Hard spheres are different from ideal gas. They have diameters and they **can not overlap**. This means you have to write code to check if two particles (`A` and `B`) are overlapping. If so, do not accept the configuration.

Typicall you would write something like this

```
if distance_between_A_and_B < (radius_A + radius_B):
  # do not accept configuration
```
