# Hard-Sphere-Monte-Carlo

## Introduction

This repository is set up for the computational nanoscience course by Paddy Royall. Fergus and Yushi wrote some basic Monte-Carlo simulations code mentioned in the course.

The code is written in a way that anyone without prior programming experiences could ~~easily~~ understand it. We deliberately avoided any [advanced python feature](https://docs.python.org/3/tutorial/classes.html) and [libraries](https://docs.scipy.org/doc/scipy/reference/spatial.distance.html). If you are looking for good and pythonic code, please take a look at [Josh's repository](https://github.com/tranqui/monte_carlo), which performs the same Monte-Carlo simulation.

## What to Do

There are four steps towards a successful Monte-Carlo simulation of hard spheres.

1. Simulating a ideal gas with the periodic boundary condition (PBC).
2. Simulating hard spheres with PBC.
3. Simulating attracting hard spheres with PBC.
4. Change the parameters and observe different behaviours.

You are expected to write you own code in the class, and we will upload our version to this repository after each course as a reference.

## Generating Lattice

(:shushing_face:)

```
unit_repeat = 5
x, y, z = [], [], []
for i in range(0, unit_repeat):
    for j in range(0, unit_repeat):
        for k in range(0, unit_repeat):
            # Learning
```

## What is ideal gas

Essentally you want to generate a lattice (many ordered xyz coordinates), and randomly move them. Being "ideal" means gas molecules **would not** interact with each other and they can overlap. For instance we do something like this

```
for frame_number in range(100):
    for particle_id in range(particle_number):
        x[particle_id] += random_move_x
        y[particle_id] += random_move_y
        z[particle_id] += random_move_z
    #output_frame
```

## Random Movements

You can use the `random` library comes with python to get random numbers, like this

```
import random

random_move_x = random.uniform(0, 1)  # generate a random number from 0 to 10
random_move_y = random.uniform(0, 1)
random_move_z = random.uniform(0, 1)
```

## Getting a movie

You are expected to generate a movie. Which means move **every paritcle randomly** each time. And output a **frame** after all particles were moved.

## Output a frame `.xyz` file

There are the code for output a `xyz` file. Incorporate it in your `for` loop.

```
  with open('filename.xyz', 'a') as f:
      f.write(str(len(x)) + '\n')
      f.write('\n')
      for i in range(len(x)):
          # xyz file is a file format to store 3D position
          # the general format is:
          # PARTICLE_TYPE  X  Y  Z
          # here we just call our random gas particles "G"
          f.write('G' + '\t' + str(x[i]) + '\t' + str(y[i]) + '\t' + str(z[i]) + '\n')
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
distance_nd = []
for dimension in range(3):
    distance_1d = abs(p2[dimension] - p1[dimension])  # p1 and p2 are xyz coordinates two particles
    if distance_1d > (box[dimension] / 2):
        distance_1d = box[dimension] - distance_1d
    distance_nd.append(distance_1d)
 
distance = 0
for dimension in range(3):
    distance = distance + distance_nd[dimension] ** 2
```

## What is hard sphere

Hard spheres are different from ideal gas. They have diameters and they **can not overlap**. This means you have to write code to check if two particles (`A` and `B`) are overlapping. If so, do not accept the configuration.

Typicall you would write something like this

```
if distance_between_A_and_B < (radius_A + radius_B):
  # do not accept configuration
```
