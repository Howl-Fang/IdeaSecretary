import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Stack, Paper, Card, CardContent } from '@mui/material';
import { useTranslation } from 'react-i18next';
import SendIcon from '@mui/icons-material/Send';
import MicIcon from '@mui/icons-material/Mic';
import ImageIcon from '@mui/icons-material/Image';

function TreasuryPanel({ user }) {
  const { t } = useTranslation();
  const [input, setInput] = useState('');
  const [ideas, setIdeas] = useState([]);
  const [statistics, setStatistics] = useState({ total: 0, words: 0, inspirations: 0 });

  const handleSubmit = async () => {
    if (!input.trim()) return;

    // TODO: Send to backend and organize with AI
    const newIdea = {
      id: Date.now(),
      content: input,
      timestamp: new Date().toLocaleString()
    };

    setIdeas([newIdea, ...ideas]);
    setInput('');
    setStatistics({
      ...statistics,
      total: statistics.total + 1,
      words: statistics.words + input.split(' ').length
    });
  };

  return (
    <Box sx={{ maxWidth: 1200 }}>
      <Typography variant="h5" sx={{ mb: 3, fontWeight: 'bold' }}>
        {t('treasury')}
      </Typography>

      {/* Input Area */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <TextField
          fullWidth
          multiline
          rows={4}
          placeholder={t('whatOnYourMind')}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          sx={{ mb: 2 }}
        />
        <Stack direction="row" spacing={1} sx={{ justifyContent: 'space-between' }}>
          <Stack direction="row" spacing={1}>
            <Button startIcon={<MicIcon />} variant="outlined" size="small">
              {t('voice')}
            </Button>
            <Button startIcon={<ImageIcon />} variant="outlined" size="small">
              {t('image')}
            </Button>
          </Stack>
          <Button 
            endIcon={<SendIcon />} 
            variant="contained"
            onClick={handleSubmit}
            disabled={!input.trim()}
          >
            {t('submit')}
          </Button>
        </Stack>
      </Paper>

      {/* Statistics */}
      <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 2, mb: 3 }}>
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              {t('totalIdeas')}
            </Typography>
            <Typography variant="h4">{statistics.total}</Typography>
          </CardContent>
        </Card>
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              {t('totalWords')}
            </Typography>
            <Typography variant="h4">{statistics.words}</Typography>
          </CardContent>
        </Card>
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              {t('inspirations')}
            </Typography>
            <Typography variant="h4">{statistics.inspirations}</Typography>
          </CardContent>
        </Card>
      </Box>

      {/* Recent Ideas */}
      <Typography variant="h6" sx={{ mb: 2 }}>
        {t('recentIdeas')}
      </Typography>
      <Stack spacing={2}>
        {ideas.map((idea) => (
          <Card key={idea.id}>
            <CardContent>
              <Typography variant="body2" color="textSecondary" sx={{ mb: 1 }}>
                {idea.timestamp}
              </Typography>
              <Typography>{idea.content}</Typography>
            </CardContent>
          </Card>
        ))}
      </Stack>
    </Box>
  );
}

export default TreasuryPanel;
