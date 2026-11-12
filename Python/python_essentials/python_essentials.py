#!/usr/bin/env python3
"""
Python Essentials: a runnable, annotated reference.

A cheat-sheet of Python techniques that come up when writing
small pentest / DevSecOps tools. The topics follow my notes on the book
"Automate the Boring Stuff with Python" by Al Sweigart, with security-flavoured
examples.

How to use this file:
    python python_essentials.py              list all topics
    python python_essentials.py 12           print the code of topic 12, then run it
    python python_essentials.py 11 12 13     several topics in a row
    python python_essentials.py all          run every topic that needs no input or network

How to read this file:
  * Every topic is one small function: topic_NN_name(). Read it, run it, change
    it, run it again.
  * Imports live inside the topic that needs them, so each body can be copied
    into your own script as it is.
  * "# ->" marks the output you should see for that line.
  * Third-party packages are imported only inside topics 26 and 32-34. Everything
    else runs on the standard library alone.

Contents
--------
PART 1: CORE PYTHON
    1.  Collections: set and grouping with defaultdict
    2.  Loop helpers: enumerate and zip
    3.  Tuple unpacking
    4.  Functions
    5.  References, aliases and copying
    6.  Equality: == vs is, and type checks
    7.  Errors: try / except / else / finally, and raise
    8.  Files
    9.  Modules: import
    10. Virtual environments (venv)
PART 2: WORKING WITH COLLECTIONS
    11. List comprehension
    12. Dictionary comprehension
    13. any() and all()
    14. Sorting: sorted() + lambda
    15. Counting: Counter and defaultdict(int)
    16. De-duplicate while keeping order
PART 3: BYTES, HASHES, DATA FORMATS
    17. Text and bytes (encoding / decoding)
    18. Bytes deeper: hex, endianness, struct
    19. Encoding, hashing and base64
    20. JSON
    21. SQLite (and SQL injection)
PART 4: PROCESSES, NETWORK, CLI
    22. subprocess: run other programs
    23. subprocess in practice: wrapping nmap
    24. Command injection (why shell=True is dangerous)
    25. socket: talk to a service directly
    26. requests: HTTP calls
    27. ipaddress: IPs and networks
    28. A small CLI script (argv, exit codes, __main__)
    29. argparse: real CLI parameters
    30. stdout vs stderr
    31. print(file=...) and repr()
PART 5: WEB AUTOMATION AND INTROSPECTION
    32. BeautifulSoup: parse HTML
    33. Selenium: drive a real browser
    34. Playwright: modern browser automation
    35. Introspection: type(), dir(), help(), chr(), ord()

Responsible use: topics 23, 25, 26 and 32-34 talk to other hosts. Point them only
at your own lab, a CTF platform, or a system you have written permission to test.
"""

# ====================================================================
# PART 1: CORE PYTHON
# ====================================================================

# --------------------------------------------------------------------
# 1. Collections: set and grouping with defaultdict
# --------------------------------------------------------------------
def topic_01_collections():
    """Collections: set and grouping with defaultdict"""
    from collections import defaultdict

    # A set is written with {} but WITHOUT colons. It drops duplicates automatically.
    ips = {'10.10.10.5', '10.10.10.6', '10.10.10.5'}
    print(sorted(ips))              # -> ['10.10.10.5', '10.10.10.6']   (one copy of .5)
    # sorted() is here only because a set has no fixed order.

    # Group ports by host: defaultdict(list) creates an empty list the first time a
    # new key is touched, so we can .append() without checking if the key exists yet.
    pairs = [('10.10.10.5', 22), ('10.10.10.5', 80), ('10.10.10.6', 445)]
    by_host = defaultdict(list)
    for host, port in pairs:
        by_host[host].append(port)
    print(dict(by_host))            # -> {'10.10.10.5': [22, 80], '10.10.10.6': [445]}
    # dict() only hides the "defaultdict(<class 'list'>, ...)" prefix in the output.


# --------------------------------------------------------------------
# 2. Loop helpers: enumerate and zip
# --------------------------------------------------------------------
def topic_02_enumerate_zip():
    """Loop helpers: enumerate and zip"""
    # enumerate yields an (index, item) pair on each step: (0, 'Ivan'), (1, 'Kate'), ...
    # "i, user" unpacks that pair into two variables (see topic 3).
    users = ['Ivan', 'Kate', 'John']
    for i, user in enumerate(users):
        print(i, user)              # -> 0 Ivan  /  1 Kate  /  2 John

    # zip walks two lists in parallel: first items together, then second, and so on.
    # It stops at the SHORTER list, so 'server3' is never printed.
    hosts = ['server1', 'server2', 'server3']
    ports = [[22, 80], [443, 445]]
    for host, open_ports in zip(hosts, ports):
        print(host, open_ports)     # -> server1 [22, 80]  /  server2 [443, 445]


# --------------------------------------------------------------------
# 3. Tuple unpacking
# --------------------------------------------------------------------
def topic_03_unpacking():
    """Tuple unpacking"""
    # When several names sit on the left of "=", Python spreads the values across
    # them in order.
    ip, port = ('10.10.10.5', 80)
    print(ip)                       # -> 10.10.10.5
    print(port)                     # -> 80


# --------------------------------------------------------------------
# 4. Functions
# --------------------------------------------------------------------
def topic_04_functions():
    """Functions"""
    # A typical workflow: prepare the data, define the function with its parameters,
    # then pass the data into those parameters when calling it.
    target = {'host': '192.168.22.32', 'port': 80}

    def make_url(ip, port):             # def defines a function; ip, port are its inputs
        return f'http://{ip}:{port}/'   # return is what the function hands back

    url = make_url(target['host'], target['port'])
    print(url)                          # -> http://192.168.22.32:80/
    # If there is no return (or the function never reaches it), it returns None.


# --------------------------------------------------------------------
# 5. References, aliases and copying
# --------------------------------------------------------------------
def topic_05_references_and_copies():
    """References, aliases and copying"""
    import copy

    # A variable is a label on an object. Two labels can point at the SAME list,
    # so a change through one is visible through the other.
    a = [22, 80, 443]
    b = a                       # b is another label on the same list, not a copy
    b.append(445)
    print(a)                    # -> [22, 80, 443, 445]   a sees it too

    # Rebinding one label to a NEW list does not touch the other:
    d = [22, 80]
    e = d
    d = [443]                   # d points at a new list; e still points at [22, 80]
    print(d, e)                 # -> [443] [22, 80]

    # Editing the shared list in place (slice assignment) IS seen by both:
    d = [22, 80]
    e = d
    d[:] = [443]
    print(d, e)                 # -> [443] [443]

    # A real (shallow) copy: a new list with the same items.
    f = a.copy()
    print(f == a, f is a)       # -> True False   same content, different object
    # For a list that contains other lists or dicts, use a deep copy instead:
    nested = [[22, 80], [443]]
    g = copy.deepcopy(nested)
    g[0].append(8080)
    print(nested)               # -> [[22, 80], [443]]   the original is untouched


# --------------------------------------------------------------------
# 6. Equality: == vs is, and type checks
# --------------------------------------------------------------------
def topic_06_equality_and_types():
    """Equality: == vs is, and type checks"""
    a = [22, 80]
    b = [22, 80]
    c = a
    print(a == b)                   # -> True    "is the content equal?"
    print(a is b)                   # -> False   "is it the SAME object?" No: two lists
    print(a is c)                   # -> True    two labels on one list

    # Comparing types:
    print(type(a) is type(b))       # -> True    exactly the same type
    print(isinstance(a, list))      # -> True    a is a list (subclasses count too)
    # A subclass is a more specific type built on another one. bool is a subclass of int:
    print(isinstance(True, int))    # -> True
    print(type(True) is int)        # -> False   the exact type is bool


# --------------------------------------------------------------------
# 7. Errors: try / except / else / finally, and raise
# --------------------------------------------------------------------
def topic_07_errors():
    """Errors: try / except / else / finally, and raise"""
    # --- Basic form: try / except ---
    # Read a traceback bottom to top: the last line is the actual error.
    try:
        data = {'greeting': ['hey', 'friend']}
        data.append([])             # dicts have no .append() -> AttributeError
    except Exception as e:
        # Exception is the common parent of almost all errors (except KeyboardInterrupt
        # and SystemExit). Catching it is a safe way to handle nearly any error.
        print(f'There is an error: {e}')   # -> There is an error: 'dict' object has no attribute 'append'

    # --- Full form: try / except / else / finally ---
    try:
        f = open('users.txt', encoding='utf-8')     # the one risky operation
    except FileNotFoundError:
        print('No such file')                       # runs only on THIS error
    else:
        print(f.read())                             # runs only if NO error happened
        f.close()
    finally:
        print('The End.')                           # runs ALWAYS, error or not
    # Keep only the risky call (open) in try and put the success code in else, so the
    # except does not accidentally catch an error coming from the success code.

    # --- raise: throw an error yourself ---
    ports = [21, 22, 80, 99999, 445]
    try:
        for p in ports:
            if p < 1 or p > 65535:                  # outside the valid range: OR, not AND
                raise ValueError(f'Bad port: {p}')
            print(p)                                # -> 21  /  22  /  80
    except ValueError as e:
        print(f'Stopped: {e}')                      # -> Stopped: Bad port: 99999
    # The loop never reaches 445: raise leaves it at 99999.
    # Without the try/except around it, raise would stop the whole script and print
    # a traceback. raise SystemExit('message') stops it without a traceback.


# --------------------------------------------------------------------
# 8. Files
# --------------------------------------------------------------------
def topic_08_files():
    """Files"""
    # Modes: 'r' read (default), 'w' overwrite, 'a' append, 'rb' / 'wb' binary.
    # "with" closes the file automatically, even if an error happens inside.
    with open('some_file.txt', 'w', encoding='utf-8') as f:
        for word in ['Hello, ', 'you! ', 'I am ', 'Dexter Morgan']:
            f.write(word)

    with open('some_file.txt', 'a', encoding='utf-8') as f:
        f.write('\nSecond line, added with mode a')

    with open('some_file.txt', encoding='utf-8') as f:
        print(f.read())
    # -> Hello, you! I am Dexter Morgan
    # -> Second line, added with mode a


# --------------------------------------------------------------------
# 9. Modules: import
# --------------------------------------------------------------------
def topic_09_modules():
    """Modules: import"""
    # A module is a ready-made set of functions, pulled in with "import".
    import json

    parsed = json.loads('[{"greeting": "Hello!"}, {"bye": "A bientot!"}]')
    print(parsed)                   # -> [{'greeting': 'Hello!'}, {'bye': 'A bientot!'}]

    # Standard library modules (json, socket, sqlite3, ...) ship with Python.
    # Third-party ones (requests, bs4, ...) must be installed first: see topic 10.
    print(json.__file__)            # where the module was loaded from


# --------------------------------------------------------------------
# 10. Virtual environments (venv)
# --------------------------------------------------------------------
def topic_10_venv():
    """Virtual environments (venv)"""
    # A venv keeps the third-party modules of one project apart from the rest of
    # the system. In a terminal:
    #   python3 -m venv .venv            create an isolated environment
    #   source .venv/bin/activate        activate it (Windows: .venv\Scripts\activate)
    #   pip install requests             install a module into THIS environment
    #
    # Never name your own file after a module (requests.py, socket.py): Python would
    # find your file before the real module and the import breaks.
    import sys

    print(sys.prefix != sys.base_prefix)    # -> True inside a venv, False outside
    print(sys.executable)                   # the interpreter that is running this file


# ====================================================================
# PART 2: WORKING WITH COLLECTIONS
# ====================================================================

# --------------------------------------------------------------------
# 11. List comprehension
# --------------------------------------------------------------------
def topic_11_list_comprehension():
    """List comprehension"""
    # A loop folded into one line that builds a list.
    raw = ['22', '80', 'http']
    ports = [int(p) for p in raw if p.isdigit()]
    #        ^ what to keep  ^ where from    ^ which ones to keep
    # Read it as: for p in raw -> if p.isdigit() -> keep int(p).
    print(ports)                    # -> [22, 80]


# --------------------------------------------------------------------
# 12. Dictionary comprehension
# --------------------------------------------------------------------
def topic_12_dict_comprehension():
    """Dictionary comprehension"""
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


# --------------------------------------------------------------------
# 13. any() and all()
# --------------------------------------------------------------------
def topic_13_any_all():
    """any() and all()"""
    # any() stops at the first True; all() stops at the first False.
    ports = [22, 80, 443, 445, 4444, 8080]
    print(any(p == 4444 for p in ports))    # -> True    at least one port equals 4444
    print(all(p < 1024 for p in ports))     # -> False   not ALL ports are below 1024 (privileged)


# --------------------------------------------------------------------
# 14. Sorting: sorted() + lambda
# --------------------------------------------------------------------
def topic_14_sorting():
    """Sorting: sorted() + lambda"""
    print(sorted([443, 22, 80]))                    # -> [22, 80, 443]
    print(sorted([443, 22, 80], reverse=True))      # -> [443, 80, 22]

    # sorted() can order numbers and strings on its own, but not dicts: you must
    # tell it WHICH field to sort by, via key=. lambda is a one-line nameless function.
    findings = [
        {'target': '10.10.10.1', 'vulnerabilities': 15},
        {'target': '10.10.10.2', 'vulnerabilities': 7},
        {'target': '10.10.10.3', 'vulnerabilities': 9},
    ]
    by_vulns = sorted(findings, key=lambda f: f['vulnerabilities'], reverse=True)
    #                           ^ for each f, compare by f['vulnerabilities']
    print([f['target'] for f in by_vulns])          # -> ['10.10.10.1', '10.10.10.3', '10.10.10.2']
    print(by_vulns[0]['vulnerabilities'])           # -> 15   the worst host comes first
    # Sort by two fields: return a tuple, e.g. key=lambda f: (f['host'], f['port']).


# --------------------------------------------------------------------
# 15. Counting: Counter and defaultdict(int)
# --------------------------------------------------------------------
def topic_15_counting():
    """Counting: Counter and defaultdict(int)"""
    from collections import Counter, defaultdict

    ips = ['11.11.11.5', '11.11.11.6', '11.11.11.5', '11.11.11.5']

    # Counter: counts occurrences in one line.
    print(Counter(ips).most_common())     # -> [('11.11.11.5', 3), ('11.11.11.6', 1)]

    # defaultdict(int): the same count built by hand (each new key starts at 0).
    count = defaultdict(int)
    for ip in ips:
        count[ip] += 1                    # same ip -> same key -> its counter grows
    print(dict(count))                    # -> {'11.11.11.5': 3, '11.11.11.6': 1}


# --------------------------------------------------------------------
# 16. De-duplicate while keeping order
# --------------------------------------------------------------------
def topic_16_dedupe():
    """De-duplicate while keeping order"""
    items = ['b', 'a', 'b', 'c']
    print(sorted(set(items)))             # -> ['a', 'b', 'c']   no duplicates, original order lost
    print(list(dict.fromkeys(items)))     # -> ['b', 'a', 'c']   no duplicates, order kept
    # dict.fromkeys turns the items into dict KEYS (which are unique), so repeats
    # collapse while the first-seen order is preserved; list() then reads the keys back.


# ====================================================================
# PART 3: BYTES, HASHES, DATA FORMATS
# ====================================================================

# --------------------------------------------------------------------
# 17. Text and bytes (encoding / decoding)
# --------------------------------------------------------------------
def topic_17_text_and_bytes():
    """Text and bytes (encoding / decoding)"""
    # The network and files deal in bytes; humans deal in str. Convert explicitly.
    print('my_name_is_Alice'.encode('utf-8'))     # -> b'my_name_is_Alice'   str -> bytes
    print(b'my_name_is_Alice'.decode('utf-8'))    # -> my_name_is_Alice      bytes -> str

    # One character is not always one byte: "e with an accent" takes two in UTF-8.
    word = 'caf\xe9'                              # \xe9 is that accented e, written as an escape
    print(word.encode('utf-8'))                   # -> b'caf\xc3\xa9'
    print(len(word), len(word.encode('utf-8')))   # -> 4 5


# --------------------------------------------------------------------
# 18. Bytes deeper: hex, endianness, struct
# --------------------------------------------------------------------
def topic_18_bytes_deeper():
    """Bytes deeper: hex, endianness, struct"""
    import struct

    # A byte is just a number from 0 to 255. Hex is a compact way to write it:
    # two hex digits = one byte. \x41 inside b'...' means "the byte 0x41".
    print(b'AB'.hex())                            # -> 4142     'A' is 0x41, 'B' is 0x42
    print(bytes.fromhex('4142'))                  # -> b'AB'
    print(bytes([65, 1, 66]))                     # -> b'A\x01B'   printable bytes show as letters

    # A number above 255 needs several bytes. Endianness = which byte comes first.
    print((255).to_bytes(1, 'big'))               # -> b'\xff'       255 fits in a single byte
    print((255).to_bytes(2, 'big'))               # -> b'\x00\xff'   two bytes: 0*256 + 255*1
    print(int.from_bytes(b'\x01\x00', 'big'))     # -> 256   big-endian: high byte first (1*256 + 0)
    print(int.from_bytes(b'\x01\x00', 'little'))  # -> 1     little-endian: low byte first (1*1 + 0)

    # struct packs numbers into bytes by a format string; you meet it in exploit code.
    # '<I' means: < little-endian, I unsigned 4-byte integer.
    print(struct.pack('<I', 1))                           # -> b'\x01\x00\x00\x00'
    print(struct.unpack('<I', b'\x01\x00\x00\x00'))       # -> (1,)   always a tuple


# --------------------------------------------------------------------
# 19. Encoding, hashing and base64
# --------------------------------------------------------------------
def topic_19_encoding_and_hashing():
    """Encoding, hashing and base64"""
    import base64
    import hashlib

    # Encoding: the same data in another form (base64, hex, URL-encoding).
    #           Reversible, no key needed. It is NOT protection.
    # Hashing:  a fixed-length fingerprint of the data (MD5, SHA-256). Not reversible.
    creds = base64.b64encode(b'admin:admin')
    print(creds)                       # -> b'YWRtaW46YWRtaW4='
    print(base64.b64decode(creds))     # -> b'admin:admin'

    hashed = hashlib.sha384(b'secret_password').hexdigest()   # hexdigest: the hash as hex text
    print(len(hashed))                 # -> 96
    print(hashed)                      # handy for comparing hashes and checking file integrity
    # Length hints: 32 hex chars -> MD5, 40 -> SHA-1, 64 -> SHA-256, 96 -> SHA-384, 128 -> SHA-512.


# --------------------------------------------------------------------
# 20. JSON
# --------------------------------------------------------------------
def topic_20_json():
    """JSON"""
    import json

    # JSON is a text format that looks almost like Python dicts and lists.
    # Many web services and tools return their data in it.
    text = '{"username": "Someone_173", "roles": ["PenTester", "DevSecOps"]}'
    data = json.loads(text)                   # JSON text -> Python dict
    print(data['username'])                   # -> Someone_173
    print(data['roles'][0])                   # -> PenTester   (dict -> list -> item 0)
    print(json.dumps(data, indent=2))         # dict -> nicely formatted JSON text

    # For a web response in JSON, r.json() from requests does the same as json.loads(r.text).


# --------------------------------------------------------------------
# 21. SQLite (and SQL injection)
# --------------------------------------------------------------------
def topic_21_sqlite():
    """SQLite (and SQL injection)"""
    import sqlite3

    # SQLite is a database in a single file (.db / .sqlite). Common in small web apps.
    # ':memory:' keeps this demo database in RAM; pass a name such as 'recon.db'
    # to keep it on disk.
    conn = sqlite3.connect(':memory:')
    conn.execute("""
        CREATE TABLE IF NOT EXISTS services (
            id        INTEGER PRIMARY KEY,
            host      TEXT NOT NULL,
            port      INTEGER NOT NULL,
            proto     TEXT DEFAULT 'tcp',                  -- used if the column is omitted on insert
            service   TEXT,
            notes     TEXT,
            found_at  TEXT DEFAULT CURRENT_TIMESTAMP,      -- current UTC date and time
            UNIQUE (host, port, proto)                     -- the whole combination must be unique
        )
    """)

    first_findings = [
        ('10.10.120.1', 22,  'ssh',   'No valid keys or credentials found yet'),
        ('10.10.120.1', 80,  'http',  None),
        ('10.10.120.1', 443, 'https', None),
        ('10.10.120.2', 445, 'smb',   'Not enumerated yet'),
    ]
    # executemany runs the same INSERT for every tuple in the list.
    # The ? placeholders keep the values apart from the SQL text.
    conn.executemany(
        'INSERT OR IGNORE INTO services (host, port, service, notes) VALUES (?, ?, ?, ?)',
        first_findings,
    )
    conn.commit()                             # without commit the changes are not saved

    # Update one row. SET is part of UPDATE ... SET column = value, not a separate command.
    conn.execute(
        'UPDATE services SET notes = ? WHERE host = ? AND port = ?',
        ('Valid creds for john:john123', '10.10.120.1', 22),
    )
    conn.commit()

    # Read: execute() returns a cursor. .fetchall() gives the rows as a list of tuples.
    rows = conn.execute(
        'SELECT port, service, notes FROM services WHERE host = ? ORDER BY port',
        ('10.10.120.1',),                     # one value still needs a tuple: note the comma
    ).fetchall()
    for row in rows:
        print(row)
    # -> (22, 'ssh', 'Valid creds for john:john123')
    # -> (80, 'http', None)
    # -> (443, 'https', None)

    # SQL injection: the same "user input" through a placeholder and through an f-string.
    user_input = "nothing' OR '1'='1"
    safe = conn.execute(
        'SELECT COUNT(*) FROM services WHERE host = ?', (user_input,),
    ).fetchone()[0]
    unsafe = conn.execute(
        f"SELECT COUNT(*) FROM services WHERE host = '{user_input}'",
    ).fetchone()[0]
    print(safe)                               # -> 0   SAFE: the input stayed plain data
    print(unsafe)                             # -> 4   DANGEROUS: the input became SQL and matched every row
    conn.close()


# ====================================================================
# PART 4: PROCESSES, NETWORK, CLI
# ====================================================================

# --------------------------------------------------------------------
# 22. subprocess: run other programs
# --------------------------------------------------------------------
def topic_22_subprocess():
    """subprocess: run other programs"""
    import subprocess
    import sys

    # The command is a LIST: one argument per item (topic 24 explains why).
    r = subprocess.run(['whoami'], capture_output=True, text=True)
    print(f'Exit code: {r.returncode}')       # -> Exit code: 0
    print(f'Output: {r.stdout.strip()}')      # your user name

    # Two options worth adding almost every time. sys.executable is the Python that
    # runs this file; it stands in for "some other program" so the demo works anywhere.

    # check=True: raise an error on a non-zero exit code instead of continuing silently.
    # (Some tools use non-zero for normal results: grep returns 1 when it finds nothing.)
    try:
        subprocess.run([sys.executable, '-c', 'import sys; sys.exit(3)'], check=True)
    except subprocess.CalledProcessError as e:
        print(f'The program failed with exit code {e.returncode}')   # -> ... exit code 3

    # timeout=N: stop the program if it runs longer than N seconds.
    try:
        subprocess.run([sys.executable, '-c', 'import time; time.sleep(5)'], timeout=1)
    except subprocess.TimeoutExpired:
        print('The program took too long and was stopped')


# --------------------------------------------------------------------
# 23. subprocess in practice: wrapping nmap
# --------------------------------------------------------------------
def topic_23_wrapping_nmap():
    """subprocess in practice: wrapping nmap"""
    import subprocess

    target = input('Host you are allowed to scan (Enter to skip): ').strip()
    if not target:
        print('Skipped.')
        return
    if target.startswith('-'):
        # A list protects from shell injection, but the tool itself would still read
        # a value such as "-oN file" as one of its own options. Refuse it.
        print('A target cannot start with "-".')
        return

    try:
        r = subprocess.run(
            ['nmap', '-p-', '--min-rate', '3000', '-T4', target],
            capture_output=True, text=True, timeout=1000,
        )
        print(r.stdout or r.stderr)
    except FileNotFoundError:
        print('nmap is not installed or not in PATH.')
    except subprocess.TimeoutExpired:
        print('The scan took too long and was stopped.')


# --------------------------------------------------------------------
# 24. Command injection (why shell=True is dangerous)
# --------------------------------------------------------------------
def topic_24_command_injection():
    """Command injection (why shell=True is dangerous)"""
    import os
    import subprocess
    import sys

    # If user or network text reaches a command that runs through the shell,
    # characters like ; or & are read by the shell as "now run another command".
    separator = '&' if os.name == 'nt' else ';'
    user_input = f'hello {separator} whoami'      # imagine this arrived from a web form

    # DANGEROUS: one string + shell=True. The shell prints hello, then RUNS whoami.
    r = subprocess.run(f'echo {user_input}', shell=True, capture_output=True, text=True)
    print(r.stdout.strip())

    # SAFE: a list. Every item is exactly one argument, so ; is only a character.
    r = subprocess.run(
        [sys.executable, '-c', 'import sys; print(sys.argv[1])', user_input],
        capture_output=True, text=True,
    )
    print(r.stdout.strip())                       # -> hello ; whoami   (printed, not executed)


# --------------------------------------------------------------------
# 25. socket: talk to a service directly
# --------------------------------------------------------------------
def topic_25_socket():
    """socket: talk to a service directly"""
    import socket

    # A socket is a "phone line" between two programs: connect, send bytes, get bytes.
    target_ip = input('Target IP in your lab (Enter to skip): ').strip()
    if not target_ip:
        print('Skipped.')
        return
    try:
        target_port = int(input('Target port: ').strip())     # input() returns str: convert it
    except ValueError:
        print('The port must be a number.')
        return

    try:
        with socket.create_connection((target_ip, target_port), timeout=7) as s:
            banner = s.recv(1024)             # read up to 1024 bytes (FTP, SSH, SMTP greet first)
            print(banner.decode(errors='replace'))
            s.sendall(b'Hello, G!\n')         # send bytes: note the b'' prefix and the newline
            print(s.recv(4096).decode(errors='replace'))
    except OSError as e:                      # refused, unreachable, timed out, ...
        print(f"Couldn't talk to the service. Error: {e}")


# --------------------------------------------------------------------
# 26. requests: HTTP calls
# --------------------------------------------------------------------
def topic_26_requests():
    """requests: HTTP calls"""
    import requests

    url = input('URL to request (Enter for https://example.com): ').strip() or 'https://example.com'
    if not url.startswith(('http://', 'https://')):
        url = f'https://{url}'

    try:
        response = requests.get(url, timeout=7)   # always set a timeout: there is none by default
        response.raise_for_status()               # turn 4xx / 5xx answers into an error
        print(response.status_code)               # 200 ok, 301/302 redirect, 404 not found, ...
        print(response.headers.get('Server'))     # one response header (None if it is absent)
        print(response.text[:200])                # the page as text; .content is the raw bytes
    except requests.RequestException as e:        # base class of all requests errors
        print(f"Couldn't complete the request. Error: {e}")


# --------------------------------------------------------------------
# 27. ipaddress: IPs and networks
# --------------------------------------------------------------------
def topic_27_ipaddress():
    """ipaddress: IPs and networks"""
    import ipaddress

    # ip_address turns the text into a real number, so membership and sorting work.
    host = ipaddress.ip_address('192.168.2.1')      # an IPv4Address object
    net = ipaddress.ip_network('192.168.2.0/30')    # an IPv4Network object
    print(host in net)                              # -> True
    print(ipaddress.ip_address('10.10.1.2') in ipaddress.ip_network('10.10.0.0/24'))   # -> False

    # Build a target list from "network / mask" (the mask as /29 or as 255.255.255.248):
    network, mask = '10.10.10.0', '255.255.255.248'
    net = ipaddress.ip_network(f'{network}/{mask}')
    print(net.num_addresses)                        # -> 8   ALL addresses, with network and broadcast
    print([str(ip) for ip in net.hosts()])          # only the addresses usable by hosts
    # -> ['10.10.10.1', '10.10.10.2', '10.10.10.3', '10.10.10.4', '10.10.10.5', '10.10.10.6']

    # Sorting IPs as plain strings is wrong ('10' sorts before '9'). Sort them as addresses:
    ips = ['10.10.10.10', '10.10.10.9']
    print(sorted(ips))                              # -> ['10.10.10.10', '10.10.10.9']   wrong
    print(sorted(ips, key=ipaddress.ip_address))    # -> ['10.10.10.9', '10.10.10.10']   right


# --------------------------------------------------------------------
# 28. A small CLI script (argv, exit codes, __main__)
# --------------------------------------------------------------------
def topic_28_cli_script():
    """A small CLI script (argv, exit codes, __main__)"""
    import sys

    def main(argv):
        if len(argv) != 2:                        # argv[0] is the script name itself
            print('usage: ./check.py <ip>', file=sys.stderr)
            return 1                              # a non-zero exit code means "error"
        ip = argv[1]
        print(f'Scanning {ip}')
        return 0

    # In a real script the file ends with these two lines. The condition is true only
    # when the file is launched directly, not when it is imported as a module:
    #
    #     if __name__ == '__main__':
    #         sys.exit(main(sys.argv))
    #
    # Here we call main() by hand with the lists the shell would have produced:
    print(main(['check.py']))                     # -> 1   (and the usage line on stderr)
    print(main(['check.py', '10.10.10.5']))       # -> Scanning 10.10.10.5  /  0


# --------------------------------------------------------------------
# 29. argparse: real CLI parameters
# --------------------------------------------------------------------
def topic_29_argparse():
    """argparse: real CLI parameters"""
    import argparse

    # argparse reads the words typed after the script name and turns them into
    # named values, based on the arguments you declare.
    p = argparse.ArgumentParser(prog='check.py', description='Check one port of a host.')
    p.add_argument('ip', metavar='IP', help='target IP address')          # no dash: positional, required
    p.add_argument('-p', '--port', type=int, default=80, metavar='PORT',
                   help='target port (default: 80)')                      # optional, converted to int
    p.add_argument('-v', '--verbose', action='store_true',
                   help='print detailed information')                     # flag: present -> True

    # parse_args() with no arguments reads the real command line (sys.argv[1:]).
    # A list is passed here so the demo can show two different command lines.
    args = p.parse_args(['10.10.10.5'])
    print(args.ip, args.port, args.verbose)       # -> 10.10.10.5 80 False

    args = p.parse_args(['-p', '443', '10.10.10.5', '-v'])
    print(args.ip, args.port, args.verbose)       # -> 10.10.10.5 443 True

    print(p.format_usage().strip())               # -> usage: check.py [-h] [-p PORT] [-v] IP
    # Notes:
    #   * Everything from the shell arrives as str, so type=int converts the port.
    #   * With two names, the variable is named after the LONG one (--port -> args.port);
    #     dest='...' overrides it.
    #   * metavar (meta + variable) is the placeholder shown for the value in --help.
    #   * -h / --help is generated for you from the help= texts.


# --------------------------------------------------------------------
# 30. stdout vs stderr
# --------------------------------------------------------------------
def topic_30_stdout_vs_stderr():
    """stdout vs stderr"""
    import subprocess
    import sys

    # A program has two output streams: stdout for results, stderr for diagnostics.
    # To see them apart, run a small script as a child process and capture both.
    child_script = (
        "import sys\n"
        "for host in ['10.10.10.5', 'bad-ip', '10.10.10.6']:\n"
        "    if host[0].isdigit():\n"
        "        print(host)\n"
        "    else:\n"
        "        print(f'skip invalid host: {host}', file=sys.stderr)\n"
    )
    r = subprocess.run([sys.executable, '-c', child_script], capture_output=True, text=True)
    print(repr(r.stdout))   # -> '10.10.10.5\n10.10.10.6\n'     the result only
    print(repr(r.stderr))   # -> 'skip invalid host: bad-ip\n'   the diagnostics only
    # This is why "tool > result.txt" in a shell saves clean data while the warnings
    # stay on the screen.


# --------------------------------------------------------------------
# 31. print(file=...) and repr()
# --------------------------------------------------------------------
def topic_31_print_and_repr():
    """print(file=...) and repr()"""
    # print() can write to any file object via file=, not just to the screen.
    with open('some_file.txt', 'w', encoding='utf-8') as f:
        print('No, it is me, Tony Soprano', file=f)
    with open('some_file.txt', encoding='utf-8') as f:
        print(f.read().strip())     # -> No, it is me, Tony Soprano

    # repr(x) returns a string that shows the value EXACTLY as it is: with quotes and
    # with special characters written as \n, \t. Plain print shows the human view
    # (a newline really breaks the line, quotes are invisible).
    role = '\tsys_admin\n'
    print(role)                     # ->     sys_admin   (a tab before, an empty line after)
    print(repr(role))               # -> '\tsys_admin\n'
    # repr() is the fastest way to spot a stray space or newline in data you parse.


# ====================================================================
# PART 5: WEB AUTOMATION AND INTROSPECTION
# http://books.toscrape.com/ is a site built for scraping practice.
# ====================================================================

# --------------------------------------------------------------------
# 32. BeautifulSoup: parse HTML
# --------------------------------------------------------------------
def topic_32_beautifulsoup():
    """BeautifulSoup: parse HTML"""
    import requests
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin, urlparse

    # BeautifulSoup reads the HTML text, finds the opening and closing tags and
    # builds a tree in memory. After that you query the tree, not the raw string.
    #
    # Example: a tiny two-level link counter for a page and the pages it links to.

    def get_links(url, session, timeout=5):
        r = session.get(url, timeout=timeout)
        r.raise_for_status()                              # raise on 4xx / 5xx
        soup = BeautifulSoup(r.text, 'html.parser')
        links = []
        for tag in soup.find_all('a', href=True):         # every <a> that has an href
            full = urljoin(url, tag['href'])              # turn relative links into absolute ones
            if urlparse(full).scheme in ('http', 'https'):    # drop mailto:, javascript:, ...
                links.append(full)
        return list(dict.fromkeys(links))                 # de-duplicate, keep order (topic 16)

    default_url = 'http://books.toscrape.com/'
    start_url = input(f'URL to parse (Enter for {default_url}): ').strip() or default_url
    max_pages = 10                                        # be polite: visit only a few pages
    session = requests.Session()                          # reuses the connection and keeps cookies

    try:
        first_level = get_links(start_url, session)
    except requests.RequestException as e:
        print(f"Can't fetch the start page {start_url}. Error: {e}")
        return

    print(f'The start page has {len(first_level)} unique links. Visiting the first {max_pages}...')

    second_level = []
    for link in first_level[:max_pages]:
        try:
            second_level.extend(get_links(link, session))
        except requests.RequestException as e:
            print(f"Can't fetch {link}. Error: {e}")

    second_level = list(dict.fromkeys(second_level))
    print(f'Found {len(second_level)} unique links on the second level.')


# --------------------------------------------------------------------
# 33. Selenium: drive a real browser
# --------------------------------------------------------------------
def topic_33_selenium():
    """Selenium: drive a real browser"""
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    # Use a real browser when the page is built by JavaScript and the data is not
    # in r.text. "By" says HOW to locate an element: By.ID, By.CSS_SELECTOR,
    # By.CLASS_NAME, By.TAG_NAME, By.XPATH.
    # The default page is the practice page from the book; it has a login form
    # with the element ids used below. For another page, change the ids.
    default_url = 'https://autbor.com/example3.html'
    url = input(f'URL to open (Enter for {default_url}): ').strip() or default_url

    browser = webdriver.Firefox()                         # opens a real Firefox window
    try:
        browser.get(url)
        user = browser.find_element(By.ID, 'login_user')  # first match; find_elements -> list of all
        user.send_keys('admin')                           # type into the field
        password = browser.find_element(By.ID, 'login_pass')
        password.send_keys('not_a_real_password')
        password.submit()                                 # sends the WHOLE form once, from any field in it
        print(browser.title)
    finally:
        browser.quit()                                    # mandatory: closes the browser process


# --------------------------------------------------------------------
# 34. Playwright: modern browser automation
# --------------------------------------------------------------------
def topic_34_playwright():
    """Playwright: modern browser automation"""
    from playwright.sync_api import sync_playwright

    # Playwright does the same job as Selenium, but it waits for an element to be
    # ready before acting and ships its own browser builds.
    # Locator cheat-sheet (Selenium -> Playwright):
    #     find_element(By.CSS_SELECTOR, 'a')  ->  page.locator('a')
    #     find_element(By.ID, 'x')            ->  page.locator('#x')
    #     find_element(By.XPATH, '//a')       ->  page.locator('xpath=//a')
    #     elem.send_keys('abc')               ->  page.locator(...).fill('abc')
    #     elem.text                           ->  page.locator(...).inner_text()
    default_url = 'https://autbor.com/example3.html'
    url = input(f'URL to open (Enter for {default_url}): ').strip() or default_url

    with sync_playwright() as pw:                         # starts the driver (a Node.js process)
        browser = pw.firefox.launch(headless=False)       # a separate Firefox process; False shows the window
        page = browser.new_page()                         # a fresh isolated profile and one tab
        page.goto(url)

        page.locator('#login_user').fill('admin')
        page.locator('#login_pass').fill('not_a_real_password')
        page.locator('input[type=submit]').click()        # input is the tag, type=submit an attribute filter

        print(page.title())
        browser.close()     # "with" stops only the driver, so close the browser as well.
                            # Alternative: with pw.firefox.launch() as browser: ...


# --------------------------------------------------------------------
# 35. Introspection: type(), dir(), help(), chr(), ord()
# --------------------------------------------------------------------
def topic_35_introspection():
    """Introspection: type(), dir(), help(), chr(), ord()"""
    # Ask Python itself what an object is and what it can do.
    data = b'admin'
    print(type(data))                                       # -> <class 'bytes'>
    print([name for name in dir(data) if 'hex' in name])    # -> ['fromhex', 'hex']
    print(data.hex.__doc__.splitlines()[0])                 # the first line of the built-in help
    # In the interactive shell, help(data.hex) or help(bytes) shows the full text
    # (like man in bash or Get-Help in PowerShell).

    print(chr(77))                  # -> M    number -> character
    print(ord('I'))                 # -> 73   character -> number

    # Printing a function WITHOUT calling it shows the object, not a result:
    print(str.upper)                # -> <method 'upper' of 'str' objects>
    print(str.upper('admin'))       # -> ADMIN   the parentheses make the call


# ====================================================================
# RUNNER
# The part below only lists and launches the topics above. You do not need to
# read it to use the reference, but it is itself built from topics 7, 12 and 29.
# ====================================================================

PARTS = {
    1: 'PART 1: CORE PYTHON',
    11: 'PART 2: WORKING WITH COLLECTIONS',
    17: 'PART 3: BYTES, HASHES, DATA FORMATS',
    22: 'PART 4: PROCESSES, NETWORK, CLI',
    32: 'PART 5: WEB AUTOMATION AND INTROSPECTION',
}

# Topics that ask for input or reach other hosts. "all" skips them.
NEEDS = {
    23: 'nmap and a lab target',
    25: 'a lab target',
    26: 'network, requests',
    32: 'network, requests, beautifulsoup4',
    33: 'network, selenium, Firefox',
    34: 'network, playwright',
}


def collect_topics():
    """Return {number: function} for every topic_NN_* function in this file."""
    topics = {}
    for name, obj in globals().items():
        parts = name.split('_')
        if parts[0] == 'topic' and len(parts) > 2 and parts[1].isdigit():
            topics[int(parts[1])] = obj
    return dict(sorted(topics.items()))


def list_topics(topics):
    for number, func in topics.items():
        if number in PARTS:
            print(f'\n{PARTS[number]}')
        note = f'   [needs: {NEEDS[number]}]' if number in NEEDS else ''
        print(f'  {number:>2}  {func.__doc__}{note}')
    print('\nRun a topic:  python python_essentials.py NUMBER [NUMBER ...]')
    print('Run all offline topics:  python python_essentials.py all')


def body_of(func):
    """Return the body of a topic function as text, without the def line and docstring."""
    import inspect
    import textwrap

    lines = inspect.getsource(func).splitlines()
    return textwrap.dedent('\n'.join(lines[2:])).strip('\n')


def run_topic(number, func, show_source=True):
    title = f' {number}. {func.__doc__} '
    print(f'\n{title:=^72}')
    if show_source:
        print(body_of(func))
        print(f'{" output ":-^72}')
    try:
        func()
    except ModuleNotFoundError as e:
        print(f'Missing package: {e.name}. Install the extras: pip install -r requirements.txt')
    except (KeyboardInterrupt, EOFError):         # Ctrl+C, or the input was closed
        print('\nInterrupted.')


def main(argv=None):
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description='Python Essentials for beginners: print a topic and run it.',
        epilog='With no arguments the list of topics is shown.',
    )
    parser.add_argument('topics', nargs='*', metavar='TOPIC',
                        help='topic numbers to run, or "all" for every offline topic')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='run the topic without printing its code first')
    args = parser.parse_args(argv)

    topics = collect_topics()
    if not args.topics:
        list_topics(topics)
        return 0

    if args.topics == ['all']:
        numbers = [n for n in topics if n not in NEEDS]
    else:
        try:
            numbers = [int(t) for t in args.topics]
        except ValueError:
            print('A topic must be a number, or the single word "all".', file=sys.stderr)
            return 2
        unknown = [n for n in numbers if n not in topics]
        if unknown:
            print(f'No such topic: {unknown}. Valid numbers: 1-{max(topics)}.', file=sys.stderr)
            return 2

    for number in numbers:
        run_topic(number, topics[number], show_source=not args.quiet)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
