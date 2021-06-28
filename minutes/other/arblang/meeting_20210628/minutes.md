# Arblang meeting 28.06.2021

## `var` and `real`
* Everything is `var` except constants and parameters. We can remove both `var` and `real` and use quantities instead (e.g. `voltage`, `conductance` etc.)
* Can/Should we have functions that accept all quantity types as arguments?
    * These functions shouldn't be too common. But if needed we can have some special type that accepts all quantities.

## State/init
* Merged or seperate?
    * Merged allows for reuse between `init` and `state`. For example the same kinetic system can be solved at steady state for `init` and solved normally for `state`.
    * If seperate how would we enable reuse between `state` and `init`?
        * SLACK convo building on SY proposal:
            * Let's say we have a kinetic scheme that defines a linear ODE system of 2 differential equations of the state variables `a` and `b`. This ODE system is stored in a record `state'` containing the derivatives of each of `a` and `b`. The record `state'` is returned by a function `evolve`.
            * Let's also say we want the `init` function to solve this ODE system at steady-state.
            * Kinetic schemes always produce underdetermined ODE systems, so solving at steady-state requires a starting point from which the steady-state should be considered to have been evolved. In NMODL, this is supplied using an extra `CONSERVE` statement.
            * `init` can be defined as follows: `initial steady_state from (initial state expression)`. Where `initial state expression` is a value of type `state`, and the ODE system we're trying to solve at steady-state is automatically retrieved from the `evolve` function. Let's say, for example, the `CONSERVE` statemet `a + b = 1` is needed to solve the previously defined kinetic scheme at steady-state. We would write `initial steady_state from { a = 0.4; b = 0.6; }` where any 2 values of `a` and `b` with sum equal to 1 would produce the same solution.
        * Transcript of extra notes from SLACK convo:
            * For non-linear ODE systems, the only way to determine steady state, if there even is one, is to try and integrate it empirically.
            *  On `initial steady_state from (initial state expression)`:
                *  If the ODE is `x' = f(x)`, and we can solve `f(x)=0` exactly, then the `initial state expression` would determine the values for `x` in the case that `f(x)=0` is underdetermined, as it would be in kinetic schemes for example.
                *  If the steady state solution is `xinf, xinf = lim t→∞ x(t)` where `x(0) = x₀` and  `x'=f(x)`, then "f" would be given by the `evolve` keyword, and "x₀" would be given by the thing in `initial steady_state from x₀`.
                *  The syntax could also be repurposed for the case when you want the initial state to be what you get after some integration period (I think Sebastian? brought up this use case?)
`initial integrate 3 ms from { a = 1; b = 2; }`.
            * For kinetic schemes at least we can determine the conserved linear subspaces, so it's fairly straightforward [to solve at steady-state]. For general ODEs, more tricky. But even knowing the invariant subspaces, it's not guaranteed there is a steady state solution for a nonlinear kinetic scheme anyhow.
* What do the signatures look like?
* What do the ODEs look like?

## Timeline
- We should have an initial version of the language ready by September.
- We still need to think about:
    - Units.
    - Stochasitic differential equations.
    - State machines.
