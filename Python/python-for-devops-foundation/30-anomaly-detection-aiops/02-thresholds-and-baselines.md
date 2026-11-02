# Thresholds and Baselines

A threshold is a rule such as “alert when 5xx rate exceeds 2% for 10 minutes.” A baseline describes expected behavior for a context and time window.

## Approaches
- Fixed thresholds
- Rolling mean and standard deviation
- Median and median absolute deviation (robust to outliers)
- Seasonal baselines by hour/day
- Service-specific baselines

## Example: robust deviation
For a metric series, compare the current value with a rolling median and MAD. Define minimum sample counts and handle zero MAD explicitly.

Thresholds are transparent and often the best first step. Machine learning should add value beyond a well-designed rule.
