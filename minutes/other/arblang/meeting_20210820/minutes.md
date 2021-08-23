# Arblang Meeting 19.08.2021

Presence: NA, SY, TH

## Arblang Specification
Thanks Sam for writing the arblang language specification! 
- Review of the [PR](https://github.com/arbor-sim/arblang/pull/2) is on GH. 
- Missing some examples of individual rules, expressions as well as full mechanism examples. 
- Missing rules for allowing interface and module descriptions and imports across multiple files. (Although this is not necessarily part of language specification.)
    - Search path(s) when calling the compiler. 
    - Module imports are (treated as if) inlined.  

### Some concerns 
- Keeping the contexts and scopes straight, this is an issue in modcc. 
- When expressions: The logic of when exactly they are triggered, especially when they provoke regime changes. I can imagine it being confusing and becoming a source of subtle bugs.
- The keywords: `def` for functions and constants, `parameter` for parameters, `type` for records and other type-aliases. Maybe they should each have their own keyword. `function`, `constant`, `parameter`, `record`, `type`.
- I would like to have a good working version with the minimum needed features as our first goal. This will mean that some feature implementations will have to be postponed.

### Features that don't have to make it in the first version
These are really cool features, but we can live without them at first. This is an incomplete list.
- Super and sub-types. 
- Preferential union of records. 
- Offset units. Algebraic operations will cause confusion and mistakes. 
- Unicode.
- Regimes. 
- Binding functions using let value bindings. Or any local function definitions. 
- User defined units (doh!)

### MVP
- Only ODEs
- No `steady state`
- No `evolve for`

## CPS 
https://www.microsoft.com/en-us/research/wp-content/uploads/2007/10/compilingwithcontinuationscontinued.pdf 

### Minutes
- TH summarized the important parts of the paper. 
- NA opinion: 
    - CPS is more complex of an IR than needed. 
    - To feel confident enough to write and debug optimization passes using CPS IR, more education on CPS would be necessary. 
    - We can create our own IR, it can be based on CPS without the continuations, we can make our own rewrite rules and optimization algorithms. 
- SY makes the distinction between 2 main phases of optimization: 
    1. Algebraic transformations. Such as inlining, CSE, constant propagation. This is all the optimizations we would perform before the code generation step. These don't need CPS, we can have our own simple IR. 
    2. Code generation transformations. Such as early exit for SIMD, subexpression lifting out of for loops, other optimizations after reduction transformation etc. These could use a different, more complex IR such as CPS. 
- TH opinion
    - CPS is a well understood approach with lots of literature and 
      working compilers based on it, similar to SSA.
    - The above is not true for a TBD approach unless we take 
      a lot of care. Frankly much more than to understand a single paper.
    - I think it's too early to decide what is 'too complicated'. ArbLang
      as written has quite a lot of features.
    - I also think that the complexity of CPS is way less than you make it out
      to be.
    - Optimisation passes are laid out in Kennedey '07 or can be derived by
      us simply enough.
        - Application, Specialisation, Inlining are written out.
        - CSE is straightforward.
        - Algebraic rules live independently in the primitive ops.

### To Do 
- Reach tentavive agreement on the form of the IR. 
- Question: Why do we need a more complex IR for Code generation transformations. In specific, how would continuations help us?  
