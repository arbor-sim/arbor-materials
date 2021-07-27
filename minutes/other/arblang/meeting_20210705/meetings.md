Arblang meeting 05.07.2021
==========================
- Extra meeting minutes at the bottom.
- [NA] prepared the doc prior to the meeting with some questions. The answers to the questions are **highlighted** in the text and surrounded by ** **  in the code. 

## Language proposal
- Sam's language proposal from last week is popular with the team. 
- We can use it as a first draft for what Arblang is going to look like. 

## Formalizing the details
(Most of the following is copied from Sam's proposal)

Expressions include:
- function expressions
- algebraic expressions
- let expressions
- conditional expressions
- record field access

All identifiers must be bound via a preceding:
- interface binding statement
- parameter declaration
- constant declaration
- function definition
- let expression

Every expression has a type, which is either:
- A boolean value
- A quantity
- A record type

### Quantities 
- Represent physical quantities, which in turn comprise a magnitude and a physical dimension. The specific unit scale underlying the representation of a physical quantity is implicit.
- The special quantity `real` refers to a scalar value. Otherwise a quantity is defined as a product term of basic quantities such as voltage, time, resistance, etc. The set of basic quantities is predefined, and can't be extended within arblang.
- Examples:
    ```
    real a;
    voltage v;
    current/area/time g'; # a time derivative of areal current density.
    ```
- Expressions which evaluate to a given quantity follow normal algebraic rules; constant values must be introduced with a compatible unit if non-zero.
    ```
    voltage v = 23 * 10 mV - 2 µV;
    ```
- **Questions**:
    - Which predefined quantities do we allow? **SI quantities with shortened 1-word names. [SY] has a full list:**
        - **Length**
        - **Time**
        - **Amount of substance**
        - **Electric current**
        - **Temperature**
        - **Mass**
    - In the following `voltage v = 23 * 10 mV - 2 µV;`, is there a situation when we would care about the unit denomination of `v` (does it matter if it is `10 mV` or `0.01 V`)? If yes, do we allow converting to a different unit denomination and how? 
        - **No.**
    - Do we allow operations such as `exp`, `log`, `pow`, `sin` etc on non-scalar values? Do we allow these functions to work on all quantity types? Do we have a special 'any' quantity type so users can create their own generic functions? 
        - **The quantity type of `exp(voltage)` is `exp(voltage)`. We can't do much with that operation other than take the `log` of it. These situations don't come up often and don't need to be supported.**  
    - What is the type/unit of `pow(voltage, scalar)`, when the scalar value is not an integer, or is a run-time variable? 
        - **When the scalar value is not an integer, we don't need to support the operation. It makes the unit system complex, and these things don't/shouldn't come up.**

### Records
- Record types can be given names (aliases), or they can be anonymous, but any two record values have the same type if they have the same set of field names and types.
- Syntax: 
  ```
  record _optional identifier_ {
      _type_ _identifier_;
      [_type_ _identifier_;]
  }
  ```
- Example:
  ```
  record state {
      conductance g;
      real scale;
  };
  ```
- A record value is constructed from the name given to a record type, or from an anonymous record specification, or derived from an existing record value: Examples:
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
  Except when constructing a record type by a field modification (the last example), all fields must be given a value.
- Record fields can be accessed by name `s.g` or `s.scale`.
- When constructing a record, Every record field needs to be set, or else be taken from an existing value, or else have a default value given in the record definition.
- Records can be differentiated with respect to time by adding `'` to the record name. The result is a new record type, mirroring the original record with the following differences: the field names are appended with `'`, and the original quanities are devided by time. 
- **[SY] has made some changes to the record type which will be shared in a later doc.**.
              
### Conditional expressions
- Simple if/else expressions. Else is mandatory. Result must be bound to a variable. 
- Syntax:
  ```
  let _optional type_ _identifier_ = if _condition_ {_value_} else {_value_} _expression_;
  ```
- The 2 `_value_`s must have the same type.
- The type is optional if it can be deduced from the provided value.
- Example:
  ```
  let voltage x = if (c > 0) {3 mV} else {6 mV}
  let x = if (c > 0) {3 mV} else {6 mV}
  ``` 

### Let expressions 
- Bind a varible to a value, or expose the fields of a record. 
- Syntax:
  ```
  let _optional type_ _identifier_ = _value_ _expression_;
  with _optional type_ _record-valued expression_ _expression_;
  ```
- The scope is the `_expression_`.
- The types are optional if they can be deduced from the provided value. The with expression binds an identifier for each field of the record to the corresponding field value.
- Examples: 
  ```
  let a = 3mV
  let current b = 2nA
  let conductance g = foo(a, b)
  ```
  ```
  let g = let a = v*v a/p1 + a/p2 g*3
  # Equivalent to 
  let g = (let a = v*v {a/p1 + a/p2}) 
  g*3
  ```
  ```
  record state {
     conductance g;
  }
  let s = state {g = 3 mS;}
  with state s 
  let current = g*v # g is s.g 
  ```

### Function definitions
- Syntax:
  ```
  def _identifier_ ([_type_ _identifier]) -> _optional type_ {} 
  ```
- Need type annotations for arguments.
- Type of the returned variable if optional if it can be deduced from the provided value.
- Return the last expression.
- Example: 
  ```
  def foo(state s, voltage v) -> voltage {
    s.v + v;
  }
  ```
- **Observation: only function arguments and record fields need to have explicit quantity types. Everywhere else, the quantity can be deduced.** 
  
### ODEs
- Not defined explicitly as a single statement. 
- If an ODE is needed to describe the progression of a variable, the rate of the variable with respect to time needs to be defined. For example if the variable has a type `conductance`, a seperate variable with type `conductance/time` needs to defined and returned by the state/evolution function.

### Modules
- A module is a container for parameter definitions, constant definitions, and function definitions. Modules can `import` other modules in order to bring their names into scope.
- Syntax:
  ```
  module _identifier_ {
  ...
  }
  ```
- Wrapping functions in modules allows for reuse of functions. 
- Modules are similar to C++ namespaces.
- **They can be used as libraries to be used by other mechanisms. We can provide a set of helpful modules, for example nernst.**

### Parameters and constants

- Parameters are identifiers with a constant value which is given a default value in the module, but which can also be potentially overridden by a cell model. The expression on the right-hand side of a parameter declaration is evaluated _after_ any user-provided settings.
- The type of the parameter can be automatically deduced if omitted.
   ```
   parameter scalar abc = 123;
   parameter voltage erev = abc * 2 mV; # If abc value is changed, erev will change too.
   ```
- Constants are essentially immutable parameters — they cannot be overridden in cell models.
   ```
   constant conductance g0 = 1.23 µS;
   constant e0 = 23 mV; # type is deduced
   ```

### Interfaces
- An interface is a collection of the callback functions and bindings needed by the simulator for a certain mechanism kind.
- Syntax:
  ```
  interface _model kind_ "model name" {}
  ```
- Can import modules to bring them into scope. `import _model name_;`
- `_model kind_` can be 'point_process', 'distributed_process', 'concentration_model' etc. 
- Each `_model kind_` has a list of callbacks which must be defined. For example, a 'point_process' needs: 'initial', 'evolve', 'current', and a way to process events. Callback can be defined inline in the `interface`, or can reference an external function from an imported module. 
  ```
  initial foo.initial();
  evolve foo.evolution(S, v);
  
  current = S.g * v; # equal or no equal?
  ```
- If a callback function requires arguments, these arguments must be bound to simulator variables. **Or literals, or parameters.**
  ```
  bind v = membrane_voltage;
  bind S = process_state;
  evolve foo.evolution(S, v);
  ```
- **Interfaces can create new parameters/constants.**
- **Interfaces can introduce new parameters that mirror the parameters of a module. Only these _interface_ parameters can be overridden by the user. Module parameters are not visibile to the user.**

### Processing events
- A 'point_process' needs to respond to external events. 
- Syntax:  **(needs clarification)**
  ```
  when _condition_ [ do _state-valued expression_ ]
                   then _state'-valued expression_;
  ```
- **This needs more work. [SY] is rethinking the interface.**

## Examples

### Simple synapse

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

### Allen catalogue/ Ih
```
module Ih {

parameter conductance/area gbar = 0.00001 S/cm^2;
parameter voltage ehcn = -45 mV;

record state {
    scalar m;
}

def vtrap(voltage x, voltage y) -> scalar {
    y*exprelr(x/y); 
    # Does the argument of exprelr need to be scalar? 
    # **Yes, it does.*
}

def malpha(voltage v) -> scalar {
    0.001*6.43*vtrap(v+154.9 mV, 11.9 mV);
}

def mbeta(voltage v) -> scalar {
    0.001*193*exp(v/33.1 mV);
}

def initial(voltage v) -> state {
    let t = malpha(v);
    state {m = t/(t + mbeta(v))};
}

def evolution(state s, voltage v) -> state' {
    let a = malpha(v);
    let b = mbeta(v);
    state' {
        m' = a -s.m * (a + b);
    };
}

def current (state s, voltage v) -> current/area {  
    # is current/area the right quantity?
    # **Yes, the `/area` helps to differentiate from point_processes.**
    s.m * gbar * (v - ehcn)
}

} # end of module definition

interface distributed_process "Ih" {
    import Ih;

    bind v = membrane_voltage;
    bind S = process_state;

    initial Ih.initial();
    evolve  Ih.evolution(S, v);
    current Ih.current(S, v);
}
```

### Kinetic scheme (https://github.com/arbor-sim/arbor/blob/purkinje/mechanisms/mod/Kca1_1.mod)

```
module Kca1_1 {

constant scalar q10 = 3;
constant charge faraday = 96.4853 C*mM^-1;
constant energy R = 8.313424 J*degC^-1*M^-1; 

parameter conductance/area gbar = 0.01 S/cm^2; 
parameter scalar Qo = 0.73;
parameter scalar Qc = -0.67;

parameter 1/concentration k1  = 1.0e3 mM^-1;
parameter 1/time onoffrate = 1 ms^-1;

parameter Kc  = 11.0e-3 mM; # Is this allowed? **Yes, and encouraged.**
parameter Ko  = 1.1e-3  mM;

parameter pf0 = 2.39e-3 ms^-1;
parameter pf1 = 7.0e-3  ms^-1;
parameter pf2 = 40e-3   ms^-1;
parameter pf3 = 295e-3  ms^-1;
parameter pf4 = 557e-3  ms^-1;

parameter pb0 = 3936e-3 ms^-1;
parameter pb1 = 1152e-3 ms^-1;
parameter pb2 = 659e-3  ms^-1;
parameter pb3 = 486e-3  ms^-1;
parameter pb4 = 92e-3   ms^-1;

record state {
    scalar C0; # from 0 to 1? **Not for a while, needs special syntax.**
    scalar C1;
    scalar C2;
    scalar C3;
    scalar C4;
    scalar O0;
    scalar O1;
    scalar O2;
    scalar O3;
    scalar O4;
}

record rates {
    1/time c01, c12, c23, c34;
    1/time o01, o12, o23, o34;
    1/time f0, f1, f2, f3, f4;
    1/time c10, c21, c32, c43;
    1/time o10, o21, o32, o43;
    1/time b0, b1, b2, b3, b4;
}

def calculate_rates(amount conc, temperature temp) -> rates {
    let scalar qt  = q10^((temp - 23 degC)/10 degC);
    
    let t0 = k1*onoffrate*qt;  
    let 1/time prod_c  = conc*t0;
    let 1/time prod_Kc = Kc*t0;
    let 1/time prod_Ko = Ko*t0;
    
    # Is NMODL doing any unit conversions here? **It should be.** 
    # (C*mM^-1 * v*J^-1*degC*M*degC^-1) = C*mM^-1 * M*C^-1 -> factor of 1000.)
    let scalar t1 = faraday * v/R/temp;  
    let scalar alpha = exp(Qo * t1) * qt;
    let scalar beta  = exp(Qc * t1) * qt;

    rates {
        c01 = 4 * prod_c;
        c12 = 3 * prod_c;
        c23 = 2 * prod_C;
        c34 = prod_c; 
        o01 = c01; # Is this allowed? **No, will make renaming harder.** 
        o12 = c12;
        o23 = c23; 
        o34 = c34;
        c10 = prod_Kc;
        c21 = 2 * prod_Kc;
        c32 = 3 * prod_Kc;
        c43 = 4 * prod_Kc;
        o10 = prod_Ko;
        o21 = 2 * prod_Ko;
        o32 = 3 * prod_Ko;
        o43 = 4 * prod_Ko;
        f0  = pf0 * alpha;
        f1  = pf1 * alpha;
        f2  = pf2 * alpha;
        f3  = pf3 * alpha;
        f4  = pf4 * alpha;
        b0  = pb0 * beta;
        b1  = pb1 * beta;
        b2  = pb2 * beta;
        b3  = pb3 * beta;
        b4  = pb4 * beta;
    }
}

def evolution(state S, voltage v, amount c, temperature t) -> state' {
    let r = rates(c, t);
    with r;
    with s; 
    state' {
        C0 <-> C1 (c01, c10); # Is this clear? **Not so much, see below**
        C1 <-> C2 (c12, c21);
        C2 <-> C3 (c23, c32);
        C3 <-> C4 (c34, c43);
        O0 <-> O1 (o01, o10);
        O1 <-> O2 (o12, o21);
        O2 <-> O3 (o23, o32);
        O3 <-> O4 (o34, o43);
        C0 <-> O0 (f0,  b0);
        C1 <-> O1 (f1,  b1);
        C2 <-> O2 (f2,  b2);
        C3 <-> O3 (f3,  b3);
        C4 <-> O4 (f4,  b4);
    }
}

def current (state s, voltage v, voltage erev) -> current {
    gbar * (s.O0 + s.O1 + s.O2 + s.O3 + s.O4) * (v - erev);
}

} # end of module definition

interface distributed_process "Kca1_1" {
    import Kca1_1;

    bind v = membrane_voltage;
    bind S = process_state;
    bind cai = int_concentration("ca");
    bind ek = reversal_potential("k");
    bind temp = model_temperature;

    # How to associate initial with Kca1_1?
    # **We don't need to. It is associated with `evolve` which is in turn associated with Kca1_1.**
    initial steady_state from {C0=1; C1=0; C2=0; C3=0; C4=0; O0=0; O1=0; O2=0; O3=0; O4=0}
    evolve  Kca1_1.evolution(S, v, cai, temp);
    current Kca1_1.current(S, v, ek);
}
```

### BBP catalogue/ CaDynamics_E2

```
# **This whole thing needs to be reconsidered.**
# **Use flux instead of concentration.**
# **Define callbacks specifically for updating the individual concentrations.**
interface concentration_process "CaDynamics" {
    constant charge faraday = 96485.3321233100184 C*M^-1;
    parameter scalar gamma = 0.05;
    parameter time decay = 80 ms;
    parameter length depth = 0.1 um;
    parameter amount minCai = 1e-4 mM;
    parameter amount initCai = 5e-5 mM;

    def evolution(amount c, current i) -> amount/time {
        -5000*i*gamma/(faraday*depth) - (c - minCai)/decay;
    }

    bind ica = ionic_current("ca");
    bind cai = process_state; 

    initial = initCai;
    evolve evolution(cai, ica);
    int_conc = cai;
}
```

### Default catalogue/ Nernst
```
# **Nernst and all other reversal potential calculations will be
# absorbed into mechanism descriptions, and removed from arbor. 
# Ions that need the reversal potential calculated by a rev_pot 
# mechanism can import the module of a that mechanism and call the 
# `erev` function.**
module nernst {
constant R = 8.31446261815324 J*k^-1*M^-1;
constant F = 96485.3321233100184 C*M^-1;

def erev(temperature t, amount ci, amount co, scalar valence) -> voltage {
    R*t/valence*F
}
}

# **The interface is not needed, because rev_pot methods do not need to be exposed to the simulator.**
interface concentration_process "nernst/x" {
    import nernst;
    
    bind xi = ionic_current("x");
    bind xo = int_concentration("x");
    bind xv = valence("x");
    bind temp = model_temperature;
    
    reversal_potantial nernst.erve(temp, xi, xo, xv); # how do we bind ex to the output?
}
```

## Extra meeting minutes: 
- Fluxes in concentration models:
    - Using fluxes in concentration models is the way to go. It makes it possible to have multiple models that contribute to the flux. 
    - **[NA] This is a change from mol to mol/area? How is this related to charge? Is it similar to non-specific current? We would have non-specific concentrations? Question for next meeting.**
    - Users probably won't care, it won't change their mechanisms too much. 
    - It would be great to discuss this with actual NMODL writers, but we don't have many such contacts except perhaps Stefano Masoli. 
- State machines: 
    - What are we modeling our work against? 
        - Sebastians lif.mod: https://github.com/arbor-sim/arbor/pull/1517/files
        - LEMS: http://lems.github.io/LEMS/example-regimes.html
    - Do they need to be part of the arblang v1? No, but we need to keep them in the back of our head during the implementation. 
- Stochastic processes: 
    - SPDE intro: https://hal.archives-ouvertes.fr/hal-00973887v2/document
    - Do they need to be part of the arblang v1? No, but we need to keep them in the back of our minds during the implementation.
    - Not really [NA]'s area of expertise, [SY] has some ideas which were introduced in last week's doc. [SY] is also working with arborio on this so it should get clearer in the near future. 
    - There was some discussion about spatial variation, but this is not similar to the spatially varying/inhomogeneous parameters used in NMODL.  
- Reactions systems: Transcript of message posted by [SY] on slack:
> Regarding reaction system syntax, I think it's easiest if it is purely syntactic sugar, requiring names from the state record to be brought into scope as you noted, @Nora Abi Akar. So, e.g.
```
{
    a ⇄ 2b + c (α, β);
    b ⇄ d      (γ, δ);
}
```
> gets translated syntactically to:
```
{
    a' = -α*a + β*b^2*c;
    b' = 2*α*a - 2*β*b^2*c - γ*b + δ*d;
    c' = α*a - β*b^2*c;
    d' = γ*b - δ*d;
}
```
> where a, b, c and d are any valid unqualified identifiers, and α, β, γ, and δ are any expressions without free variables. (Rather than rely on common subexpression elimination, this could be translated instead into an equivalent where the reaction rate coefficient expressions are bound first in let-forms.)
This would mean in an ODE rhs function that the members of the state record would need to be brought into scope explicitly with `with` or `let`, and that a field could participate as a species in one or more reaction equations, or in a standard derivative assignment, but not both. E.g. with a state record with fields a, b and c, the following would all be fine,
```
def deriv(state S) → state' {
    with S; { a' = 3*b; b ⇄ c (1, a); };
}
# or
def deriv(state S) → state' {
    let b = S.b;
    let c = S.c;
    { a' = 3*b; b ⇄ c (1, S.a) };
}
```
> but not: 
```
def deriv(state S) → state' {
    with S; { c' = 3*b; b ⇄ c (1, a); };
}
```
> because we'd be assigning the field c' twice in the same record.
> The downside to this approach is that this can't be used to translate a reaction system into a stochastic chemical kinetic representation — it throws away information.
But we don't have to commit to implementing this transformation as a strictly syntactical one, if we want to support stochastic schemes, just that it is equivalent to doing so in the regular ODE case.

- Next steps: 
    - Decide what we want in arblang v1.
    - Write specs.
    - Start compiler design. 
