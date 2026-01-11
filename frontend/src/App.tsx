import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Layout from './components/Layout';

// Pages
import Catalog from './pages/Catalog';
import MangaDetail from './pages/MangaDetail';
import Reader from './pages/Reader';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';
import MyLists from './pages/MyLists';
import PublicLists from './pages/PublicLists';
import ListDetail from './pages/ListDetail';
import Upload from './pages/Upload';

import './App.css';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Layout>
          <Routes>
            {/* Public routes */}
            <Route path="/" element={<Catalog />} />
            <Route path="/manga/:id" element={<MangaDetail />} />
            <Route path="/read/:mangaId/:chapterId" element={<Reader />} />
            <Route path="/lists" element={<PublicLists />} />
            <Route path="/list/:id" element={<ListDetail />} />

            {/* Auth routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Protected routes */}
            <Route path="/profile" element={<Profile />} />
            <Route path="/my-lists" element={<MyLists />} />
            <Route path="/upload" element={<Upload />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
