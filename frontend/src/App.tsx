import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Intro from './pages/Intro'
import Login from './pages/Login'
import './i18n'
import './index.css'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Intro />} />
        <Route path="/login" element={<Login />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  )
}

export default App
