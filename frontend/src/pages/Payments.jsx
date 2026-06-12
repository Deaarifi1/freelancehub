import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/api';

export default function Payments() {
  const [payments, setPayments] = useState([]);
  const [contracts, setContracts] = useState([]);
  const [escrow, setEscrow] = useState({});
  const [form, setForm] = useState({ contract_id: '', amount: '' });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    API.get('/payments/my-payments').then(res => setPayments(res.data)).catch(() => {});
    API.get('/contracts/').then(res => setContracts(res.data)).catch(() => {});
  }, []);

  const loadEscrow = async (contractId) => {
    try {
      const res = await API.get(`/payments/escrow/${contractId}`);
      setEscrow(prev => ({ ...prev, [contractId]: res.data }));
    } catch {
      setEscrow(prev => ({ ...prev, [contractId]: null }));
    }
  };

  const handlePayment = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await API.post('/payments/', {
        contract_id: parseInt(form.contract_id),
        amount: parseFloat(form.amount)
      });
      setMessage('✅ Payment was successful!');
      setForm({ contract_id: '', amount: '' });
      const res = await API.get('/payments/my-payments');
      setPayments(res.data);
    } catch (err) {
      setMessage('❌ ' + (err.response?.data?.detail || 'Error!'));
    } finally {
      setLoading(false);
    }
  };

  const handleReleaseEscrow = async (contractId) => {
    try {
      await API.put(`/payments/escrow/${contractId}/release`);
      setMessage('✅ Escrow was released — freelancer received payment!');
      loadEscrow(contractId);
    } catch (err) {
      setMessage('❌ ' + (err.response?.data?.detail || 'Error!'));
    }
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

        {/* Payment Form */}
        <div>
          <div style={{ background: 'white', borderRadius: '12px', border: '1px solid #eee', padding: '20px', marginBottom: '20px' }}>
            <h4 style={{ margin: '0 0 16px', color: '#333' }}>Make Payment</h4>
            {message && <p style={{ color: message.includes('✅') ? 'green' : 'red', marginBottom: '12px' }}>{message}</p>}
            <form onSubmit={handlePayment}>
              <select
                style={{ width: '100%', padding: '10px', border: '1px solid #ddd', borderRadius: '8px', marginBottom: '10px', boxSizing: 'border-box' }}
                value={form.contract_id}
                onChange={e => {
                  setForm({ ...form, contract_id: e.target.value });
                  if (e.target.value) loadEscrow(e.target.value);
                }}
                required
              >
                <option value="">Choose the contract...</option>
                {contracts.map(c => (
                  <option key={c.id} value={c.id}>
                    Kontrata #{c.id} — ${c.total_amount}
                  </option>
                ))}
              </select>
              <input
                style={{ width: '100%', padding: '10px', border: '1px solid #ddd', borderRadius: '8px', marginBottom: '10px', boxSizing: 'border-box' }}
                type="number"
                placeholder="AMOUNT ($)"
                value={form.amount}
                onChange={e => setForm({ ...form, amount: e.target.value })}
                required
              />
              <button
                type="submit"
                disabled={loading}
                style={{ width: '100%', padding: '11px', background: '#1D9E75', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '14px' }}
              >
                {loading ? 'By paying...' : 'Pay'}
              </button>
            </form>
          </div>

          {/* Escrow Status */}
          {form.contract_id && escrow[form.contract_id] !== undefined && (
            <div style={{ background: 'white', borderRadius: '12px', border: '1px solid #eee', padding: '20px' }}>
              <h4 style={{ margin: '0 0 12px', color: '#333' }}>Escrow</h4>
              {escrow[form.contract_id] ? (
                <>
                  <p style={{ fontSize: '14px', marginBottom: '8px' }}>
                    <strong>Balance:</strong> ${escrow[form.contract_id].balance}
                  </p>
                  <p style={{ fontSize: '14px', marginBottom: '12px' }}>
                    <strong>Status:</strong>{' '}
                    <span style={{ color: escrow[form.contract_id].is_released ? '#1D9E75' : '#854F0B' }}>
                      {escrow[form.contract_id].is_released ? '✅ Released' : '⏳ Blocked'}
                    </span>
                  </p>
                  {!escrow[form.contract_id].is_released && (
                    <button
                      onClick={() => handleReleaseEscrow(form.contract_id)}
                      style={{ width: '100%', padding: '10px', background: '#1D9E75', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer' }}
                    >
                      Release Escrow → Freelancer receives payment
                    </button>
                  )}
                </>
              ) : (
                <p style={{ color: '#666', fontSize: '13px' }}>There is no escrow for this contract.</p>
              )}
            </div>
          )}
        </div>

        {/* Payments List */}
        <div>
          <h3 style={{ marginBottom: '16px', color: '#333' }}>My Payments</h3>
          {payments.length === 0 ? (
            <div style={{ background: 'white', borderRadius: '12px', border: '1px solid #eee', padding: '40px', textAlign: 'center', color: '#666' }}>
              <p>No payment yet.</p>
            </div>
          ) : (
            payments.map(p => (
              <div key={p.id} style={{ background: 'white', borderRadius: '12px', border: '1px solid #eee', padding: '16px', marginBottom: '10px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <span style={{ fontWeight: '600', color: '#1D9E75' }}>${p.amount}</span>
                  <span style={{
                    fontSize: '11px', padding: '3px 8px', borderRadius: '20px',
                    background: p.status === 'completed' ? '#E1F5EE' : '#f5f5f5',
                    color: p.status === 'completed' ? '#0F6E56' : '#666'
                  }}>
                    {p.status}
                  </span>
                </div>
                <p style={{ fontSize: '12px', color: '#999', margin: 0 }}>
                  Kontrata #{p.contract_id} · {new Date(p.created_at).toLocaleDateString()}
                </p>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}