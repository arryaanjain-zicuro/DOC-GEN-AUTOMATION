import { Navigate, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import FileUpload from './components/FileUpload';

function App() {
  return (
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/upload" element={<FileUpload />} />
      </Routes>
  );
}

export default App;