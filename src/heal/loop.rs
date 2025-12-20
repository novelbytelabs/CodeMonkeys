use crate::heal::apply::{apply_fix, restore_backup};
use crate::heal::context::ContextBuilder;
use crate::heal::llm::{LlmClient, OllamaClient};
use crate::heal::parser_rust::TestFailure;
use crate::heal::prompts::PromptTemplates;
use crate::heal::verify::VerificationGate;
use crate::oracle::OracleStore;
use anyhow::Result;
use std::io::Write;
use std::path::PathBuf;
use std::process::Command;
use tempfile::NamedTempFile;

pub struct HealingLoop {
    context_builder: ContextBuilder,
    llm: Box<dyn LlmClient>,
    max_attempts: u32,
    root: PathBuf,
}

#[derive(Debug)]
pub enum HealOutcome {
    Success,
    CompileFailed,
    TestFailed,
    NoFixGenerated,
    MaxAttemptsExceeded,
}

impl HealingLoop {
    /// Create a new HealingLoop with an OllamaClient
    pub fn new(
        store: OracleStore,
        root: PathBuf,
        max_attempts: u32,
        ollama_endpoint: &str,
        ollama_model: &str,
    ) -> Result<Self> {
        let context_builder = ContextBuilder::new(store, root.clone());
        let llm = Box::new(OllamaClient::new(ollama_endpoint, ollama_model));

        Ok(Self {
            context_builder,
            llm,
            max_attempts,
            root,
        })
    }

    /// Create with default localhost Ollama
    pub fn with_default_ollama(
        store: OracleStore,
        root: PathBuf,
        max_attempts: u32,
        model: &str,
    ) -> Result<Self> {
        Self::new(store, root, max_attempts, "http://localhost:11434", model)
    }

    pub fn run(&mut self, failure: &TestFailure) -> Result<HealOutcome> {
        for attempt in 0..self.max_attempts {
            println!("Healing attempt {}/{}", attempt + 1, self.max_attempts);

            // 1. Build context
            let ctx = self.context_builder.build_context(failure)?;

            // 2. Generate prompt
            let prompt = if failure.file_path.ends_with(".rs") {
                PromptTemplates::rust_repair(&ctx)
            } else {
                PromptTemplates::python_repair(&ctx)
            };

            println!("Sending prompt to LLM ({} chars)...", prompt.len());

            // 3. Generate fix from LLM
            let fix = self.llm.generate_fix(&prompt)?;
            if fix.is_empty() {
                println!("LLM generated no fix");
                return Ok(HealOutcome::NoFixGenerated);
            }

            println!("Received fix ({} chars)", fix.len());

            // 4. Preview Diff and Apply fix
            let file_path = self.root.join(&failure.file_path);
            self.show_diff(&file_path, &fix)?;

            apply_fix(&file_path, &fix)?;

            // 5. Verify
            let gate = VerificationGate::new(self.root.clone());
            if gate.check_compile()? && gate.check_lint()? && gate.check_tests()? {
                return Ok(HealOutcome::Success);
            }

            println!("Verification failed, rolling back...");
            restore_backup(&file_path)?;
        }

        Ok(HealOutcome::MaxAttemptsExceeded)
    }

    fn show_diff(&self, file_path: &PathBuf, new_content: &str) -> Result<()> {
        // Write new content to a temp file to diff it
        let mut temp_file = NamedTempFile::new()?;
        write!(temp_file, "{}", new_content)?;

        println!("\n--- Proposed Changes ---");
        let output = Command::new("diff")
            .arg("-u")
            .arg("--color=always")
            .arg(file_path)
            .arg(temp_file.path())
            .output();

        if let Ok(out) = output {
            // diff returns exit code 1 if differences found, which is what we expect
            if !out.stdout.is_empty() {
                println!("{}", String::from_utf8_lossy(&out.stdout));
            } else {
                println!("No changes detected.");
            }
        } else {
            // Fallback if diff command missing
            println!("(diff command not available)");
        }
        println!("------------------------\n");
        Ok(())
    }
}
