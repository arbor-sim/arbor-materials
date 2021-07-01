# Documentation at https://docs.arbor-sim.org
# Use the Python section, and Cable Cell, Cell * pages in particular

import arbor
from math import sqrt

# Construct a cell with the following morphology.
# The soma (at the root of the tree) is marked 's', and
# the end of each branch i is marked 'bi'.
#
#         b1
#        /
# s----b0
#        \
#         b2

def make_cable_cell(gid):
    # (1) Build a segment tree
    # https://docs.arbor-sim.org/en/latest/concepts/morphology.html
    tree = arbor.segment_tree()

    # Soma (tag=1) with radius 6 μm, modelled as cylinder of length 2*radius
    s = tree.append(arbor.mnpos, arbor.mpoint(-12, 0, 0, 6), arbor.mpoint(0, 0, 0, 6), tag=1)

    # Single dendrite (tag=3) of length 50 μm and radius 2 μm attached to soma.
    b0 = tree.append(s, arbor.mpoint(0, 0, 0, 2), arbor.mpoint(50, 0, 0, 2), tag=3)

    # Attach two dendrites (tag=3) of length 50 μm to the end of the first dendrite.
    # Radius tapers from 2 to 0.5 μm over the length of the dendrite.
    b1 = TODO
    # Constant radius of 1 μm over the length of the dendrite.
    b2 = TODO

    # Associate labels to tags
    # https://docs.arbor-sim.org/en/latest/concepts/labels.html
    labels = arbor.label_dict()
    labels['soma'] = '(tag 1)'
    labels['dend'] = '(tag 3)'

    # (2) Mark location for synapse at the midpoint of branch 1 (the first dendrite).
    # https://docs.arbor-sim.org/en/latest/concepts/labels.html
    labels['synapse_site'] = TODO
    # Mark the root of the tree.
    labels['root'] = TODO

    # (3) Create a decor and a cable_cell
    # https://docs.arbor-sim.org/en/latest/python/decor.html
    decor = arbor.decor()

    # Put hh dynamics on soma, and passive properties on the dendrites.
    decor.paint('"soma"', 'hh')
    decor.paint('"dend"', 'pas')

    # (4) Attach a single synapse.
    decor.place('"synapse_site"', 'expsyn', 'syn')

    # Attach a spike detector with threshold of -10 mV.
    decor.place( TODO )

    cell = arbor.cable_cell(tree, labels, decor)

    return cell

make_cable_cell()
