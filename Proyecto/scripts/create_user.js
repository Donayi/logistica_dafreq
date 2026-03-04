require('dotenv').config();
const { Pool } = require('pg');
const bcrypt = require('bcrypt');

async function createUser() {
  const pool = new Pool({ connectionString: process.env.DATABASE_URL });
  const username = process.env.SAMPLE_USER || 'admin';
  const password = process.env.SAMPLE_PASS || 'secret123';
  const name = process.env.SAMPLE_NAME || 'Admin Logistica';
  const email = process.env.SAMPLE_EMAIL || 'admin@example.com';
  const role = process.env.SAMPLE_ROLE || 'admin';
  try {
    const hashed = await bcrypt.hash(password, 10);
    const res = await pool.query(
      'INSERT INTO users (username, password, name, email, role) VALUES ($1,$2,$3,$4,$5) ON CONFLICT (username) DO NOTHING RETURNING id',
      [username, hashed, name, email, role]
    );
    if (res.rowCount === 0) console.log('Usuario ya existe o no se insertó.');
    else console.log('Usuario creado, id=', res.rows[0].id);
  } catch (err) {
    console.error('Error creando usuario:', err.message || err);
  } finally {
    await pool.end();
  }
}

createUser();
