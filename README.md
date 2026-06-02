# Continuous Tetration Calculator

A Python implementation of continuous-height tetration using my interpolation formulas.

Tetration is the fourth hyper-operation (iterative exponentiation). While integer-height tetration is well-defined, extending it to fractional and negative heights has no universally accepted solution. This calculator implements a geometric interpolation for positive real heights and a recursive logarithmic approach for negative continuous heights.

## Features

- Positive integer height tetration with scientific notation fallback for astronomically large values
- Positive continuous height tetration using geometric interpolation
- Negative continuous (fractional) height tetration via recursive logarithmic approximation
- Convergence detection for infinite power towers within $e^{-e}$ and $e^{1/e}$
- Handles values too large for floating point

## Restrictions

- Base: any positive real number
- Height: any value in $(-2, 0) \cup [0, \infty)$, non-integer for continuous modes
- Heights at or below $-2$ are not reachable within this framework

Enter a base and height when prompted and it will return the computations for you.

## Reference

Not until I publish the paper as a pre-print haha
