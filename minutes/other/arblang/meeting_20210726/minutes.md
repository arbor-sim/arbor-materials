# Arblang meeting 26.07.2021

## Status update:
- [NA] Current status of compiler:
    - Basic lexer and parser into the top level AST (rawIR: no name resolution or type checking at this stage).
    - No unit tests yet.
    - Will open a rough draft PR before I leave for vacation (this Thrusday).
    - Code/design reviews are welcome.

## Discussion points:
- Arblang syntax proposal.
    - No new updates 
- Main IR for optimization:
    -  options: 
        - SSA
        - CPS 
        - Custom functional IR (CPS, without continuations).
    - Continuations:
        -  Can be useful for: 
            - Looping until convergence: e.g. when solving non-linear ODE systems. 
            - For early exit in conditional branches. (Mostly for SIMD, right now we use masking and calculate both true and false branches.)
        - Both of these use cases don't *need* continuations. We can deal with them at code generation time. 
        - We most likely don't need or want continuations: we don't have general recursion or exceptions in the DSL. If at some point we need it, we can then add it. **Start off with an IR that doesn't include continuations, add them in later if needed.**
        - To be certain in our decision, we agreed to read `Compiling with Continuations, continued - Kennedy 2007`. We will have a meeting to discuss the paper Wednesday 28.07.21, and then make a final decision.
    - Symbolic representation: 
        - Needed, for example, for determining the conserved space in kinetic reaction schemes. These result in underdetermined systems that could be stabilized by swapping out one of generated equations for solving the ODE system for the conservation formula. Some of the info needed to find the conserved space is lost when we desugar the language, (reaction system is translated into ODEs) but it can be later reconstructed using symbolic manipulation of the reactions. This will probably be done while generating the AST consisting of the main IR (the IR where most optimizations are performed).
        - Also needed for linearity analysis, symbolically solving ODE/linear systems. 
    - Automatic differentiation: 
        - This will be used for determining the conductance term from the current update expression. (Anything else?)
        - It will likely need to be implemented right before the code generation step.
    - SIMD: 
        - When integrating with LLVM (at a later stage) we want to make sure the transcendental functions implemeneted in the SIMD backends are inlined and optimized. 
        - For generating SIMD code, we may need a separate level of the IR that looks less functional that can aid in generating SIMD code. 


