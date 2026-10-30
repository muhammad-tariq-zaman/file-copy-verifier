# file-copy-verifier

Verify a copied directory against its source using file sizes and SHA-256 hashes, listing missing, extra and differing files.

## How to run

```sh
python3 main.py source_dir dest_dir
```

## Example output

```
missing: 1, extra: 0, differing: 1
- missing: b.txt
- differing: a.txt
```

Standard library only. Run the tests with `python3 -m unittest discover`.
