import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/api';
import { useAuth } from '../context/useAuth';

export default function Bids() {
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [bids, setBids] = useState([]);
  const [form, setForm] = useState({ amount: '', proposal: '', delivery_days: '' });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    API.get('/projects/').then(res => setProjects(res.data)).catch(() => {});
  }, []);

  const loadBids = async (projectId) => {
    setSelectedProject(projectId);
    const res = await API.get(`/bids/project/${projectId}`);
    setBids(res.data);
  };

  const handleSubmitBid = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await API.post('/bids/', {
        project_id: selectedProject,
        amount: parseFloat(form.amount),
        proposal: form.proposal,
        delivery_days: parseInt(form.delivery_days)
      });
      setMessage('✅ The offer was sent successfully!');
      setForm({ amount: '', proposal: '', delivery_days: '' });
      loadBids(selectedProject);
    } catch (err) {
      setMessage('❌ ' + (err.response?.data?.detail || 'Error!'));
    } finally {
      setLoading(false);
    }
  };

  const handleAccept = async (bidId) => {
    await API.put(`/bids/${bidId}/accept`);
    loadBids(selectedProject);
  };

  const handleReject = async (bidId) => {
    await API.put(`/bids/${bidId}/reject`);
    loadBids(selectedProject);
  };

  return (
    <div style={{ minHeight: '100vh', background: '#f5f5f5', fontFamily: 'sans-serif' }}>
      <div style={{ background: 'white', padding: '14px 24px', display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #eee' }}>
        <div style={{ fontWeight: '700', fontSize: '18px', color: '#1D9E75', cursor: 'pointer' }} onClick={() => navigate('/')}>
          FreelanceHub
        </div>
        <button onClick={() => navigate('/dashboard')} style={{ padding: '8px 16px', border: '1px solid #ddd', borderRadius: '8px', cursor: 'pointer', background: 'white' }}>
          ← Dashboard
        </button>
      </div>

      <div style={{ padding: '24px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>

        {/* Projects List */}
        <div>
          <h3 style={{ marginBottom: '16px', color: '#333' }}>Projects</h3>
          {projects.map(p => (
            <div
              key={p.id}
              onClick={() => loadBids(p.id)}
              style={{
                background: selectedProject === p.id ? '#E1F5EE' : 'white',
                border: `1px solid ${selectedProject === p.id ? '#1D9E75' : '#eee'}`,
                borderRadius: '10px', padding: '16px', marginBottom: '10px', cursor: 'pointer'
              }}
            >
              <p style={{ fontWeight: '600', margin: '0 0 4px', color: '#222' }}>{p.title}</p>
              <p style={{ fontSize: '13px', color: '#666', margin: '0 0 8px' }}>{p.description?.slice(0, 80)}...</p>
              <span style={{ fontSize: '13px', fontWeight: '600', color: '#1D9E75' }}>${p.budget_min} – ${p.budget_max}</span>
            </div>
          ))}
        </div>

        {/* Bids Section */}
        <div>
          {selectedProject && (
            <>
              {/* Submit Bid Form — only for freelancers */}
              {user?.role === 'freelancer' && (
                <div style={{ background: 'white', borderRadius: '12px', border: '1px solid #eee', padding: '20px', marginBottom: '20px' }}>
                  <h4 style={{ margin: '0 0 16px', color: '#333' }}>Send Offer</h4>
                  {message && <p style={{ color: message.includes('✅') ? 'green' : 'red', marginBottom: '12px' }}>{message}</p>}
                  <form onSubmit={handleSubmitBid}>
                    <input
                      style={{ width: '100%', padding: '10px', border: '1px solid #ddd', borderRadius: '8px', marginBottom: '10px', boxSizing: 'border-box' }}
                      type="number"
                      placeholder="AMOUNT ($)"
                      value={form.amount}
                      onChange={e => setForm({ ...form, amount: e.target.value })}
                      required
                    />
                    <textarea
                      style={{ width: '100%', padding: '10px', border: '1px solid #ddd', borderRadius: '8px', marginBottom: '10px', boxSizing: 'border-box', height: '80px' }}
                      placeholder="Your proposal..."
                      value={form.proposal}
                      onChange={e => setForm({ ...form, proposal: e.target.value })}
                      required
                    />
                    <input
                      style={{ width: '100%', padding: '10px', border: '1px solid #ddd', borderRadius: '8px', marginBottom: '10px', boxSizing: 'border-box' }}
                      type="number"
                      placeholder="Delivery day"
                      value={form.delivery_days}
                      onChange={e => setForm({ ...form, delivery_days: e.target.value })}
                      required
                    />
                    <button
                      type="submit"
                      disabled={loading}
                      style={{ width: '100%', padding: '11px', background: '#1D9E75', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '14px' }}
                    >
                      {loading ? 'Sending...' : 'Send Offer'}
                    </button>
                  </form>
                </div>
              )}

              {/* Bids List */}
              <div style={{ background: 'white', borderRadius: '12px', border: '1px solid #eee', padding: '20px' }}>
                <h4 style={{ margin: '0 0 16px', color: '#333' }}>bids ({bids.length})</h4>
                {bids.length === 0 ? (
                  <p style={{ color: '#666', textAlign: 'center' }}>There are no offers yet.</p>
                ) : (
                  bids.map(bid => (
                    <div key={bid.id} style={{ border: '1px solid #eee', borderRadius: '8px', padding: '14px', marginBottom: '10px' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                        <span style={{ fontWeight: '600', color: '#1D9E75' }}>${bid.amount}</span>
                        <span style={{
                          fontSize: '11px', padding: '3px 8px', borderRadius: '20px',
                          background: bid.status === 'accepted' ? '#E1F5EE' : bid.status === 'rejected' ? '#FEE' : '#f5f5f5',
                          color: bid.status === 'accepted' ? '#0F6E56' : bid.status === 'rejected' ? '#cc0000' : '#666'
                        }}>
                          {bid.status}
                        </span>
                      </div>
                      <p style={{ fontSize: '13px', color: '#555', marginBottom: '8px' }}>{bid.proposal}</p>
                      <p style={{ fontSize: '12px', color: '#999', marginBottom: '10px' }}>📅 {bid.delivery_days} days</p>

                      {/* Accept/Reject buttons — only for clients */}
                      {user?.role === 'client' && bid.status === 'pending' && (
                        <div style={{ display: 'flex', gap: '8px' }}>
                          <button
                            onClick={() => handleAccept(bid.id)}
                            style={{ flex: 1, padding: '8px', background: '#1D9E75', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '13px' }}
                          >
                            ✅ Accept
                          </button>
                          <button
                            onClick={() => handleReject(bid.id)}
                            style={{ flex: 1, padding: '8px', background: '#ff4444', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '13px' }}
                          >
                            ❌ Reject
                          </button>
                        </div>
                      )}
                    </div>
                  ))
                )}
              </div>
            </>
          )}

          {!selectedProject && (
            <div style={{ background: 'white', borderRadius: '12px', border: '1px solid #eee', padding: '40px', textAlign: 'center', color: '#666' }}>
              <p>Select a project from the list to view offers.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}