# Arblang Meeting 23.08.2021

Presence: NA

## The IR(s)

### Recap of last meeting

- NA opinion:
    - CPS is more complex of an IR than needed.
    - To feel confident enough to write and debug optimization passes using CPS IR, more education on CPS would be necessary.
    - We can create our own IR, it can be based on CPS without the continuations, we can create/adapt the rewrite rules and optimization algorithms.
- SY makes the distinction between 2 main phases of optimization:
    - Algebraic transformations. Such as inlining, CSE, constant propagation. This is all the optimizations we would perform before the code generation step. These don’t need CPS, we can have our own simple IR.
    - Code generation transformations. Such as early exit for SIMD, subexpression lifting out of for loops, other optimizations after reduction transformation etc. These could use a different, more complex IR such as CPS.
- TH opinion
    - CPS is a well understood approach with lots of literature and working compilers based on it, similar to SSA.
    - The above is not true for a TBD approach unless we take a lot of care. Frankly much more than to understand a single paper.
    - (Probably) a better wording for my concerns: I fear that the complexity will be entering the IR anyhow, but on less principled grounds.
    - I think it’s too early to decide what is ‘too complicated’. ArbLang as written has quite a lot of features.
    - I also think that the complexity of CPS is way less than you make it out to be.
    - Optimisation passes are laid out in Kennedey '07 or can be derived by us simply enough.
        - Application, Specialisation, Inlining are written out.
        - CSE is straightforward.
        - Algebraic rules live independently in the primitive ops.

### Decision
[NA]: The IR is a small though important part of the compiler, and I don't want it to be a source of contention. But this is also an exercise in how we will handle differing opinions at different stages in this project so I don't want to delay/ignore the issue. Usually, I would say we should discuss the technicalities, the pros and cons of each approach, but we have done this and now we are going in circles and we need to make a decision. I am not against CPS, I see the advantages. **We should start simple and increase the complexity if needed (during the initial stages of development). This means a simple IR inspired by CPS but without continuations for the main optimizations, pre-code generation.** 

### Phases
- Expression categorisation: iterate until converged:
  1. Expression categorization based on dependencies:
     * Truely constant.
     * Parameter-dependent constant, including pseudo-parameters like temperature, geometry.
     * Non-constant and not state dependent.
     * Non-constant and state dependent.
  2. Constant elimination from 'true constant' values.

- Phases of compiler optimizations:
    - Stable AST with ODEs:
        - Constant propagation
        - Algebraic simplification and normalisation
          - collecting powers
      - (Selective) Inlining
    - Solved ODEs:
      - Algebraic simplication pass II
      - Inlining
      - CSE
      - Hoisting out parameter-constant data into hidden state
  - Pre-code generation: 
      - Machine Specific Optimisations
  - Code generation:
      - Print C++/CUDA


