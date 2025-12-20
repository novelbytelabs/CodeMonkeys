use crate::oracle::store::OracleStore;
use anyhow::Result;

pub struct QueryEngine {
    store: OracleStore,
}

#[derive(Debug)]
pub struct QueryResult {
    pub name: String,
    pub path: String,
    pub score: f32,
    pub snippet: String,
}

impl QueryEngine {
    pub async fn new(db_path: &str, _vector_uri: &str) -> Result<Self> {
        let store = OracleStore::open(db_path)?;
        Ok(Self { store })
    }

    pub async fn query(&mut self, text: &str) -> Result<Vec<QueryResult>> {
        // Extract keywords from query
        let keywords: Vec<&str> = text
            .split_whitespace()
            .filter(|w| w.len() > 2) // Skip short words
            .collect();

        let mut results = Vec::new();

        // If we have keywords, search for each
        if !keywords.is_empty() {
            for keyword in &keywords {
                if let Ok(nodes) = self.store.search_nodes(keyword) {
                    for (id, path, node_type, name) in nodes {
                        // Avoid duplicates
                        if !results
                            .iter()
                            .any(|r: &QueryResult| r.name == name && r.path == path)
                        {
                            results.push(QueryResult {
                                name,
                                path,
                                score: 1.0, // Simple match
                                snippet: format!("[{}] id={}", node_type, id),
                            });
                        }
                    }
                }
            }
        }

        // If no results or no keywords, show some nodes
        if results.is_empty() {
            if let Ok(nodes) = self.store.get_all_nodes(20) {
                for (id, path, node_type, name) in nodes {
                    results.push(QueryResult {
                        name,
                        path,
                        score: 0.5,
                        snippet: format!("[{}] id={}", node_type, id),
                    });
                }
            }
        }

        Ok(results)
    }
}
