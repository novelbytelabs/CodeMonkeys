use crate::oracle::edges::GraphEdge;
use crate::oracle::graph::GraphNode;
use crate::oracle::schema::init_db;
use rusqlite::{params, Connection, Result};
use std::path::Path;

pub struct OracleStore {
    conn: Connection,
}

impl OracleStore {
    pub fn open<P: AsRef<Path>>(path: P) -> Result<Self> {
        let conn = Connection::open(path)?;
        init_db(&conn)?;
        Ok(Self { conn })
    }

    pub fn insert_node(&mut self, node: &GraphNode) -> Result<i64> {
        let tx = self.conn.transaction()?;
        tx.execute(
            "INSERT INTO nodes (path, type, name, start_line, end_line, signature_hash, docstring)
             VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)
             ON CONFLICT(path, type, name, start_line) DO UPDATE SET
             signature_hash=excluded.signature_hash, end_line=excluded.end_line",
            params![
                node.path,
                node.node_type,
                node.name,
                node.start_line,
                node.end_line,
                node.signature_hash,
                node.docstring
            ],
        )?;
        let id = tx.last_insert_rowid();
        tx.commit()?;
        Ok(id)
    }

    pub fn insert_edge(&mut self, edge: &GraphEdge) -> Result<()> {
        // Find IDs first (simplified logic: assumes uniqueness by name for MVP)
        // In reality, would need path resolution.
        let source_id: Option<i64> = self
            .conn
            .query_row(
                "SELECT id FROM nodes WHERE name = ?1 LIMIT 1",
                params![edge.source_node_name],
                |row| row.get(0),
            )
            .optional()?;

        let target_id: Option<i64> = self
            .conn
            .query_row(
                "SELECT id FROM nodes WHERE name = ?1 LIMIT 1",
                params![edge.target_node_name],
                |row| row.get(0),
            )
            .optional()?;

        if let (Some(sid), Some(tid)) = (source_id, target_id) {
            self.conn.execute(
                "INSERT INTO edges (source_id, target_id, type) VALUES (?1, ?2, ?3)",
                params![sid, tid, edge.edge_type],
            )?;
        }
        Ok(())
    }

    /// Search nodes by name pattern
    pub fn search_nodes(&self, pattern: &str) -> Result<Vec<(i64, String, String, String)>> {
        let search_pattern = format!("%{}%", pattern.to_lowercase());
        let mut stmt = self
            .conn
            .prepare("SELECT id, path, type, name FROM nodes WHERE LOWER(name) LIKE ?1 LIMIT 20")?;

        let rows = stmt.query_map(params![search_pattern], |row| {
            Ok((row.get(0)?, row.get(1)?, row.get(2)?, row.get(3)?))
        })?;

        let mut results = Vec::new();
        for row in rows {
            results.push(row?);
        }
        Ok(results)
    }

    /// Get all nodes (limited)
    pub fn get_all_nodes(&self, limit: usize) -> Result<Vec<(i64, String, String, String)>> {
        let mut stmt = self
            .conn
            .prepare("SELECT id, path, type, name FROM nodes LIMIT ?1")?;

        let rows = stmt.query_map(params![limit as i64], |row| {
            Ok((row.get(0)?, row.get(1)?, row.get(2)?, row.get(3)?))
        })?;

        let mut results = Vec::new();
        for row in rows {
            results.push(row?);
        }
        Ok(results)
    }
}

// Add optional helper trait
use rusqlite::OptionalExtension;
