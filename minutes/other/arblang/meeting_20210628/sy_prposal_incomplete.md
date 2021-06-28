# Broad outline

The aim of this proposal is a surface language that is primarily functional,
splitting the definition of a mechanism into a set of free function definitions
and a collection of bindings that describe how the dynamics of a mechanism are
implemented in terms of those functions.

This contrasts with a declarative approach that would define the evolutionary
dynamics of a mechanism in terms of an explicit ODE system (or similar).

## Components of a mechanism

From Arbor's point of view, a mechanism comprises:

*  A 'kind' — the mechanism is either a point or a
   density mechanism. (Leaving aside reversal potential mechanisms for now.)
*  A dynamic state, consisting of zero or more state
   variables which can be inspected by name.
*  A set of named scalar parameters whose values
   can be set at mechanism initialization time, and which are then constant.
*  A set of ion bindings which dictate which values
   of which ions can be read or modified by the mechanism.
*  A closed set of entry points called by Arbor to: initialize mechanism
   state; update state over an integration step; update non-specific and
   ionic currents and conductances; and update ionic concentrations.

NMODL provides (poorly) syntax for all these features, where state update
is described by a system of ODEs or a reaction system over the state variables.
State variables can also be updated directly, outside of an ODE description,
but due to implementation issues, these currently occur as part of the current
update phase.

## State evolution descriptions

In the surface language, we need to be able to describe state evolution
as at least an (explicit) ODE system or reaction system.

NMODL make a distinction between state evolution (via `DERIVATIVE` blocks)
and setting initial state. This distinction is useful for the case where
the initialization may be non-trivial: e.g. when the initial state should
correspond to a steady-state solution of the ODE system.

As noted above, NMODL quite happily mixes a description of non-integrative
state updates with current updates etc., which is not ideal. An approach
that capture both in a matematically neat way is to define the evolution
in terms of a state machine: each state is governed by an ODE description,
and transitions between states are described by threshold criteria or
by domain definitions, together with a transfromation of the state
vector.

We should also support, at least partially, dynamics described by a system
of stochastic differential equationds. For one-dimensional (time) processes,
these can typically be described in the form

> d _X_(_t_) = _f_(_X_,_t_) + _g_(_X_,_t_) d _W_(_t_)

where _W_ is the Wiender process, but with some abuse of notation, this
can be written like an ODE

> _X_' = _f_(_X_,_t_) = _g_(_X_,_t_)ζ(_t_)

where ζ represents (n-dimensional) Gaussian white noise. A symbolic
representation could then piggyback on a symbolic ODE representation with
a new special symbol representing ζ; a functional representaion as
proposed below would use an SDE binding that specified the evolution in
terms of the functions _f_ and _g_.

Other possible evolutions that we might want to include in the future include
stochastic partial differential equation systems, which include a noise term
with spatial correlations, and stochastic reaction systems that represent (part
of) the state in terms of species counts rather than continuous quantities, and
their evolution is govverned by a continuous time Markov process described in
turn by a system of reaction equations.

In the current state of Arbor, an ODE solver is determined automatically by
symbolic analysis of the provided ODE system. This can be performed also for
arblang, with or without explicit hints. Such hints fit more naturally where
the state evolution description is 'bound' to a mechanism interface in the
language, rather than as part of the ODE description itself.

## Ionic bindings

A mechanism can have ion dependencies, in that the state evolution can be
modulated by ionic concentrations, and that the current contributions can be
tied to specific ionic flows. More generally, a mechanism could be used to
describe the flux of a species across the mebrane, even if that species carries
no charge, though this cannot be specified in a natural way in NMODL.

While biophysical models are generally specified in terms of specific ionic
species, it can be useful to maintain multiple, distinct ionic populations of
the same species, and a parameterized mechanism might be repurposed to
represent the dynamics of a different ion without any changes to its
mathematical description. How should this sort of flexibility be represented in
an arblang mechanism description?

A couple of proposals are presented below in terms of the binding interface.

## Ion concentration evolution

NMODL makes no real distinction between mechanisms that describe ion channel
process and mechansisms that describe the evolution of ionic concentrations.

As the initial state of a mechanism can depend upon correct ion concentrations,
and as those concentrations may be set by a different mechanism governing ionic
concentrations, there arises a dependency problem. Additionally, what should it
mean if multiple mechanisms are responsible for maintaining the concentration
of the same ionic species?

A possible solution is to describe such processes by (literally) a different
class of mechanism; concentration mechanisms would have a different set of
bindings. Two approaches come to mind:

1.  An ion in any given region is governed by at most one such concentration
    mechanism. The mechanism can provide initial ion concentrations and a state
    evolution for a state which includes the relevant concentrations and which
    takes total ionic currents or fluxes as parameters.

2.  A concentration model provides only fluxes: it does not set the initial
    ionic concentration — this is supplied externally — and its state
    evolution, if any, does not include any explicit ion concentrations. Ionic
    updates are specified in terms of rates — instantaneous change in
    concentration per time. These could then be safely accumulated over
    multiple mechanisms, and a change in concentration would consitute a
    time integral over these rates. This would also be compatible with any
    diffusive processes we would want to incorporate in the future.

# Mechanism description proposal

A mechanism is defined by an interface specification that depends on the
sort of mechanism (e.g. point process, density process, concentration model).
In the interface block, keywords introduce: bindings of names to cellular
state or mechanism state; specification of user-visible parameters;
specfication of state evolution.

The expressions that are given in an interface block can be complete in
and of themselves, with optional typing (if no types, then types are
deduced). But they can also reference function definitions, constants
and parameters in one or more named _modules_.

## Expressions and types

Every expression has a type, which is either:
1. A boolean value.
2. A quantity (see below).
3. A record type, comprising an unordered sequence of named fields,
   with each field being either a quantity or another record type.

### Quantities

Quantities represent physical quantities, which in turn comprise
a magnitude and a physical dimension. The specific unit scale underlying
the representation of a physical quantity is implicit.

The special quantity `real` refers to a scalar value. Otherwise a
quantity is defined as a product term of basic quantities such
as voltage, time, resistance, etc. The set of basic quantities is
predefined, and can't be extended within arblang.

Examples:

```
real a;
voltage v;
current/area/time g'; # a time derivative of areal current density.
```

Expressions which evaluate to a given quantity follow normal algebraic
rules; constant values must be introduced with a compatible unit if
non-zero.

```
voltage v = 23 * 10 mV - 2 µV;
```

### Record types

Record types can be given names (aliases), or they can be anonymous, but any two
record values have the same type if they have the same set of field names
and types.

A record definition example:
```
record state {
    conductance g;
    real scale;
};
```

A record value is constructed from the name given to a record type, or
from an anonymous record specification, or derived from an existing
record value:

Examples:

```
   # From record alias:
   state { g = 3 mS; scale = 2; };

   # From explicit record type:
   record { conductance g; real scale; } { g = 3 mS; scale = 2; };

   # Implicitly:
   record { conductance g = 3 mS; real scale = 2; };

   # Implicitly with deduced field types:
   record { g = 3 mS; scale = 2; };

   # As a modification on an existing record value;
   state s = state { g = 3 mS; scale = 2; };
   s { scale = 3; };

   # As `s` doesn't have a field `u`, the following would be an error:
   s { u = 23; }
```

Except when constructing a record type by a field modification (the last
example), all fields must be given a value.

### Expressions

TODO: conditional expressions and boolean values.

Expressions include function expressions, algebraic expressions, let
expressions, and record field access. All identifiers must be bound
via a preceding interface binding statement, parameter declaration,
constant declaration, function definition, or let expression.

Let expressions are of the forms:
```
    let _optional type_ _identider_ = _value_ _expression_;
```
or
```
    with _optional type_ _record-valued expression_ _expression_;
```
The types are optional if they can be deduced from the provided value.
The `with` expression binds an identifier for each field of the record
to the corresponding field value.

## Modules

A module is a container for parameter definitions, constant definitions,
and function definitions. Modules can import other modules in order
to bring their names into scope.

Syntax:
```
module _identifier_ {
..
}
```

### Parameters and constants

Parameters are identifiers with a constant value which is given a default
value in the module, but which can also be potentially overridden by
a cell model. The expression on the right-hand side of a parameter declaration
is evaluated _after_ any user-provided settings.

The type of the parameter can be automatically deduced if omitted.
```
parameter scalar abc = 123;

parameter voltage erev = abc * 2 mV; # If abc value is changed, erev will change too.
```

Constants are essentially immutable parameters — they cannot be overridden in
cell models.
```
constant conductance g0 = 1.23 µS;
constant e0 = 23 mV; # type is deduced
```

### Function definitions

TODO.

## Interfaces

For now, have to look at example ...

# Example (WIP)
## Simple synapse


### Functions and common parameters are scoped in modules.

```
# Wrapping everything in a module allows us to more easily mix-and-match definitions
# and values across mechanism descriptions down the road.

module foo {

# "voltage" here specifies the quantity type of erev.

parameter voltage erev = -23 mV;

# The "parameter" keyword introduces a new parameter. The rhs should always be specified
# as a default parameter value, but should allow expressions in terms of previously
# declared parameter values too?

parameter time tau = 2.0 ms;

# There is nothing special about the name "state", it is just the name given to
# the record type.

record state {
    conductance g;
}

# "def" introduces a function definition.

def initial() -> state {
    # The name of a record type also acts as its constructor.
    # Every record field needs to be set, or else be taken from an existing value, or
    # else have a default value given in the record definition.

    state { g = 0; };
}

# "state'" is a struct that is automatically defined given a struct called "state".

def evolution(state s, voltage v) -> state' {
    state' {
        # Record field access is by dot.
        g' = -s.g / tau;
    };
}

# But there's nothing magic about "state'"; we could instead write:

record state_deriv {
    conductance/time g' = 0;
}

def evolution2(state s, voltage v) -> state_deriv {
    state_deriv {
        g' = -s.g / tau;
    };
}

# And maybe the record syntax is too clunky, so we can import field names into scope.
# "let" and "with" statements introduce a new scope for the following expression, and
# functions ultimately provide a single expression.

def evolution3(state s, voltage v) -> state' {
    with s; # equivalent to: "let g = s.g"
    state' {
        g' = g / tau;
    };
}

# All of "evolution", "evolution2", and "evolution3" have the same functional type
# and the same semantics, and should be able to be used interchangeably.

# This is a synapse model, so we'll also need a function that describes what happens
# on the receipt of a post-synaptic event.

def on_event(state s, real weight) {
    state {
        g = s.g + weight * 1 µS  # explicit scaling of weight required for unit correctness.
    };
}

} # end of module definition
```

### Functions and parameters are bound to models in a separate declaration

```
# 'point_process' is one of the available model types; others would include
# e.g. 'distributed_process', 'concentration_model', and others as we need
# them. Each model type can have different sorts of bindings.

# Interface names are used to reference the model from cell descriptions etc.
# Could be a free string as here, or instead an identifier.

interface point_process "exponential synapse" {
    # Names on the right-hand side of a bind refer to external (cell) quantities.
    # Identifiers on the left-hand side can then be used in expressions below.
    bind v = membrane_voltage;

    # We could have put this interface definition inside the module 'foo', but
    # if it's outside, we need to import the module to make the names available.
    # Could also write e.g. import foo as bar;
    import foo;

    # Parameters have to be explicitly made public.
    parameter tau = foo.tau;

    # But a parameter can also be published under a new name:
    #
    # parameter τ = foo.tau;
    #
    # Functions in the foo module still see the value in `tau`, but external
    # cell descriptions reference that as `τ`, and further, the name `τ` can
    # be used in rhs expressions below.
    #
    # A parameter doesn't have to live in a module, but then it is only visible
    # in the rhs expressions below:
    #
    # parameter ρ = 3 Ω·meter;
    #
    # Type qualifications on `bind` and `parameter` are optional, if the type
    # can be deduced from the rhs.

    # State and state evolution:
    # A name for the state can be given with bind.
    bind S = process_state;

    # Initial value (and type); rhs is an expression.
    initial foo.initial();

    # Governing ODE. Bound names and parameters can be used in rhs expression.
    evolve foo.evolution(S, v);

    # Handling discrete event: ev is an identifier bound to the real-valued event weight.
    when event ev do foo.on_event(S, ev);

    # Postsyn event synax? t is an identifier bound to the time-valued event delay.
    # when postsyn t do foo.on_post_event(S, t);

    # Types in event-driven when clauses are optional, e.g.:
    # when event real ev do foo.on_event(S, ev);
    # when postsyn time t do foo.on_event(S, ev);

    # Possible general stateful syntax:
    # when _condition_ [ do _state-valued expression_ ] then _state'-valued expression_;

    # Current contribution:
    # Here the current expression is a simple expression, but it could have been a
    # function evaluation. We haven't bound any ion names, so this is a 'non-specific'
    # current.

    current = S.g * v;
}
```
