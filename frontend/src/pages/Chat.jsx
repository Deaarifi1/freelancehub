import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/api';
import { useAuth } from '../context/useAuth';

export default function Chat() {
  const [conversations, setConversations] = useState([]);
  const [selectedConv, setSelectedConv] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    API.get('/messages/conversations')
      .then(res => setConversations(res.data))
      .catch(() => {});
  }, []);

  const loadMessages = async (conv) => {
    setSelectedConv(conv);
    const res = await API.get(`/messages/${conv.id}`);
    setMessages(res.data);
    await API.put(`/messages/${conv.id}/read`);
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;
    setLoading(true);
    try {
      await API.post('/messages/', {
        conversation_id: selectedConv.id,
        content: newMessage
      });
      setNewMessage('');
      const res = await API.get(`/messages/${selectedConv.id}`);
      setMessages(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
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

      <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', height: 'calc(100vh - 57px)' }}>

        {/* Conversations List */}
        <div style={{ background: 'white', borderRight: '1px solid #eee', overflowY: 'auto' }}>
          <div style={{ padding: '16px', borderBottom: '1px solid #eee' }}>
            <h4 style={{ margin: 0, color: '#333' }}>Konversacionet</h4>
          </div>
          {conversations.length === 0 ? (
            <p style={{ padding: '20px', color: '#666', fontSize: '13px', textAlign: 'center' }}>
              There are no conversations yet.
            </p>
          ) : (
            conversations.map(conv => (
              <div
                key={conv.id}
                onClick={() => loadMessages(conv)}
                style={{
                  padding: '16px', cursor: 'pointer', borderBottom: '1px solid #eee',
                  background: selectedConv?.id === conv.id ? '#E1F5EE' : 'white'
                }}
              >
                <p style={{ margin: '0 0 4px', fontWeight: '600', fontSize: '14px', color: '#222' }}>
                  Conversation #{conv.id}
                </p>
                <p style={{ margin: 0, fontSize: '12px', color: '#666' }}>
                  Project #{conv.project_id || 'N/A'}
                </p>
              </div>
            ))
          )}
        </div>

        {/* Messages Area */}
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          {selectedConv ? (
            <>
              <div style={{ padding: '16px', background: 'white', borderBottom: '1px solid #eee' }}>
                <h4 style={{ margin: 0, color: '#333' }}>Conversation #{selectedConv.id}</h4>
              </div>

              {/* Messages */}
              <div style={{ flex: 1, overflowY: 'auto', padding: '16px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {messages.length === 0 ? (
                  <p style={{ textAlign: 'center', color: '#666' }}>There are no messages yet.</p>
                ) : (
                  messages.map(msg => (
                    <div
                      key={msg.id}
                      style={{
                        display: 'flex',
                        justifyContent: msg.sender_id === user?.id ? 'flex-end' : 'flex-start'
                      }}
                    >
                      <div style={{
                        maxWidth: '60%', padding: '10px 14px', borderRadius: '12px',
                        background: msg.sender_id === user?.id ? '#1D9E75' : 'white',
                        color: msg.sender_id === user?.id ? 'white' : '#333',
                        border: msg.sender_id === user?.id ? 'none' : '1px solid #eee',
                        fontSize: '14px'
                      }}>
                        <p style={{ margin: '0 0 4px' }}>{msg.content}</p>
                        <p style={{ margin: 0, fontSize: '11px', opacity: 0.7 }}>
                          {new Date(msg.created_at).toLocaleTimeString()}
                        </p>
                      </div>
                    </div>
                  ))
                )}
              </div>

              {/* Send Message */}
              <div style={{ padding: '16px', background: 'white', borderTop: '1px solid #eee' }}>
                <form onSubmit={handleSend} style={{ display: 'flex', gap: '8px' }}>
                  <input
                    style={{ flex: 1, padding: '10px 14px', border: '1px solid #ddd', borderRadius: '8px', fontSize: '14px' }}
                    placeholder="Write the message..."
                    value={newMessage}
                    onChange={e => setNewMessage(e.target.value)}
                  />
                  <button
                    type="submit"
                    disabled={loading}
                    style={{ padding: '10px 20px', background: '#1D9E75', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '14px' }}
                  >
                    Submit
                  </button>
                </form>
              </div>
            </>
          ) : (
            <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#666' }}>
              <p>Select a conversation from the list.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}