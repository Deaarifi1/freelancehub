import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/api';

export default function Home() {
    const [projects, setProjects] = useState([]);
    const [search, setSearch] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        API.get('/projects/').then(res => setProjects(res.data)).catch(() => {});
    }, []);

    return (
     <div style={s.page}>
        <nav style={s.nav}>
            <div style={s.logo}><span style={s.dot}></span>FreelanceHub</div>
                <div style={s.navLinks}>
                    <span style={s.navLink} onClick={() => navigate('/projects')}>Projects</span>
                    <span style={s.navLink} onClick={() => navigate('/freelancers')}>Freelancers</span>
                    <span style={s.navLink} onClick={() => navigate('/agencies')}>Agencies</span>
                    <button style={s.btnOutline} onClick={() => navigate('/login')}>Log in</button>
                    <button style={s.btnPrimary} onClick={() => navigate('/register')}>Register</button>
                </div>
        </nav>

        <div style={s.tabs}>
            {['Home','Projects','Freelancers','AI Matching','Contracts'].map((t, i) => (
                <span key={t} style={i === 0 ? s.tabActive : s.tab}>{t}</span>
            ))}
        </div>
        
        <div style={s.conent}>
          <div style={s.hero}>
            <h1 style={s.heroTittle}>Find the right freelancer with AI</h1>
            <p style={s.heroDesc}>Publish your project and let artificial intelligence automatically find the best freelancers for you.</p>
            <div style={s.searchBar}>
                <input
                style={s.searchInput}
                placeholder="E.g. I need a React developer for e-commerce..."
                value={search}
                onChange={e => setSearch(e.target.value)}/>
                <button style={s.searchBtn}>Search with AI</button>
            </div>
        </div>

        <div style={s.statsGrid}>
            {[
                {label: 'Active Freelancers', value: '2,847', sub: '+12% this month' },
                {label: 'Active Projects', value: '423', sub: '+8% this month' },
                {label: 'Closed Contracts', value: '1,204', sub: '+24% this month' },
                {label: 'Partner Agencies', value: '38', sub: '+3 new ones' },
            ].map(stat => (
                <div key={stat.label} style={s.statCard}>
                    <p style={s.statLabel}>{stat.label}</p>
                    <p style={s.statValue}>{stat.value}</p>
                    <p style={s.statSub}>{stat.sub}</p>
                </div>
            ))}
        </div>

        <h2 style={s.sectionTitle}>Recent projects</h2>
        <div style={s.projectsGrid}>
            {projects.length > 0 ? projects.map(p => (
                <div key={p.id} style={s.projectCard}>
                    <div style={s.projectHeader}>
                        <span style={s.projectTitle}>{p.title}</span>
                        <span style={{
                            ...s.badge,
                            background: p.status === 'open' ? '#E1f5EE' : '#FAEEDA',
                            color: p.status === 'open' ? '#0F6E56' : '854F0B'
                        }}>
                            {p.status === 'open' ? 'Open' : 'In progress'}
                        </span>
                    </div>
                    <p style={s.projectDesc}>{p.description}</p>
                    <div style={s.projectFooter}>
                        <span style={s.budget}>${p.budget_min} - ${p.budget_max}</span>
                        <span style={s.meta}>${p.project_type}</span>
                    </div>
                </div>
            )) : (
                // placeholder cards
                [
                    {title: 'E-commerce Platform with React', status: 'open', desc: 'Experienced React and backend developer wanted.', min: 2000, max: 4000 },
                    {title: 'Logo and Brand Identity', status: 'open', desc: 'Startup seeks designer for logo creation.', min: 500, max: 1200 },
                    {title: 'Mobile App iOS & Android', status: 'in_progress', desc: 'Application for managing restaurant orders.', min: 5000, max: 8000 },
                    {title: 'AI Chatbot for Support', status: 'open', desc: 'Chatbot integration with OpenAI GPT-4 for 24/7 support.', min: 3000, max: 6000 },
                ].map ((p, i) => (
                    <div key={i} style={s.projectCard}>
                        <div style={s.projectHeader}>
                            <span style={s.projectTitle}>{p.title}</span>
                            <span style={{
                                ...s.badge,
                                background: p.status === 'open' ? '#E1F5EE' : '#FAEEDA',
                                color: p.status === 'open' ? '#0F6E56' : '#854F0B'
                            }}>
                                {p.status === 'open' ? 'Open' : 'In progress'}
                            </span>
                        </div>
                        <p style={s.projectDesc}>{p.desc}</p>
                        <div style={p.projectFooter}>
                            <span style={s.budget}>${p.min} - ${p.max}</span>
                        </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    </div>
    );
}

const s = {
    page: { minHeight: '100vh', background: '#fff', fontFamily: 'sans-serif' },
    nav: {
        display: 'flex', alignItems: 'center', justifycontent: 'space-between',
        padding: '14px 24px', borderBottom: '1px solid #eee'
    },
    logo: { fontSize: '16px', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '8px' },
    dot: { width: '8px', height: '8px', borderRadius: '50%', background: '#1D9E75', display: 'inline-block' },
    navLinks: { display: 'flex', alignItems: 'center', gap: '20px' },
    navLink: { fontSize: '14px', color: '#555', cursor: 'pointer' },
    btnOutline: {
        padding: '7px 16px', border: '1px solid #ccc',
        borderRadius: '8px', background: 'white',
        fontSize: '13px', cursor: 'pointer'
    },
    btnPrimary:{
        padding: '7px 16px', border: 'none',
        borderRadius: '8px', background: '#1D9E75',
        color: 'white', fontSize: '13px', cursor: 'pointer'
    },
    tabs: {
        display: 'flex', gap: '4px', padding: '0 24px',
        borderBottom: '1px solid #eee' 
    },
    tab: { padding: '12px 16px', fontSize: '14px', color: '#666', cursor: 'pointer' },
    tabActive: {
        padding: '12px 16px', fontSize: '14px',
        color: '#1D9E75', borderBottom: '2px solid #1D9E75',
        fontWeight: '500', cursor: 'pointer'
    },
    content: { padding: '24px' },
    hero: {
        background: '#f9f9f7', borderRadius: '12px',
        padding: '32px', marginBottom: '20px', border: '1px solid #eee'
    },
    heroTittle: { fontSize: '24px', fontWeight: '600', marginBottom: '8px', color: '#222' },
    heroDesc: { fontSize: '14px', color: '#666', marginBottom: '16px', lineHeight: '1.6' },
    searchBar: { display: 'flex', gap: '8px' },
    searchInput: {
        flex: 1, padding: '10px 14px', border: '1px solid #ddd',
        borderRadius: '8px', fontSize: '14px'
    },
    searchBtn: {
        padding: '10px 20px', background: '#1D9E75',
        color: 'white', border: 'none', borderRadius: '8px',
        fontSize: '13px', cursor: 'pointer'
    },
    statsGrid: {
        display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)',
        gap: '12px', marginBottom: '24px'
    },
    statCard: {
        background: '#f9f9f7', borderRadius: '10px',
        padding: '16px', border: '1px solid #eee'
    },
    statLabel: { fontSize: '13px', color: '#666', margin: '0 0 6px' },
    statValue: { fontSize: '24px', fontWeight: '600', color: '#222', margin: '0 0 4px' },
    statSub: { fontSize: '12px', color: '#1D9E75', margin: 0 },
    sectionTitle: { fontSize: '16px', fontWeight: '600', color: '#222', marginBottom: '14px' },
    projectsGrid: {
        display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '14px'
    },
    projectCard: {
        background: 'white', borderRadius: '12px',
        border: '1px solid #eee', padding: '18px'
    },
    projectHeader: {
        display: 'flex', justifyContent: 'space-between',
        alignItems: 'flex-start', marginBottom: '10px'
    },
    projectTitle: { fontSize: '14px', fontWeight: '600', color: '#222', flex: 1 },
    badge: { fontSize: '11px', padding: '3px 10px', borderRadius: '20px', marginLeft: '8px' },
    projectDesc: { fontSize: '13px', color: '#666', lineHeight: '1.5', marginBottom: '12px' },
    projectFooter: { display: 'flex', justifyContent: 'space-between' },
    budget: { fontSize: '14px', fontWeight: '600', color: '#1D9E75' },
    meta: { fontSize: '12px', color: '#999' },
}; 