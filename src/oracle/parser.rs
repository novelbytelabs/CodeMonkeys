use anyhow::{Context, Result};
use tree_sitter::{Language, Parser, Tree};

pub struct RustParser {
    parser: Parser,
}

impl RustParser {
    pub fn new() -> Result<Self> {
        let mut parser = Parser::new();
        // tree-sitter 0.22+ API: LanguageFn into_raw() -> Language
        let language: Language = tree_sitter_rust::LANGUAGE.into();
        parser
            .set_language(&language)
            .context("Error loading Rust grammar")?;
        Ok(Self { parser })
    }

    pub fn parse(&mut self, code: &str) -> Option<Tree> {
        self.parser.parse(code, None)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parser_creates_successfully() {
        let parser = RustParser::new();
        assert!(parser.is_ok());
    }

    #[test]
    fn test_parse_simple_function() {
        let mut parser = RustParser::new().unwrap();
        let code = "fn main() { println!(\"Hello\"); }";
        let tree = parser.parse(code);
        assert!(tree.is_some());
        let tree = tree.unwrap();
        assert_eq!(tree.root_node().kind(), "source_file");
    }

    #[test]
    fn test_parse_struct() {
        let mut parser = RustParser::new().unwrap();
        let code = "struct Point { x: i32, y: i32 }";
        let tree = parser.parse(code).unwrap();
        let root = tree.root_node();
        assert!(root.child_count() > 0);
    }

    #[test]
    fn test_parse_finds_function_item() {
        let mut parser = RustParser::new().unwrap();
        let code = "fn hello() {}";
        let tree = parser.parse(code).unwrap();
        let root = tree.root_node();
        let child = root.child(0).unwrap();
        assert_eq!(child.kind(), "function_item");
    }

    #[test]
    fn test_parse_empty_returns_some() {
        let mut parser = RustParser::new().unwrap();
        let tree = parser.parse("");
        assert!(tree.is_some()); // Empty is valid source_file
    }
}
