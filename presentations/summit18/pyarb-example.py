#!/usr/bin/python3

import pyarb as arb

class ring_recipe(arb.recipe):
  def __init__(self, n):
    super().__init__()
    self.ncells = n

  def num_cells(self):
    return self.ncells

  # each cell is a soma-only cell
  def cell_description(self, gid):
    cell = arb.make_soma_cell()
    loc = arb.segment_location(0, 0.5)
    cell.add_synapse(loc)
    cell.add_detector(loc, 20)

    if gid==0: # add a stimulus to first cell
      cell.add_stimulus(loc, 0, 20, 0.01)

    return cell

  # 1 synapse target on each cell
  def num_targets(self, gid):
    return 1

  # 1 spike detector on each cell
  def num_sources(self, gid):
    return 1

  # all cells are multi-compartment
  def kind(self, gid):
    return arb.cell_kind.cable1d

  # each cell has one
  # incoming connection from
  # the cell with gid-1
  def connections_on(self, gid):
    src_id = (gid-1) % self.ncells
    src = arb.cell_member(src, 0)
    tgt = arb.cell_member(gid, 0)
    return [arb.connection(src, tgt, 0.1, 10)]

# get parallel arbor context
# by default takes all
# available cores and GPUs
ctx = arb.context()

# make a 4 cell ring
recipe = ring_recipe(4)

# make the simulation
sim = arb.simulation(recipe, ctx)

# get a spike recorder
recorder = arb.make_spike_recorder(sim)

# run simulation for 100 ms
sim.run(100, 0.025)

# print the spikes
for spike in recorder.spikes:
  print('cell {} at {:8.3f} ms' \
        .format(spike.source.gid, spike.time))
