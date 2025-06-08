#!/usr/bin/env python3
"""Version consistency checker script.

This script verifies that all version references in the project are consistent
with the single source of truth in python_template/__init__.py.
"""

import re
import subprocess
import sys
from pathlib import Path


def get_init_version() -> str:
    """Get version from python_template/__init__.py (single source of truth)."""
    init_file = Path("python_template/__init__.py")
    if not init_file.exists():
        raise FileNotFoundError("python_template/__init__.py not found")

    content = init_file.read_text()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        raise ValueError("Version not found in __init__.py")

    return match.group(1)


def get_changelog_version() -> str | None:
    """Get the latest version from CHANGELOG.md."""
    changelog_file = Path("docs/CHANGELOG.md")
    if not changelog_file.exists():
        return None

    content = changelog_file.read_text()
    match = re.search(r"## \[([^\]]+)\]", content)
    return match.group(1) if match else None


def get_latest_git_tag() -> str | None:
    """Get the latest git tag."""
    try:
        result = subprocess.run(
            ["git", "tag", "-l", "--sort=-version:refname"],
            capture_output=True,
            text=True,
            check=True,
        )
        tags = result.stdout.strip().split("\n")
        if tags and tags[0]:
            # Remove 'v' prefix if present
            return tags[0].lstrip("v")
        return None
    except subprocess.CalledProcessError:
        return None


def check_pyproject_dynamic_version() -> bool:
    """Check if pyproject.toml uses dynamic versioning."""
    pyproject_file = Path("pyproject.toml")
    if not pyproject_file.exists():
        return False

    content = pyproject_file.read_text()
    has_dynamic = 'dynamic = ["version"]' in content
    has_hatch_version = "[tool.hatch.version]" in content
    has_path_config = 'path = "python_template/__init__.py"' in content

    return has_dynamic and has_hatch_version and has_path_config


def main():
    """Check version consistency across the project."""
    print("🔍 Checking version consistency...")
    print("=" * 50)

    # Get versions from different sources
    try:
        init_version = get_init_version()
        print(f"📦 __init__.py version: {init_version}")
    except Exception as e:
        print(f"❌ Error reading __init__.py: {e}")
        sys.exit(1)

    changelog_version = get_changelog_version()
    if changelog_version:
        print(f"📋 CHANGELOG.md version: {changelog_version}")
    else:
        print("⚠️  No version found in CHANGELOG.md")

    git_tag_version = get_latest_git_tag()
    if git_tag_version:
        print(f"🏷️  Latest git tag: v{git_tag_version}")
    else:
        print("⚠️  No git tags found")

    # Check pyproject.toml configuration
    if check_pyproject_dynamic_version():
        print("✅ pyproject.toml correctly configured for dynamic versioning")
    else:
        print("❌ pyproject.toml not properly configured for dynamic versioning")

    print("=" * 50)

    # Validate consistency
    errors = []

    if changelog_version and changelog_version != init_version:
        errors.append(
            f"CHANGELOG.md version ({changelog_version}) != "
            f"__init__.py version ({init_version})"
        )

    if git_tag_version and git_tag_version != init_version:
        errors.append(
            f"Latest git tag (v{git_tag_version}) != "
            f"__init__.py version ({init_version})"
        )

    if not check_pyproject_dynamic_version():
        errors.append("pyproject.toml not configured for dynamic versioning")

    if errors:
        print("❌ Version inconsistencies found:")
        for error in errors:
            print(f"   • {error}")
        print("\n💡 Fix: Update versions to match python_template/__init__.py")
        sys.exit(1)
    else:
        print("✅ All versions are consistent!")
        print(f"✅ Single source of truth: {init_version}")


if __name__ == "__main__":
    main()
