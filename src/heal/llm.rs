use anyhow::{Context, Result};
use serde::{Deserialize, Serialize};

/// Trait for LLM clients used in healing
pub trait LlmClient: Send {
    fn generate_fix(&mut self, prompt: &str) -> Result<String>;
}

/// Ollama-based LLM client
pub struct OllamaClient {
    endpoint: String,
    model: String,
    client: reqwest::blocking::Client,
}

#[derive(Serialize)]
struct OllamaRequest<'a> {
    model: &'a str,
    prompt: &'a str,
    stream: bool,
}

#[derive(Deserialize)]
struct OllamaResponse {
    response: String,
}

impl OllamaClient {
    pub fn new(endpoint: &str, model: &str) -> Self {
        Self {
            endpoint: endpoint.to_string(),
            model: model.to_string(),
            client: reqwest::blocking::Client::builder()
                .timeout(std::time::Duration::from_secs(120))
                .build()
                .expect("Failed to create HTTP client"),
        }
    }

    /// Default constructor using localhost Ollama
    pub fn default_local(model: &str) -> Self {
        Self::new("http://localhost:11434", model)
    }
}

impl LlmClient for OllamaClient {
    fn generate_fix(&mut self, prompt: &str) -> Result<String> {
        let url = format!("{}/api/generate", self.endpoint);

        let request = OllamaRequest {
            model: &self.model,
            prompt,
            stream: false,
        };

        let response = self
            .client
            .post(&url)
            .json(&request)
            .send()
            .context("Failed to send request to Ollama")?;

        if !response.status().is_success() {
            anyhow::bail!("Ollama returned error status: {}", response.status());
        }

        let ollama_resp: OllamaResponse =
            response.json().context("Failed to parse Ollama response")?;

        // Extract code from response (look for code fences)
        let code = extract_code_block(&ollama_resp.response);
        Ok(code)
    }
}

/// Extract code from markdown code fences if present
fn extract_code_block(response: &str) -> String {
    // Look for ```rust or ```python blocks
    if let Some(start) = response.find("```") {
        let after_fence = &response[start + 3..];
        // Skip the language identifier line
        if let Some(newline) = after_fence.find('\n') {
            let code_start = &after_fence[newline + 1..];
            if let Some(end) = code_start.find("```") {
                return code_start[..end].trim().to_string();
            }
        }
    }
    // No code fence found, return raw response
    response.trim().to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_extract_code_block_rust() {
        let response = r#"Here's the fix:

```rust
fn main() {
    println!("Hello");
}
```

This should work."#;

        let code = extract_code_block(response);
        assert_eq!(code, "fn main() {\n    println!(\"Hello\");\n}");
    }

    #[test]
    fn test_extract_code_block_no_fence() {
        let response = "fn main() { println!(\"Hello\"); }";
        let code = extract_code_block(response);
        assert_eq!(code, "fn main() { println!(\"Hello\"); }");
    }
}
