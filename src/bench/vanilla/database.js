/* ~~/src/bench/vanilla/postgres.js */

// imports
import postgres from 'postgres'

// creates a connection pool to connect to postgres.
const sql = postgres({
  host: 'localhost',
  database: 'benchdb',
  username: 'bench',
  password: 'benchpwd',
  max: 20,
})

export default sql
