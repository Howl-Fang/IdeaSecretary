import React from 'react';
import { Box, Container, Button, Typography, Stack } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';

function LandingPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();

  return (
    <Container maxWidth="lg">
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
        {/* Header */}
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%', mb: 8 }}>
          <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
            IDEA SECRETARY
          </Typography>
          <Stack direction="row" spacing={2}>
            <Button variant="text" onClick={() => navigate('/login')}>
              {t('login')}
            </Button>
            <Button variant="contained" onClick={() => navigate('/register')}>
              {t('register')}
            </Button>
          </Stack>
        </Box>

        {/* Main Content */}
        <Box sx={{ textAlign: 'center' }}>
          <Typography variant="h2" sx={{ mb: 4, fontWeight: 'bold', animation: 'fadeIn 1s ease-in' }}>
            {t('landing.title')}
          </Typography>
          
          <Typography variant="h5" sx={{ mb: 4, color: 'text.secondary', maxWidth: '600px' }}>
            {t('landing.description')}
          </Typography>

          <Stack direction="row" spacing={3} sx={{ justifyContent: 'center' }}>
            <Button 
              variant="contained" 
              size="large"
              onClick={() => navigate('/register')}
            >
              {t('getStarted')}
            </Button>
            <Button 
              variant="outlined" 
              size="large"
              onClick={() => navigate('/login')}
            >
              {t('login')}
            </Button>
          </Stack>

          {/* Features Preview */}
          <Box sx={{ mt: 8, display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 3 }}>
            <Box sx={{ p: 3, border: '1px solid', borderColor: 'divider', borderRadius: 2 }}>
              <Typography variant="h6" sx={{ mb: 2 }}>📝 {t('features.input')}</Typography>
              <Typography variant="body2" color="text.secondary">
                {t('features.inputDesc')}
              </Typography>
            </Box>
            <Box sx={{ p: 3, border: '1px solid', borderColor: 'divider', borderRadius: 2 }}>
              <Typography variant="h6" sx={{ mb: 2 }}>🤖 {t('features.ai')}</Typography>
              <Typography variant="body2" color="text.secondary">
                {t('features.aiDesc')}
              </Typography>
            </Box>
            <Box sx={{ p: 3, border: '1px solid', borderColor: 'divider', borderRadius: 2 }}>
              <Typography variant="h6" sx={{ mb: 2 }}>🔍 {t('features.search')}</Typography>
              <Typography variant="body2" color="text.secondary">
                {t('features.searchDesc')}
              </Typography>
            </Box>
          </Box>
        </Box>

        {/* Footer */}
        <Box sx={{ mt: 8, textAlign: 'center', width: '100%', borderTop: '1px solid', borderColor: 'divider', pt: 4 }}>
          <Typography variant="body2" color="text.secondary">
            © 2026 IdeaSecretary | 
            <Button 
              size="small" 
              href="https://github.com/Howl-Fang/IdeaSecretary" 
              target="_blank" 
              rel="noopener noreferrer"
              sx={{ ml: 1 }}
            >
              GitHub
            </Button>
          </Typography>
        </Box>
      </Box>
    </Container>
  );
}

export default LandingPage;
