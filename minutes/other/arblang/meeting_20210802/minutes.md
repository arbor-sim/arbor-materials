# Arblang meeting 02.08.2021

Present: Sam Yates [SY] Thorsten Hater [TH]

## Status updates

Sam: formalizing lexical grammar; trialing alternative syntax for definitions, functions. Discussions in #arblang on Slack.

## Open (and closed) questions

- Generic functions.
    - Not in the sense of
      ```
      unsafe_coerce: a -> b
      ```
    - ok
      ```
      id: a -> a
      scale: a -> a length
      ```
      where `a` is simple quantity.

      [SY] Fine with generics (though I would leave out the return types, and say that they are just deduced — because it means we need to have a more elaborate syntax for do operations on type variables); argument against up to now has been that: 1) don't trust users to put types in where they ought, and so support requests; 2) probably not much of a use case for truly generic functions, given the constraints imposed by units and quantities.

      e.g.
      ```
      f (a, b) a + b + 1 m; # a and b are already constrained to be length.
      g (x: A) x * 2 m : A * length; 
      ```
    - Verdict: Not for now, maybe implicitly by inference

- Binding syntax! Which keywords where? (from #arblang) def, vs type, vs let o my. Debate to continue in #arblang

- User-suppliedunits: definitely useful; pain to support, so maybe let's not.

  Benefits: people could import e.g. cgs units; writing some of arblang in arblang; ...
  Downside: unitcide (everything is done unitless with some magic fudge factors added when defining effects)
  TH: something that could be added later, but notes that we'll need something under the hood now that would form the basis of a user-visible implementation later.

- Should we have integer types? SY wants 'no' (in e.g. powers of unit-bearing quantities) we can tokenize a numeric literal but reject in parse. 

- Type assertions and function return types.

  Paraphrasing #arblang chat and discussion in meeting:

  * TH prefers type assertion to follow argument in function args, e.g. `f(v: voltage)`; SY also happy with this.
  * SY thinks we can use that to handle any function return type declaration too, by letting any expression have a type assertion. Grammar fragment: _expr_ ::= _expr_ (`:` _type-expr_)? | …
  * TH: But then the return type sits at the end of the function, not up the top.

    ```
    def f = fn (v: voltage, t:time)
     let a = v*t;
     let ...;
     ...
     a*b+c: voltage*time; # type assertion of result asserts type of function return
    ```

  * SY: We could put the types first, e.g. `f(voltage! v) voltage! 3*v`. TH: no no nope no nope.
  * TH: Not fond of `;` after `let` — can't we use `in`? Also: semicolons here may be misleading to people expecting C.
  * SY obstinantly clings to the stark beauty of _identifier_ = _expression_ `;` syntax.
  * Compromise: style guide to make things clear, perhaps encourage use of parentheses around function result expression, even if this isn't mandatory and doesn't actually change the semantics at all, e.g.

   ```
   def f = fn (v : voltage, t : time) (
       let a = v*t;
       a*3
   ) : voltage*time;
   ```






