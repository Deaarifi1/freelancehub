import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/api';

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    API.get('/projects/')
      .then(res => setProjects(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  const filtered = projects.filter(p =>
    p.title.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div style={styles.container}>
      <div style={styles.navbar}>
        <h2 style={styles.logo}>FreelanceHub</h2>
        <button style={styles.backBtn} onClick={() => navigate('/dashboard')}>
          ← Dashboard
        </button>
      </div>

      <div style={styles.content}>
        <div style={styles.header}>
          <h3 style={styles.title}>Projektet</h3>
          <input
            style={styles.search}
            placeholder="Kërko projekte..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>

        {loading ? (
          <p>Duke u ngarkuar...</p>
        ) : filtered.length === 0 ? (
          <p style={styles.empty}>Nuk u gjetën projekte.</p>
        ) : (
          <div style={styles.grid}>
            {filtered.map(project => (
              <div key={project.id} style={styles.card}>
                <div style={styles.cardHeader}>
                  <h4 style={styles.cardTitle}>{project.title}</h4>
                  <span style={{
                    ...styles.badge,
                    background: project.status === 'open' ? '#E1F5EE' : '#FAEEDA',
                    color: project.status === 'open' ? '#0F6E56' : '#854F0B'
                  }}>
                    {project.status}
                  </span>
                </div>
                <p style={styles.desc}>{project.description}</p>
                <div style={styles.cardFooter}>
                  <span style={styles.budget}>
                    ${project.budget_min} - ${project.budget_max}
                  </span>
                  <span style={styles.type}>{project.project_type}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: { 
    minHeight: '100vh', 
    background: '#f5f5f5' },
  navbar: {
    background: 'white', 
    padding: '16px 24px',
    display: 'flex', 
    justifyContent: 'space-between',
    alignItems: 'center', 
    boxShadow: '0 1px 4px rgba(0,0,0,0.1)'
  },
  logo: { 
    color: '#1D9E75', 
    margin: 0 },
  backBtn: {
    padding: '8px 16px', 
    background: 'transparent',
    border: '1px solid #ddd', 
    borderRadius: '8px', 
    cursor: 'pointer'
  },
  content: { 
    padding: '24px' },
  header: {
    display: 'flex', 
    justifyContent: 'space-between',
    alignItems: 'center', 
    marginBottom: '20px'
  },
  title: { 
    margin: 0, 
    color: '#333' },
  search: {
    padding: '10px 16px', 
    border: '1px solid #ddd',
    borderRadius: '8px', 
    fontSize: '14px', 
    width: '250px'
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
    gap: '16px'
  },
  card: {
    background: 'white', 
    padding: '20px',
    borderRadius: '12px', 
    boxShadow: '0 1px 4px rgba(0,0,0,0.1)'
  },
  cardHeader: {
    display: 'flex', 
    justifyContent: 'space-between',
    alignItems: 'flex-start', 
    marginBottom: '10px'
  },
  cardTitle: { 
    margin: 0, 
    fontSize: '15px', 
    color: '#333', 
    flex: 1 },
  badge: {
    fontSize: '11px', 
    padding: '3px 8px',
    borderRadius: '20px', 
    marginLeft: '8px', 
    whiteSpace: 'nowrap'
  },
  desc: { fontSize: '13px', color: '#666', marginBottom: '12px', lineHeight: '1.5' },
  cardFooter: { display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
  budget: { fontSize: '14px', fontWeight: '500', color: '#1D9E75' },
  type: { fontSize: '12px', color: '#999' },
  empty: { textAlign: 'center', color: '#666', marginTop: '40px' }
};