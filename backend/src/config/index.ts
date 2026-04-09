import dotenv from 'dotenv'

dotenv.config()

export const config = {
  port: process.env.PORT || 3001,
  env: process.env.NODE_ENV || 'development',
  jwt: {
    secret: process.env.JWT_SECRET || 'your-secret-key',
    expiresIn: '7d' as const
  },
  database: {
    path: process.env.DB_PATH || './data/ideasecretary.db'
  },
  openai: {
    apiKey: process.env.OPENAI_API_KEY || '',
    apiUrl: process.env.OPENAI_API_URL || 'https://api.openai.com/v1',
  },
  cors: {
    origin: process.env.CORS_ORIGIN || 'http://localhost:5173'
  }
}
