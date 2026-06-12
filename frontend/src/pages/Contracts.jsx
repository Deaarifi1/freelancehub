import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/api';
import { useAuth } from '../context/useAuth';

export default function Contracts() {
  const [contracts, setContracts] = useState([]);
  const [milestones, setMilestones] = useState({});
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    API.get('/contracts/')
      .then(res => setContracts(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const loadMilestones = async (contractId) => {
    const res = await API.get(`/contracts/${contractId}/milestones`);
    setMilestones(prev => ({ ...prev, [contractId]: res.data }));
  };

  const handleComplete = async (contractId) => {
    try {
      await API.put(`/contracts/${contractId}/complete`);
      setMessage('✅ The contract was successfully closed!');
      const res = await API.get('/contracts/');
      setContracts(res.data);
    } catch (err) {
      setMessage('❌ ' + (err.response?.data?.detail || 'Error!'));
    }
  };

  const handleCompleteMilestone = async (contractId, milestoneId) => {
    await API.put(`/contracts/${contractId}/milestones/${milestoneId}/complete`);
    loadMilestones(contractId);
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

      <div style={{ padding: '24px' }}>
        <h3 style={{ marginBottom: '16px', color: '#333' }}>Kontratat</h3>
        {message && <p style={{ color: message.includes('✅') ? 'green' : 'red', marginBottom: '12px' }}>{message}</p>}

        {loading ? (
          <p>Loading...</p>
        ) : contracts.length === 0 ? (
          <p style={{ textAlign: 'center', color: '#666', padding: '40px' }}>No contract yet.</p>
        ) : (
          <div style={{ display: 'grid', gap: '16px' }}>
            {contracts.map(c => (
              <div key={c.id} style={{ background: 'white', borderRadius: '12px', border: '1px solid #eee', padding: '20px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                  <div>
                    <p style={{ fontWeight: '600', margin: '0 0 4px', color: '#222' }}>Contracts #{c.id}</p>
                    <p style={{ fontSize: '13px', color: '#666', margin: 0 }}>Project #{c.project_id}</p>
                  </div>
                  <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                    <span style={{
                      fontSize: '12px', padding: '4px 10px', borderRadius: '20px',
                      background: c.status === 'completed' ? '#E1F5EE' : c.status === 'active' ? '#FAEEDA' : '#f5f5f5',
                      color: c.status === 'completed' ? '#0F6E56' : c.status === 'active' ? '#854F0B' : '#666'
                    }}>
                      {c.status}
                    </span>
                    <span style={{ fontWeight: '600', color: '#1D9E75' }}>${c.total_amount}</span>
                  </div>
                </div>

                {c.terms && (
                  <p style={{ fontSize: '13px', color: '#555', marginBottom: '12px', padding: '10px', background: '#f9f9f7', borderRadius: '8px' }}>
                    {c.terms}
                  </p>
                )}

                <div style={{ display: 'flex', gap: '8px', marginBottom: '12px' }}>
                  <button
                    onClick={() => loadMilestones(c.id)}
                    style={{ padding: '8px 14px', border: '1px solid #ddd', borderRadius: '8px', cursor: 'pointer', background: 'white', fontSize: '13px' }}
                  >
                    View Milestones
                  </button>
                  {user?.role === 'client' && c.status === 'active' && (
                    <button
                      onClick={() => handleComplete(c.id)}
                      style={{ padding: '8px 14px', background: '#1D9E75', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '13px' }}
                    >
                      ✅ Close the Contract
                    </button>
                  )}
                </div>

                {/* Milestones */}
                {milestones[c.id] && (
                  <div style={{ borderTop: '1px solid #eee', paddingTop: '12px' }}>
                    <p style={{ fontWeight: '600', fontSize: '14px', marginBottom: '10px', color: '#333' }}>Milestones:</p>
                    {milestones[c.id].length === 0 ? (
                      <p style={{ fontSize: '13px', color: '#666' }}>There are no milestones.</p>
                    ) : (
                      milestones[c.id].map(m => (
                        <div key={m.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px', background: '#f9f9f7', borderRadius: '8px', marginBottom: '8px' }}>
                          <div>
                            <p style={{ fontWeight: '500', margin: '0 0 2px', fontSize: '14px' }}>{m.title}</p>
                            <p style={{ fontSize: '12px', color: '#666', margin: 0 }}>${m.amount}</p>
                          </div>
                          <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                            <span style={{
                              fontSize: '11px', padding: '3px 8px', borderRadius: '20px',
                              background: m.is_completed ? '#E1F5EE' : '#f5f5f5',
                              color: m.is_completed ? '#0F6E56' : '#666'
                            }}>
                              {m.is_completed ? '✅ Complete' : '⏳ In progress'}
                            </span>
                            {!m.is_completed && (
                              <button
                                onClick={() => handleCompleteMilestone(c.id, m.id)}
                                style={{ padding: '6px 12px', background: '#1D9E75', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '12px' }}
                              >
                                close
                              </button>
                            )}
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}