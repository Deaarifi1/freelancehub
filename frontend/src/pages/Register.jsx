import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/useAuth';

export default function Register() {
  const [form, setForm] = useState({
    email: '', username: '', password: '', role: 'client'
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await register(form);
      setSuccess('Regjistrimi u krye! Po të ridrejtojmë...');
      setTimeout(() => navigate('/login'), 2000);
    } catch {
      setError('Gabim gjatë regjistrimit. Provo përsëri.');
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.logo}>FreelanceHub</h1>
        <h2 style={styles.title}>Krijo llogari</h2>
        {error && <p style={styles.error}>{error}</p>}
        {success && <p style={styles.success}>{success}</p>}
        <form onSubmit={handleSubmit}>
          <input
            style={styles.input}
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={e => setForm({...form, email: e.target.value})}
            required
          />
          <input
            style={styles.input}
            type="text"
            placeholder="Username"
            value={form.username}
            onChange={e => setForm({...form, username: e.target.value})}
            required
          />
          <input
            style={styles.input}
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={e => setForm({...form, password: e.target.value})}
            required
          />
          <select
            style={styles.input}
            value={form.role}
            onChange={e => setForm({...form, role: e.target.value})}
          >
            <option value="client">Klient</option>
            <option value="freelancer">Freelancer</option>
            <option value="agency_manager">Agency Manager</option>
          </select>
          <button style={styles.button} type="submit">
            Regjistrohu
          </button>
        </form>
        <p style={styles.link}>
          Ke llogari? <Link to="/login">Hyr</Link>
        </p>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: '#f5f5f5'
  },
  card: {
    background: 'white',
    padding: '40px',
    borderRadius: '12px',
    boxShadow: '0 2px 20px rgba(0,0,0,0.1)',
    width: '100%',
    maxWidth: '400px'
  },
  logo: { color: '#1D9E75', textAlign: 'center', marginBottom: '8px' },
  title: {
    textAlign: 'center', marginBottom: '24px',
    color: '#333', fontSize: '18px', fontWeight: '500'
  },
  input: {
    width: '100%', padding: '12px', marginBottom: '12px',
    border: '1px solid #ddd', borderRadius: '8px',
    fontSize: '14px', boxSizing: 'border-box'
  },
  button: {
    width: '100%', padding: '12px', background: '#1D9E75',
    color: 'white', border: 'none', borderRadius: '8px',
    fontSize: '15px', cursor: 'pointer', marginTop: '8px'
  },
  error: { color: 'red', textAlign: 'center', marginBottom: '12px', fontSize: '14px' },
  success: { color: 'green', textAlign: 'center', marginBottom: '12px', fontSize: '14px' },
  link: { textAlign: 'center', marginTop: '16px', fontSize: '14px', color: '#666' }
};