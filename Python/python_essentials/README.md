# Python Essentials

A runnable cheat-sheet of the Python I actually use for security work: 35 short topics, from sets and comprehensions to sockets, SQLite, `subprocess` and browser automation. Every topic is a small function you can read, run and change.

The topics follow my notes on the book *Automate the Boring Stuff with Python* by Al Sweigart. The examples are rewritten around PenTest and DevSecOps tasks: grouping ports by host, parsing scan results, grabbing a service banner, spotting SQL and command injection.

## Who it is for

- Beginners who know some Python syntax and want to see how it is used in security tooling.
- Anyone preparing for hands-on labs (HTB, CTFs...) who needs a quick reminder of how `argparse`, `struct` or `ipaddress` work.

## Getting started

You need Python 3.10 or newer. 31 of the 35 topics use only the standard library, so you can start without installing anything:

```
python python_essentials.py
```

On Linux and macOS, use `python3` if `python` is not available.

The topics on HTTP and browser automation (26, 32, 33, 34) need third-party packages. Install them in a virtual environment:

```
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install firefox       # only for topic 34
```

Topic 33 also needs Firefox installed, and topic 23 needs `nmap`.

## How it works

| Command | What it does |
|---|---|
| `python python_essentials.py` | Lists all topics |
| `python python_essentials.py 12` | Prints the code of topic 12, then runs it |
| `python python_essentials.py 11 12 13` | Runs several topics in a row |
| `python python_essentials.py all` | Runs every topic that needs no input and no network |
| `python python_essentials.py -q 12` | Runs topic 12 without printing its code first |

Inside the file, each topic is one function named `topic_NN_name()`. A comment that starts with `# ->` shows the output you should see for that line, so you can compare it with the real output below the code.

To experiment, open `python_essentials.py`, change a value inside a topic and run that topic again. To add your own topic, write a new `topic_NN_name()` function with a one-line docstring: the list picks it up automatically.

## Example

```
$ python python_essentials.py 12

===================== 12. Dictionary comprehension =====================
# Like a list comprehension, but it builds a dict: written as key: value.
# Handy trick: index a list of findings by port for instant lookup.
findings = [
    {'host': '192.168.66.2', 'port': 22},
    {'host': '192.168.66.3', 'port': 21},
    {'host': '192.168.66.4', 'port': 445},
]
by_port = {f['port']: f for f in findings}
print(list(by_port))            # -> [22, 21, 445]   the new keys
print(by_port[22])              # -> {'host': '192.168.66.2', 'port': 22}   one whole finding
print(by_port[22]['host'])      # -> 192.168.66.2    one value inside it
# Trap: keys are unique, so if two findings share a port, the second one
# overwrites the first.
-------------------------------- output --------------------------------
[22, 21, 445]
{'host': '192.168.66.2', 'port': 22}
192.168.66.2
```

## Topics

| Part | Topics |
|---|---|
| 1. Core Python | 1 sets and `defaultdict`, 2 `enumerate` and `zip`, 3 tuple unpacking, 4 functions, 5 references and copies, 6 `==` vs `is`, 7 `try` / `except` / `else` / `finally` / `raise`, 8 files, 9 modules, 10 virtual environments |
| 2. Working with collections | 11 list comprehension, 12 dict comprehension, 13 `any` and `all`, 14 `sorted` with `lambda`, 15 `Counter`, 16 de-duplication that keeps order |
| 3. Bytes, hashes, data formats | 17 text and bytes, 18 hex, endianness and `struct`, 19 base64 and hashing, 20 JSON, 21 SQLite and SQL injection |
| 4. Processes, network, CLI | 22 `subprocess`, 23 wrapping `nmap`, 24 command injection, 25 `socket`, 26 `requests`, 27 `ipaddress`, 28 a CLI script with exit codes, 29 `argparse`, 30 stdout vs stderr, 31 `print(file=...)` and `repr()` |
| 5. Web automation and introspection | 32 BeautifulSoup, 33 Selenium, 34 Playwright, 35 `type`, `dir`, `help`, `chr`, `ord` |

Two topics show a vulnerability and its fix side by side, with output you can check yourself:

- Topic 21 sends the same input to SQLite through a `?` placeholder and through an f-string. The first query matches 0 rows, the second matches every row.
- Topic 24 passes `hello ; whoami` to a command as a shell string and as a list. The shell runs `whoami`; the list prints the text.

## Topics that need a target

Topics 23, 25, 26, 32, 33 and 34 ask for a host or a URL before they do anything, and `all` skips them. Press Enter at the prompt to skip a scan or to use the default practice page:

| Topic | Default |
|---|---|
| 23 `nmap`, 25 `socket` | No default: enter a host from your own lab |
| 26 `requests` | `https://example.com` |
| 32 BeautifulSoup | `http://books.toscrape.com/`, a site built for scraping practice. The demo visits at most 10 pages |
| 33 Selenium, 34 Playwright | `https://autbor.com/example3.html`, the practice page from the book |

## Responsible use

The network topics are intended for learning and authorised testing only: your own lab, CTF platforms, or systems you have written permission to test.

All hosts, credentials and names in the examples are made up. Addresses come from private ranges (`10.x`, `192.168.x`).

## Files the demos create

Topics 8 and 31 write a small `some_file.txt` in the current folder. It is listed in `.gitignore`. The SQLite topic keeps its database in memory and leaves nothing on disk.

## Credits

The selection of topics is based on [Automate the Boring Stuff with Python](https://automatetheboringstuff.com/) by Al Sweigart. The explanations and examples here are my own study notes, not a copy of the book. If you are starting out, read the book first.

## Project structure

```
python_essentials/
├── python_essentials.py
├── requirements.txt
├── .gitignore
└── README.md
```
