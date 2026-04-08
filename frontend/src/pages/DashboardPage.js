import React, { useState } from 'react';
import { Box, Drawer, AppBar, Toolbar, Typography, IconButton, Tooltip } from '@mui/material';
import { useTranslation } from 'react-i18next';
import MenuIcon from '@mui/icons-material/Menu';
import CloseIcon from '@mui/icons-material/Close';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import LightModeIcon from '@mui/icons-material/LightMode';
import TranslateIcon from '@mui/icons-material/Translate';
import LogoutIcon from '@mui/icons-material/Logout';

// Components
import Sidebar from '../components/Sidebar';
import TreasuryPanel from '../components/TreasuryPanel';

function DashboardPage({ user, setUser, theme, toggleTheme, changeLanguage }) {
  const { t, i18n } = useTranslation();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activePanel, setActivePanel] = useState('treasury');

  const handleLogout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    setUser(null);
  };

  const renderPanel = () => {
    switch (activePanel) {
      case 'treasury':
        return <TreasuryPanel user={user} />;
      case 'library':
        return <Typography>{t('myIdeaBase')}</Typography>;
      case 'account':
        return <Typography>{t('account')}</Typography>;
      case 'settings':
        return <Typography>{t('settings')}</Typography>;
      default:
        return <TreasuryPanel user={user} />;
    }
  };

  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      {/* Sidebar */}
      <Drawer 
        variant="permanent" 
        sx={{ 
          width: sidebarOpen ? 250 : 80,
          transition: 'width 0.3s',
          '& .MuiDrawer-paper': {
            width: sidebarOpen ? 250 : 80,
            transition: 'width 0.3s',
          }
        }}
      >
        <Sidebar 
          activePanel={activePanel} 
          setActivePanel={setActivePanel}
          sidebarOpen={sidebarOpen}
        />
      </Drawer>

      {/* Main Content */}
      <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        {/* Top Bar */}
        <AppBar position="static">
          <Toolbar>
            <IconButton 
              color="inherit" 
              onClick={() => setSidebarOpen(!sidebarOpen)}
              sx={{ mr: 2 }}
            >
              {sidebarOpen ? <CloseIcon /> : <MenuIcon />}
            </IconButton>

            <Typography variant="h6" sx={{ flex: 1 }}>
              IDEA SECRETARY
            </Typography>

            {/* Theme Toggle */}
            <Tooltip title={t('toggleTheme')}>
              <IconButton color="inherit" onClick={toggleTheme}>
                {theme === 'light' ? <DarkModeIcon /> : <LightModeIcon />}
              </IconButton>
            </Tooltip>

            {/* Language Toggle */}
            <Tooltip title={t('switchLanguage')}>
              <IconButton 
                color="inherit" 
                onClick={() => changeLanguage(i18n.language === 'en' ? 'zh' : 'en')}
              >
                <TranslateIcon />
              </IconButton>
            </Tooltip>

            {/* Logout */}
            <Tooltip title={t('logout')}>
              <IconButton color="inherit" onClick={handleLogout}>
                <LogoutIcon />
              </IconButton>
            </Tooltip>
          </Toolbar>
        </AppBar>

        {/* Content Area */}
        <Box sx={{ flex: 1, overflow: 'auto', p: 3 }}>
          {renderPanel()}
        </Box>
      </Box>
    </Box>
  );
}

export default DashboardPage;
