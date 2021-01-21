# Test Bench

Work In Progress.

Requirements:

- Python 3.7+
- Rust
- `hyperfine`

## Using Test Bench

```sh
# you can enable testing bottom AND regress, or bottom OR regress.
$ py -m test_bench --bottom --regress
$ py -m test_bench --bottom
$ py -m test_bench --regress
# if the commandline name is not `bottomify`, specify one as such:
$ py -m test_bench --command "commandline"
```
