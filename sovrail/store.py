import sqlite3, time
from .config import settings

def db():
    c=sqlite3.connect(settings.db_path, check_same_thread=False)
    c.row_factory=sqlite3.Row
    c.executescript('''
    PRAGMA journal_mode=WAL;
    CREATE TABLE IF NOT EXISTS client_keys(
      id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,key_hash TEXT UNIQUE NOT NULL,
      prefix TEXT NOT NULL,scopes TEXT NOT NULL,enabled INTEGER NOT NULL DEFAULT 1,
      rpm INTEGER NOT NULL DEFAULT 120,daily_limit INTEGER NOT NULL DEFAULT 5000,
      daily_budget_micros INTEGER NOT NULL DEFAULT 0,expires_at INTEGER,created_at INTEGER NOT NULL);
    CREATE TABLE IF NOT EXISTS usage(
      id INTEGER PRIMARY KEY AUTOINCREMENT,key_hash TEXT,provider TEXT,endpoint TEXT,status INTEGER,
      cost_micros INTEGER NOT NULL DEFAULT 0,latency_ms INTEGER NOT NULL DEFAULT 0,created_at INTEGER NOT NULL);
    CREATE INDEX IF NOT EXISTS idx_usage_key_time ON usage(key_hash,created_at);
    CREATE TABLE IF NOT EXISTS cache(cache_key TEXT PRIMARY KEY,payload TEXT NOT NULL,expires_at INTEGER NOT NULL);
    CREATE TABLE IF NOT EXISTS idempotency(key_hash TEXT NOT NULL,idem_key TEXT NOT NULL,response TEXT NOT NULL,
      expires_at INTEGER NOT NULL,PRIMARY KEY(key_hash,idem_key));
    CREATE TABLE IF NOT EXISTS rate_bucket(key_hash TEXT PRIMARY KEY,tokens REAL NOT NULL,updated_at REAL NOT NULL);
    CREATE TABLE IF NOT EXISTS circuits(provider TEXT PRIMARY KEY,failures INTEGER NOT NULL DEFAULT 0,
      opened_until INTEGER NOT NULL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT,event TEXT NOT NULL,payload TEXT NOT NULL,
      prev_hash TEXT NOT NULL,event_hash TEXT NOT NULL,created_at INTEGER NOT NULL);
    ''')
    c.commit(); return c

def now(): return int(time.time())
