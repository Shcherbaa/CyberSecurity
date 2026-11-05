# Regex Trainer

A small command-line tool for practicing regular expressions. Pick a text file, type a regex and see exactly what it matched. The sample files focus on patterns that are useful in security work, such as finding exposed secrets.

## Getting started

You need Python 3.10 or newer. There is nothing to install: the program uses only the standard library.

```
python regex_trainer.py
```

On Linux and macOS, use `python3` if `python` is not available.

## How it works

1. Choose a sample file by its number, or enter `f` to use your own file.
2. Type a regex.
3. The program prints every full match and the total count, then returns to the menu.

Open the file in a text editor next to the terminal so you can see what you are searching.

Enter `q` in the menu to quit. In the regex prompt, `q` is treated as a normal pattern.

If the regex has a syntax error, the program shows the reason and returns to the menu. If the regex is valid but matches the wrong text, you will see that in the results and can try again.

## Example

```
Exercises:
1. 01_secrets.txt
2. 02_quantifiers.txt
3. 03_classes_anchors_groups.txt
4. 04_lookaround.txt
f. Use your own file
q. Quit
Your choice: 2
Regex: key\d
key1
key2
key3
Total matches: 3

Exercises:
1. 01_secrets.txt
2. 02_quantifiers.txt
3. 03_classes_anchors_groups.txt
4. 04_lookaround.txt
f. Use your own file
q. Quit
Your choice: 2
Regex: (
Invalid regex: missing ), unterminated subpattern at position 0

Exercises:
1. 01_secrets.txt
2. 02_quantifiers.txt
3. 03_classes_anchors_groups.txt
4. 04_lookaround.txt
f. Use your own file
q. Quit
Your choice: q
```

## Exercises

| File | Topics | What to find |
|---|---|---|
| `01_secrets.txt` | Secret detection | AWS access key IDs, GitHub tokens, Slack tokens, quoted passwords and API keys, private key blocks |
| `02_quantifiers.txt` | Greedy and lazy quantifiers | Single HTML tags, quoted strings, repeated letters, spelling variants, key-value pairs |
| `03_classes_anchors_groups.txt` | Character classes, anchors, groups | Emails, dates, IP addresses, phone numbers, times, hex colors, URLs, file names |
| `04_lookaround.txt` | Lookahead and lookbehind | Amounts after a currency sign, numbers before a unit, values after a label |

Some lines are decoys: they look like a target but should not match.

## Regex flags

The program compiles your regex without flags. To use one, put it at the start of the pattern:

| Flag | Meaning |
|---|---|
| `(?i)` | Ignore case |
| `(?m)` | `^` and `$` match at the start and end of each line |
| `(?s)` | `.` also matches a newline |

## Using your own files

There are two ways:

- Enter `f` in the menu and type the path to any text file. It can be anywhere on your computer.
- Put a `.txt` file in the `exercises` folder. It will appear in the menu the next time you start the program.

Files that are not in UTF-8 still open, but characters that cannot be decoded are shown as `�`.

Do not commit real credentials, logs or other private data to a fork of this repository.

## About the sample data

All data in the `exercises` folder is synthetic. The keys, tokens, passwords and private keys are fake and do not give access to anything. Some values copy the format of real credentials on purpose, so secret scanners may flag them.

## Project structure

```
regex_trainer/
├── regex_trainer.py
├── exercises/
└── README.md
```
