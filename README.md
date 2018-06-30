# Debsec

Prints Debian Security Advisories.

## Installation

Requires Python >= 3.5, libxml2 and libxslt.

```sh
$ pip install -r requirements.txt
```

## Usage

```sh
$ python debsec.py
4078 linux security update
4079 poppler security update
4080 php7.0 security update
4081 php5 security update
[...]
```

```sh
$ python debsec.py 4078
Package        : linux
CVE ID         : CVE-2017-5754

Multiple researchers have discovered a vulnerability in Intel processors,
enabling an attacker controlling an unprivileged process to read memory from
arbitrary addresses, including from the kernel and all other processes running
on the system.
[...]
```

## Tests

```sh
$ python -m unittest
```
