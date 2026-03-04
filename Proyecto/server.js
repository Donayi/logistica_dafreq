require('dotenv').config();
const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');
const bcrypt = require('bcrypt');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

app.post('/api/login', async (req, res) => {
  const { username, password } = req.body || {};
  if (!username || !password) return res.status(400).json({ status: 'error', message: 'Faltan credenciales' });
  try {
    const result = await pool.query('SELECT id, username, password, name, email, role FROM users WHERE username=$1', [username]);
    if (result.rows.length === 0) return res.status(401).json({ status: 'error', message: 'Credenciales inválidas' });
    const user = result.rows[0];
    const match = await bcrypt.compare(password, user.password);
    if (!match) return res.status(401).json({ status: 'error', message: 'Credenciales inválidas' });
    const profile = { id: user.id, username: user.username, name: user.name, email: user.email, role: user.role };
    res.json({ status: 'ok', profile });
  } catch (err) {
    console.error(err);
    res.status(500).json({ status: 'error', message: 'Error del servidor' });
  }
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Server listening on ${port}`));
