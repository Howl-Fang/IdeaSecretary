import sqlite3 from 'sqlite3'
import { open, Database } from 'sqlite'
import path from 'path'
import { fileURLToPath } from 'url'
import { config } from './config/index'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

let db: Database | null = null

export async function getDatabase(): Promise<Database> {
  if (db) return db

  db = await open({
    filename: config.database.path,
    driver: sqlite3.Database
  })

  await db.exec('PRAGMA foreign_keys = ON')
  await initializeSchema()

  return db
}

async function initializeSchema() {
  if (!db) return

  // Users table
  await db.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id TEXT PRIMARY KEY,
      email TEXT UNIQUE NOT NULL,
      name TEXT NOT NULL,
      password_hash TEXT NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `)

  // Knowledge bases table
  await db.exec(`
    CREATE TABLE IF NOT EXISTS knowledge_bases (
      id TEXT PRIMARY KEY,
      user_id TEXT NOT NULL,
      name TEXT NOT NULL,
      description TEXT,
      is_default BOOLEAN DEFAULT 0,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
  `)

  // Ideas table
  await db.exec(`
    CREATE TABLE IF NOT EXISTS ideas (
      id TEXT PRIMARY KEY,
      kb_id TEXT NOT NULL,
      parent_id TEXT,
      title TEXT NOT NULL,
      content TEXT,
      category TEXT,
      tags TEXT,
      type TEXT DEFAULT 'text',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (kb_id) REFERENCES knowledge_bases(id) ON DELETE CASCADE,
      FOREIGN KEY (parent_id) REFERENCES ideas(id) ON DELETE CASCADE
    )
  `)

  // Media resources table
  await db.exec(`
    CREATE TABLE IF NOT EXISTS media_resources (
      id TEXT PRIMARY KEY,
      user_id TEXT NOT NULL,
      filename TEXT NOT NULL,
      file_path TEXT NOT NULL,
      mime_type TEXT,
      size INTEGER,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      deleted_at DATETIME,
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
  `)

  // Search index
  await db.exec(`
    CREATE VIRTUAL TABLE IF NOT EXISTS search_index USING fts5(
      idea_id,
      title,
      content,
      content=ideas,
      content_rowid=rowid
    )
  `)

  console.log('Database schema initialized')
}

export async function closeDatabase() {
  if (db) {
    await db.close()
    db = null
  }
}
