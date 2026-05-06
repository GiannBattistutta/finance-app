const API = '';
let token = localStorage.getItem('token');
let currentTab = 'login';

// --- INIT ---
window.onload = () => {
  if (token) showDashboard();
};

// --- AUTH ---
function switchTab(tab) {
  currentTab = tab;
  document.querySelectorAll('.tab').forEach((t, i) => {
    t.classList.toggle('active', (i === 0 && tab === 'login') || (i === 1 && tab === 'register'));
  });
  hideError('auth-error');
}

async function handleAuth() {
  const email = document.getElementById('auth-email').value.trim();
  const password = document.getElementById('auth-password').value;

  if (!email || !password) return showError('auth-error', 'Please fill in all fields.');

  if (currentTab === 'register') {
    const res = await fetch(`${API}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    if (!res.ok) {
      const data = await res.json();
      return showError('auth-error', data.detail || 'Registration failed.');
    }
  }

  // Login
  const form = new FormData();
  form.append('username', email);
  form.append('password', password);

  const res = await fetch(`${API}/auth/login`, { method: 'POST', body: form });
  const data = await res.json();

  if (!res.ok) return showError('auth-error', data.detail || 'Login failed.');

  token = data.access_token;
  localStorage.setItem('token', token);
  document.getElementById('nav-email').textContent = email;
  showDashboard();
}

function logout() {
  token = null;
  localStorage.removeItem('token');
  document.getElementById('dashboard-screen').classList.add('hidden');
  document.getElementById('auth-screen').classList.remove('hidden');
  document.getElementById('auth-email').value = '';
  document.getElementById('auth-password').value = '';
}

// --- DASHBOARD ---
async function showDashboard() {
  document.getElementById('auth-screen').classList.add('hidden');
  document.getElementById('dashboard-screen').classList.remove('hidden');
  await Promise.all([loadSummary(), loadTransactions()]);
}

async function loadSummary() {
  const res = await authFetch('/transactions/summary');
  if (!res.ok) return;
  const data = await res.json();
  document.getElementById('total-income').textContent = formatMoney(data.total_income);
  document.getElementById('total-expense').textContent = formatMoney(data.total_expense);
  document.getElementById('total-balance').textContent = formatMoney(data.balance);
}

async function loadTransactions() {
  const res = await authFetch('/transactions/');
  if (!res.ok) return;
  const data = await res.json();
  const list = document.getElementById('transactions-list');

  if (data.length === 0) {
    list.innerHTML = '<div class="empty-state">No transactions yet.</div>';
    return;
  }

  list.innerHTML = data.reverse().map(t => `
    <div class="transaction-item" id="t-${t.id}">
      <div class="t-left">
        <div class="t-title">${t.title}</div>
        <div class="t-meta">${t.category} · ${formatDate(t.date)}</div>
      </div>
      <div class="t-right">
        <div class="t-amount ${t.type}">${t.type === 'income' ? '+' : '-'}${formatMoney(t.amount)}</div>
        <button class="btn-delete" onclick="deleteTransaction(${t.id})">🗑</button>
      </div>
    </div>
  `).join('');
}

async function addTransaction() {
  const title = document.getElementById('t-title').value.trim();
  const amount = parseFloat(document.getElementById('t-amount').value);
  const type = document.getElementById('t-type').value;
  const category = document.getElementById('t-category').value.trim() || 'general';

  if (!title || !amount || amount <= 0) return showError('form-error', 'Please fill in title and a valid amount.');

  const res = await authFetch('/transactions/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, amount, type, category })
  });

  if (!res.ok) {
    const data = await res.json();
    return showError('form-error', data.detail || 'Failed to add transaction.');
  }

  hideError('form-error');
  document.getElementById('t-title').value = '';
  document.getElementById('t-amount').value = '';
  document.getElementById('t-category').value = '';
  await Promise.all([loadSummary(), loadTransactions()]);
}

async function deleteTransaction(id) {
  const res = await authFetch(`/transactions/${id}`, { method: 'DELETE' });
  if (res.ok) await Promise.all([loadSummary(), loadTransactions()]);
}

// --- HELPERS ---
function authFetch(url, options = {}) {
  return fetch(`${API}${url}`, {
    ...options,
    headers: { ...options.headers, 'Authorization': `Bearer ${token}` }
  });
}

function formatMoney(value) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function showError(id, msg) {
  const el = document.getElementById(id);
  el.textContent = msg;
  el.classList.remove('hidden');
}

function hideError(id) {
  document.getElementById(id).classList.add('hidden');
}