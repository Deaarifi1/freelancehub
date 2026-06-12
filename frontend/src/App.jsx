import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthProvider';
import { useAuth } from './context/useAuth';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Projects from './pages/Projects';
import Home from './pages/Home';
import Freelancers from './pages/Freelancers';
import Agencies from './pages/Agencies';
import Bids from './pages/Bids';
import Contracts from './pages/Contracts';
import Payments from './pages/Payments';
import Chat from './pages/Chat';


function PrivateRoute({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <div>Loading...</div>;
  return user ? children : <Navigate to="/login" />;
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/projects" element={<Projects />} />
          <Route path='/freelancers' element={<Freelancers />} />
          <Route path='/agencies' element={<Agencies />} />
          <Route path="/home" element={<Home />} />
          <Route path="/bids" element={
            <PrivateRoute><Bids /></PrivateRoute>
            } />
          <Route path="/contracts" element={
            <PrivateRoute><Contracts /></PrivateRoute>
            } />
          <Route path="/dashboard" element={
            <PrivateRoute><Dashboard /></PrivateRoute>
          } />
          <Route path="/projects" element={
            <PrivateRoute><Projects /></PrivateRoute>
          } />
          <Route path="/payments" element={
            <PrivateRoute><Payments /></PrivateRoute>
            } />
          <Route path="/chat" element={
            <PrivateRoute><Chat /></PrivateRoute>
            } />
          <Route path="/" element={<Home />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;