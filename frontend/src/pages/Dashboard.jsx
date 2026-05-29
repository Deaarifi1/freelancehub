import { useAuth } from '../context/useAuth';
import { useNavigate } from 'react-router-dom';

export default function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div style={styles.container}>
      <div style={styles.navbar}>
        <h2 style={styles.logo}>FreelanceHub</h2>
        <div style={styles.navRight}>
          <button style={styles.navBtn} onClick={() => navigate('/')}>Kryefaqja</button>
          <button style={styles.navBtn} onClick={() => navigate('/projects')}>Projektet</button>
          <span style={styles.welcome}>welcome, {user?.username}!</span>
          <button style={styles.logoutBtn} onClick={handleLogout}>Log out</button>
        </div>
      </div>

      <div style={styles.content}>
        <div style={styles.statsGrid}>
          <div style={styles.statCard}>
            <p style={styles.statLabel}>Role</p>
            <p style={styles.statValue}>{user?.role}</p>
          </div>
          <div style={styles.statCard}>
            <p style={styles.statLabel}>Email</p>
            <p style={styles.statValue}>{user?.email}</p>
          </div>
          <div style={styles.statCard}>
            <p style={styles.statLabel}>Status</p>
            <p style={styles.statValue}>{user?.is_active ? 'Aktiv' : 'Inaktiv'}</p>
          </div>
        </div>

        <div style={styles.actions}>
          <button
            style={styles.actionBtn}
            onClick={() => navigate('/projects')}
          >
            View Projects
          </button>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: { minHeight: '100vh', background: '#f5f5f5' },
  navbar: {
    background: 'white',
    padding: '16px 24px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    boxShadow: '0 1px 4px rgba(0,0,0,0.1)'
  },
  logo: { color: '#1D9E75', margin: 0 },
  navRight: { display: 'flex', alignItems: 'center', gap: '16px' },
  navBtn: {
    padding: '8px 16px', background: 'transparent',
    border: '1px solid #ddd', borderRadius: '8px',
    cursor: 'pointer', fontSize: '14px'
  },
  welcome: { fontSize: '14px', color: '#666' },
  logoutBtn: {
    padding: '8px 16px', background: '#ff4444',
    color: 'white', border: 'none',
    borderRadius: '8px', cursor: 'pointer'
  },
  content: { padding: '24px' },
  statsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '16px', marginBottom: '24px'
  },
  statCard: {
    background: 'white', padding: '20px',
    borderRadius: '12px',
    boxShadow: '0 1px 4px rgba(0,0,0,0.1)'
  },
  statLabel: { color: '#666', fontSize: '13px', margin: '0 0 8px' },
  statValue: { color: '#333', fontSize: '16px', fontWeight: '500', margin: 0 },
  actions: { display: 'flex', gap: '12px' },
  actionBtn: {
    padding: '12px 24px', background: '#1D9E75',
    color: 'white', border: 'none',
    borderRadius: '8px', cursor: 'pointer', fontSize: '14px'
  }
};