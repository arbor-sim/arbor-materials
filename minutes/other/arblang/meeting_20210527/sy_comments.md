# Sam's comments on arblang proposal

## Integration pipeline
* Does the gap junction current update also update mechanism internal state?
  > *I was thinking that once gap junctions are added to arblang/modcc, they would be similar to point mechanisms with seperate state and current updates: the state update takes care of the internal state, and the current update takes care of the gap junction current.*

* Blue vertical arrowed line: this represents input from shared and mechanism
  specific state?
  > *Yes. At least that's how things are implemented currently: all mechanisms have read access to everything in the shared state and the mechanism state.*

## Language requirements
* Should we require ODE solver specification? Hints could be useful, but
  otherwise I think we should try to determine the appropriate solver
  programmatically.
  > *I would prefer not to require it, but the proposed syntax allows for hints if we decide that they're needed.*

* Tuples might not be necessary, at least not explicitly: would multiple return
  values be sufficient, along with a mechanism for binding them to local
  variables? e.g. `let a, b, c = somefn(x, y, z)`
  > *Binding the return values to multiple local variables would eliminate the need for the `tuple._#` syntax. I think it's a cleaner design, and it means we wouldn't need tuples as a user feature.*

* **I'd add to the requirements, that we need to be able to represent entire
  mechanisms, as we do currently for NMODL density and point mehcanisms, but in
  addition also smaller fragments of user-supplied code, such as for example
  nonlinear gap junction conductance expressions.**
  > *I agree, I had that in mind but I forgot to add it to the requirements. As for gap junctions, the most straight forward way is to model a full mechanism with state (conductance) and current updates. However, if the current update can only be `i = g*(v_peer - v_local)`, and the only allowed state parameter is the conductance `g`, then that could be simplified.*

## Language proposal

* In the examples given, the `in {` part of the let syntax is redundant. The
  syntax could be covered by e.g.
  ```
  expr := let-binding expr | ...
  let-binding := LET symbol = expr
  ```
  That said, that would allow possibly confusing constructs as
  ```
  let g = let a = v*v a/p1 + a/p2 g*3
  ```
  corresponding to:
  ```
  (let (g (let (a (* v v)) (+ (/ a p1) (/ a p2)))) (* g 3))
  ```
  The lexical scope of various bindings should be made explicit; for
  let-bindings, this scope could be defined as the following expression, in a
  scheme such as that above, or else to the end of the enclosing
  brace-delimited block.
  
  > *I personally find nested let expressions such as `let g = let a = v*v a/p1 + a/p2 g*3` to be confusing and would rather discourage their use. We could make brace-delimination optional:* 
  >  - *`let g = (let a = v*v {a/p1 + a/p2}) {g*3}` is a bit less confusing.*
  >  - *`let a = 2 let b = 3 let c = a + b` is still valid and clear without using `in {}`*
  >  
  > *How do you feel about disallowing let-expression variables from being bound to another let-expression? I know it's useful, but it's not necessary and may be more trouble than it's worth. Then again, I see no real harm in allowing it to be used, as long as we don't use it too much in our examples, and document it properly.*


* I'm not fond of the implicit semantics of the `state` functions: rather than
  providing a description of how to determine a new state from an old state,
  which introduces an implicit dependence upon an invisible time parameter in
  something that looks like a function (`solve_ode`), I think it is more in the
  declarative spirit to describe the derivatives, be it in terms of ODEs,
  reaction schemes, or a combination.
  
  > *I understand what you mean, and agree with you to a certain extent. It was challenging to find a way to represent ODEs in a clear manner, that was also declarative in style and allowed us to return a new `state` object.*

  Related to this, access to and description of state components and their
  derivatives is awkward; as an example, symbols look like they are something
  that can be returned by a special function. In
  ```
  let m = sym()
  ```
  what is the 'type' of `m`?
  
  > *`m` is a new object of type symbol. `sym()` is a constructor, it's consistent with the syntax of creating a struct object.*

  **I propose a specific syntax: one for bringing struct members into scope; one
  for specifying a struct value in terms of member assignments; and one for
  describing derivative terms.**

  **As an example, the state derivative and initialization could be described
  along the lines of**
  ```
  struct state {
    real m
  }

  def init(real v) -> state {
    let t = malpha(v)
    state {
        m = t/(t+mbeta(v))
    }
  }

  def dynamics(real v, state S) -> state' {
    let a = malpha(v)
    let b = mbeta(v)
    state' {
        m' = a - S.m*(a + b)
    }
  }
  ```
  where the struct name `state` is used also as a value constructor, with
  fields names used as the LHS of assignment expressions, and `state'` does
  something similar for the automatically deduced time-derivative of the
  `state` compound value.
  
  > *I don't especially like the syntax of using `state` as a value constructor, maybe we can use parentheses instead of brackets? It would be similar to python's named arguments.*
  > 
  > ***I also find it confusing that the ODE is not written in terms of a single variable: we have `m` on the LHS and `S.m` on the RHS, and `S.m` has a value, but should be treated as a symbol**. In the original proposal, it is clear what has a numerical value and what is the variable to be integrated, here it is not. And the return value is a `state'`; what is the type of `state'`? what can be done with it?* 
  > 
  > ***In addition, does this mean that all variables in the state struct need to be integrated? Is that a reasonable requirement?***
  >
  > *Using `S.m` in the RHS of the ODE, is similar to what was in the original proposal: binding a symbol `m` to the input state `S.m` using `solve_ode(ode_m, (m, S.m)`. I chose the concept of a symbol in order to write the entire ODE in terms of a single symbolic variable. Then `solve_ode` would take as an argument the initial conditions of the ODE, and the solution would be the output of the function. This can also be thought of as binding both `m` on the RHS and the LHS to `S.m`. However, I agree that the resulting method is imperative in style.*


  The components of `state` could be brought into scope with something like:
  ```
  def dynamics(real v, state S) -> state' {
    let a = malpha(v)
    let b = mbeta(v)
    with S
    state' {
        m' = a - m*(a + b)
    }
  }
  ```
  Here `with struct-value` brings the field names of the compound value into
  the subsequent scope. It would be a short hand for `let m = S.m` etc.
  
  > Would this be the only supported way of writing the ODE? Or would using `S.m` in the RHS still be allowed? 
  > ***If `S.m` on the RHS is still allowed, I think this might be a bit confusing: the `m` on the RHS of the ODE is actually `S.m`, but the `m'` on the LHS is not**. Although, it looks more like an ODE this way.*

  Derivative value blocks could also handle reaction system syntax, with
  species names in reaction equations being corresponding to variable
  derivative terms. Provided that a state variable derivative appears either
  only on the LHS of an ODE equation, or as a reactant in a reaction system,
  ODEs and kinetic schemes can be mixed in the same specification — useful for
  those coupled ODE/kinetic scheme descriptions of those AMPA and NDMA
  synapses.
  ```
  def dynamics(real v, state S) -> state' {
    with S
    state' {
        a' = a + b
        b' = b*b
        c <-> d (param1, a)
    }
  }
  ```

  These can then be translated into the corresponding explicit ODE system, with
  annotations for conserved linear combinations derived from the reaction
  system say.
  
  > *I like this, being able to mix ODEs and kinetic schemes.*

* Regarding the binding declarations, I don't think we need to have explicit
  references to the shared state data _and_ an association of functions to
  mechanism entry points — the latter should be sufficient, though we will also
  need some way of stating what the mechanism state value type (`mech_state` in
  the examples) is.

  For example, given the signature of a current contribution function has to be
  _(voltage, state) -> current_ or _(voltage, state) -> (current,
  conductance)_, the binding of a non-specific current contribution could be
  just:
  ```
  parameter { real ehcn; real gbar }
  stuct state { real g }
  def Ih_current(real v, state S) {
    let g = S.m * gbar
    g*(v - ehcn), g
  }

  /* some sort of declaration that 'state' is the mechanism state */

  defg CURRENT = Ih_current
  ```

  I think `defg` could simply be something like `bind` — `defg` reads like it
  is defining an externally visible interface to the mechanism, while `bind`
  reads more of an instruction to associate something internal with an
  external interface. The former feels more like an open class; the latter,
  a closed one governed by the mechanism interface.
  
  > *I think we should bind the arguments and return values as well as the functions for the following reasons:*
  >   - *We wouldn't be forcing the user to memorize the prototypes of the mechanism entry points.*
  >   - *Users don't have to change their code if the mechanism prototype changes.*
  >   - *It would allow for more flexible prototypes for functions and mechanism entry points: we wouldn't have to force the user to include an argument that isn't being used for example.*
  >   - *It forces the user to think about the interactions with the simulator which will hopefully lead to better code.*
  >   - *It provides a simple way to indicate to the compiler which ion concentrations are being manipulated, if any.*

* **Binding more complicated dynamics: this isn't mentioned in the proposal,
  but we may well want to be able to allow descriptions where the mechanism
  can transition between different dynamical domains, to support things
  such as Sebastian's LIF dynamics. Syntax for this is wide open!**
  > *I haven't thought about this yet. I'll add it to the open questions.*

* Arrays: I don't think we need them, even for kinetic schemes, at least
  if we adopt an approach like the one sketched above.

## Open questions

* Mechansim composition: for me, this would ideally be something handled behind
  the scenes, rather than a feature exposed in the surface language.

* **Reversal potentials: I'd really like to get rid of them as mechanisms, and
  instead have ion channels just describe what they want in their ion current
  functions, using common subexpresion elimination to remove overhead**.
  
  > *Can you expain more what you mean?*

* **Units: the ideal for me would be that any type in the surface language is
  either: a quantity, such as length, or voltage; or a record type (struct).
  Rather than `real v`, we'd have `voltage v` (for example), and then
  we could freely mix in an expression values of the same quantity, but with
  different units. An assignment `voltage erev = 3` would be an error, but
  `voltage erver = 3 mV + 0.03 V` would be perfectly legal. This simplifies
  the typing for state time derivatives: the struct `state` might have
  for an ion channel fields**
  ```
    real m;  /* scalar */
    real h;  /* scalar */
  ```
  or for a synapse,
  ```
    conductance A;
    conductance B;
  ```
  while the implicitly defined time derivative struct `state'` would have
  fields
  ```
    real/time m';
    real/time h';
  ```
  or
  ```
    conductance/time A';
    conductance/time B';
  ```

  This complicates the syntax a little, because types could now be given by
  quantity-expressions, not just simple names. On the plus side, it eliminates,
  from the user point of view, problems of Kelvin vs degree Centigrade, or
  nanoamperes vs microamperes.
  
  > *I've started thinking about this, but I don't have a concrete proposal yet.*
  > *Would this proposal remove the `real` types? How would we deal with pure mathematical functions that don't have units?*
  > *Is it possible to only optionally attach units to arguments and return values and natural numbers, and have the compiler check correctness?*
  > *What is the value of using `voltage`, `current`, `conductance` types, as opposed to `real` + unit?*
