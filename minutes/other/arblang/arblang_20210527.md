# Arblang 

The arblang project can be split into 2 (almost) independent problems: 
1. Designing the language.
2. Designing the compiler.

Both the language and the compiler need to interface with arbor in different ways: 
- State and current updates; events on synapses; ion parameters manipulation etc need an Arblang interface to arbor. (Part of the language design).
- The generated C++ code needs to interface with arbor and other simulators. This should be clearer now that we have a Mechanims ABI. (Part of the compiler design).
- We need to discuss how and when to compose mechanisms, and what kind of compositions we allow. And if and how we would use LLVM for that purpose. (Part of the compiler design).

We can follow a top-down approach and start with designing the language. This is a prerequisite for designing the compiler and will guide the decisions we have to make there.

The rest of this page is dedicated to the **language design**.

# The Integration pipeline

Different parts of the integration pipeline are/will be programmable using Arblang.

> Diagram: A simplification of the integration loop from the POV of mechanisms . 
> LHS: The integration loop. RHS: The resources available to the integration loop. 
> LHS: green blocks are programmable; red blocks are not; purple blocks will be.
> The directions of the arrows indicate the relationship between the blocks. An arrow originating from block "1" on the RHS to block "A" on the LHS indicates that block "1" is an input of block "A". An arrow originating from block "A" on the LHS to block "1" on the RHS indicates that block "1" is an output of block "A".
> The main blue arrow originating from the RHS to the LHS indicates that all the blocks on the LHS have access to all the resources on the RHS.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_a5f32566980c734ca954c5933180b93a.png)


# The Language

#### General requirements for arblang: 
- Declarative style.
- Restricted set of features and tools. 
- Extendable. 
- Well defined. 
- Well documented.
- Capable of representing small fragments of user-supplied code as well as entire mechanisms.

#### Feature requirements: 
1. An interface to arbor and CV state without using "magic" variables. 
2. A declarative way of representing:
    - ODEs
    - Kinetic schemes
    - Linear systems (Is this needed or can it be replaced by solving kinetic schemes at steady state?)
3. A representation for the mechanism state, and separately, the mechanism parameters. 
4. A format for declaring current and state updates. 
5. A format for receiving events (both from other cells, and self-events for plasticity).
6. A format for manipulating ion parameters. 
7. A method for selecting how ODEs should be solved. 
8. Unit representation, conversion and checking. 

#### Language style requirements:
1. The language itself should have enough sugar to make it appealing to users. 
2. Simple branching, with no side effects. If we can get away with just the C++ ternary operator that would be ideal. 
3. Simple functions, with no side effects. 
4. No recursion allowed. 
5. No loops allowed. 
6. No arrays. 
7. Structs and tuple for representing states, parameters, arguments and return values. 

## Proposal A : a pocedural language 

Somewhat inspired by **HLSL**: High Level Shading Language developed by Microsoft. 
> HLSL is a computer graphics language, used in 3D applications to program how to go from vertices and triangles to the pixels shown on the screen. In a nutshell, HLSL programs (called shaders) can be written for the different steps of the graphics pipeline (steps to go from vertices to pixels).

- Shaders are analogous to the mechanism methods (initialization, state update, current update etc.): they both apply to a predefined set of objects (vertices or CVs), they need information about the state of objects (positions, colors or voltages, concentrations), and they transform the state of the objects in some way. They can also have an internal state. 
- We can take inspiration for how to bind arguments to simulator state. 

### Example A1 - Density mechanism (Ih.mod mechanism from the allen catalogue).

```
// Variables in 'parameters' and 'constants' are global variables.
// Block structure used to help keep files organized.

// Read only - may be overridden by simulator
parameters {
  real gbar = 0.00001, // typed fields
  real ehcn = -45
}

// Read only and constant - can not be read or written by simulator.
constants {
  real pi = 3.14159
}

/* An alternative to `parameters` and `constants`: Global values outside 
   of any scope.
   
mutable real gbar = 0.00001 // Can be overridden by simulator.
mutable real ehcn = -45     // Can be overridden by simulator.
const real pi = 3.14159     // Can not be overridden by simulator.
*/

// Struct containing main mechanism state.
struct mech_state {
  real m  // typed fields
}

// Define helper functions
// Functional style (inspired by Scala / OCAML)
// Typed arguments and return values.
// Functions can return single values, structs or tuples. 
def vtrap(real x, real y) -> real {
  y*exprelr(x/y)
}

def malpha(real v) -> real {
  0.001*6.43*vtrap(v+154.9, 11.9)
}

def mbeta(real v) -> real {
  0.001*193*exp(v/33.1)
}

// The following functions are pure. 
// They do not represent the interface to the simulator. 
def init(real v) -> mech_state {
  let t = malpha(v)
  let m = t/(t + mbeta(v))
     
  // Structs can be constructed from tuples of matching fields 
  // or single values in the case of a struct with one field.
  mech_state(m)
}

// Functions can return single values, structs or tuples. Here, a struct.
def state(real v, mech_state in) -> mech_state {
  let a = malpha(v)
  let b = mbeta(v)

  // ODEs are written in terms of `symbols`
  let m  = sym()
  let ode_m = (m` == a - m * (a + b))
  // solve takes as arguments an ODE, and a tuple binding the used 
  // symbol to its initial value. It returns a tuple of the new 
  // value of the symbol.
  // The returned tuple is used to create the new mech_state.
  mech_state(solve(ode_m, (m, in.m)))
}

// Functions can return single values, structs or tuples. Here, a tuple
def current(real v, mech_state in) -> (real, real) {
  let g = in.m * gbar
  let i = g * (v - ehcn)
  (i, g)
}

// The following functions represent the interface to the simulator. 
// They bind arguments and outputs to simulator variables.
// Functions don't have or need access to all variables by default.
// Inputs and outputes are selected via 'binding'.

// Bindings starting with `SIM` bind to simulator state. 
// Currently all simulator state is exposed as `real` variables.
// Bindings starting with `MECH` bind to mechanism state. 
// Currently only MECH_STATE is allowed and it binds to the user-defined 
// struct containing all the mechanisms state variables.

// The compiler can check the validity of the signature of the following
// functions by checking read/write permissions. 

// The names of these functions can either be predefined, 
// or selected by the user and indicated to the compiler.

defg initialize(real v: SIM_VOLTAGE) -> mech_state: MECH_STATE {
  init(v)
}

defg update_state(real v: SIM_VOLTAGE, mech_state in: MECH_STATE) -> 
  mech_state: MECH_STATE {
  state(v, in)
}

defg update_current(real v: SIM_VOLTAGE, mech_state in: MECH_STATE) -> 
  (real: SIM_NONSPECIFIC_CURRENT, real: SIM_CONDUCTANCE) {
  current(v, in)
}
```

### Example A2 - kinetic scheme

Nmodl representation: 
```
KINETIC state {
    LOCAL alpha, beta, gamma, delta
    alpha = f_alpha(v)
    beta  = f_beta(v)
    gamma = f_gamma(v)
    delta = f_delta(v)

    ~ s <-> h (alpha, beta)
    ~ d <-> s (gamma, delta)
}
```

Arblang representation:
```
struct mech_state {
  real s, 
  real d, 
  real h
}

def state(real v, mech_state in) -> mech_state {
  let alpha = f_alpha(v)
  let beta  = f_beta(v)
  let gamma = f_gamma(v)
  let delta = f_delta(v)
  
  let s = sym()
  let h = sym()
  let d = sym()
  
  // Kinetic reaction system defined as a list of reactions. 
  // Only situation where a list can be used. 
  let kin = [s <-> h (alpha, beta),
             d <-> s (gamma, delta)] 
             
  // solve takes as an argument the reaction system and
  // a tuple of the previous values of s, d, and h.
  // It returns a tuple of the new values of s, d and h, 
  // in the same order they were passed to the function.
  // The tuple is used to create the new mech_state object.
  mech_state(solve(kin, ((s, in.s), (d, in.d), (h, in.h))))
}
```

### Example A3 - Point mechanism (expsyn.mod from the default catalogue)

```
parameters {
  real tau = 2.0,
  real e = 0
}

struct mech_state {
  real g
}

def init() -> mech_state {
  mech_state(0)
}

def state(mech_state in) -> mech_state {
  let g  = sym()
  let ode_g = (g’ == g/tau)
  mech_state(solve(ode_g, (g, in.g)))
}

def current(real v, mech_state in) -> real {
  in.g * (v - e)
}

def event(real weight, mech_state in) -> mech_state {
  in.g + weight
}

// Define mechanism functions
defg initialize() -> mech_state: MECH_STATE {
  init()
}

defg update_state(mech_state in: MECH_STATE) -> mech_state: MECH_STATE {
  state(v, in)
}

// If the current update doesn't return a conductance value, 
// it should be inferred by the compiler.
defg update_current(real v: SIM_VOLTAGE, mech_state in: MECH_STATE) 
  -> real: SIM_NONSPECIFIC_CURRENT {
  current(v, in)
}

defg receive_event(real weight: SIM_WEIGHT, mech_state in: MECH_STATE)
  -> mech_state: MECH_STATE {
  event(weight, in)
}
```

### Example A4 - Ion concentrations (CaDynamics_E2.mod from the bbp catalogue)

```
// Global variables - can be overridden by simulator
parameters {
  real F       = 96485.3321233100184,
  real gamma   = 0.05,
  real decay   = 80,
  real depth   = 0.1,
  real minCai  = 1e-4,
  real initCai = 5e-5
}

// This is not the mechanism state, because the contained 
// variable is ultimately owned by the simulator.
// A struct is not needed, but is used for illustration. 
struct ion_state {
  real cai
}

def init() -> ion_state {
  ion_state(initCai)
}

// This function returns a struct. However, the tuple returned by `solve` 
// could have been returned instead. 
def state(real ica, ion_state s) -> ion_state {
  let cai = sym()
  let ode = (cai` == -5000*ica*gamma/(F*depth) - (cai - minCai)/decay)
  ion_state(solve(ode, (cai, s.cai)))
}

// `init` returns a struct. But `mech_init` needs to return a real value 
// to bind to a simulator variable   
defg mech_init() -> real : SIM_ION_INT_CONC("ca") {
  init().cai
}

// Similarly, state needs a struct argument and returns a struct. 
// `update_state` needs real values to interface with the simulator. 
defg update_state(real ica: SIM_ION_CURRENT("ca"), 
                  real cai: SIM_ION_INT_CONC("ca")) 
  -> real : SIM_ION_INT_CONC("ca") {
  state(ica, ion_state(s)).cai
}
```

### Language A syntax

- Functions: 
    - Defined using `def`.
    - Need type annotations for arguments and results.
    - Return the last expression.
    - Cannot have argument or return type bindings to the simulator.
```
def foo (type x, type y) -> type {
    z
}
```

- Interface or "glue" functions: 
    - Defined using `defg`. 
    - Need type annotations and binding to the simulator for every argument and for the return values.
    - Return last expression. 
    - Either have predefined names, or the user decides on the names and indicates them to the compiler.

```
defg update_state(real v: SIM_VOLTAGE, mech_state in: MECH_STATE) 
  -> mech_state: MECH_STATE {
  state(v, in)
}
```

- Conditionals: 
    - Return a result which must be bound to a varible. 
    - else is mandatory.
    - Braces are optional.
```
let x = if p {a} else {b}
```

- Variable bindings: 
    - Scope is the next statement.
    - Can lead to complex statements. 

```
let a = ...
let b = ...
foo(a, b)
```
```
let g = let a = v*v a/p1 + a/p2 g*3

// Equivalent to:
// let g = (let a = v*v {a/p1 + a/p2}) 
// g*3
```

- Tuples: 
    - Used to initialize structs with compatible fields.
    - Used to bind symbols to previous values in ODEs/Reactions.
    - Used as arguments or return values of functions.
    - Interface functions that return multiple values, should return them in the form of tuples. 
    - To destructure, bind to multiple variables. 
```
struct foo {
  real x, 
  real y,
  real z
}

bar = foo(1, 2, 3)
let a, b, c, = bar
```
```
kin = ... 
// Nested tuple
let a, b = solve_kin(kin, ((v0, 0), (v1, 1)))
```

- Structs: 
    - Equivalent to named tuples with named fields.
    - New objects can be created from a tuple with the same fields.
    - Members accessible by name. 
```
struct foo {
  type x, 
  type y
}
let bar = foo(1, 2)
let sum = bar.x + bar.y 
```

- Symbols: 
    - Used in ODEs, reactions, linear systems.
    - Need to be bound to a previous values when solving ODEs or reactions.
```
let a = sym()
```

- ODEs: 
    - Integrated variables must be symbols.
    - use `==` instead of `=` 
```
let a = ...
let b = ...
let m  = sym()
let ode = m` == a - m * (a + b)
```

- Kinetic schemes: 
    - List of reactions with forward and backward rates.
    - Can also include regular ODEs.
    - Integrated variables must be symbols.
```
let alpha = ...
let beta = ...
let s = sym()
let h = sym()
let d = sym()
let m = sym()
let kin = [s <-> h (alpha, 2*alpha),
           d <-> s (beta, 3*beta), 
           m' == alpha*m - beta] 
```

- Solving ODEs and kinetic reactions 
    - The `solve`, method.
    - Arguments are the ODE/reactions; and a tuple of symbol to previous value bindings. 
    - A third argument can be added as a hint to the solver. 
    - `solve` returns a tuple corresponding to the new values of the symbols, in the order they were provided. 
```
my_struct {
  real m
}

...
let a = ...
let b = ...
let m = sym()
let ode = (m` == a - m * (a + b))
my_struct(solve(ode, ((m, 0))))
```
```
let input = ...
let a = ...
let b = ...

let s = sym()
let d = sym()
let m = sym()

let kin = [s <-> d (a, b), m' == a*m - b] 
let new_s, new_d, new_m = solve(kin, ((s, input.s), (d, input.d), (m, input.m)))
```

- Bindings:
    - Input to all mechanism methods:
        - SIM_VOLTAGE
        - SIM_TEMPERATURE
        - SIM_DIAMETER
        - SIM_ION_CURRENT("ion_name")
        - SIM_ION_INT_CONC("ion_name")
        - SIM_ION_EXT_CONC("ion_name")
        - SIM_ION_REV_POT("ion_name")
        - MECH_STATE
    - Input to method receiving events:
        - SIM_WEIGHT
    - Input to method processing self-events:
        - SIM_TIME_SINCE_SPIKE
    - Output of method updating current: 
        - SIM_NONSPECIFIC_CURRENT
        - SIM_CONDUCTANCE
        - SIM_ION_CURRENT("ion_name")
    - Output of method initializing/updating state: 
        - SIM_ION_INT_CONC("ion_name")
        - SIM_ION_EXT_CONC("ion_name")
        - MECH_STATE
    - Output of methods receiving events/processing self-events:
        - MECH_STATE


## Proposal B : a symbolic language 

The Integration pipeline puts us in a procedural mindset: `update_state` and `update_current` are called in a loop where they calculate new values based on previous ones. However, the mechanisms themselves are more mathematical in nature: `state` and `current` can be used to define the system once, not to describe the explicit change at every time step. For example, a mechanism with no ions and one state variable `m` should be capable of being described using the following formulas:

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_12357c95318ecf3d5f8edbb454c55599.png)

The following language proposal takes a more symbolic and functional route. The main diffenece from the procedural language proposal is the `var` type. 

- `var` is a varying quantity: a function of some other variable, such as time. 
- `var` is differentiable. 
- The derivative of `var`: `var’` does not exist by itself, it is part of the definition of `var`. So, a function cannot have a `var’` as an argument or a return value, only `var`, which may or may not have a defined derivative.
- Given an object of type `var`, the value of its derivative can be defined using an ODE or kinetic reaction. 
- An object of type `var` is well-defined if it is a function of other `var` objects, or if its derivative is well defined, and its initial value is known.

If `var`is defined as an ODE + initial state, then the initial state is expected to be set up in the `init` function. This can be awkward because we split the definition of `var` into 2 stages, but is a bit closer to the familiar nmodl interface. (Check proposal C for an alternative).

### Example B1 - Density mechanism (Ih.mod mechanism from the allen catalogue)

```
// Global values outside of any scope.
mutable real gbar = 0.00001 
mutable real ehcn = -45    
const real pi = 3.14159    

struct mech_state {
  var m  // m has type “var”; is an implicit function of time
}

// Helper functions can be in terms of “var” or “real”
// operations between “var” and “real” are well-defined 
def vtrap(var x, real y) -> var {
  y*exprelr(x/y)
}

def malpha(var v) -> var {
  0.001*6.43*vtrap(v+154.9, 11.9)
}

def mbeta(var v) -> var {
  0.001*193*exp(v/33.1)
}

// "init" sets up the system prior to the start of the simulation
def init(var v) -> mech_state = {
  let t = malpha(v)
  mech_state(t/(t + mbeta(v)))
}

// "state" returns a mech_state with well-defined derivatives
// The initial values of the ODEs are set up in "init".
def state(var v) -> mech_state {
  let a = malpha(v)
  let b = mbeta(v)

  // The construction of mech_state is special: 
  // Reactions or ODEs could be used.
  // m is exposed and can be used inside the constructor. 
  
  mech_state(m’ = a - m * (a + b))
  
  // The previous line is equivalent to: 
  //   let m = var()
  //   m' =  a - m * (a + b)
  //   mech_state(m)
}

// "current" defines the current contribution in terms of objects of type "var"
def current(var v, mech_state in) -> (var, var) {
  let g = in.m * gbar
  let i = g * (v - ehcn)
  (i, g)
}

// Mechanism callback binidngs
defg initialize(var v: SIM_VOLTAGE) ->mech_state: MECH_STATE { 
  init(v) 
}
defg update_state(var v: SIM_VOLTAGE) -> mech_state: MECH_STATE {
  state(v) 
}
defg update_current(var v: SIM_VOLTAGE, mech_state in: MECH_STATE) 
  -> (var: SIM_NONSPECIFIC_CURRENT, var: SIM_CONDUCTANCE) {
  current(v, in)
}
```

### Example B2 - kinetic scheme

Nmodl representation: 
```
KINETIC state {
    LOCAL alpha, beta, gamma, delta
    alpha = f_alpha(v)
    beta  = f_beta(v)
    gamma = f_gamma(v)
    delta = f_delta(v)

    ~ s <-> h (alpha, beta)
    ~ d <-> s (gamma, delta)
}
```

Arblang representation:
```
struct mech_state {
  var s, 
  var h, 
  var d
}

def state(var v) -> mech_state {
  let alpha = f_alpha(v)
  let beta  = f_beta(v)
  let gamma = f_gamma(v)
  let delta = f_delta(v)

  // The constructor of a mech_state is special:
  // - It accepts any number of statement.
  // - Statements can be ODEs or reactions.
  // - Members of the struct can be used in the statement definitions.
  // - If derivative expressions are provided for each member of the struct, 
  //   the constructor is considered valid. 
  // The initial values of the ODEs should be set up in "init"
  
  mech_state(s <-> h (alpha, beta),
             d <-> s (gamma, delta))

  // The previous line is equivalent to: 
  //   let s = var()
  //   let d = var()
  //   let h = var()
  //   s <-> h (alpha, beta)
  //   d <-> s (gamma, delta)
  //   mech_state(s, h, d)
}
```

### Example B3 - Point mechanism (expsyn.mod from the default catalogue)

```
parameters {
  real tau = 2.0,
  real e = 0
}

struct mech_state {
  var g
}

def init() -> mech_state {
  mech_state(0)
}

def state() -> mech_state {
  mech_state(g’ = g/tau)
}

def current(var v, mech_state in) -> var {
  in.g * (v - e)
}

def event(real weight, mech_state in) -> mech_state {
  in.g + weight
}

// Mechanism callbacks
defg initialize() -> mech_state: MECH_STATE {
  init()
}

defg point_state() -> mech_state: MECH_STATE {
  state(in)
}

defg point_current(var v: SIM_VOLTAGE, mech_state in: MECH_STATE) ->      
  real: SIM_NONSPECIFIC_CURRENT {
  current(v, in)
}

defg receive_event(real weight: SIM_WEIGHT, mech_state in: MECH_STATE) 
 -> mech_state: MECH_STATE {
 event(weight, in)
}


```

### Example B4 - Ion concentrations (CaDynamics_E2.mod from the bbp catalogue)

```
// Global variables - can be overridden by simulator
parameters {
  real F       = 96485.3321233100184,
  real gamma   = 0.05,
  real decay   = 80,
  real depth   = 0.1,
  real minCai  = 1e-4,
  real initCai = 5e-5
}

struct ion_state {
  var cai
}

def init() -> ion_state {
  ion_state(initCai)
}

def state(var ica) -> ion_state {
  ion_state(cai’ = -5000*ica*gamma/(F*depth) - (cai - minCai)/decay)
}

defg mech_init() -> var : SIM_ION_INT_CONC("ca") {
  init().cai
}

defg update_state(var ica: SIM_ION_CURRENT("ca")) -> 
   var : SIM_ION_INT_CONC("ca") {
  state(ica).cai
}

```

### Language B syntax

> Functions, glue function, conditionals, variable bindings, tuples and bindings are identical to proposal A and are omitted.

- Structs: 
    - Equivalent to named tuples with named fields.
    - New objects can be created from a tuple with the same fields.
    - Members accessible by name. 
    - For structs with `var` members: to simplify defining `var` derivatives, a struct object can be constructed from one or more ODEs or reactions. The members are accessible in the constructor. 

```
struct foo { var x, var y }

// Construct a system of ODEs and assign
// the derivatives of each `var` member 
foo(x’ = 2*x, x <-> y (1, 2))  
```

- ODEs: 
    - Used to construct the derivative of a `var` object. 
```
let m  = var()
// define the derivative of m
m’ = a - m * (a + b) 
```

- Reactions: 
    - Converted to ODEs. 
```
let s = var()
let d = var()
let h = var()
s <-> h (alpha, 2*alpha)  
d <-> s (beta,  3*beta)

// Reactions are equivalent to: 
// s' = (-alpha -3*beta)*s + 2*alpha*h + beta*d
// h' = alpha*s - 2*alpha*h
// d' = 3*beta*s - beta*d
```

## Proposal C : a symbolic language 

This proposal is very similar to proposal B. It also uses the `var` type. As mentioned, an object of type `var` is well-defined if it is a function of other `var` objects, or if its derivative is well defined, and its initial value is known.

Proposal B splits the definitions of the derivative and the initial value of a `var`. This proposal unifies the definition of `var` and removes the `init` callback function.

### Example C1 - Density mechanism (Ih.mod mechanism from the allen catalogue)

```
// Global values outside of any scope.
mutable real gbar = 0.00001 
mutable real ehcn = -45    
const real pi = 3.14159    

struct mech_state {
  var m  // m has type “var”; is an implicit function of time
}

// Helper functions can be in terms of “var” or “real”
// operations between “var” and “real” are well-defined 
def vtrap(var x, real y) -> var {
  y*exprelr(x/y)
}

def malpha(var v) -> var {
  0.001*6.43*vtrap(v+154.9, 11.9)
}

def mbeta(var v) -> var {
  0.001*193*exp(v/33.1)
}

// state returns a mech_state with well-defined derivatives
// and initial values
def state(var v) -> mech_state {
  let a = malpha(v)
  let b = mbeta(v)
  let t = a/(a+b)
  // The construction of mech_state is special: 
  // Reactions or ODEs could be used. m, a and b 
  // m is exposed and can be used inside the constructor. 
  
  mech_state(m.init = t.init, m’ = a - m * (a + b))

  // Equivalent to: 
  //   let m = var()
  //   m.init = t.init
  //   m’ = m’ = a - m * (a + b)
  //   mech_state(m)
}

def current(var v, mech_state in) -> (var, var) {
  let g = in.m * gbar
  let i = g * (v - ehcn)
  (i, g)
}
```

### Example C2 - kinetic scheme

Nmodl representation: 
```
KINETIC state {
    LOCAL alpha, beta, gamma, delta
    alpha = f_alpha(v)
    beta  = f_beta(v)
    gamma = f_gamma(v)
    delta = f_delta(v)

    ~ s <-> h (alpha, beta)
    ~ d <-> s (gamma, delta)
}
```

Arblang representation:
```
struct mech_state {
  var s, 
  var h, 
  var d
}

def state(var v) -> mech_state {
  let alpha = f_alpha(v)
  let beta  = f_beta(v)
  let gamma = f_gamma(v)
  let delta = f_delta(v)

  mech_state(s.init = ...,
             h.init = ..., 
             d.init = ..., 
             s <-> h (alpha, beta),
             d <-> s (gamma, delta))

  // Equivalent to: 
  //   let s = var() 
  //   let d = var()
  //   let h = var()
  //   s.init = ... 
  //   d.init = ... 
  //   h.init = ...
  //   s <-> h (alpha, beta)
  //   d <-> s (gamma, delta)
  //   mech_state(s, h, d)
}

```

### Example C3 - Point mechanism (expsyn.mod from the default catalogue)

```
parameters {
  real tau = 2.0,
  real e = 0
}

struct mech_state {
  var g
}

def state() -> mech_state {
  mech_state(g.init = 0, g’ = g/tau)
}

def current(var v, mech_state in) -> var {
  in.g * (v - e)
}

def event(real weight, mech_state in) -> mech_state {
  in.g + weight
}

defg point_state() -> mech_state: MECH_STATE {
  state(in)
}

defg point_current(var v: SIM_VOLTAGE, mech_state in: MECH_STATE) ->      
  real: SIM_NONSPECIFIC_CURRENT {
  current(v, in)
}

defg receive_event(real weight: SIM_WEIGHT, mech_state in: MECH_STATE) 
 -> mech_state: MECH_STATE {
 event(weight, in)
}
```

### Example C4 - Ion concentrations (CaDynamics_E2.mod from the bbp catalogue)

```
// Global variables - can be overridden by simulator
parameters {
  real F       = 96485.3321233100184,
  real gamma   = 0.05,
  real decay   = 80,
  real depth   = 0.1,
  real minCai  = 1e-4,
  real initCai = 5e-5
}

struct ion_state {
  var cai
}

def state(var ica) -> ion_state {
  let t = -5000*ica*gamma/(F*depth)
  ion_state(cai.init = initCai, 
            cai’ = t - (cai - minCai)/decay)
}

defg update_state(var ica: SIM_ION_CURRENT("ca")) -> 
   var : SIM_ION_INT_CONC("ca") {
  state(ica).cai
}

```

### Language C syntax

> Functions, glue function, conditionals, variable bindings, tuples, ODEs, reactions and bindings are identical to proposal B and are omitted.

- `var`: 
    - Defined as a function of other `var` objects. 
    - Or as an ODE + initial state. 
    - ODE is defined by assigning `name'`, initial state is defined or accessed by assigning `name.init`. 

- Structs: 
    - Equivalent to named tuples with named fields.
    - New objects can be created from a tuple with the same fields.
    - Members accessible by name. 
    - For structs with `var` members: to simplify defining `var` derivatives and initial values, a struct object can be constructed from one or more ODEs, reactions and initial values. The members are accessible in the constructor. 

```
struct foo { var x, var y }

// Construct a system of ODEs and assign
// the derivatives and initial values of each `var` member 
foo(x’ = 2*x, 
    x <-> y (1, 2), 
    x.init = 2, 
    y.init = 0)  
```

## Open questions: 
- How to represent units? how much support for automatic conversion? which version of arblang?
- Is mechanism composition a language feature or a compiler feature or both?
- How are reversal potential updates different from the state and current updates? Do they need their own mechanism method? 
