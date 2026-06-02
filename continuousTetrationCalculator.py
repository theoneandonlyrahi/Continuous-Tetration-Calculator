'''
Name: Rahidul Alam
Program Name: Continuous Height Tetration Calculator
Date: 12 February, 2026
Description: This calculator was created for my Tetration: Expanded & Continuous research project.
Please refer to the height and base restrictions for tetration. Many large or absurd values are undefined :).
'''
'''Import Libraries'''
import math
'''User-Defined Settings'''
# Maximum Height: Defined and can be adjusted according to performance issues or exploration
maximumHeight = 3000
# Positive Integer Heights: A set of heights defined as positive integers 0 <= height <= maximum.
positiveIntegerHeights = set(range(0, maximumHeight + 1))
'''Quick helper functions'''
# Pos-Integer Scientific Notation: Converts a large positive integer tetration to scientific notation.
# Returns a float if it fits, or a string "1e<exp>" or "1e1e<exp>" for tower values.
def valueToSci(base, height):
    # Check the obvious: height=0 or base=1 always results in 1
    if height == 0 or base == 1:
        return 1.0
    try:
        prevHeight = posIntTetration(base, height - 1)
        logBase10_value = prevHeight * math.log10(base)
        return f"1e{logBase10_value:.7f}"
    except (OverflowError, ValueError):
        prevHeight = valueToSci(base, height - 1)
        # If prevHeight is already a plain float/int, compute normally
        if isinstance(prevHeight, (int, float)):
            logBase10_value = prevHeight * math.log10(base)
            return f"1e{logBase10_value:.7f}"
        # If prevHeight is "1e<X>" where X is a regular float string
        if isinstance(prevHeight, str) and prevHeight.startswith("1e"):
            inner = prevHeight[2:]
            # Already a double-tower "1e1e<X>" — too large to represent
            if inner.startswith("1e"):
                return "Value Error: Value is too astronomically large to properly represent!"
            # Single tower "1e<X>": the exponent X is itself a big number
            # log10(base ^ (1e<X>)) = 1e<X> * log10(base), still a tower
            # Represent as "1e1e<X>" (absorbing log10(base) factor as negligible at this scale)
            return f"1e1e{inner}"
    return "Value Error: Value is too astronomically large to properly represent!"
'''Tetration Functions'''
# Positive Integer Height: Basic definition of tetration using the iterative formula.
def posIntTetration(base, height):
    # base = 1 always returns 1
    if base == 1:
        return 1
    # height = 0 always returns 1 (by convention)
    if height == 0:
        return 1
    if height not in positiveIntegerHeights:
        return "Invalid height error: Height is not a positive integer or exceeds computational boundaries!"
    # Iterative tower computation: each step is base^(previous result)
    result = base
    for _ in range(1, int(height)):
        result = math.pow(base, result)
    return result
# Positive Continuous Height: Interpolates between floor and ceiling integer heights.
def posContinuousTetration(base, height):
    # Reject integer heights — use posIntTetration for those
    if height == int(height):
        return "Invalid height error: Height is not a positive non-integer. Use posIntTetration for integer heights."
    floorHeight = math.floor(height)
    ceilHeight  = math.ceil(height)
    fractional  = height - floorHeight
    # --- Try exact float arithmetic first ---
    try:
        floor_val = float(posIntTetration(base, floorHeight))
        ceil_val  = float(posIntTetration(base, ceilHeight))
        if floor_val == 0:
            return floor_val
        evaluation = floor_val * (ceil_val / floor_val) ** fractional
        return evaluation
    except (OverflowError, ValueError):
        pass
    # --- Fall back to log-space interpolation using scientific notation ---
    floor_sci = valueToSci(base, floorHeight)
    ceil_sci  = valueToSci(base, ceilHeight)
    def sci_to_log10(sci):
        """Extract log10 of the value from a sci string or plain number."""
        if isinstance(sci, (int, float)):
            if sci <= 0:
                return float('-inf')
            return math.log10(sci)
        if sci.startswith("1e1e"):
            # Value is 10^(10^X): log10 = 10^X, which is itself huge — return as string tag
            return ("tower", sci[4:])
        if sci.startswith("1e"):
            return float(sci[2:])
        return float('-inf')
    floor_log = sci_to_log10(floor_sci)
    ceil_log  = sci_to_log10(ceil_sci)
    # Both are normal large exponents: interpolate directly
    if isinstance(floor_log, float) and isinstance(ceil_log, float):
        interp_log = floor_log + fractional * (ceil_log - floor_log)
        return f"1e{interp_log:.7f}"
    # floor is a normal large exponent, ceil is a double-tower (1e1e...)
    # At any fractional > 0, the result is dominated by the ceil tower.
    # log10(result) ≈ frac * 10^floor_log + (1-frac) * floor_log ≈ frac * 10^floor_log
    # which is still a tower: represent as 1e1e<floor_log> (frac factor negligible at this scale)
    if isinstance(floor_log, float) and isinstance(ceil_log, tuple):
        # Interpolated inner exponent: log10(frac * 10^floor_log) = log10(frac) + floor_log
        approx_inner = math.log10(fractional) + floor_log if fractional > 0 else floor_log
        return f"1e1e{approx_inner:.7f}"
    # Both are double-towers: result is also a double-tower (use floor as lower bound)
    return f"1e1e{floor_sci[4:]}"
# Negative Continuous Height: Derived by recursive positive fractional heights.
def negContinuousTetration(base, height):
    # height here is the ABSOLUTE VALUE, expected in (0, 2) exclusive, non-integer
    if not (0 < height < 2 and int(height) != float(height)):
        return "Invalid height error: Height is not a negative non-integer or exceeds computational boundaries!"
    if 1 < height < 2:
        evaluation = math.log(1 - (height - 1), base)
    elif 0 < height < 1:
        evaluation = 1 - height
    return evaluation
'''Computational Functions'''
# Convergence Check: Checks if the infinite tower converges and approximates the limit.
def convergenceCheck(base, height):
    if math.exp(-math.e) <= base <= math.exp(1 / math.e) and height > 0:
        convergenceValue = (posIntTetration(base, maximumHeight) + posIntTetration(base, maximumHeight - 1)) / 2
        return "Converging", convergenceValue
    else:
        return "Diverging", None
'''Display Helper'''
def formatEvaluation(value):
    """Pretty-print an evaluation that might be a float, int, or sci string."""
    if isinstance(value, str):
        return value
    # Large integers: use scientific notation for readability
    if isinstance(value, float) and (value > 1e15 or (value != 0 and abs(value) < 1e-10)):
        return f"{value:.6e}"
    return str(value)
print("Note:\n This calculator is functional and has been finished. \nHowever, I am experimenting with scientific notation, \n so expect some computational errors here and there.")
'''Main Loop'''
while True:
    print("\nWelcome to the continuous tetration calculator! Please enter:")
    # Ask for base
    while True:
        inputBase = input("\nA numerical base (round any non-integer input to 4 decimal places): ")
        if ((inputBase.replace(".", "")).replace("-", "")).isdigit():
            break
    # Ask for height
    while True:
        inputHeight = input("\nA numerical height (round any non-integer input to 4 decimal places): ")
        cleaned = (inputHeight.replace("-", "")).replace(".", "")
        if cleaned.isdigit() and not (float(inputHeight) <= -2):
            break
    base   = float(inputBase)
    height = float(inputHeight)
    # --- Positive integer height ---
    if height >= 0 and height == int(height):
        print(f"\n\nTetration:\033[38;2;255;100;0m {inputBase} ^^ {inputHeight} \033[0m")
        try:
            evaluation = posIntTetration(base, int(height))
            print(f"\nEvaluation:\033[34m {formatEvaluation(evaluation)} \033[0m")
        except (OverflowError, ValueError):
            scientific = valueToSci(base, int(height))
            print(f"\nEvaluation:\033[34m {scientific} \033[0m")
        behavior, value = convergenceCheck(base, int(height))
        if behavior == "Converging":
            bStr = "\033[32mConverging\033[0m"
        else:
            bStr = "\033[31mDiverging\033[0m"
        print(f"\nBase Sequence Behavior: {bStr}")
        if behavior == "Converging":
            print(f"\nConvergence Value: approx.\033[32m {value} \033[0m")
        print("\n")
    # --- Positive continuous (non-integer) height ---
    elif height >= 0 and height != int(height):
        print(f"\n\nTetration:\033[38;2;255;100;0m {inputBase} ^^ {inputHeight} \033[0m")
        result = posContinuousTetration(base, height)
        print(f"\nEvaluation: approx.\033[34m {formatEvaluation(result)} \033[0m")
        behavior, value = convergenceCheck(base, height)
        if behavior == "Converging":
            bStr = "\033[32mConverging\033[0m"
        else:
            bStr = "\033[31mDiverging\033[0m"
        print(f"\nBase Sequence Behavior: {bStr}")
        if behavior == "Converging":
            print(f"\nConvergence Value: approx.\033[32m {value} \033[0m")
        print("\n")
    # --- Negative continuous (non-integer) height ---
    elif height < 0 and height != int(height):
        print(f"\nTetration:\033[38;2;255;100;0m {inputBase} ^^ {inputHeight} \033[0m")
        result = negContinuousTetration(base, abs(height))
        print(f"\nEvaluation: approx.\033[34m {formatEvaluation(result)} \033[0m")
        print("\n")
    else:
        print("\nBase/Height Error: You have inputted bases or heights not supported by this calculator!")