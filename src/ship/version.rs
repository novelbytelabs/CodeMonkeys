use crate::ship::commits::Commit;
use anyhow::Result;
use std::fmt;

#[derive(Debug, Clone)]
pub struct SemVer {
    pub major: u32,
    pub minor: u32,
    pub patch: u32,
}

impl SemVer {
    pub fn parse(version_str: &str) -> Result<Self> {
        let clean = version_str.trim_start_matches('v');
        let parts: Vec<&str> = clean.split('.').collect();

        let major = parts.first().and_then(|s| s.parse().ok()).unwrap_or(0);
        let minor = parts.get(1).and_then(|s| s.parse().ok()).unwrap_or(0);
        let patch = parts.get(2).and_then(|s| s.parse().ok()).unwrap_or(0);

        Ok(Self {
            major,
            minor,
            patch,
        })
    }

    pub fn bump_major(&self) -> Self {
        Self {
            major: self.major + 1,
            minor: 0,
            patch: 0,
        }
    }

    pub fn bump_minor(&self) -> Self {
        Self {
            major: self.major,
            minor: self.minor + 1,
            patch: 0,
        }
    }

    pub fn bump_patch(&self) -> Self {
        Self {
            major: self.major,
            minor: self.minor,
            patch: self.patch + 1,
        }
    }
}

impl fmt::Display for SemVer {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}.{}.{}", self.major, self.minor, self.patch)
    }
}

/// Calculate next version based on conventional commits
pub fn calculate_next_version(current: &SemVer, commits: &[Commit]) -> SemVer {
    let has_breaking = commits.iter().any(|c| c.is_breaking);
    let has_feat = commits.iter().any(|c| c.commit_type == "feat");

    if has_breaking {
        current.bump_major()
    } else if has_feat {
        current.bump_minor()
    } else {
        current.bump_patch()
    }
}

/// Generate changelog from commits
pub fn generate_changelog(version: &SemVer, commits: &[Commit]) -> String {
    let mut changelog = format!("## v{}\n\n", version);

    // Group by type
    let features: Vec<_> = commits.iter().filter(|c| c.commit_type == "feat").collect();
    let fixes: Vec<_> = commits.iter().filter(|c| c.commit_type == "fix").collect();
    let others: Vec<_> = commits
        .iter()
        .filter(|c| c.commit_type != "feat" && c.commit_type != "fix")
        .collect();

    if !features.is_empty() {
        changelog.push_str("### Features\n\n");
        for commit in features {
            changelog.push_str(&format!("- {}\n", commit.description));
        }
        changelog.push('\n');
    }

    if !fixes.is_empty() {
        changelog.push_str("### Bug Fixes\n\n");
        for commit in fixes {
            changelog.push_str(&format!("- {}\n", commit.description));
        }
        changelog.push('\n');
    }

    if !others.is_empty() {
        changelog.push_str("### Other Changes\n\n");
        for commit in others {
            changelog.push_str(&format!("- {}\n", commit.description));
        }
        changelog.push('\n');
    }

    changelog
}

#[cfg(test)]
mod tests {
    use super::*;

    fn make_commit(commit_type: &str, description: &str, is_breaking: bool) -> Commit {
        Commit {
            hash: "abc123".to_string(),
            commit_type: commit_type.to_string(),
            scope: None,
            description: description.to_string(),
            is_breaking,
        }
    }

    #[test]
    fn test_semver_parse_full() {
        let v = SemVer::parse("1.2.3").unwrap();
        assert_eq!(v.major, 1);
        assert_eq!(v.minor, 2);
        assert_eq!(v.patch, 3);
    }

    #[test]
    fn test_semver_parse_with_v_prefix() {
        let v = SemVer::parse("v2.0.1").unwrap();
        assert_eq!(v.major, 2);
        assert_eq!(v.minor, 0);
        assert_eq!(v.patch, 1);
    }

    #[test]
    fn test_semver_parse_partial() {
        let v = SemVer::parse("1.2").unwrap();
        assert_eq!(v.major, 1);
        assert_eq!(v.minor, 2);
        assert_eq!(v.patch, 0);
    }

    #[test]
    fn test_semver_display() {
        let v = SemVer {
            major: 3,
            minor: 2,
            patch: 1,
        };
        assert_eq!(format!("{}", v), "3.2.1");
    }

    #[test]
    fn test_bump_major() {
        let v = SemVer {
            major: 1,
            minor: 2,
            patch: 3,
        };
        let bumped = v.bump_major();
        assert_eq!(bumped.major, 2);
        assert_eq!(bumped.minor, 0);
        assert_eq!(bumped.patch, 0);
    }

    #[test]
    fn test_bump_minor() {
        let v = SemVer {
            major: 1,
            minor: 2,
            patch: 3,
        };
        let bumped = v.bump_minor();
        assert_eq!(bumped.major, 1);
        assert_eq!(bumped.minor, 3);
        assert_eq!(bumped.patch, 0);
    }

    #[test]
    fn test_bump_patch() {
        let v = SemVer {
            major: 1,
            minor: 2,
            patch: 3,
        };
        let bumped = v.bump_patch();
        assert_eq!(bumped.major, 1);
        assert_eq!(bumped.minor, 2);
        assert_eq!(bumped.patch, 4);
    }

    #[test]
    fn test_calculate_next_version_breaking() {
        let current = SemVer {
            major: 1,
            minor: 0,
            patch: 0,
        };
        let commits = vec![
            make_commit("feat", "new feature", true), // breaking!
        ];
        let next = calculate_next_version(&current, &commits);
        assert_eq!(next.major, 2);
        assert_eq!(next.minor, 0);
    }

    #[test]
    fn test_calculate_next_version_feature() {
        let current = SemVer {
            major: 1,
            minor: 0,
            patch: 0,
        };
        let commits = vec![make_commit("feat", "new feature", false)];
        let next = calculate_next_version(&current, &commits);
        assert_eq!(next.major, 1);
        assert_eq!(next.minor, 1);
    }

    #[test]
    fn test_calculate_next_version_fix() {
        let current = SemVer {
            major: 1,
            minor: 0,
            patch: 0,
        };
        let commits = vec![make_commit("fix", "bug fix", false)];
        let next = calculate_next_version(&current, &commits);
        assert_eq!(next.major, 1);
        assert_eq!(next.minor, 0);
        assert_eq!(next.patch, 1);
    }

    #[test]
    fn test_generate_changelog_has_version() {
        let v = SemVer {
            major: 1,
            minor: 0,
            patch: 0,
        };
        let commits = vec![make_commit("feat", "Add new API", false)];
        let changelog = generate_changelog(&v, &commits);
        assert!(changelog.contains("## v1.0.0"));
        assert!(changelog.contains("### Features"));
        assert!(changelog.contains("Add new API"));
    }
}
