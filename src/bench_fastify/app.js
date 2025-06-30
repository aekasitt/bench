/* ~~/src/bench_fastify/app.js */

// imports
import cluster from 'node:cluster'
import histogram from './metrics.js'
import save from './devices.js'
import { randomUUID } from 'node:crypto'
import { register } from 'prom-client'
import memcached from './cache.js'
import Fastify from 'fastify'
import { serverFactory } from '@geut/fastify-uws'

const server = Fastify({
  keepAliveTimeout: 60000,
  serverFactory,
})

// metrics route
server.get('/metrics', async (_, reply) => {
  reply.header('Content-Type', register.contentType).send(await register.metrics())
})

// health check route
server.get('/healthz', async (_, reply) => {
  reply.type('text/plain').send('OK')
})

// GET /api/devices
server.get('/api/devices', async (_, reply) => {
  const devices = [
    {
      id: 1,
      uuid: '9add349c-c35c-4d32-ab0f-53da1ba40a2a',
      mac: 'EF-2B-C4-F5-D6-34',
      firmware: '2.1.5',
      created_at: '2024-05-28T15:21:51.137Z',
      updated_at: '2024-05-28T15:21:51.137Z',
    },
    {
      id: 2,
      uuid: 'd2293412-36eb-46e7-9231-af7e9249fffe',
      mac: 'E7-34-96-33-0C-4C',
      firmware: '1.0.3',
      created_at: '2024-01-28T15:20:51.137Z',
      updated_at: '2024-01-28T15:20:51.137Z',
    },
    {
      id: 3,
      uuid: 'eee58ca8-ca51-47a5-ab48-163fd0e44b77',
      mac: '68-93-9B-B5-33-B9',
      firmware: '4.3.1',
      created_at: '2024-08-28T15:18:21.137Z',
      updated_at: '2024-08-28T15:18:21.137Z',
    },
  ]

  reply.send(devices)
})

// POST /api/devices
server.post('/api/devices', async (request, reply) => {
  const device = request.body
  const datetime = new Date()

  device.uuid = randomUUID()
  device.createdAt = datetime
  device.updatedAt = datetime

  const dbTimer = histogram.startTimer()
  try {
    const result = await save(device)
    dbTimer({ op: 'insert' })
    device.id = result[0].id

    const cacheTimer = histogram.startTimer()
    memcached.set(device.uuid, device, 20, error => {
      if (error) {
        server.log.error(error)
        reply.status(400).send({ message: error.message })
        return
      }

      cacheTimer({ op: 'set' })
      reply.status(201).send(device)
    })
  } catch (error) {
    server.log.error(error)
    reply.status(400).send({ message: error.message })
  }
})

server.setNotFoundHandler((_, reply) => {
  reply.status(404).type('text/plain').send('Not Found')
})

const NUM_WORKERS = 8
if (cluster.isPrimary) {
  console.log(`Node is listening on http://0.0.0.0:8080 ...`)
  for (let i = 0; i < NUM_WORKERS; i++) {
    cluster.fork();
  }

  cluster.on(
    "exit",
    (worker, code, signal) => console.log(`worker ${worker.process.pid} died`),
  );
} else {
  server.listen({
    host: '0.0.0.0',
    port: 8080,
  })
}
