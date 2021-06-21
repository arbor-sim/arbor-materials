ArbLang 21.06.2021
==================

## Meeting minutes
  -  Went over langauge proposals from last meeting (27.05.2021).
      - Is `var` needed? Everything can be thought of as a varying quantity, the entire language is symbolic. The language can still be typed, but the type can then describe the quantity contained in an object such as `voltage`, `concentration` etc. 
      - Comment from BC. Instead of:
      ```
      let m = mech_state(m.init = t.init, m' = m*(a-b))
      ```
      try: 
      ```
      let m = mech_state(m.init = t, m' = a - m*(a+b))
      ```
      or: 
      ```
      let m = var(t, rate*(a-b))
      ```
      - Things we agree on
        - Functional language, clarification
          - No mutable global state.
          - No reassigning variables.
          - All functions are pure incl Sim Interface.
        - Typed, maybe quantified.
        - Keep simulator bindings separate from function defeinitions.
      - Issues we should settle next: 
          - initialization and state definition functions: should they be merged or split? Arguments for splitting: 
              1. Allows a description in terms of pure functions. Merging would complicate the type system. 
              2. Allows more clarity for complex initializtions, for example solving a linear system at steady state. (NA comment: This is one of the reasons I merged `init` and `state`. They share a lot of logic, for example a kinetic scheme can be used to initialize the values of state variables (by solving at steadystate) and then also update their values. Doing this in the same spot would make sense.)
          - How do quantity types (`volatge`, `current` etc) fit into the language? Do they play a role in the simulator bindings?
      - Features that are yet to be discussed (pointed out by SY)
          - State machines.
          - Stochastic processes.
          - Units.  
     
## TH comments
- `var` vs `real` seems a bit weird for some reasons
  - utility functions need to be generic over `var`iability
  - Can `var` be a subtyping specifier, ie `var real` can be used as a `real` and decays to the current value.
  - Assume `var x; real y; x = y` what happens? It seems that `var`s can only be set once.
  - TH: I would prefer to do away with `var`. Saying `real y = var(42, y)` could be enough to get an ODE where `y(t=0)` and `y'(t) = y(t)`. The issue here is that we singled out this `var` thing as we cannot write
    ```
    let x = 42;
    let z = y; // Huh?
    let y = var(x, y);
    ```
  - However, the same issue exists in the current proposal. 
  - A way around this is to use `y = symbolic(), z = y, y = ode(42, y)`. But then we are back where we started and `=` has sometimes a different meaning. 
  - Potentially this could work
    ```
    ode Y {
        var y(t);     // Which variable are we using
        y(0) = 42;    // Initial
        y'(t) = y(t); // Derivative
    }
    let y_t = Y.y(t); // Get current value
    ```
    for a system
    ```
    ode S {
        var y(t), z(t);
        y(0) = 42;
        z(0) = 23;
        y'(t) = z(t);
        z'(t) = y(t)
    }
    let z_t = S.z(t); // Get current value
    ```

- Syntax Nitpicks
  - Please let us use (optional) trailing types, eg `let x: real = 42.0`
  - For sanity when parsing/error reporting, also let us use semicola `let x = 42;`

- Interface block instead of `defg`. Hasty example
  ```
  interface {
      state: my_state
      update: Ca.current -> Ca.int_conc = my_update
  }
  ```
  where `my_update` has a type _compatible_ with the one given in the interface, eg `real -> real` or `Concentration/Time -> Concentration`.

- SY
  - Discrete Domains governed by different ODEs
  - Need SDE (Arborio)
  - May need non-ensemble dynamics, ie ion counts instead of concentration
  - Units and quantities. TH likes this.

- Also, we will at some point need state machines.

