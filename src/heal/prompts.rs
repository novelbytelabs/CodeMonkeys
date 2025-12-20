use crate::heal::context::HealContext;

pub struct PromptTemplates;

impl PromptTemplates {
    /// Generate a repair prompt for Rust code
    pub fn rust_repair(ctx: &HealContext) -> String {
        let related = if ctx.related_signatures.is_empty() {
            "None".to_string()
        } else {
            ctx.related_signatures.join("\n")
        };

        format!(
            r#"You are an expert Rust developer tasked with fixing a compilation error or test failure.
Your goal is to provide ONLY the corrected code block that fixes the issue.

CONTEXT:
File: {}
Line: {}
Error Message:
{}

RELATED CODE:
{}

SOURCE CODE:
```rust
{}
```

INSTRUCTIONS:
1. Analyze the error message, related code, and the source code.
2. Determine the necessary changes to fix the error.
3. Provide the COMPLETE corrected code block.
4. DO NOT include any explanations, markdown headers, or conversational text.
5. ONLY output the code block enclosed in ```rust and ``` logic.

RESPONSE:
```rust
"#,
            ctx.failure.file_path,
            ctx.failure
                .line
                .map(|l| l.to_string())
                .unwrap_or_else(|| "unknown".to_string()),
            ctx.failure.error_message,
            related,
            ctx.source_snippet
        )
    }

    /// Generate a repair prompt for Python code
    pub fn python_repair(ctx: &HealContext) -> String {
        let related = if ctx.related_signatures.is_empty() {
            "None".to_string()
        } else {
            ctx.related_signatures.join("\n")
        };

        format!(
            r#"You are an expert Python developer tasked with fixing a test failure.
Your goal is to provide ONLY the corrected code block that fixes the issue.

CONTEXT:
File: {}
Test Name: {}
Error Message:
{}

RELATED CODE:
{}

SOURCE CODE:
```python
{}
```

INSTRUCTIONS:
1. Analyze the error message, related code, and the source code.
2. Determine the necessary changes to fix the error.
3. Provide the COMPLETE corrected code block.
4. DO NOT include any explanations, markdown headers, or conversational text.
5. ONLY output the code block enclosed in ```python and ``` logic.

RESPONSE:
```python
"#,
            ctx.failure.file_path,
            ctx.failure.test_name,
            ctx.failure.error_message,
            related,
            ctx.source_snippet
        )
    }
}
