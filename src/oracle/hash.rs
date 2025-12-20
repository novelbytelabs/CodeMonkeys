use sha2::{Digest, Sha256};

pub fn compute_hash(content: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(content.as_bytes());
    format!("{:x}", hasher.finalize())
}

pub fn compute_signature_hash(name: &str, body: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(name.as_bytes());
    hasher.update(b"::");
    hasher.update(body.as_bytes());
    format!("{:x}", hasher.finalize())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_compute_hash_deterministic() {
        let content = "fn main() { println!(\"Hello\"); }";
        let hash1 = compute_hash(content);
        let hash2 = compute_hash(content);
        assert_eq!(hash1, hash2);
        assert_eq!(hash1.len(), 64); // SHA256 produces 64 hex chars
    }

    #[test]
    fn test_compute_hash_different_inputs() {
        let hash1 = compute_hash("hello");
        let hash2 = compute_hash("world");
        assert_ne!(hash1, hash2);
    }

    #[test]
    fn test_compute_signature_hash_includes_name() {
        // Same body but different names should produce different hashes
        let hash1 = compute_signature_hash("foo", "body");
        let hash2 = compute_signature_hash("bar", "body");
        assert_ne!(hash1, hash2);
    }

    #[test]
    fn test_compute_signature_hash_includes_body() {
        // Same name but different bodies should produce different hashes
        let hash1 = compute_signature_hash("func", "body1");
        let hash2 = compute_signature_hash("func", "body2");
        assert_ne!(hash1, hash2);
    }

    #[test]
    fn test_compute_signature_hash_deterministic() {
        let hash1 = compute_signature_hash("test_fn", "{ return 42; }");
        let hash2 = compute_signature_hash("test_fn", "{ return 42; }");
        assert_eq!(hash1, hash2);
    }
}
