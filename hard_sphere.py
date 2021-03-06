# -*- coding: utf-8 -*-
"""
Hard Sphere: This script creates a lattice of particles that won't overlap
You can easily tell the difference between random gas and hard spheres from the g(r)
Most of the code is the same for random gas
"""
import random as random
import numpy as np


def check_overlap(p1, p2, diameter, box):

    """
    Here we define our first function that check if two spheres were overlap
    We check the periodic boundary condition (PBC), consider the condition below.
    The measured distance is d0, but the actural distance should be d1.
    Because p2 is identical with p3. (use monospace font to see the figure)

    ┌ ─ ─ ─ ─ ─ ─┌────────────┐
         p3  ◌   │○ p1    ○ p2│
    └ ─ ─ ─ ─│─ ─└┬───────┬───┘
             │ d1 │  d0   │

    Figure 1. Example of PBC in 1D

    The stuff below are some testing code, don't worry about it
    >>> check_overlap([1, 1], [1.5, 1.5], 2, [5, 5])
    True
    >>> check_overlap([1, 1], [4.8, 4.8], 2, [5, 5])
    True
    >>> check_overlap([1, 1], [3, 3], 2, [5, 5])
    False
    >>> check_overlap([1, 1, 1], [5, 5, 5], 2, [5, 5, 5])
    True
    """

    dimension = len(p1)
    distance_nd = []
    for d in range(dimension):
        distance_1d = abs(p2[d] - p1[d])
        if distance_1d > (box[d] / 2):
            distance_nd.append((box[d] - distance_1d) ** 2)
        else:
            distance_nd.append(distance_1d ** 2)
    distance = sum(distance_nd) ** 0.5

    if distance > diameter:
        return False  # not overlap
    else:
        return True

# Initial parameters
unit_repeat = 5  # number of unit cells per dimension
lattice_constant = 1
box_size = lattice_constant * unit_repeat
particle_number = unit_repeat ** 3  # number of particles
total_steps = 100
volume_fraction = 0.1
diameter = 1

# rewrite file
output_file = open('positions_hard_sphere.xyz', 'w')
output_file.close()

# Generate initial co-ordinates
x, y, z = [], [], []
for i in range(0, unit_repeat):
    for j in range(0, unit_repeat):
        for k in range(0, unit_repeat):
            x.append(i * lattice_constant)
            y.append(j * lattice_constant)
            z.append(k * lattice_constant)

# Rescale the box/coordinates so we achieve the correct volume fraction/density.
atoms_per_cell = 1
atom_volume = np.pi * diameter ** 3 / 6
initial_volume_fraction = atoms_per_cell * atom_volume  # / unit volume (=1)
rescale = (initial_volume_fraction / volume_fraction) ** (1. / 3)
box_size *= rescale

for a in range(0, particle_number):
    x[a] *= rescale
for a in range(0, particle_number):
    y[a] *= rescale
for a in range(0, particle_number):
    z[a] *= rescale

# Move particles, output their coordinates
for t in range(0, total_steps):
    # Write positions to file
    with open('positions_hard_sphere.xyz', 'a') as f:
        f.write(str(len(x)) + '\n')
        f.write('\n')
        for i in range(len(x)):
            # xyz file is a file format to store 3D position
            # the general format is:
            # PARTICLE_TYPE  X  Y  Z
            # here we just call our hard spheres H
            f.write('H' + '\t' + str(x[i]) + '\t' + str(y[i]) + '\t' + str(z[i]) + '\n')

    for i in range(0, particle_number):
        # Trial Move
        trial_x = x[i] + random.gauss(0, 1)
        trial_y = y[i] + random.gauss(0, 1)
        trial_z = z[i] + random.gauss(0, 1)

        # Check boundaries
        # We always move particles a small step, so don't worry if trial_x >> box_size
        if trial_x <= 0:
            trial_x += box_size
        elif trial_x >= box_size:
            trial_x -= box_size

        if trial_y <= 0:
            trial_y += box_size
        elif trial_y >= box_size:
            trial_y -= box_size

        if trial_z <= 0:
            trial_z += box_size
        elif trial_z >= box_size:
            trial_z -= box_size

        # check if the trial particle is overlaping with other particles
        is_overlap = False

        for j in range(0, particle_number):
            if is_overlap:
                break
            if i != j:
                p1 = [trial_x, trial_y, trial_z]
                p2 = [x[j], y[j], z[j]]
                box = [box_size, box_size, box_size]
                is_overlap = check_overlap(p1, p2, diameter, box)

        if not is_overlap:
            # Confirm movements
            x[i], y[i], z[i] = trial_x, trial_y, trial_z
print("Simulation box is ", box)
