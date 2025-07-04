/* ~~/src/bench/fastify/cache.js */

// imports
import Memcached from 'memcached'

Memcached.config.poolSize = 500

const memcached = new Memcached('0.0.0.0:11211')

export default memcached
