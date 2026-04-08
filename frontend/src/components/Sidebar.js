import React from 'react';
import { List, ListItem, ListItemIcon, ListItemText, Box } from '@mui/material';
import { useTranslation } from 'react-i18next';
import StorageIcon from '@mui/icons-material/Storage';
import BookmarkIcon from '@mui/icons-material/Bookmark';
import PersonIcon from '@mui/icons-material/Person';
import SettingsIcon from '@mui/icons-material/Settings';

function Sidebar({ activePanel, setActivePanel, sidebarOpen }) {
  const { t } = useTranslation();

  const menuItems = [
    { id: 'treasury', label: t('treasury'), icon: <StorageIcon /> },
    { id: 'library', label: t('myIdeaBase'), icon: <BookmarkIcon /> },
    { id: 'account', label: t('account'), icon: <PersonIcon /> },
    { id: 'settings', label: t('settings'), icon: <SettingsIcon /> }
  ];

  return (
    <Box sx={{ pt: 2 }}>
      <List>
        {menuItems.map((item) => (
          <ListItem 
            key={item.id}
            button 
            selected={activePanel === item.id}
            onClick={() => setActivePanel(item.id)}
            sx={{ px: 1 }}
          >
            <ListItemIcon sx={{ minWidth: sidebarOpen ? 40 : 0 }}>
              {item.icon}
            </ListItemIcon>
            {sidebarOpen && <ListItemText primary={item.label} />}
          </ListItem>
        ))}
      </List>
    </Box>
  );
}

export default Sidebar;
