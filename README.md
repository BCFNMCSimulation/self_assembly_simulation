# Hard-Sphere-Monte-Carlo

## Introduction

This repository is set up for the computational nanoscience course by Paddy Royall. Fergus and Yushi wrote some basic Monte-Carlo simulations code mentioned in the course.

The code is written in a way that anyone without prior programming experiences could ~~easily~~ understand it. We deliberately avoided any [advanced python feature](https://docs.python.org/3/tutorial/classes.html) and [libraries](https://docs.scipy.org/doc/scipy/reference/spatial.distance.html). If you are looking for good and pythonic code, please take a look at [Josh's repository](https://github.com/tranqui/monte_carlo), which performs the same Monte-Carlo simulation.

## What to Do

There are four steps towards a successful Monte-Carlo simulation of hard spheres.

1. Simulating a ideal gas with the periodic boundary condition (PBC). [Example Code](ideal_gas.py)
2. Simulating hard spheres with PBC. [Example Code](hard_sphere.py)
3. Simulating attracting hard spheres with PBC. [Example Code](hard_sphere_attracted.py)  (extra: [Binary System](hard_sphere_attracted_binary.py))
4. Change the parameters and observe different behaviours.

You are expected to write you own code in the class, and we will upload our version to this repository after each course as a reference.

## Ideal Gas

### What is ideal gas

Essentally you want to generate a lattice (many ordered xyz coordinates), and randomly move them. Being "ideal" means gas molecules **would not** interact with each other and they can overlap. 

### Generating Lattice :wink:

```
unit_repeat = 5
x, y, z = [], [], []
for i in range(0, unit_repeat):
    for j in range(0, unit_repeat):
        for k in range(0, unit_repeat):
            # Learning
```

### Random Movements

You can use the `random` library comes with python to get random numbers, like this

```
import random

random_move_x = random.uniform(-1, 1)  # generate a random number from -1 to 1
random_move_y = random.uniform(-1, 1)
random_move_z = random.uniform(-1, 1)
```

### Getting a movie

You are expected to generate a movie. Which means move **every paritcle randomly** each time. And output a **frame** after all particles were moved. For instance we do something like this

```
for frame_number in range(100):
    for particle_id in range(particle_number):
        x[particle_id] += random_move_x
        y[particle_id] += random_move_y
        z[particle_id] += random_move_z
    #output_frame
```

### Output a frame `.xyz` file

This is the piece of code for outputting an `xyz` file. Incorporate it in your `for frame_number ... ` loop.

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

### What is Periodic boudnary condition

The particles (xyz coordinates) we generated are assumend to be in a **box**. If a particle moves out of the box from left side, it comes back from the right side.

Implementing periodic boundary condition means you have to check is a paritcle is moving out of our box. You write something like this

```
box_left_x = 0
box_right_x = 10

if x < box_left_x:
    x = x + box_right_x
```

## Hard Spheres

### What is a hard sphere

Hard spheres are different from ideal gas. They have diameters and they **can not overlap**. This means you have to write code to check if two particles (`A` and `B`) are overlapping. If so, do not accept the configuration.

Typicall you would write something like this

```
if distance_between_A_and_B < (radius_A + radius_B):
    # do not accept configuration
```

### Distance in PBC

PBC affects the **distance** between two coordinates. If distance between `A` and `B` are greater than half of the box, the actual distance is `box_size - distance`. So you would write something like this

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

### Not accepting movements

In hard sphere simulation, we have to make sure particles do not overlap by rejecting the overlapped senarios. Typically one would write down something like this:

```
trial_x = x[particle_id] + random_move_x
trial_y = y[particle_id] + random_move_y
trial_z = z[particle_id] + random_move_z

trial_x = FIX PBC FOR X
trial_y = FIX PBC FOR Y
trial_z = FIX PBC FOR Z

for anoter_particle_id in range(particle_number):
    is_overlap = False
    if another_particle_id != particle_id:
        is_overlap = # CHECK IF [particle] and [another_particle] are overlapping
        if is_overlap:
            break

if not is_overlap:
    x[particle_id] = trial_x
    y[particle_id] = trial_y
    z[particle_id] = trial_z
```

### Check the result

In [ovito](https://www.ovito.org), we can use the tool `coordination analysis` to get the [radial distribution function](https://en.wikipedia.org/wiki/Radial_distribution_function) (g(r)). There should be no peak within one particle diameter.

To do this, follow the following procedures:

1. Click `Add modification` and add `Affine Transformation`.
    1. Select `Transform to target box` and set the box size to corret values
    2. **Deselect** tickbox `Particles` in the `Operate on` section
2. Click `Data source - Simulation Cell` and select `X`, `Y`, `Z` under the group `Periodic boundary conditiosn`.
3. Click `Add modification` and add `Analysis/Coordination analysis`.

Then you got your g(r)!

## Attractive Hard Sphere

### What is it

Now it is time to add **attraction** to the hard sphere. For the attraction, we will implement a [square well potential](https://www.researchgate.net/figure/The-square-well-potential-of-depth-un-uand-A-are-respectively-the-hard-sphere-diameter_fig1_253989608).

What we actuall do, is **lower the energy of the system** everytime if a particle goes into the attractive "well" in the potential. Very frankly, you are expected to do something like this

```
def get_energy(i, system, depth, width, diameter, box):
    """
    this function calculating the energy of one particle inside a system
    with square well potential

    The stuff below are some testing code, don't worry about it
    >>> system = [[0, 0], [1, 1], [2, 2], [3, 3]]
    >>> get_energy_square_well(system[0], system, -1, 2, [4, 4])
    -2
    """
    energy = 0
    p1 = system[i]   # particle 1
    for j, p2 in enumerate(system):    # another particle
        if i != j:
            distance = get_distance_in_pbc(p1, p2, box)
            if distance <= width + diameter:
                energy = energy + depth
    return energy
```

### Accepting movement with energy

Typicall I will do something like this

```
old_energy = get_energy(i, old_system, depth, width, diameter, box)
new_energy = get_energy(i, new_system, depth, width, diameter, box)
delta = new_energy - old_energy
accept_probability = np.exp(-1 * delta)

# if probability is HIGH, a random number is less likely to be higher than it
if random.random() < accept_probability:
    x[i], y[i], z[i] = trial_x, trial_y, trial_z
```
