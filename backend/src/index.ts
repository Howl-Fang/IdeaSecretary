import express, { Request, Response } from 'express'
import cors from 'cors'
import { config } from './config/index'
import { getDatabase, closeDatabase } from './db'
import authRoutes, { authMiddleware } from './routes/auth'

const app = express()

// Middleware
app.use(cors({
  origin: config.cors.origin,
  credentials: true
}))
app.use(express.json())

// Initialize database
await getDatabase()

// Routes
app.use('/api/auth', authRoutes)

// Health check
app.get('/api/health', (req: Request, res: Response) => {
  res.json({ status: 'ok' })
})

// Error handling
app.use((err: any, req: Request, res: Response) => {
  console.error(err)
  res.status(500).json({ message: 'Internal server error' })
})

// Start server
app.listen(config.port, () => {
  console.log(`Server running on port ${config.port}`)
})

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, shutting down gracefully')
  await closeDatabase()
  process.exit(0)
})

process.on('SIGINT', async () => {
  console.log('SIGINT received, shutting down gracefully')
  await closeDatabase()
  process.exit(0)
})

export default app
