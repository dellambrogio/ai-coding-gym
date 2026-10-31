## Part 2: Downsampling

`downsample(name, start, end, step, agg) -> list[tuple[int, float]]`: split `[start, end)` into buckets `[start, start+step)`, `[start+step, start+2*step)`, … (the last bucket is cut off at `end`) and return `(bucket_start, aggregate)` for every bucket that contains at least one point, in order. Raise `ValueError` if `step <= 0` or `agg` is unknown.
