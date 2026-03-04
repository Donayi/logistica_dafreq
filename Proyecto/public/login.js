document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value;
  const msg = document.getElementById('message');
  msg.textContent = '';
  try {
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    if (res.ok && data.status === 'ok') {
      msg.className = 'mt-4 text-center text-sm text-green-600';
      msg.textContent = `OK — Bienvenido ${data.profile.name || data.profile.username}`;
      localStorage.setItem('profile', JSON.stringify(data.profile));
    } else {
      msg.className = 'mt-4 text-center text-sm text-red-600';
      msg.textContent = data.message || 'Error de autenticación';
    }
  } catch (err) {
    msg.className = 'mt-4 text-center text-sm text-red-600';
    msg.textContent = 'Error de conexión';
  }
});
