import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import i18n from 'i18next';
import { useTranslation } from 'react-i18next';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';

// Pages
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import NotFoundPage from './pages/NotFoundPage';

// Utils
import { LANGUAGES, THEMES } from './config';

function App() {
  const { i18n } = useTranslation();
  const [theme, setTheme] = useState(THEMES.LIGHT);
  const [user, setUser] = useState(null);

  // Load user preferences from localStorage
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || THEMES.LIGHT;
    const savedLanguage = localStorage.getItem('language') || LANGUAGES.EN;
    const savedUser = localStorage.getItem('user');

    setTheme(savedTheme);
    i18n.changeLanguage(savedLanguage);
    
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  // Create MUI theme based on selected theme
  const muiTheme = createTheme({
    palette: {
      mode: theme === THEMES.DARK ? 'dark' : 'light',
      primary: {
        main: '#1976d2',
      },
      secondary: {
        main: '#dc004e',
      },
    },
  });

  const toggleTheme = () => {
    const newTheme = theme === THEMES.LIGHT ? THEMES.DARK : THEMES.LIGHT;
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
  };

  const changeLanguage = (lang) => {
    i18n.changeLanguage(lang);
    localStorage.setItem('language', lang);
  };

  return (
    <ThemeProvider theme={muiTheme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage setUser={setUser} />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route 
            path="/dashboard/*" 
            element={
              user ? (
                <DashboardPage 
                  user={user} 
                  setUser={setUser}
                  theme={theme}
                  toggleTheme={toggleTheme}
                  changeLanguage={changeLanguage}
                />
              ) : (
                <LoginPage setUser={setUser} />
              )
            } 
          />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
