import { Router, Request, Response, NextFunction } from 'express'
import bcryptjs from 'bcryptjs'
import jwt, { SignOptions } from 'jsonwebtoken'
import { v4 as uuidv4 } from 'uuid'
import { getDatabase } from '@/db'
import { config } from '@/config'
import { body, validationResult } from 'express-validator'

const router = Router()

interface AuthRequest extends Request {
  user?: { id: string; email: string }
}

export function authMiddleware(req: AuthRequest, res: Response, next: NextFunction) {
  const token = req.headers.authorization?.split(' ')[1]
  if (!token) {
    return res.status(401).json({ message: 'No token provided' })
  }

  try {
    const decoded = jwt.verify(token, config.jwt.secret) as { id: string }
    req.user = { id: decoded.id, email: '' }
    next()
  } catch {
    res.status(401).json({ message: 'Invalid token' })
  }
}

// Register
router.post('/register',
  body('email').isEmail(),
  body('password').isLength({ min: 6 }),
  body('name').notEmpty(),
  async (req: Request, res: Response) => {
    const errors = validationResult(req)
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() })
    }

    try {
      const db = await getDatabase()
      const { email, password, name } = req.body

      const existing = await db.get('SELECT id FROM users WHERE email = ?', [email])
      if (existing) {
        return res.status(400).json({ message: 'Email already registered' })
      }

      const id = uuidv4()
      const hash = await bcryptjs.hash(password, 10)

      await db.run('INSERT INTO users (id, email, name, password_hash) VALUES (?, ?, ?, ?)',
        [id, email, name, hash]
      )

      // Create default knowledge base
      const kbId = uuidv4()
      await db.run(
        'INSERT INTO knowledge_bases (id, user_id, name, is_default) VALUES (?, ?, ?, 1)',
        [kbId, id, 'Default']
      )

      const jwtOptions: SignOptions = { expiresIn: config.jwt.expiresIn }
      const token = jwt.sign({ id }, config.jwt.secret, jwtOptions)

      res.json({
        token,
        user: { id, email, name }
      })
    } catch (error) {
      console.error(error)
      res.status(500).json({ message: 'Registration failed' })
    }
  }
)

// Login
router.post('/login',
  body('email').isEmail(),
  body('password').notEmpty(),
  async (req: Request, res: Response) => {
    const errors = validationResult(req)
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() })
    }

    try {
      const db = await getDatabase()
      const { email, password } = req.body

      const user = await db.get('SELECT id, name, password_hash FROM users WHERE email = ?', [email])
      if (!user) {
        return res.status(400).json({ message: 'Invalid credentials' })
      }

      const isValid = await bcryptjs.compare(password, user.password_hash)
      if (!isValid) {
        return res.status(400).json({ message: 'Invalid credentials' })
      }

      const jwtOptions: SignOptions = { expiresIn: config.jwt.expiresIn }
      const token = jwt.sign({ id: user.id }, config.jwt.secret, jwtOptions)

      res.json({
        token,
        user: { id: user.id, email, name: user.name }
      })
    } catch (error) {
      console.error(error)
      res.status(500).json({ message: 'Login failed' })
    }
  }
)

export default router
