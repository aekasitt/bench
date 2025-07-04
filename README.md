# Bench

[![Languages](https://img.shields.io/github/languages/count/aekasitt/bench)](https://github.com/aekasitt/bench)
[![Last commit](https://img.shields.io/github/last-commit/aekasitt/bench/master)](https://github.com/aekasitt/bench)
[![Size](https://img.shields.io/github/repo-size/aekasitt/bench)](https://github.com/aekasitt/bench)
[![Top](https://img.shields.io/github/languages/top/aekasitt/bench)](https://github.com/aekasitt/bench)

[![Bench Banner](./static/bench-banner.svg)](https://github.com/aekasitt/bench/blob/master/static/bench-banner.svg)

## Contenders

* FastAPI (python)
* Fastify (node) 
* Litestar (python)
* Vanilla (node)
* Starlette (python)
* ASGI spec, henceforth called "Spartan" (python)

This repository uses [autocannon](https://npmjs.com/package/autocannon) for basic and
non-reproduceable-on-production test for a web server implemented by [FastAPI](https://fastapi.tiangolo.com),
[Fastify](https://fastify.dev), [Litestar](https://litestar.dev), simple vanilla implementation
of a web server on [Node.js](https://nodejs.org), a minimalistic [Starlette](starlette.io) applet
and finally a simple plain ASGI application according to
[Asynchronous Server Gateway Interface specs](https://asgi.readthedocs.io/en/latest/specs/main.html)
henceforth called the Spartan implementation.

## Why work on something if it does not reproduce on production?

Trends matter and [Python](https://www.python.org)'s JIT compilation and Global Interpreter Lock
experimentations may bare different fruits in the not so distant future. Having something easily
upgradeable on the local environment may prove useful for quick and dirty tests to see improvements
made in the short to intermediate term.

Plus, it's fun.

## Results

### Python FastAPI

<details>
    <summary> Autocannon results on localhost running FastAPI /api/devices </summary>

    Running 10s test @ http://localhost:8080/api/devices
    10000 connections
    
    ┌─────────┬────────┬────────┬─────────┬─────────┬───────────┬───────────┬─────────┐
    │ Stat    │ 2.5%   │ 50%    │ 97.5%   │ 99%     │ Avg       │ Stdev     │ Max     │
    ├─────────┼────────┼────────┼─────────┼─────────┼───────────┼───────────┼─────────┤
    │ Latency │ 254 ms │ 376 ms │ 1503 ms │ 4026 ms │ 567.36 ms │ 712.97 ms │ 8347 ms │
    └─────────┴────────┴────────┴─────────┴─────────┴───────────┴───────────┴─────────┘
    ┌───────────┬────────┬────────┬────────┬─────────┬──────────┬──────────┬─────────┐
    │ Stat      │ 1%     │ 2.5%   │ 50%    │ 97.5%   │ Avg      │ Stdev    │ Min     │
    ├───────────┼────────┼────────┼────────┼─────────┼──────────┼──────────┼─────────┤
    │ Req/Sec   │ 28,415 │ 28,415 │ 46,559 │ 47,455  │ 42,865.6 │ 7,257.98 │ 28,405  │
    ├───────────┼────────┼────────┼────────┼─────────┼──────────┼──────────┼─────────┤
    │ Bytes/Sec │ 19 MB  │ 19 MB  │ 31 MB  │ 31.7 MB │ 28.6 MB  │ 4.84 MB  │ 18.9 MB │
    └───────────┴────────┴────────┴────────┴─────────┴──────────┴──────────┴─────────┘
    
    Req/Bytes counts sampled once per second.
    # of samples: 5
    
    236k requests in 15.68s, 143 MB read
    12k errors (0 timeouts)
</details>
<details>
  <summary> Time verbose results wrapped around localhost running FastAPI /api/devices </summary>
  
    $ /usr/bin/time -l bench-fastapi
    >            24.33  real
    >            81.27  user
    >            15.54  sys
    >         59867136  maximum resident set size
    >                0  average shared memory size
    >                0  average unshared data size
    >                0  average unshared stack size
    >           460461  page reclaims
    >             5470  page faults
    >                0  swaps
    >                0  block input operations
    >                0  block output operations
    >           670126  messages sent
    >           270275  messages received
    >              133  signals received
    >             3161  voluntary context switches
    >          1697462  involuntary context switches
    >       2795276474  instructions retired
    >       1344843172  cycles elapsed
    >         41125120  peak memory footprint
</details>

### Python Litestar

<details>
    <summary> Autocannon results on localhost running Litestar /api/devices </summary>

    Running 10s test @ http://localhost:8080/api/devices
    10000 connections
    
    ┌─────────┬────────┬────────┬─────────┬─────────┬───────────┬───────────┬─────────┐
    │ Stat    │ 2.5%   │ 50%    │ 97.5%   │ 99%     │ Avg       │ Stdev     │ Max     │
    ├─────────┼────────┼────────┼─────────┼─────────┼───────────┼───────────┼─────────┤
    │ Latency │ 310 ms │ 401 ms │ 1909 ms │ 1963 ms │ 464.58 ms │ 362.87 ms │ 3811 ms │
    └─────────┴────────┴────────┴─────────┴─────────┴───────────┴───────────┴─────────┘
    ┌───────────┬─────────┬─────────┬─────────┬─────────┬───────────┬──────────┬─────────┐
    │ Stat      │ 1%      │ 2.5%    │ 50%     │ 97.5%   │ Avg       │ Stdev    │ Min     │
    ├───────────┼─────────┼─────────┼─────────┼─────────┼───────────┼──────────┼─────────┤
    │ Req/Sec   │ 1,998   │ 1,998   │ 49,151  │ 49,151  │ 41,242.34 │ 17,550.8 │ 1,998   │
    ├───────────┼─────────┼─────────┼─────────┼─────────┼───────────┼──────────┼─────────┤
    │ Bytes/Sec │ 1.33 MB │ 1.33 MB │ 32.8 MB │ 32.8 MB │ 27.5 MB   │ 11.7 MB  │ 1.33 MB │
    └───────────┴─────────┴─────────┴─────────┴─────────┴───────────┴──────────┴─────────┘
    
    Req/Bytes counts sampled once per second.
    # of samples: 6
    
    258k requests in 12.84s, 165 MB read</details>
</details>
<details>
    <summary> Time verbose results wrapped around localhost running Litestar /api/devices </summary>

    $ /usr/bin/time -l bench-litestar
    >            21.22  real
    >            81.36  user
    >            16.25  sys
    >         57901056  maximum resident set size
    >                0  average shared memory size
    >                0  average unshared data size
    >                0  average unshared stack size
    >           485505  page reclaims
    >             5718  page faults
    >                0  swaps
    >                0  block input operations
    >                0  block output operations
    >          1034388  messages sent
    >           327557  messages received
    >              136  signals received
    >             3432  voluntary context switches
    >          1741851  involuntary context switches
    >       2960132923  instructions retired
    >       1481913630  cycles elapsed
    >         43058624  peak memory footprint
</details>

### NodeJS Fastify

<details>
    <summary> Autocannon results on localhost running Fastify /api/devices </summary>

    Running 10s test @ http://localhost:8080/api/devices
    10000 connections
    
    ┌─────────┬────────┬────────┬─────────┬─────────┬───────────┬──────────┬─────────┐
    │ Stat    │ 2.5%   │ 50%    │ 97.5%   │ 99%     │ Avg       │ Stdev    │ Max     │
    ├─────────┼────────┼────────┼─────────┼─────────┼───────────┼──────────┼─────────┤
    │ Latency │ 113 ms │ 179 ms │ 1113 ms │ 3189 ms │ 311.23 ms │ 547.5 ms │ 6717 ms │
    └─────────┴────────┴────────┴─────────┴─────────┴───────────┴──────────┴─────────┘
    ┌───────────┬─────────┬─────────┬─────────┬─────────┬───────────┬──────────┬─────────┐
    │ Stat      │ 1%      │ 2.5%    │ 50%     │ 97.5%   │ Avg       │ Stdev    │ Min     │
    ├───────────┼─────────┼─────────┼─────────┼─────────┼───────────┼──────────┼─────────┤
    │ Req/Sec   │ 44,735  │ 44,735  │ 48,703  │ 63,583  │ 49,505.78 │ 5,113.67 │ 44,709  │
    ├───────────┼─────────┼─────────┼─────────┼─────────┼───────────┼──────────┼─────────┤
    │ Bytes/Sec │ 30.5 MB │ 30.5 MB │ 33.2 MB │ 43.4 MB │ 33.8 MB   │ 3.49 MB  │ 30.5 MB │
    └───────────┴─────────┴─────────┴─────────┴─────────┴───────────┴──────────┴─────────┘
    
    Req/Bytes counts sampled once per second.
    # of samples: 9
    
    464k requests in 12.38s, 304 MB read
    8k errors (0 timeouts)
</details>
<details>
  <summary> Time verbose results wrapped around localhost running Fastify /api/devices </summary>

    $ /usr/bin/time -l pnpm run bench:fastify
    >            18.09  real
    >             1.16  user
    >             0.19  sys
    >        129200128  maximum resident set size
    >                0  average shared memory size
    >                0  average unshared data size
    >                0  average unshared stack size
    >            55970  page reclaims
    >              154  page faults
    >                0  swaps
    >                0  block input operations
    >                0  block output operations
    >                0  messages sent
    >                8  messages received
    >               10  signals received
    >              655  voluntary context switches
    >            12925  involuntary context switches
    >       5487232381  instructions retired
    >       2183373763  cycles elapsed
    >         96192000  peak memory footprint
</details>

### NodeJS Vanilla

<details>
    <summary> Autocannon results on localhost running vanilla Node.js server /api/devices </summary>

    Running 10s test @ http://localhost:8080/api/devices
    10000 connections
    
    ┌─────────┬────────┬────────┬────────┬─────────┬───────────┬───────────┬──────────┐
    │ Stat    │ 2.5%   │ 50%    │ 97.5%  │ 99%     │ Avg       │ Stdev     │ Max      │
    ├─────────┼────────┼────────┼────────┼─────────┼───────────┼───────────┼──────────┤
    │ Latency │ 132 ms │ 176 ms │ 479 ms │ 1327 ms │ 246.75 ms │ 588.03 ms │ 11079 ms │
    └─────────┴────────┴────────┴────────┴─────────┴───────────┴───────────┴──────────┘
    ┌───────────┬─────────┬─────────┬─────────┬─────────┬──────────┬───────────┬─────────┐
    │ Stat      │ 1%      │ 2.5%    │ 50%     │ 97.5%   │ Avg      │ Stdev     │ Min     │
    ├───────────┼─────────┼─────────┼─────────┼─────────┼──────────┼───────────┼─────────┤
    │ Req/Sec   │ 9,703   │ 9,703   │ 41,151  │ 59,359  │ 39,077.2 │ 11,505.71 │ 9,699   │
    ├───────────┼─────────┼─────────┼─────────┼─────────┼──────────┼───────────┼─────────┤
    │ Bytes/Sec │ 6.96 MB │ 6.96 MB │ 29.5 MB │ 42.6 MB │ 28 MB    │ 8.25 MB   │ 6.95 MB │
    └───────────┴─────────┴─────────┴─────────┴─────────┴──────────┴───────────┴─────────┘
    
    Req/Bytes counts sampled once per second.
    # of samples: 10
    
    403k requests in 12.45s, 280 MB read
    3k errors (0 timeouts)
</details>
<details>
    <summary> Time verbose results wrapped around localhost running vanilla Node.js server /api/devices </summary>

    $ /usr/bin/time -l pnpm run bench:vanilla
    >            18.88  real
    >             9.63  user
    >             2.64  sys
    >        228696064  maximum resident set size
    >                0  average shared memory size
    >                0  average unshared data size
    >                0  average unshared stack size
    >            92464  page reclaims
    >               38  page faults
    >                0  swaps
    >                0  block input operations
    >                0  block output operations
    >           399198  messages sent
    >           399198  messages received
    >               11  signals received
    >              301  voluntary context switches
    >            38188  involuntary context switches
    >       5424555803  instructions retired
    >       2089790749  cycles elapsed
    >         92702144  peak memory footprint
</details>

### Python uvicorn with compiled endpoints

<details>
  <summary> Autocannon results on localhost running Spartan /api/devices </summary>

    Running 10s test @ http://localhost:8080/api/devices
    10000 connections
    
    ┌─────────┬────────┬────────┬─────────┬─────────┬───────────┬───────────┬─────────┐
    │ Stat    │ 2.5%   │ 50%    │ 97.5%   │ 99%     │ Avg       │ Stdev     │ Max     │
    ├─────────┼────────┼────────┼─────────┼─────────┼───────────┼───────────┼─────────┤
    │ Latency │ 210 ms │ 284 ms │ 1531 ms │ 1692 ms │ 333.63 ms │ 338.58 ms │ 4273 ms │
    └─────────┴────────┴────────┴─────────┴─────────┴───────────┴───────────┴─────────┘
    ┌───────────┬─────┬──────┬─────────┬─────────┬─────────┬───────────┬─────────┐
    │ Stat      │ 1%  │ 2.5% │ 50%     │ 97.5%   │ Avg     │ Stdev     │ Min     │
    ├───────────┼─────┼──────┼─────────┼─────────┼─────────┼───────────┼─────────┤
    │ Req/Sec   │ 0   │ 0    │ 49,151  │ 49,151  │ 42,250  │ 16,026.63 │ 45,149  │
    ├───────────┼─────┼──────┼─────────┼─────────┼─────────┼───────────┼─────────┤
    │ Bytes/Sec │ 0 B │ 0 B  │ 35.5 MB │ 35.5 MB │ 30.5 MB │ 11.6 MB   │ 32.6 MB │
    └───────────┴─────┴──────┴─────────┴─────────┴─────────┴───────────┴─────────┘
    
    Req/Bytes counts sampled once per second.
    # of samples: 8
    
    348k requests in 12.32s, 244 MB read
</details>
<details>
    <summary> Time verbose results wrapped around localhost running Spartan </summary>

    $ /usr/bin/time -l bench-uvicorn
    >            25.31  real
    >            60.10  user
    >            10.97  sys
    >         31211520  maximum resident set size
    >                0  average shared memory size
    >                0  average unshared data size
    >                0  average unshared stack size
    >           227226  page reclaims
    >             5088  page faults
    >                0  swaps
    >                0  block input operations
    >                0  block output operations
    >          1050129  messages sent
    >           359899  messages received
    >              132  signals received
    >             3008  voluntary context switches
    >           817230  involuntary context switches
    >       1241151165  instructions retired
    >        829603015  cycles elapsed
    >         20989312  peak memory footprin
</details>

## Contribution

Here is a guideline on running the tests yourself.

### Prerequisites

  * [git](https://git-scm.com/) - --fast-version-control
  * [nodejs](https://nodejs.org) (20.18.1+) - Run JavaScript Everywhere
    - [pnpm](https://pnpm.io) - Fast, disk space efficient package manager
  * [python](https://www.python.org) (3.9+) - lets you work quickly and integrate systems more effectively
    * ~~[pip](https://pypi.org/project/pip)~~ - PyPA recommended tool for installing Python packages
    - [uv](https://docs.astral.sh/uv) - extremely fast Python package and project manager, written in Rust
  * [docker](https://www.docker.com) - Accelerated container application development

The following guide walks through setting up your local working environment using `git`
as distributed version control system and `uv` as Python package and version manager.
If you do not have `git` installed, run the following command.

<details>
  <summary> Install git using Homebrew (Darwin) </summary>
  
  ```sh
  brew install git
  ```
</details>

<details>
  <summary> Install git via binary installer (Linux) </summary>
  
  * Debian-based package management
  ```sh
  sudo apt install git-all
  ```

  * Fedora-based package management
  ```sh
  sudo dnf install git-all
  ```
</details>

TODO: `nodejs` and `pnpm` setup

If you do not have `uv` installed, run the following command.

<details>
  <summary> Install uv using Homebrew (Darwin) </summary>

  ```sh
  brew install uv
  ```
</details>

<details>
  <summary> Install uv using standalone installer (Darwin and Linux) </summary>

  ```sh
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
</details>

Once you have `git` distributed version control system installed, you can
clone the current repository and  install any version of Python above version
3.12 for this project. The following commands help you set up and activate a
Python virtual environment where `uv` can download project dependencies from the `PyPI`
open-sourced registry defined under `pyproject.toml` file.

<details>
  <summary> Set up environment and synchronize project dependencies </summary>

  ```sh
  git clone git@github.com:aekasitt/bench.git
  cd bench
  uv venv --python 3.12
  source .venv/bin/activate
  uv sync --dev
  ```
</details>

## Acknowledgements

1. [Lesson 236](https://github.com/antonputra/tutorials/tree/main/lessons/236) by [@antonputra](https://github.com/antonputra)
2. [YT: FastAPI (Python) vs Node.js Performance](https://youtu.be/i3TcSeRO8gs)

## License

This project is licensed under the terms of the MIT license.
