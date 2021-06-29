import arbor

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

    # (8) Make a ring network. For each gid, provide a list of incoming connections.
    def connections_on(self, gid):
        src = (gid-1)%self.ncells
        w = 0.01
        d = 5
        weight = 0.1
        return [arbor.event_generator(arbor.cell_member(0,0), weight, sched)]

    def num_targets(self, gid):
        return 1

    def num_sources(self, gid):
        return 1

    # (9) Attach a generator to the first cell in the ring.
    def event_generators(self, gid):
        if gid==0:
            sched = arbor.explicit_schedule([1])
            return [arbor.event_generator(arbor.cell_member(0,0), 0.1, sched)]
        return []

    def probes(self, gid):
        return [arbor.cable_probe_membrane_voltage('"root"')]

    def global_properties(self, kind):
        return self.props

# (10) Instantiate recipe
ncells = 4
recipe = ring_recipe(ncells)
