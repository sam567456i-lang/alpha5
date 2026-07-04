# Mathematical Core Primitives

This document is auto-generated from the metadata exposed by pure mathematical primitives.

## Exponential Moving Average
- **Version**: 1.0.0
- **Formula**: EMA_t = Value_t * alpha + EMA_{t-1} * (1 - alpha)
- **Complexity**: O(n)
- **Memory**: O(n)
- **References**: TA-Lib EMA, Pandas EWM (adjust=False)
- **Failure Modes**: Requires continuous float64 arrays, NaN propagation on gaps

## Simple Moving Average
- **Version**: 1.0.0
- **Formula**: SMA_t = Sum_{i=t-period+1}^t Value_i / period
- **Complexity**: O(n)
- **Memory**: O(n)
- **References**: TA-Lib SMA
- **Failure Modes**: Requires continuous float64 arrays, NaN drops validity

## Weighted Moving Average
- **Version**: 1.0.0
- **Formula**: WMA_t = Sum_{i=1}^P (Value_{t-P+i} * i) / Sum(1..P)
- **Complexity**: O(n * period)
- **Memory**: O(n)
- **References**: TA-Lib WMA
- **Failure Modes**: Requires continuous float64 arrays, NaN drops validity

## Rolling Sum
- **Version**: 1.0.0
- **Formula**: Sum_{i=t-period+1}^t Value_i
- **Complexity**: O(n)
- **Memory**: O(n)
- **References**: NumPy convolve sum equivalent
- **Failure Modes**: Requires continuous float64 arrays, NaN drops validity

## Rolling Standard Deviation
- **Version**: 1.0.0
- **Formula**: StdDev_t = Sqrt(Var_t)
- **Complexity**: O(n * period)
- **Memory**: O(n)
- **References**: NumPy std
- **Failure Modes**: Requires continuous float64 arrays, NaN drops validity, ddof >= period yields division by zero

## Rolling Variance
- **Version**: 1.0.0
- **Formula**: Var_t = Sum_{i=t-period+1}^t (Value_i - Mean)^2 / (period - ddof)
- **Complexity**: O(n * period)
- **Memory**: O(n)
- **References**: NumPy var
- **Failure Modes**: Requires continuous float64 arrays, NaN drops validity, ddof >= period yields division by zero

## Rolling Variance
- **Version**: 1.0.0
- **Formula**: Var_t = Sum_{i=t-period+1}^t (Value_i - Mean)^2 / (period - ddof)
- **Complexity**: O(n * period)
- **Memory**: O(n)
- **References**: NumPy var
- **Failure Modes**: Requires continuous float64 arrays, NaN drops validity, ddof >= period yields division by zero

