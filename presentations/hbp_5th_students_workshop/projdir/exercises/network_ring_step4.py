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
    tree = arbor.segment_tree()

    # Soma (tag=1) with radius 6 μm, modelled as cylinder of length 2*radius
    s = tree.append(arbor.mnpos, arbor.mpoint(-12, 0, 0, 6), arbor.mpoint(0, 0, 0, 6), tag=1)

    # Single dendrite (tag=3) of length 50 μm and radius 2 μm attached to soma.
    b0 = tree.append(s, arbor.mpoint(0, 0, 0, 2), arbor.mpoint(50, 0, 0, 2), tag=3)

    # Attach two dendrites (tag=3) of length 50 μm to the end of the first dendrite.
    # Radius tapers from 2 to 0.5 μm over the length of the dendrite.
    b1 = tree.append(b0, arbor.mpoint(50, 0, 0, 2), arbor.mpoint(50+50/sqrt(2), 50/sqrt(2), 0, 0.5), tag=3)
    # Constant radius of 1 μm over the length of the dendrite.
    b2 = tree.append(b0, arbor.mpoint(50, 0, 0, 1), arbor.mpoint(50+50/sqrt(2), -50/sqrt(2), 0, 1), tag=3)

    # Associate labels to tags
    labels = arbor.label_dict()
    labels['soma'] = '(tag 1)'
    labels['dend'] = '(tag 3)'

    # (2) Mark location for synapse at the midpoint of branch 1 (the first dendrite).
    labels['synapse_site'] = '(location 1 0.5)'
    # Mark the root of the tree.
    labels['root'] = '(root)'

    # (3) Create a decor and a cable_cell
    decor = arbor.decor()

    # Put hh dynamics on soma, and passive properties on the dendrites.
    decor.paint('"soma"', 'hh')
    decor.paint('"dend"', 'pas')

    # (4) Attach a single synapse.
    decor.place('"synapse_site"', 'expsyn')

    # Attach a spike detector with threshold of -10 mV.
    decor.place('"root"', arbor.spike_detector(-10))

    cell = arbor.cable_cell(tree, labels, decor)

    return cell

# (5) Create a recipe that generates a network of connected cells.
class ring_recipe (arbor.recipe):

    def __init__(self, ncells):
        # The base C++ class constructor must be called first, to ensure that
        # all memory in the C++ class is initialized correctly.
        arbor.recipe.__init__(self)
        self.ncells = ncells
        self.props = arbor.neuron_cable_properties()
        self.cat = arbor.default_catalogue()
        self.props.register(self.cat)

    # (6) The num_cells method that returns the total number of cells in the model
    # must be implemented.
    def num_cells(self):
        return self.ncells

    # (7) The cell_description method returns a cell
    def cell_description(self, gid):
        return make_cable_cell(gid)

    # The kind method returns the type of cell with gid.
    # Note: this must agree with the type returned by cell_description.
    def cell_kind(self, gid):
        return arbor.cell_kind.cable

    # (8) Make a ring network
    def connections_on(self, gid):
        src = (gid-1)%self.ncells
        w = 0.01
        d = 5
        return [arbor.connection((src,0), (gid,0), w, d)]

    def num_targets(self, gid):
        return 1

    def num_sources(self, gid):
        return 1

    # (9) Attach a generator to the first cell in the ring.
    def event_generators(self, gid):
        if gid==0:
            sched = arbor.explicit_schedule([1])
            return [arbor.event_generator((0,0), 0.1, sched)]
        return []

    def probes(self, gid):
        return [arbor.cable_probe_membrane_voltage('"root"')]

    def global_properties(self, kind):
        return self.props

# (10) Instantiate recipe
ncells = 4
recipe = ring_recipe(ncells)

# (11) Create a default execution context and a default domain decomposition.
context = arbor.context()
print(context)
decomp = arbor.partition_load_balance(recipe, context)
print(decomp)

# (12) Simulation init
sim = arbor.simulation(recipe, decomp, context)
sim.record(arbor.spike_recording.all)

# Attach a sampler to the voltage probe on cell 0.
# Sample rate of 10 sample every ms.
handles = [sim.sample((gid, 0), arbor.regular_schedule(0.1)) for gid in range(ncells)]

# (13) Run simulation
sim.run(100)
print('Simulation finished')

# (14) Results

# Print spike times

# Plot the recorded voltages over time.
print("Plotting results ...")

