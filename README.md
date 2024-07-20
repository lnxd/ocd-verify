# ocd-verify
Python utility for comparing files between two directories. Checks for unique files and verifies that common files have identical MD5 checksums.

Initially created to check the accuracy of web scrapes through repeated file comparisons. 

Can also verify that the contents of a cloned or copied directory are identical to the original.

## Usage
```
python3 verify.py <directory1> <directory2>
```

## Limitations
- Tested only on macOS
- Uses MD5 for performance reasons. The probability of a mistake due to an MD5 hash collision with a large enough dataset is approximately [1 in 2^64]([https://en.wikipedia.org/wiki/MD5](https://en.wikipedia.org/wiki/Hash_collision)).
