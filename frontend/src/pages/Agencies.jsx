import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/api';

export default function Agencies() {
    const [agencies, setAgencies] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        API.get('/agencies/')
        .then(res => setAgencies(res.data))
        .catch(err => console.error(err))
        .finally(() => setLoading(false));
    }, []);

    const filtered = agencies.filter(a =>
        a.name?.toLowerCase().includes(search.toLowerCase())
    );
    
    return (
    <div style={s.page}>
        <div style={s.navbar}>
            <div style={s.logo} onClick={() => navigate('/')}>
                <span style={s.dot}></span>FreelanceHub
            </div>
            <button style={s.backBtn} onClick={() => navigate('/')}>
                ← Home
            </button>
        </div>
        
        <div style={s.content}>
            <div style={s.header}>
                <h3 style={s.title}>Agencies</h3>
                <input
                style={s.search}
                placeholder="Search for agency..."
                value={search}
                onChange={e => setSearch(e.target.value)}
                />
            </div>

            {loading ? (
                <p>Loading...</p>
            ) : filtered.length === 0 ? (
                <div style={s.empty}>
                  <p>No agencies found.</p>
                </div>
            ) : (
               <div style={s.grid}>
                {filtered.map(a => (
                  <div key={a.id} style={s.card}>
                    <div style={s.cardTop}>
                        <div style={s.avatar}>
                            {a.name?.slice(0, 2).toUpperCase()}
                        </div>
                        <div>
                            <p style={s.name}>{a.name}</p>
                            <span style={{
                                ...s.badge,
                                background: a.is_active ? '#E1F5EE' : '#FEE',
                                color: a.is_active ? '#0F6E56' : '#cc0000'
                            }}>
                                {a.is_active ? 'Active' : 'Inactive'}
                            </span>
                        </div>
                    </div>
                    <p style={s.desc}>
                        {a.description || 'No description.'}
                    </p>
                    {a.website && (
                        <a href={a.website}
                        target="_blank"
                        rel="noreferrer"
                        style={s.website}>
                    🌐 {a.website}
                    </a>
                    )}
                  </div>
                ))}
              </div>
            )}
           </div>
        </div>
    );
}

const s = {
    page: { minHeight: '100vh', background: '#f5f5f5', fontFamily: 'sans-serif' },
     navbar: {
        background: 'white', padding: '14px 24px',
        display: 'flex', justifyContent: 'space-between',
        alignItems: 'center', borderBottom: '1px solid #eee'
    },
    logo: {
        fontSize: '16px', fontWeight: '600',
        display: 'flex', alignItems: 'center',
        gap: '8px', cursor: 'pointer', color: '#222'
    },
    dot: {
        width: '8px', height: '8px',
        borderRadius: '50%', background: '#1D9E75',
        display: 'inline-block'
    },
    backBtn: {
        padding: '8px 16px', background: 'transparent',
        border: '1px solid #ddd', borderRadius: '8px', cursor: 'pointer'
    },
    content: { padding: '24px' },
    header: {
        display: 'flex', justifyContent: 'space-between',
        alignItems: 'center', marginBottom: '20px'
    },
    title: { margin: 0, color: '#333', fontSize: '18px' },
    search: {
        padding: '10px 16px', border: '1px solid #ddd',
        borderRadius: '8px', fontSize: '14px', width: '250px'
    },
    grid: { 
        display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '16px' 
    },
    card: {
        background: 'white', borderRadius: '12px',
        border: '1px solid #eee', padding: '20px',
    },
    cardTop: {
        display: 'flex', gap: '14px',
        alignItems: 'center', marginBottom: '12px' 
    },
    avatar: {
        width: '48px', height: '48px', borderRadius: '50%',
        background: '#E1F5EE', color: '#0F6E56',
        display: 'flex', alignItems: 'center',
        justifyContent: 'center', fontWeight: '600',
        fontSize: '14px', flexShrink: 0
    },
    name: { margin: '0 0 4px', fontWeight: '600', fontSize: '14px', color: '#222' },
    badge: { fontSize: '11px', padding: '3px 8px', borderRadius: '20px' },
    website: { fontSize: '12px', color: '#1D9E75', textDecoration: 'none' },
    desc: { fontSize: '13px', color: '#666', lineHeight: '1.6', margin: '0 0 10px' },
    empty: { textAlign: 'center', padding: '60px', color: '#666' }
};