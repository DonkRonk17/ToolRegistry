#!/usr/bin/env python3
"""
ToolRegistry - Unified Tool Discovery and Management for Team Brain

The command center for Team Brain's 35+ tools ecosystem. Catalog, discover, search,
and launch any tool instantly. Know what exists, what it does, and how to use it.

When Team Brain has dozens of tools, finding the right one becomes challenging.
ToolRegistry solves this by providing a unified catalog with:
- Automatic tool discovery (scans AutoProjects)
- Rich metadata extraction (README parsing, capability detection)
- Powerful search (by name, purpose, tags, capabilities)
- Quick launch (CLI or Python API)
- Ecosystem health monitoring (coverage, documentation quality)
- Usage tracking and recommendations

Author: Forge (Team Brain - Cursor)
Created: January 19, 2026
Version: 1.0.0
License: MIT
For: Logan Smith / Metaphy LLC
Q-Mode: Tool Registry (Tier 4: Integration & Control)
"""

import os
import sys
import json
import sqlite3
import hashlib
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
from collections import defaultdict
import re

# ============== CONSTANTS ==============
VERSION = "1.0.0"
DEFAULT_CONFIG_PATH = Path.home() / ".toolregistryrc"
DEFAULT_DB_PATH = Path.home() / ".toolregistry" / "registry.db"
DEFAULT_SCAN_PATHS = [
    Path.home() / "OneDrive" / "Documents" / "AutoProjects"
]

# Tool categories for classification
TOOL_CATEGORIES = {
    "synapse": ["synapse", "message", "communication", "inbox", "notification"],
    "monitoring": ["health", "watch", "monitor", "tracker", "stats", "analytics"],
    "task": ["task", "queue", "todo", "flow", "schedule", "assign"],
    "memory": ["memory", "bridge", "context", "compress", "cache"],
    "config": ["config", "setting", "env", "environment"],
    "session": ["session", "replay", "record", "collab"],
    "security": ["secure", "vault", "encrypt", "password", "auth"],
    "file": ["file", "backup", "rename", "deduplicate", "clip"],
    "network": ["net", "port", "scan", "ssh", "rest", "api"],
    "dev": ["git", "regex", "log", "data", "convert", "json"],
    "productivity": ["time", "focus", "notes", "window", "screen"],
    "routing": ["router", "route", "dispatch", "assign"]
}

# ============== CLASSES ==============

class ToolMetadata:
    """Represents metadata for a single tool."""
    
    def __init__(
        self,
        name: str,
        path: Path,
        description: str = "",
        version: str = "unknown",
        author: str = "Team Brain",
        categories: List[str] = None,
        capabilities: List[str] = None,
        cli_commands: List[str] = None,
        python_api: str = "",
        dependencies: List[str] = None,
        github_url: str = "",
        has_tests: bool = False,
        has_readme: bool = False,
        has_examples: bool = False,
        has_branding: bool = False,
        readme_lines: int = 0,
        test_count: int = 0,
        last_modified: datetime = None,
        quality_score: int = 0
    ):
        self.name = name
        self.path = path
        self.description = description
        self.version = version
        self.author = author
        self.categories = categories or []
        self.capabilities = capabilities or []
        self.cli_commands = cli_commands or []
        self.python_api = python_api
        self.dependencies = dependencies or []
        self.github_url = github_url
        self.has_tests = has_tests
        self.has_readme = has_readme
        self.has_examples = has_examples
        self.has_branding = has_branding
        self.readme_lines = readme_lines
        self.test_count = test_count
        self.last_modified = last_modified or datetime.now()
        self.quality_score = quality_score
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "path": str(self.path),
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "categories": self.categories,
            "capabilities": self.capabilities,
            "cli_commands": self.cli_commands,
            "python_api": self.python_api,
            "dependencies": self.dependencies,
            "github_url": self.github_url,
            "has_tests": self.has_tests,
            "has_readme": self.has_readme,
            "has_examples": self.has_examples,
            "has_branding": self.has_branding,
            "readme_lines": self.readme_lines,
            "test_count": self.test_count,
            "last_modified": self.last_modified.isoformat(),
            "quality_score": self.quality_score
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ToolMetadata':
        """Create from dictionary."""
        data["path"] = Path(data["path"])
        data["last_modified"] = datetime.fromisoformat(data["last_modified"])
        return cls(**data)


class ToolRegistry:
    """
    Unified tool discovery and management system for Team Brain.
    
    Provides:
    - Automatic tool discovery (scans directories)
    - Rich metadata extraction from READMEs
    - Powerful search capabilities
    - Launch tools (CLI or Python)
    - Ecosystem health monitoring
    - Usage tracking
    
    Example:
        >>> registry = ToolRegistry()
        >>> registry.scan()  # Discover all tools
        >>> tools = registry.search("synapse")  # Find Synapse tools
        >>> registry.launch("SynapseLink", ["send", "--to", "FORGE"])
    """
    
    def __init__(
        self,
        config_path: Optional[Path] = None,
        db_path: Optional[Path] = None,
        scan_paths: Optional[List[Path]] = None
    ):
        """
        Initialize ToolRegistry.
        
        Args:
            config_path: Path to config file (default: ~/.toolregistryrc)
            db_path: Path to SQLite database (default: ~/.toolregistry/registry.db)
            scan_paths: List of paths to scan for tools
        """
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self.db_path = db_path or DEFAULT_DB_PATH
        self.scan_paths = scan_paths or DEFAULT_SCAN_PATHS
        
        # Ensure directories exist
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load config
        self.config = self._load_config()
        
        # Initialize database
        self._init_db()
        
        # In-memory tool cache
        self._tools: Dict[str, ToolMetadata] = {}
        self._load_tools_from_db()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            "version": VERSION,
            "scan_paths": [str(p) for p in DEFAULT_SCAN_PATHS],
            "auto_scan_on_startup": False,
            "track_usage": True,
            "github_base_url": "https://github.com/DonkRonk17"
        }
    
    def save_config(self) -> None:
        """Save configuration to file."""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)
    
    def _init_db(self) -> None:
        """Initialize SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tools table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tools (
                name TEXT PRIMARY KEY,
                path TEXT NOT NULL,
                description TEXT,
                version TEXT,
                author TEXT,
                categories TEXT,
                capabilities TEXT,
                cli_commands TEXT,
                python_api TEXT,
                dependencies TEXT,
                github_url TEXT,
                has_tests INTEGER,
                has_readme INTEGER,
                has_examples INTEGER,
                has_branding INTEGER,
                readme_lines INTEGER,
                test_count INTEGER,
                last_modified TEXT,
                quality_score INTEGER,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        # Usage tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_name TEXT NOT NULL,
                action TEXT,
                agent TEXT,
                timestamp TEXT,
                success INTEGER,
                notes TEXT,
                FOREIGN KEY (tool_name) REFERENCES tools(name)
            )
        ''')
        
        # Tags table for flexible categorization
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_name TEXT NOT NULL,
                tag TEXT NOT NULL,
                UNIQUE(tool_name, tag),
                FOREIGN KEY (tool_name) REFERENCES tools(name)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_tools_from_db(self) -> None:
        """Load tools from database into memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tools')
        rows = cursor.fetchall()
        
        for row in rows:
            try:
                tool = ToolMetadata(
                    name=row[0],
                    path=Path(row[1]),
                    description=row[2] or "",
                    version=row[3] or "unknown",
                    author=row[4] or "Team Brain",
                    categories=json.loads(row[5]) if row[5] else [],
                    capabilities=json.loads(row[6]) if row[6] else [],
                    cli_commands=json.loads(row[7]) if row[7] else [],
                    python_api=row[8] or "",
                    dependencies=json.loads(row[9]) if row[9] else [],
                    github_url=row[10] or "",
                    has_tests=bool(row[11]),
                    has_readme=bool(row[12]),
                    has_examples=bool(row[13]),
                    has_branding=bool(row[14]),
                    readme_lines=row[15] or 0,
                    test_count=row[16] or 0,
                    last_modified=datetime.fromisoformat(row[17]) if row[17] else datetime.now(),
                    quality_score=row[18] or 0
                )
                self._tools[tool.name] = tool
            except Exception:
                continue
        
        conn.close()
    
    def _save_tool_to_db(self, tool: ToolMetadata) -> None:
        """Save a tool to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT OR REPLACE INTO tools (
                name, path, description, version, author, categories, capabilities,
                cli_commands, python_api, dependencies, github_url, has_tests,
                has_readme, has_examples, has_branding, readme_lines, test_count,
                last_modified, quality_score, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            tool.name,
            str(tool.path),
            tool.description,
            tool.version,
            tool.author,
            json.dumps(tool.categories),
            json.dumps(tool.capabilities),
            json.dumps(tool.cli_commands),
            tool.python_api,
            json.dumps(tool.dependencies),
            tool.github_url,
            int(tool.has_tests),
            int(tool.has_readme),
            int(tool.has_examples),
            int(tool.has_branding),
            tool.readme_lines,
            tool.test_count,
            tool.last_modified.isoformat(),
            tool.quality_score,
            now,
            now
        ))
        
        # Save tags
        for category in tool.categories:
            cursor.execute('''
                INSERT OR IGNORE INTO tags (tool_name, tag) VALUES (?, ?)
            ''', (tool.name, category))
        
        conn.commit()
        conn.close()
    
    def scan(self, paths: Optional[List[Path]] = None) -> int:
        """
        Scan directories for tools and extract metadata.
        
        Args:
            paths: List of paths to scan (default: configured scan_paths)
            
        Returns:
            Number of tools discovered
        """
        scan_paths = paths or self.scan_paths
        discovered = 0
        
        for base_path in scan_paths:
            base_path = Path(base_path)
            if not base_path.exists():
                continue
            
            # Scan for tool directories
            for item in base_path.iterdir():
                if not item.is_dir():
                    continue
                
                # Skip common non-tool directories
                if item.name.startswith('.') or item.name.startswith('_'):
                    continue
                if item.name in ['branding', 'backups', 'tests', 'examples', '__pycache__']:
                    continue
                
                # Check if it's a tool (has .py file with same name or main script)
                tool_script = self._find_tool_script(item)
                if tool_script:
                    metadata = self._extract_metadata(item, tool_script)
                    if metadata:
                        self._tools[metadata.name] = metadata
                        self._save_tool_to_db(metadata)
                        discovered += 1
        
        return discovered
    
    def _find_tool_script(self, tool_dir: Path) -> Optional[Path]:
        """Find the main Python script for a tool."""
        tool_name_lower = tool_dir.name.lower()
        
        # Check for script with same name as folder
        candidates = [
            tool_dir / f"{tool_name_lower}.py",
            tool_dir / f"{tool_dir.name}.py",
            tool_dir / "main.py",
            tool_dir / "__main__.py"
        ]
        
        for candidate in candidates:
            if candidate.exists():
                return candidate
        
        # Check for any .py file (excluding test files)
        py_files = [f for f in tool_dir.glob("*.py") 
                    if not f.name.startswith("test_") and f.name != "__init__.py"]
        
        if py_files:
            return py_files[0]
        
        return None
    
    def _extract_metadata(self, tool_dir: Path, script_path: Path) -> Optional[ToolMetadata]:
        """Extract metadata from a tool directory."""
        try:
            name = tool_dir.name
            
            # Read script for docstring and version
            description = ""
            version = "1.0.0"
            author = "Team Brain"
            
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Extract docstring
                    docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
                    if docstring_match:
                        docstring = docstring_match.group(1).strip()
                        # First non-empty line is description
                        for line in docstring.split('\n'):
                            line = line.strip()
                            if line and not line.startswith('Author') and not line.startswith('Created'):
                                description = line
                                break
                    
                    # Extract version
                    version_match = re.search(r'VERSION\s*=\s*["\']([^"\']+)["\']', content)
                    if version_match:
                        version = version_match.group(1)
                    
                    # Extract author
                    author_match = re.search(r'Author:\s*(.+)', content)
                    if author_match:
                        author = author_match.group(1).strip()
            except (IOError, UnicodeDecodeError):
                pass
            
            # Check for README
            readme_path = tool_dir / "README.md"
            has_readme = readme_path.exists()
            readme_lines = 0
            readme_description = ""
            github_url = ""
            
            if has_readme:
                try:
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        readme_content = f.read()
                        readme_lines = len(readme_content.split('\n'))
                        
                        # Extract description from README
                        lines = readme_content.split('\n')
                        for line in lines[1:10]:  # Skip title, check first few lines
                            line = line.strip()
                            if line and not line.startswith('#') and not line.startswith('!'):
                                if not description:
                                    description = line.rstrip('*').strip()
                                break
                        
                        # Extract GitHub URL
                        github_match = re.search(r'https://github\.com/DonkRonk17/\S+', readme_content)
                        if github_match:
                            github_url = github_match.group(0).rstrip(')')
                except (IOError, UnicodeDecodeError):
                    pass
            
            # Check for tests
            test_files = list(tool_dir.glob("test_*.py"))
            has_tests = len(test_files) > 0
            test_count = 0
            
            if has_tests:
                for test_file in test_files:
                    try:
                        with open(test_file, 'r', encoding='utf-8') as f:
                            test_content = f.read()
                            test_count += len(re.findall(r'def test_', test_content))
                    except (IOError, UnicodeDecodeError):
                        pass
            
            # Check for examples
            has_examples = (tool_dir / "EXAMPLES.md").exists()
            
            # Check for branding
            branding_dir = tool_dir / "branding"
            has_branding = branding_dir.exists() and any(branding_dir.iterdir()) if branding_dir.exists() else False
            
            # Detect categories
            categories = self._detect_categories(name, description)
            
            # Detect capabilities
            capabilities = self._detect_capabilities(tool_dir, script_path)
            
            # Detect CLI commands
            cli_commands = self._detect_cli_commands(script_path)
            
            # Generate Python API
            python_api = f"from {name.lower()} import {name}"
            
            # Check dependencies
            dependencies = []
            req_path = tool_dir / "requirements.txt"
            if req_path.exists():
                try:
                    with open(req_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                dependencies.append(line)
                except (IOError, UnicodeDecodeError):
                    pass
            
            # Get last modified time
            try:
                last_modified = datetime.fromtimestamp(script_path.stat().st_mtime)
            except OSError:
                last_modified = datetime.now()
            
            # Calculate quality score
            quality_score = self._calculate_quality_score(
                has_readme, readme_lines, has_tests, test_count,
                has_examples, has_branding, bool(description)
            )
            
            return ToolMetadata(
                name=name,
                path=tool_dir,
                description=description,
                version=version,
                author=author,
                categories=categories,
                capabilities=capabilities,
                cli_commands=cli_commands,
                python_api=python_api,
                dependencies=dependencies,
                github_url=github_url or f"https://github.com/DonkRonk17/{name}",
                has_tests=has_tests,
                has_readme=has_readme,
                has_examples=has_examples,
                has_branding=has_branding,
                readme_lines=readme_lines,
                test_count=test_count,
                last_modified=last_modified,
                quality_score=quality_score
            )
        except Exception:
            return None
    
    def _detect_categories(self, name: str, description: str) -> List[str]:
        """Detect tool categories based on name and description."""
        categories = []
        text = (name + " " + description).lower()
        
        for category, keywords in TOOL_CATEGORIES.items():
            for keyword in keywords:
                if keyword in text:
                    if category not in categories:
                        categories.append(category)
                    break
        
        if not categories:
            categories = ["utility"]
        
        return categories
    
    def _detect_capabilities(self, tool_dir: Path, script_path: Path) -> List[str]:
        """Detect tool capabilities."""
        capabilities = []
        
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                
                # Check for common capabilities
                if 'argparse' in content or 'cli' in content:
                    capabilities.append("CLI interface")
                if 'class ' in content:
                    capabilities.append("Python API")
                if 'sqlite' in content or 'database' in content:
                    capabilities.append("Persistent storage")
                if 'json' in content:
                    capabilities.append("JSON support")
                if 'async' in content or 'asyncio' in content:
                    capabilities.append("Async operations")
                if 'subprocess' in content:
                    capabilities.append("Process execution")
                if 'pathlib' in content or 'os.path' in content:
                    capabilities.append("File operations")
                if 'socket' in content or 'http' in content:
                    capabilities.append("Network operations")
        except (IOError, UnicodeDecodeError):
            pass
        
        return capabilities
    
    def _detect_cli_commands(self, script_path: Path) -> List[str]:
        """Detect CLI commands from script."""
        commands = []
        
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Look for subparser commands
                subparser_matches = re.findall(
                    r"add_parser\(['\"](\w+)['\"]",
                    content
                )
                commands.extend(subparser_matches)
                
                # Look for command choices
                choices_matches = re.findall(
                    r"choices\s*=\s*\[([^\]]+)\]",
                    content
                )
                for match in choices_matches:
                    for cmd in re.findall(r"['\"](\w+)['\"]", match):
                        if cmd not in commands:
                            commands.append(cmd)
        except (IOError, UnicodeDecodeError):
            pass
        
        return commands
    
    def _calculate_quality_score(
        self,
        has_readme: bool,
        readme_lines: int,
        has_tests: bool,
        test_count: int,
        has_examples: bool,
        has_branding: bool,
        has_description: bool
    ) -> int:
        """Calculate tool quality score (0-100)."""
        score = 0
        
        # README (30 points)
        if has_readme:
            score += 10
            if readme_lines >= 100:
                score += 5
            if readme_lines >= 200:
                score += 5
            if readme_lines >= 400:
                score += 10
        
        # Tests (25 points)
        if has_tests:
            score += 10
            if test_count >= 5:
                score += 5
            if test_count >= 10:
                score += 5
            if test_count >= 15:
                score += 5
        
        # Examples (15 points)
        if has_examples:
            score += 15
        
        # Branding (10 points)
        if has_branding:
            score += 10
        
        # Description (10 points)
        if has_description:
            score += 10
        
        # Code quality indicators (10 points)
        score += 10  # Base points for being a valid tool
        
        return min(score, 100)
    
    def get(self, name: str) -> Optional[ToolMetadata]:
        """
        Get a tool by name.
        
        Args:
            name: Tool name (case-insensitive)
            
        Returns:
            ToolMetadata or None if not found
        """
        # Exact match first
        if name in self._tools:
            return self._tools[name]
        
        # Case-insensitive match
        name_lower = name.lower()
        for tool_name, tool in self._tools.items():
            if tool_name.lower() == name_lower:
                return tool
        
        return None
    
    def list_all(self) -> List[ToolMetadata]:
        """Get all registered tools."""
        return list(self._tools.values())
    
    def search(
        self,
        query: str,
        category: Optional[str] = None,
        min_quality: int = 0
    ) -> List[ToolMetadata]:
        """
        Search for tools.
        
        Args:
            query: Search query (matches name, description, capabilities)
            category: Filter by category
            min_quality: Minimum quality score (0-100)
            
        Returns:
            List of matching tools, sorted by relevance
        """
        query_lower = query.lower()
        results = []
        
        for tool in self._tools.values():
            # Skip if below quality threshold
            if tool.quality_score < min_quality:
                continue
            
            # Filter by category
            if category and category not in tool.categories:
                continue
            
            # Calculate relevance score
            relevance = 0
            
            # Name match (highest priority)
            if query_lower in tool.name.lower():
                relevance += 100
                if tool.name.lower().startswith(query_lower):
                    relevance += 50
            
            # Description match
            if query_lower in tool.description.lower():
                relevance += 30
            
            # Category match
            for cat in tool.categories:
                if query_lower in cat.lower():
                    relevance += 20
                    break
            
            # Capability match
            for cap in tool.capabilities:
                if query_lower in cap.lower():
                    relevance += 10
                    break
            
            if relevance > 0:
                results.append((tool, relevance))
        
        # Sort by relevance
        results.sort(key=lambda x: x[1], reverse=True)
        
        return [tool for tool, _ in results]
    
    def by_category(self, category: str) -> List[ToolMetadata]:
        """Get all tools in a category."""
        return [t for t in self._tools.values() if category in t.categories]
    
    def categories(self) -> Dict[str, int]:
        """Get all categories with tool counts."""
        counts = defaultdict(int)
        for tool in self._tools.values():
            for cat in tool.categories:
                counts[cat] += 1
        return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
    
    def launch(
        self,
        name: str,
        args: Optional[List[str]] = None,
        capture_output: bool = False
    ) -> Tuple[int, str, str]:
        """
        Launch a tool with arguments.
        
        Args:
            name: Tool name
            args: Command-line arguments
            capture_output: Whether to capture stdout/stderr
            
        Returns:
            Tuple of (return_code, stdout, stderr)
        """
        tool = self.get(name)
        if not tool:
            return (1, "", f"Tool not found: {name}")
        
        # Find the main script
        script_path = self._find_tool_script(tool.path)
        if not script_path:
            return (1, "", f"No script found for tool: {name}")
        
        # Build command
        cmd = [sys.executable, str(script_path)]
        if args:
            cmd.extend(args)
        
        try:
            if capture_output:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    cwd=str(tool.path)
                )
                stdout = result.stdout
                stderr = result.stderr
                returncode = result.returncode
            else:
                result = subprocess.run(cmd, cwd=str(tool.path))
                stdout = ""
                stderr = ""
                returncode = result.returncode
            
            # Track usage
            self._track_usage(name, "launch", success=returncode == 0)
            
            return (returncode, stdout, stderr)
        except Exception as e:
            self._track_usage(name, "launch", success=False, notes=str(e))
            return (1, "", str(e))
    
    def _track_usage(
        self,
        tool_name: str,
        action: str,
        agent: str = "unknown",
        success: bool = True,
        notes: str = ""
    ) -> None:
        """Track tool usage."""
        if not self.config.get("track_usage", True):
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO usage (tool_name, action, agent, timestamp, success, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            tool_name,
            action,
            agent,
            datetime.now().isoformat(),
            int(success),
            notes
        ))
        
        conn.commit()
        conn.close()
    
    def get_usage_stats(self, tool_name: Optional[str] = None) -> Dict[str, Any]:
        """Get usage statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if tool_name:
            cursor.execute('''
                SELECT COUNT(*), SUM(success) FROM usage WHERE tool_name = ?
            ''', (tool_name,))
        else:
            cursor.execute('SELECT COUNT(*), SUM(success) FROM usage')
        
        row = cursor.fetchone()
        total = row[0] or 0
        successful = row[1] or 0
        
        # Get top tools
        cursor.execute('''
            SELECT tool_name, COUNT(*) as count
            FROM usage GROUP BY tool_name
            ORDER BY count DESC LIMIT 10
        ''')
        top_tools = [(row[0], row[1]) for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            "total_uses": total,
            "successful": successful,
            "success_rate": (successful / total * 100) if total > 0 else 0,
            "top_tools": top_tools
        }
    
    def ecosystem_health(self) -> Dict[str, Any]:
        """Generate ecosystem health report."""
        tools = self.list_all()
        
        if not tools:
            return {
                "total_tools": 0,
                "status": "No tools discovered"
            }
        
        total = len(tools)
        with_readme = sum(1 for t in tools if t.has_readme)
        with_tests = sum(1 for t in tools if t.has_tests)
        with_examples = sum(1 for t in tools if t.has_examples)
        with_branding = sum(1 for t in tools if t.has_branding)
        
        avg_quality = sum(t.quality_score for t in tools) / total
        avg_readme_lines = sum(t.readme_lines for t in tools) / total
        avg_tests = sum(t.test_count for t in tools) / total
        
        high_quality = [t for t in tools if t.quality_score >= 80]
        needs_work = [t for t in tools if t.quality_score < 50]
        
        categories = self.categories()
        
        return {
            "total_tools": total,
            "documentation_coverage": f"{with_readme / total * 100:.1f}%",
            "test_coverage": f"{with_tests / total * 100:.1f}%",
            "examples_coverage": f"{with_examples / total * 100:.1f}%",
            "branding_coverage": f"{with_branding / total * 100:.1f}%",
            "average_quality_score": f"{avg_quality:.1f}/100",
            "average_readme_lines": f"{avg_readme_lines:.0f}",
            "average_test_count": f"{avg_tests:.1f}",
            "high_quality_tools": len(high_quality),
            "needs_improvement": len(needs_work),
            "categories": categories,
            "top_quality": sorted(tools, key=lambda t: t.quality_score, reverse=True)[:5],
            "needs_work_list": sorted(needs_work, key=lambda t: t.quality_score)[:5]
        }
    
    def export(self, format: str = "json") -> str:
        """
        Export registry to specified format.
        
        Args:
            format: 'json' or 'markdown'
            
        Returns:
            Formatted string
        """
        tools = self.list_all()
        
        if format == "json":
            return json.dumps(
                [t.to_dict() for t in tools],
                indent=2,
                default=str
            )
        
        elif format == "markdown":
            lines = [
                "# Team Brain Tool Registry",
                "",
                f"**Total Tools:** {len(tools)}",
                f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                "",
                "---",
                ""
            ]
            
            # By category
            categories = self.categories()
            for category, count in categories.items():
                lines.append(f"## {category.title()} ({count} tools)")
                lines.append("")
                
                for tool in sorted(self.by_category(category), key=lambda t: t.name):
                    quality_icon = "🟢" if tool.quality_score >= 80 else "🟡" if tool.quality_score >= 50 else "🔴"
                    lines.append(f"### {tool.name} {quality_icon}")
                    lines.append(f"- **Description:** {tool.description}")
                    lines.append(f"- **Version:** {tool.version}")
                    lines.append(f"- **Quality:** {tool.quality_score}/100")
                    lines.append(f"- **GitHub:** [{tool.name}]({tool.github_url})")
                    if tool.cli_commands:
                        lines.append(f"- **Commands:** {', '.join(tool.cli_commands)}")
                    lines.append("")
            
            return "\n".join(lines)
        
        else:
            raise ValueError(f"Unknown format: {format}")
    
    def recommend(self, task: str) -> List[ToolMetadata]:
        """
        Recommend tools for a given task.
        
        Args:
            task: Description of the task
            
        Returns:
            List of recommended tools
        """
        # Extract keywords from task
        task_lower = task.lower()
        keywords = []
        
        # Check for category keywords
        for category, cat_keywords in TOOL_CATEGORIES.items():
            for kw in cat_keywords:
                if kw in task_lower:
                    keywords.append(category)
                    break
        
        # Search for matching tools
        results = []
        for keyword in keywords:
            matches = self.by_category(keyword)
            for tool in matches:
                if tool not in results:
                    results.append(tool)
        
        # Also do a general search
        search_results = self.search(task)
        for tool in search_results:
            if tool not in results:
                results.append(tool)
        
        # Sort by quality
        results.sort(key=lambda t: t.quality_score, reverse=True)
        
        return results[:5]


# ============== CLI INTERFACE ==============

def format_tool_summary(tool: ToolMetadata) -> str:
    """Format a tool for display."""
    quality_icon = "[OK]" if tool.quality_score >= 80 else "[!]" if tool.quality_score >= 50 else "[X]"
    
    lines = [
        f"{quality_icon} {tool.name} v{tool.version}",
        f"   {tool.description[:80]}{'...' if len(tool.description) > 80 else ''}",
        f"   Categories: {', '.join(tool.categories)}",
        f"   Quality: {tool.quality_score}/100 | Tests: {tool.test_count} | README: {tool.readme_lines} lines"
    ]
    return "\n".join(lines)


def main():
    """CLI entry point."""
    # Fix Windows console encoding for Unicode characters
    import sys
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass  # If reconfigure fails, continue anyway
    
    parser = argparse.ArgumentParser(
        description="ToolRegistry - Unified Tool Discovery for Team Brain",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  toolregistry scan                    # Discover all tools
  toolregistry list                    # List all registered tools
  toolregistry search synapse          # Find Synapse-related tools
  toolregistry info SynapseLink        # Get detailed info on a tool
  toolregistry launch SynapseLink send # Launch a tool with args
  toolregistry health                  # Show ecosystem health report
  toolregistry export --format md      # Export registry to markdown
  toolregistry recommend "send message to team"  # Get tool recommendations

GitHub: https://github.com/DonkRonk17/ToolRegistry
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # scan command
    scan_parser = subparsers.add_parser("scan", help="Scan for tools")
    scan_parser.add_argument("--path", "-p", help="Custom path to scan")
    
    # list command
    list_parser = subparsers.add_parser("list", help="List all tools")
    list_parser.add_argument("--category", "-c", help="Filter by category")
    list_parser.add_argument("--quality", "-q", type=int, default=0, help="Minimum quality score")
    list_parser.add_argument("--compact", action="store_true", help="Compact output")
    
    # search command
    search_parser = subparsers.add_parser("search", help="Search for tools")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--category", "-c", help="Filter by category")
    
    # info command
    info_parser = subparsers.add_parser("info", help="Get detailed tool info")
    info_parser.add_argument("name", help="Tool name")
    
    # launch command
    launch_parser = subparsers.add_parser("launch", help="Launch a tool")
    launch_parser.add_argument("name", help="Tool name")
    launch_parser.add_argument("args", nargs="*", help="Tool arguments")
    
    # health command
    subparsers.add_parser("health", help="Show ecosystem health report")
    
    # categories command
    subparsers.add_parser("categories", help="List all categories")
    
    # export command
    export_parser = subparsers.add_parser("export", help="Export registry")
    export_parser.add_argument("--format", "-f", choices=["json", "markdown", "md"], default="json")
    export_parser.add_argument("--output", "-o", help="Output file")
    
    # recommend command
    rec_parser = subparsers.add_parser("recommend", help="Get tool recommendations")
    rec_parser.add_argument("task", help="Task description")
    
    # stats command
    stats_parser = subparsers.add_parser("stats", help="Show usage statistics")
    stats_parser.add_argument("--tool", "-t", help="Specific tool name")
    
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    
    args = parser.parse_args()
    
    # Create registry
    registry = ToolRegistry()
    
    if args.command == "scan":
        paths = [Path(args.path)] if args.path else None
        count = registry.scan(paths)
        print(f"[OK] Discovered {count} tools")
        
    elif args.command == "list":
        tools = registry.list_all()
        
        if args.category:
            tools = [t for t in tools if args.category in t.categories]
        
        if args.quality > 0:
            tools = [t for t in tools if t.quality_score >= args.quality]
        
        tools.sort(key=lambda t: t.name.lower())
        
        if not tools:
            print("No tools found. Run 'toolregistry scan' first.")
            return
        
        print(f"[REGISTRY] Team Brain Tool Registry ({len(tools)} tools)")
        print("=" * 60)
        
        for tool in tools:
            if args.compact:
                quality_icon = "🟢" if tool.quality_score >= 80 else "🟡" if tool.quality_score >= 50 else "🔴"
                print(f"{quality_icon} {tool.name} - {tool.description[:50]}...")
            else:
                print(format_tool_summary(tool))
                print()
        
    elif args.command == "search":
        results = registry.search(args.query, args.category)
        
        if not results:
            print(f"No tools found matching '{args.query}'")
            return
        
        print(f"🔍 Search results for '{args.query}' ({len(results)} matches)")
        print("=" * 60)
        
        for tool in results:
            print(format_tool_summary(tool))
            print()
        
    elif args.command == "info":
        tool = registry.get(args.name)
        
        if not tool:
            print(f"Tool not found: {args.name}")
            print("Run 'toolregistry scan' to discover tools.")
            return
        
        quality_icon = "🟢" if tool.quality_score >= 80 else "🟡" if tool.quality_score >= 50 else "🔴"
        
        print(f"{quality_icon} {tool.name} v{tool.version}")
        print("=" * 60)
        print(f"Description: {tool.description}")
        print(f"Author: {tool.author}")
        print(f"Path: {tool.path}")
        print(f"GitHub: {tool.github_url}")
        print()
        print(f"Categories: {', '.join(tool.categories)}")
        print(f"Capabilities: {', '.join(tool.capabilities)}")
        print()
        print(f"CLI Commands: {', '.join(tool.cli_commands) if tool.cli_commands else 'None detected'}")
        print(f"Python API: {tool.python_api}")
        print()
        print("Quality Metrics:")
        print(f"  Score: {tool.quality_score}/100")
        print(f"  README: {'[OK]' if tool.has_readme else '[X]'} ({tool.readme_lines} lines)")
        print(f"  Tests: {'[OK]' if tool.has_tests else '[X]'} ({tool.test_count} tests)")
        print(f"  Examples: {'[OK]' if tool.has_examples else '[X]'}")
        print(f"  Branding: {'[OK]' if tool.has_branding else '[X]'}")
        print()
        print(f"Dependencies: {', '.join(tool.dependencies) if tool.dependencies else 'None (stdlib only)'}")
        print(f"Last Modified: {tool.last_modified.strftime('%Y-%m-%d %H:%M')}")
        
    elif args.command == "launch":
        print(f"[LAUNCH] Launching {args.name}...")
        returncode, stdout, stderr = registry.launch(args.name, args.args)
        
        if stdout:
            print(stdout)
        if stderr:
            print(stderr, file=sys.stderr)
        
        sys.exit(returncode)
        
    elif args.command == "health":
        health = registry.ecosystem_health()
        
        if health.get("total_tools", 0) == 0:
            print("No tools discovered. Run 'toolregistry scan' first.")
            return
        
        print("🏥 Team Brain Ecosystem Health Report")
        print("=" * 60)
        print(f"Total Tools: {health['total_tools']}")
        print()
        print("Coverage Metrics:")
        print(f"  Documentation: {health['documentation_coverage']}")
        print(f"  Tests: {health['test_coverage']}")
        print(f"  Examples: {health['examples_coverage']}")
        print(f"  Branding: {health['branding_coverage']}")
        print()
        print("Quality Metrics:")
        print(f"  Average Score: {health['average_quality_score']}")
        print(f"  High Quality (80+): {health['high_quality_tools']} tools")
        print(f"  Needs Work (<50): {health['needs_improvement']} tools")
        print()
        print("Categories:")
        for cat, count in health['categories'].items():
            print(f"  {cat}: {count} tools")
        print()
        print("Top Quality Tools:")
        for tool in health['top_quality'][:5]:
            print(f"  🟢 {tool.name} ({tool.quality_score}/100)")
        
        if health['needs_work_list']:
            print()
            print("Needs Improvement:")
            for tool in health['needs_work_list'][:5]:
                print(f"  🔴 {tool.name} ({tool.quality_score}/100)")
        
    elif args.command == "categories":
        categories = registry.categories()
        
        if not categories:
            print("No categories found. Run 'toolregistry scan' first.")
            return
        
        print("📁 Tool Categories")
        print("=" * 40)
        for cat, count in categories.items():
            print(f"  {cat}: {count} tools")
        
    elif args.command == "export":
        fmt = "markdown" if args.format == "md" else args.format
        output = registry.export(fmt)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"[OK] Exported to {args.output}")
        else:
            print(output)
        
    elif args.command == "recommend":
        recommendations = registry.recommend(args.task)
        
        if not recommendations:
            print(f"No recommendations found for: {args.task}")
            print("Try running 'toolregistry scan' first.")
            return
        
        print(f"🎯 Recommended tools for: {args.task}")
        print("=" * 60)
        
        for i, tool in enumerate(recommendations, 1):
            print(f"{i}. {tool.name} - {tool.description[:60]}...")
            print(f"   Quality: {tool.quality_score}/100 | GitHub: {tool.github_url}")
            print()
        
    elif args.command == "stats":
        stats = registry.get_usage_stats(args.tool)
        
        print("📊 Usage Statistics")
        print("=" * 40)
        print(f"Total Uses: {stats['total_uses']}")
        print(f"Successful: {stats['successful']}")
        print(f"Success Rate: {stats['success_rate']:.1f}%")
        
        if stats['top_tools']:
            print()
            print("Most Used Tools:")
            for name, count in stats['top_tools']:
                print(f"  {name}: {count} uses")
    
    else:
        parser.print_help()


# ============== QUICK API ==============

def quick_scan() -> int:
    """Convenience function to scan for tools."""
    registry = ToolRegistry()
    return registry.scan()


def quick_search(query: str) -> List[ToolMetadata]:
    """Convenience function to search for tools."""
    registry = ToolRegistry()
    return registry.search(query)


def quick_info(name: str) -> Optional[Dict[str, Any]]:
    """Convenience function to get tool info."""
    registry = ToolRegistry()
    tool = registry.get(name)
    return tool.to_dict() if tool else None


def quick_launch(name: str, args: List[str] = None) -> int:
    """Convenience function to launch a tool."""
    registry = ToolRegistry()
    returncode, _, _ = registry.launch(name, args)
    return returncode


if __name__ == "__main__":
    main()
