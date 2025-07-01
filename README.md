# Bench: performance is a feature

## FastAPI (python) vs Fastify (node) vs Litestar (python) vs Vanilla (node)

This repository uses [autocannon](https://npmjs.com/package/autocannon) for basic and
non-reproduceable-on-production test for a web server implemented by [FastAPI](https://fastapi.tiangolo.com),
[Fastify](https://fastify.dev), [Litestar](https://litestar.dev) and simple vanilla implementation
of a web server on [Node.js](https://nodejs.org)

## Why work on something if it does not reproduce on production?

Trends matter and [Python](https://www.python.org)'s JIT compilation and Global Interpreter Lock
experimentations may bare different fruits in the not so distant future. Having something easily
upgradeable on the local environment may prove useful for quick and dirty tests to see improvements
made in the short to intermediate term.

Plus, it's fun.

## Results

<details>
    <summary> Autocannon results on localhost running FastAPI /api/devices </summary>

    Running 10s test @ http://localhost:8080/api/devices
    10 connections
    
    ┌─────────┬──────┬──────┬───────┬──────┬─────────┬─────────┬───────┐
    │ Stat    │ 2.5% │ 50%  │ 97.5% │ 99%  │ Avg     │ Stdev   │ Max   │
    ├─────────┼──────┼──────┼───────┼──────┼─────────┼─────────┼───────┤
    │ Latency │ 1 ms │ 2 ms │ 3 ms  │ 3 ms │ 1.83 ms │ 0.58 ms │ 22 ms │
    └─────────┴──────┴──────┴───────┴──────┴─────────┴─────────┴───────┘
    ┌───────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
    │ Stat      │ 1%      │ 2.5%    │ 50%     │ 97.5%   │ Avg     │ Stdev   │ Min     │
    ├───────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
    │ Req/Sec   │ 4,327   │ 4,327   │ 4,399   │ 4,479   │ 4,404   │ 38.26   │ 4,327   │
    ├───────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
    │ Bytes/Sec │ 2.89 MB │ 2.89 MB │ 2.93 MB │ 2.99 MB │ 2.94 MB │ 25.3 kB │ 2.89 MB │
    └───────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘
    
    Req/Bytes counts sampled once per second.
    # of samples: 10
    
    44k requests in 10.04s, 29.4 MB read
</details>

<details>
    <summary> Autocannon results on localhost running Litestar /api/devices </summary>

    Running 10s test @ http://localhost:8080/api/devices
    10 connections
    
    ┌─────────┬──────┬──────┬───────┬──────┬─────────┬─────────┬───────┐
    │ Stat    │ 2.5% │ 50%  │ 97.5% │ 99%  │ Avg     │ Stdev   │ Max   │
    ├─────────┼──────┼──────┼───────┼──────┼─────────┼─────────┼───────┤
    │ Latency │ 1 ms │ 1 ms │ 1 ms  │ 2 ms │ 1.03 ms │ 0.41 ms │ 23 ms │
    └─────────┴──────┴──────┴───────┴──────┴─────────┴─────────┴───────┘
    ┌───────────┬─────────┬─────────┬─────────┬─────────┬─────────┬────────┬─────────┐
    │ Stat      │ 1%      │ 2.5%    │ 50%     │ 97.5%   │ Avg     │ Stdev  │ Min     │
    ├───────────┼─────────┼─────────┼─────────┼─────────┼─────────┼────────┼─────────┤
    │ Req/Sec   │ 7,039   │ 7,039   │ 7,983   │ 8,043   │ 7,756.8 │ 356.17 │ 7,036   │
    ├───────────┼─────────┼─────────┼─────────┼─────────┼─────────┼────────┼─────────┤
    │ Bytes/Sec │ 4.69 MB │ 4.69 MB │ 5.32 MB │ 5.37 MB │ 5.17 MB │ 237 kB │ 4.69 MB │
    └───────────┴─────────┴─────────┴─────────┴─────────┴─────────┴────────┴─────────┘

    Req/Bytes counts sampled once per second.
    # of samples: 10
    
    78k requests in 10.05s, 51.7 MB read
</details>

<details>
    <summary> Autocannon results on localhost running Fastify /api/devices </summary>

    Running 10s test @ http://localhost:8080/api/devices
    10 connections
    
    ┌─────────┬──────┬──────┬───────┬──────┬─────────┬─────────┬───────┐
    │ Stat    │ 2.5% │ 50%  │ 97.5% │ 99%  │ Avg     │ Stdev   │ Max   │
    ├─────────┼──────┼──────┼───────┼──────┼─────────┼─────────┼───────┤
    │ Latency │ 0 ms │ 0 ms │ 0 ms  │ 0 ms │ 0.01 ms │ 0.16 ms │ 22 ms │
    └─────────┴──────┴──────┴───────┴──────┴─────────┴─────────┴───────┘
    ┌───────────┬─────────┬─────────┬─────────┬─────────┬──────────┬──────────┬─────────┐
    │ Stat      │ 1%      │ 2.5%    │ 50%     │ 97.5%   │ Avg      │ Stdev    │ Min     │
    ├───────────┼─────────┼─────────┼─────────┼─────────┼──────────┼──────────┼─────────┤
    │ Req/Sec   │ 41,567  │ 41,567  │ 49,407  │ 50,399  │ 48,371.2 │ 2,548.96 │ 41,548  │
    ├───────────┼─────────┼─────────┼─────────┼─────────┼──────────┼──────────┼─────────┤
    │ Bytes/Sec │ 28.3 MB │ 28.3 MB │ 33.7 MB │ 34.4 MB │ 33 MB    │ 1.74 MB  │ 28.3 MB │
    └───────────┴─────────┴─────────┴─────────┴─────────┴──────────┴──────────┴─────────┘
    
    Req/Bytes counts sampled once per second.
    # of samples: 10
    
    484k requests in 10.04s, 330 MB read
</details>

<details>
    <summary> Autocannon results on localhost running vanilla Node.js server /api/devices </summary>
  
    Running 10s test @ http://localhost:8080/api/devices
    10 connections
    
    ┌─────────┬──────┬──────┬───────┬──────┬─────────┬────────┬───────┐
    │ Stat    │ 2.5% │ 50%  │ 97.5% │ 99%  │ Avg     │ Stdev  │ Max   │
    ├─────────┼──────┼──────┼───────┼──────┼─────────┼────────┼───────┤
    │ Latency │ 0 ms │ 0 ms │ 0 ms  │ 0 ms │ 0.01 ms │ 0.2 ms │ 27 ms │
    └─────────┴──────┴──────┴───────┴──────┴─────────┴────────┴───────┘
    ┌───────────┬─────────┬─────────┬─────────┬────────┬───────────┬──────────┬─────────┐
    │ Stat      │ 1%      │ 2.5%    │ 50%     │ 97.5%  │ Avg       │ Stdev    │ Min     │
    ├───────────┼─────────┼─────────┼─────────┼────────┼───────────┼──────────┼─────────┤
    │ Req/Sec   │ 31,439  │ 31,439  │ 39,231  │ 40,383 │ 38,584.81 │ 2,581.75 │ 31,425  │
    ├───────────┼─────────┼─────────┼─────────┼────────┼───────────┼──────────┼─────────┤
    │ Bytes/Sec │ 22.5 MB │ 22.5 MB │ 28.1 MB │ 29 MB  │ 27.7 MB   │ 1.85 MB  │ 22.5 MB │
    └───────────┴─────────┴─────────┴─────────┴────────┴───────────┴──────────┴─────────┘
    
    Req/Bytes counts sampled once per second.
    # of samples: 10
    
    386k requests in 10.04s, 277 MB read
</details>

<details>
  <summary> Autocannon results on localhost running uvicorn with mypycified /api/devices </summary>

    Running 10s test @ http://localhost:8080/api/devices
    10000 connections
    
    running [====================] 100%
    ┌─────────┬────────┬────────┬─────────┬─────────┬───────────┬───────────┬─────────┐
    │ Stat    │ 2.5%   │ 50%    │ 97.5%   │ 99%     │ Avg       │ Stdev     │ Max     │
    ├─────────┼────────┼────────┼─────────┼─────────┼───────────┼───────────┼─────────┤
    │ Latency │ 160 ms │ 282 ms │ 1116 ms │ 1596 ms │ 385.94 ms │ 519.27 ms │ 9008 ms │
    └─────────┴────────┴────────┴─────────┴─────────┴───────────┴───────────┴─────────┘
    ┌───────────┬─────────┬─────────┬─────────┬─────────┬─────────┬────────┬─────────┐
    │ Stat      │ 1%      │ 2.5%    │ 50%     │ 97.5%   │ Avg     │ Stdev  │ Min     │
    ├───────────┼─────────┼─────────┼─────────┼─────────┼─────────┼────────┼─────────┤
    │ Req/Sec   │ 46,207  │ 46,207  │ 46,367  │ 47,039  │ 46,512  │ 328.22 │ 46,190  │
    ├───────────┼─────────┼─────────┼─────────┼─────────┼─────────┼────────┼─────────┤
    │ Bytes/Sec │ 33.3 MB │ 33.3 MB │ 33.4 MB │ 33.9 MB │ 33.5 MB │ 238 kB │ 33.3 MB │
    └───────────┴─────────┴─────────┴─────────┴─────────┴─────────┴────────┴─────────┘
</details>
<details>
  <summary> Time verbose results wrapped around localhost running uvicorn </summary>

  ```sh
  $ /usr/bin/time -l bench-uvicorn
  >            17.80  real
  >            45.06  user
  >             8.90  sys
  >         32030720  maximum resident set size
  >                0  average shared memory size
  >                0  average unshared data size
  >                0  average unshared stack size
  >           225990  page reclaims
  >             5070  page faults
  >                0  swaps
  >                0  block input operations
  >                0  block output operations
  >           724741  messages sent
  >           248407  messages received
  >              132  signals received
  >             2170  voluntary context switches
  >           625147  involuntary context switches
  >       1150187160  instructions retired
  >        752487685  cycles elapsed
  >         20497664  peak memory footprint
  ```
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
