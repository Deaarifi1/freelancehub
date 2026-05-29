import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/api';

export default function Home() {
  const [projects, setProjects] = useState([]);
  const [search, setSearch] = useState('');
  const [aiResult, setAiResult] = useState(null);
  const [aiLoading, setAiLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    API.get('/projects/').then(res => setProjects(res.data)).catch(() => {});
  }, []);

  const handleAiSearch = async () => {
    if (!search.trim()) return;
    setAiLoading(true);
    try {
      const token = localStorage.getItem('token');
      const res = await API.post('/ai/analyze',
        { description: search },
        { headers: { Authorization: `Bearer ${token}` }}
    );
      setAiResult(res.data);
    } catch (err) {
        if (err.response?.status === 401) {
            alert('You must be logged in for AI search!');
            navigate('/login');
        } else {
            console.error(err);
            alert('error in server!');
        }
    } finally {
      setAiLoading(false);
    }
  };

  return (
    <div style={{ fontFamily: 'sans-serif', minHeight: '100vh', background: '#fff' }}>

      {/* Navbar */}
      <nav style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '14px 32px', borderBottom: '1px solid #eee' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '32px' }}>
          <div style={{ fontWeight: '700', fontSize: '18px', color: '#222', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#1D9E75', display: 'inline-block' }}></span>
            FreelanceHub
          </div>
          <span style={{ fontSize: '14px', color: '#555', cursor: 'pointer' }} onClick={() => navigate('/projects')}>Projects</span>
          <span style={{ fontSize: '14px', color: '#555', cursor: 'pointer' }} onClick={() => navigate('/freelancers')}>Freelancers</span>
          <span style={{ fontSize: '14px', color: '#555', cursor: 'pointer' }} onClick={() => navigate('/agencies')}>Agencies</span>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button onClick={() => navigate('/login')} style={{ padding: '8px 18px', border: '1px solid #ccc', borderRadius: '8px', background: 'white', cursor: 'pointer', fontSize: '14px' }}>Log in</button>
          <button onClick={() => navigate('/register')} style={{ padding: '8px 18px', border: 'none', borderRadius: '8px', background: '#1D9E75', color: 'white', cursor: 'pointer', fontSize: '14px' }}>Register</button>
        </div>
      </nav>

      <div style={{ padding: '24px 32px' }}>

        {/* Hero */}
        <div style={{ background: '#f9f9f7', borderRadius: '12px', padding: '32px', marginBottom: '24px', border: '1px solid #eee' }}>
          <h1 style={{ fontSize: '26px', fontWeight: '700', marginBottom: '8px', color: '#222' }}>Find the right freelancer with AI</h1>
          <p style={{ fontSize: '14px', color: '#666', marginBottom: '16px' }}>Publish your project and let artificial intelligence automatically find the best freelancers for you.</p>
          <div style={{ display: 'flex', gap: '8px' }}>
            <input
              style={{ flex: 1, padding: '11px 14px', border: '1px solid #ddd', borderRadius: '8px', fontSize: '14px' }}
              placeholder="E.g. I need a React developer for e-commerce..."
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
            <button
              onClick={handleAiSearch}
              style={{ padding: '11px 20px', background: '#1D9E75', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '14px' }}
            >
              {aiLoading ? 'Analyzing...' : 'Search with AI'}
            </button>
          </div>

          {/* AI Result */}
          {aiResult && (
            <div style={{ marginTop: '16px', background: 'white', borderRadius: '8px', padding: '16px', border: '1px solid #ddd' }}>
              <p style={{ fontWeight: '600', marginBottom: '8px', color: '#222' }}>AI result:</p>
              <p style={{ fontSize: '13px', color: '#555' }}>
                <strong>Skills:</strong> {aiResult.skills?.join(', ')}
              </p>
              <p style={{ fontSize: '13px', color: '#555' }}>
                <strong>Budget:</strong> ${aiResult.budget_range?.min} - ${aiResult.budget_range?.max}
              </p>
              <p style={{ fontSize: '13px', color: '#555' }}>
                <strong>Complexity:</strong> {aiResult.complexity}
              </p>
              <p style={{ fontSize: '13px', color: '#555' }}>
                <strong>Duration:</strong> {aiResult.estimated_duration}
              </p>
            </div>
          )}
        </div>

        {/* Stats */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px', marginBottom: '24px' }}>
          {[
            { label: 'Active freelancers', value: '2,847', sub: '+12% this month' },
            { label: 'Active Projects', value: '423', sub: '+8% this month' },
            { label: 'Closed contracts', value: '1,204', sub: '+24% this month' },
            { label: 'Partner agency', value: '38', sub: '+3 new' },
          ].map(stat => (
            <div key={stat.label} style={{ background: '#f9f9f7', borderRadius: '10px', padding: '16px', border: '1px solid #eee' }}>
              <p style={{ fontSize: '13px', color: '#666', margin: '0 0 6px' }}>{stat.label}</p>
              <p style={{ fontSize: '24px', fontWeight: '700', color: '#222', margin: '0 0 4px' }}>{stat.value}</p>
              <p style={{ fontSize: '12px', color: '#1D9E75', margin: 0 }}>{stat.sub}</p>
            </div>
          ))}
        </div>

        {/* Projects */}
        <h2 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '14px', color: '#222' }}>Recent projects</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '14px' }}>
          {projects.length > 0 ? projects.slice(0, 4).map(p => (
            <div key={p.id} style={{ background: 'white', borderRadius: '12px', border: '1px solid #eee', padding: '18px', cursor: 'pointer' }} onClick={() => navigate('/projects')}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span style={{ fontSize: '14px', fontWeight: '600', color: '#222' }}>{p.title}</span>
                <span style={{ fontSize: '11px', padding: '3px 10px', borderRadius: '20px', background: p.status === 'open' ? '#E1F5EE' : '#FAEEDA', color: p.status === 'open' ? '#0F6E56' : '#854F0B' }}>
                  {p.status === 'open' ? 'Open' : 'In progress'}
                </span>
              </div>
              <p style={{ fontSize: '13px', color: '#666', marginBottom: '12px', lineHeight: '1.5' }}>{p.description}</p>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ fontSize: '14px', fontWeight: '600', color: '#1D9E75' }}>${p.budget_min} – ${p.budget_max}</span>
                <span style={{ fontSize: '12px', color: '#999' }}>{p.project_type}</span>
              </div>
            </div>
          )) : (
            <p style={{ color: '#666', gridColumn: 'span 2', textAlign: 'center', padding: '40px' }}>
              There are no projects yet. <span style={{ color: '#1D9E75', cursor: 'pointer' }} onClick={() => navigate('/login')}>Log in and create your first project!</span>
            </p>
          )}
        </div>
      </div>
    </div>
  );
}