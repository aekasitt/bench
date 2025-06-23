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

Not looking good for FastAPI and Python so far, but wait there's more...

## Acknowledgements

1. [Lesson 236](https://github.com/antonputra/tutorials/tree/main/lessons/236) by [@antonputra](https://github.com/antonputra)
2. [YT: FastAPI (Python) vs Node.js Performance](https://youtu.be/i3TcSeRO8gs)

## License

This project is licensed under the terms of the MIT license.
