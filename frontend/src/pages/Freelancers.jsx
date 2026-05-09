import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/api';

export default function Freelancers() {
    const [freelancers, setFreelancers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        API.get('/search/freelancers/')
        .then(res => setFreelancers(res.data))
        .catch(err => console.error(err))
        .finally(() => setLoading(false));
    }, []);

    const filtered = freelancers.filter(f =>
    f.bio?.toLowerCase().includes(search.toLowerCase())
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
                  <h3 style={s.title}>Freelancers</h3>
                  <input
                  style={s.search}
                  placeholder="search for freelancers..."
                  value={search}
                  onChange={e => setSearch(e.target.value)}
                  />
            </div>    

            {loading ? (
                <p>Loading...</p>
            ) : filtered.length === 0 ? (
                <div style={s.empty}>
                    <p>No freelancers found.</p>
                </div>
            ) : (
            <div style={s.grid}>
                {filtered.map(f => (
                    <div key={f.id} style={s.card}>
                        <div style={s.avatar}>
                            {f.user_id?.toString().slice(0, 2).toUpperCase() || 'FL'}
                        </div>
                        <div style={s.info}>
                            <p style={s.name}>Freelancer #{f.id}</p>
                            <p style={s.bio}>{f.bio || 'No bio'}</p>
                            <div style={s.details}>
                                <span style={s.rate}>
                                    {f.hourly_rate ? `$${f.hourly_rate}/hour` : 'Unspecified rate'}
                                </span>
                                <span style={s.rating}>⭐ {f.average_rating || 0}</span>
                                <span style={{
                                    ...s.badge,
                                    background: f.is_available ? '#E1F5EE' : '#FEE',
                                    color: f.is_available ? '#0F6E56' : '#cc0000'
                                }}>
                                    {f.is_available ? 'Available' : 'Busy'}
                                </span>
                            </div>
                        </div>
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
        display: 'flex', gap: '16px', alignItems: 'flex-start'
    },
    avatar: {
        width: '48px', height: '48px', borderRadius: '50%',
        background: '#E1F5EE', color: '#0F6E56',
        display: 'flex', alignItems: 'center',
        justifyContent: 'center', fontWeight: '600',
        fontSize: '14px', flexShrink: 0
    },
    info: { flex: 1 },
    name: { margin: '0 0 4px', fontWeight: '600', fontSize: '14px', color: '#222' },
    bio: { margin: '0 0 10px', fontSize: '13px', color: '#666', lineHeight: '1.5' },
    details: { display: 'flex', gap: '8px', flexWrap: 'wrap', alignItems: 'center' },
    rate: { fontSize: '13px', fontWeight: '600', color: '#1D9E75' },
    rating: { fontSize: '12px', color: '#666' },
    badge: { fontSize: '11px', padding: '3px 8px', borderRadius: '20px' },
    empty: { textAlign: 'center', padding: '60px', color: '#666' }
};