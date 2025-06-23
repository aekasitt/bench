/* ~~/src/bench_fastify/cache.js */

// imports
import Memcached from 'memcached'

Memcached.config.poolSize = 500

const memcached = new Memcached('localhost:11211')

export default memcached
