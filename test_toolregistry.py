#!/usr/bin/env python3
"""
Comprehensive test suite for ToolRegistry v1.0

Tests cover:
- Core functionality (scan, search, get)
- Metadata extraction
- Category detection
- Quality scoring
- Database operations
- Usage tracking
- Export functionality
- Edge cases and error handling

Run: python test_toolregistry.py
"""

import unittest
import sys
import os
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from toolregistry import (
    ToolRegistry, ToolMetadata, VERSION,
    quick_scan, quick_search, quick_info, quick_launch
)


class TestToolMetadata(unittest.TestCase):
    """Test ToolMetadata class."""
    
    def test_initialization(self):
        """Test ToolMetadata initialization with defaults."""
        tool = ToolMetadata(
            name="TestTool",
            path=Path("/test/path")
        )
        self.assertEqual(tool.name, "TestTool")
        self.assertEqual(tool.path, Path("/test/path"))
        self.assertEqual(tool.version, "unknown")
        self.assertEqual(tool.author, "Team Brain")
        self.assertEqual(tool.categories, [])
        self.assertEqual(tool.quality_score, 0)
    
    def test_initialization_full(self):
        """Test ToolMetadata initialization with all parameters."""
        tool = ToolMetadata(
            name="FullTool",
            path=Path("/full/path"),
            description="A complete tool",
            version="2.0.0",
            author="Test Author",
            categories=["test", "utility"],
            capabilities=["CLI interface", "JSON support"],
            cli_commands=["run", "test"],
            python_api="from fulltool import FullTool",
            dependencies=["requests"],
            github_url="https://github.com/test/FullTool",
            has_tests=True,
            has_readme=True,
            has_examples=True,
            has_branding=True,
            readme_lines=500,
            test_count=20,
            quality_score=95
        )
        
        self.assertEqual(tool.name, "FullTool")
        self.assertEqual(tool.version, "2.0.0")
        self.assertEqual(tool.description, "A complete tool")
        self.assertTrue(tool.has_tests)
        self.assertEqual(tool.test_count, 20)
        self.assertEqual(tool.quality_score, 95)
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        tool = ToolMetadata(
            name="DictTool",
            path=Path("/dict/path"),
            description="Tool for dict test",
            version="1.0.0"
        )
        
        data = tool.to_dict()
        
        self.assertIsInstance(data, dict)
        self.assertEqual(data["name"], "DictTool")
        self.assertEqual(data["path"], str(Path("/dict/path")))
        self.assertEqual(data["description"], "Tool for dict test")
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            "name": "FromDictTool",
            "path": "/from/dict/path",
            "description": "Created from dict",
            "version": "1.5.0",
            "author": "Dict Author",
            "categories": ["test"],
            "capabilities": [],
            "cli_commands": [],
            "python_api": "",
            "dependencies": [],
            "github_url": "",
            "has_tests": True,
            "has_readme": True,
            "has_examples": False,
            "has_branding": False,
            "readme_lines": 100,
            "test_count": 5,
            "last_modified": datetime.now().isoformat(),
            "quality_score": 60
        }
        
        tool = ToolMetadata.from_dict(data)
        
        self.assertEqual(tool.name, "FromDictTool")
        self.assertEqual(tool.version, "1.5.0")
        self.assertTrue(tool.has_tests)
        self.assertIsInstance(tool.path, Path)


class TestToolRegistry(unittest.TestCase):
    """Test ToolRegistry class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        
        # Create mock tool directories
        self._create_mock_tool("MockTool1", has_readme=True, has_tests=True)
        self._create_mock_tool("MockTool2", has_readme=True, has_tests=False)
        self._create_mock_tool("SynapseTest", has_readme=True, has_tests=True, has_examples=True)
        
        # Create registry with temp paths
        self.registry = ToolRegistry(
            config_path=self.temp_path / ".toolregistryrc",
            db_path=self.temp_path / ".toolregistry" / "registry.db",
            scan_paths=[self.temp_path]
        )
    
    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.temp_dir)
    
    def _create_mock_tool(
        self,
        name: str,
        has_readme: bool = False,
        has_tests: bool = False,
        has_examples: bool = False,
        has_branding: bool = False
    ):
        """Create a mock tool directory for testing."""
        tool_dir = self.temp_path / name
        tool_dir.mkdir(parents=True, exist_ok=True)
        
        # Create main script
        script_content = f'''#!/usr/bin/env python3
"""
{name} - A mock tool for testing

This is a test tool created for unit testing purposes.
It provides basic functionality for testing the ToolRegistry.

Author: Test Author
Created: 2026-01-19
Version: 1.0.0
License: MIT
"""

VERSION = "1.0.0"

class {name}:
    """Main class for {name}."""
    
    def __init__(self):
        pass
    
    def run(self):
        """Run the tool."""
        return "success"

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["run", "test", "help"])
    args = parser.parse_args()
    
    tool = {name}()
    print(tool.run())

if __name__ == "__main__":
    main()
'''
        
        (tool_dir / f"{name.lower()}.py").write_text(script_content)
        
        if has_readme:
            readme_content = f'''# {name}

**A mock tool for testing purposes.**

This tool provides functionality for testing the ToolRegistry.

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

```bash
pip install {name.lower()}
```

## Usage

```python
from {name.lower()} import {name}
tool = {name}()
tool.run()
```

## GitHub

https://github.com/DonkRonk17/{name}

## License

MIT License
'''
            (tool_dir / "README.md").write_text(readme_content)
        
        if has_tests:
            test_content = f'''import unittest

class Test{name}(unittest.TestCase):
    def test_init(self):
        pass
    
    def test_run(self):
        pass
    
    def test_basic(self):
        pass

if __name__ == "__main__":
    unittest.main()
'''
            (tool_dir / f"test_{name.lower()}.py").write_text(test_content)
        
        if has_examples:
            (tool_dir / "EXAMPLES.md").write_text(f"# {name} Examples\n\n## Example 1\n...")
        
        if has_branding:
            branding_dir = tool_dir / "branding"
            branding_dir.mkdir(exist_ok=True)
            (branding_dir / "BRANDING_PROMPTS.md").write_text("# Branding")
        
        (tool_dir / "requirements.txt").write_text("# No dependencies")
    
    def test_initialization(self):
        """Test registry initializes correctly."""
        self.assertIsNotNone(self.registry)
        self.assertTrue(self.registry.db_path.parent.exists())
    
    def test_scan(self):
        """Test scanning for tools."""
        count = self.registry.scan()
        self.assertGreaterEqual(count, 3)
    
    def test_list_all(self):
        """Test listing all tools."""
        self.registry.scan()
        tools = self.registry.list_all()
        self.assertGreaterEqual(len(tools), 3)
        self.assertTrue(all(isinstance(t, ToolMetadata) for t in tools))
    
    def test_get_existing_tool(self):
        """Test getting an existing tool."""
        self.registry.scan()
        tool = self.registry.get("MockTool1")
        self.assertIsNotNone(tool)
        self.assertEqual(tool.name, "MockTool1")
    
    def test_get_nonexistent_tool(self):
        """Test getting a nonexistent tool."""
        self.registry.scan()
        tool = self.registry.get("NonexistentTool")
        self.assertIsNone(tool)
    
    def test_get_case_insensitive(self):
        """Test case-insensitive get."""
        self.registry.scan()
        tool1 = self.registry.get("MockTool1")
        tool2 = self.registry.get("mocktool1")
        tool3 = self.registry.get("MOCKTOOL1")
        
        self.assertIsNotNone(tool1)
        self.assertIsNotNone(tool2)
        self.assertIsNotNone(tool3)
        self.assertEqual(tool1.name, tool2.name)
    
    def test_search_by_name(self):
        """Test searching by name."""
        self.registry.scan()
        results = self.registry.search("Mock")
        self.assertGreaterEqual(len(results), 2)
    
    def test_search_by_category(self):
        """Test searching with category filter."""
        self.registry.scan()
        results = self.registry.search("", category="synapse")
        # Should find SynapseTest
        self.assertGreaterEqual(len(results), 1)
    
    def test_search_no_results(self):
        """Test search with no results."""
        self.registry.scan()
        results = self.registry.search("xyznonexistent123")
        self.assertEqual(len(results), 0)
    
    def test_by_category(self):
        """Test filtering by category."""
        self.registry.scan()
        # After scanning, tools should have categories
        tools = self.registry.list_all()
        if tools:
            first_cat = tools[0].categories[0] if tools[0].categories else "utility"
            cat_tools = self.registry.by_category(first_cat)
            self.assertGreaterEqual(len(cat_tools), 1)
    
    def test_categories(self):
        """Test getting category counts."""
        self.registry.scan()
        categories = self.registry.categories()
        self.assertIsInstance(categories, dict)
        # Should have at least one category
        self.assertGreaterEqual(len(categories), 1)


class TestQualityScoring(unittest.TestCase):
    """Test quality score calculation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        
        self.registry = ToolRegistry(
            config_path=self.temp_path / ".toolregistryrc",
            db_path=self.temp_path / ".toolregistry" / "registry.db",
            scan_paths=[self.temp_path]
        )
    
    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.temp_dir)
    
    def test_quality_score_empty(self):
        """Test quality score with nothing."""
        score = self.registry._calculate_quality_score(
            has_readme=False, readme_lines=0,
            has_tests=False, test_count=0,
            has_examples=False, has_branding=False,
            has_description=False
        )
        self.assertEqual(score, 10)  # Base points only
    
    def test_quality_score_readme_only(self):
        """Test quality score with just README."""
        score = self.registry._calculate_quality_score(
            has_readme=True, readme_lines=50,
            has_tests=False, test_count=0,
            has_examples=False, has_branding=False,
            has_description=False
        )
        self.assertEqual(score, 20)  # 10 base + 10 for README
    
    def test_quality_score_good_readme(self):
        """Test quality score with good README (400+ lines)."""
        score = self.registry._calculate_quality_score(
            has_readme=True, readme_lines=500,
            has_tests=False, test_count=0,
            has_examples=False, has_branding=False,
            has_description=True
        )
        # 10 base + 10 readme + 5 (100+) + 5 (200+) + 10 (400+) + 10 description = 50
        self.assertEqual(score, 50)
    
    def test_quality_score_with_tests(self):
        """Test quality score with tests."""
        score = self.registry._calculate_quality_score(
            has_readme=True, readme_lines=100,
            has_tests=True, test_count=15,
            has_examples=False, has_branding=False,
            has_description=True
        )
        # 10 base + 10 readme + 5 (100 lines) + 10 tests + 5 (5+) + 5 (10+) + 5 (15+) + 10 desc = 60
        self.assertEqual(score, 60)
    
    def test_quality_score_full(self):
        """Test quality score with everything."""
        score = self.registry._calculate_quality_score(
            has_readme=True, readme_lines=500,
            has_tests=True, test_count=20,
            has_examples=True, has_branding=True,
            has_description=True
        )
        # Should be 100 (capped)
        self.assertEqual(score, 100)


class TestCategoryDetection(unittest.TestCase):
    """Test category detection."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        
        self.registry = ToolRegistry(
            config_path=self.temp_path / ".toolregistryrc",
            db_path=self.temp_path / ".toolregistry" / "registry.db",
            scan_paths=[self.temp_path]
        )
    
    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.temp_dir)
    
    def test_synapse_category(self):
        """Test detecting synapse category."""
        categories = self.registry._detect_categories(
            "SynapseLink", "Messaging tool for AI communication"
        )
        self.assertIn("synapse", categories)
    
    def test_monitoring_category(self):
        """Test detecting monitoring category."""
        categories = self.registry._detect_categories(
            "AgentHealth", "Monitor agent health and performance"
        )
        self.assertIn("monitoring", categories)
    
    def test_task_category(self):
        """Test detecting task category."""
        categories = self.registry._detect_categories(
            "TaskQueuePro", "Task queue management system"
        )
        self.assertIn("task", categories)
    
    def test_default_category(self):
        """Test default category for unknown tools."""
        categories = self.registry._detect_categories(
            "RandomTool", "A random tool"
        )
        self.assertIn("utility", categories)
    
    def test_multiple_categories(self):
        """Test detecting multiple categories."""
        categories = self.registry._detect_categories(
            "SynapseWatcher", "Watch synapse for messages and monitor activity"
        )
        self.assertIn("synapse", categories)
        self.assertIn("monitoring", categories)


class TestExport(unittest.TestCase):
    """Test export functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        
        # Create a mock tool
        tool_dir = self.temp_path / "ExportTest"
        tool_dir.mkdir()
        (tool_dir / "exporttest.py").write_text('"""ExportTest tool"""\nVERSION = "1.0"')
        (tool_dir / "README.md").write_text("# ExportTest\n\nA test tool.")
        
        self.registry = ToolRegistry(
            config_path=self.temp_path / ".toolregistryrc",
            db_path=self.temp_path / ".toolregistry" / "registry.db",
            scan_paths=[self.temp_path]
        )
        self.registry.scan()
    
    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.temp_dir)
    
    def test_export_json(self):
        """Test JSON export."""
        output = self.registry.export("json")
        self.assertIsInstance(output, str)
        
        # Should be valid JSON
        data = json.loads(output)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
    
    def test_export_markdown(self):
        """Test Markdown export."""
        output = self.registry.export("markdown")
        self.assertIsInstance(output, str)
        self.assertIn("# Team Brain Tool Registry", output)
        self.assertIn("Total Tools:", output)
    
    def test_export_invalid_format(self):
        """Test invalid export format raises error."""
        with self.assertRaises(ValueError):
            self.registry.export("invalid")


class TestEcosystemHealth(unittest.TestCase):
    """Test ecosystem health report."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        
        # Create mock tools with varying quality
        self._create_high_quality_tool()
        self._create_low_quality_tool()
        
        self.registry = ToolRegistry(
            config_path=self.temp_path / ".toolregistryrc",
            db_path=self.temp_path / ".toolregistry" / "registry.db",
            scan_paths=[self.temp_path]
        )
        self.registry.scan()
    
    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.temp_dir)
    
    def _create_high_quality_tool(self):
        """Create a high quality tool."""
        tool_dir = self.temp_path / "HighQualityTool"
        tool_dir.mkdir()
        
        script = '''"""HighQualityTool - A complete tool
        
Full documentation and features.

Author: Test
Version: 1.0.0
"""
VERSION = "1.0.0"

class HighQualityTool:
    pass
'''
        (tool_dir / "highqualitytool.py").write_text(script)
        
        readme = "# HighQualityTool\n\n" + "Line\n" * 450
        (tool_dir / "README.md").write_text(readme)
        
        tests = "def test_1(): pass\n" * 20
        (tool_dir / "test_highqualitytool.py").write_text(tests)
        
        (tool_dir / "EXAMPLES.md").write_text("# Examples")
        
        branding = tool_dir / "branding"
        branding.mkdir()
        (branding / "BRANDING_PROMPTS.md").write_text("# Branding")
    
    def _create_low_quality_tool(self):
        """Create a low quality tool."""
        tool_dir = self.temp_path / "LowQualityTool"
        tool_dir.mkdir()
        (tool_dir / "lowqualitytool.py").write_text("# Minimal tool\npass")
    
    def test_health_report_structure(self):
        """Test health report has expected structure."""
        health = self.registry.ecosystem_health()
        
        self.assertIn("total_tools", health)
        self.assertIn("documentation_coverage", health)
        self.assertIn("test_coverage", health)
        self.assertIn("average_quality_score", health)
        self.assertIn("categories", health)
    
    def test_health_report_metrics(self):
        """Test health report metrics are reasonable."""
        health = self.registry.ecosystem_health()
        
        self.assertGreaterEqual(health["total_tools"], 2)
        self.assertGreaterEqual(health["high_quality_tools"], 1)


class TestUsageTracking(unittest.TestCase):
    """Test usage tracking functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        
        # Create a mock tool
        tool_dir = self.temp_path / "UsageTool"
        tool_dir.mkdir()
        script = '''import sys
print("Success")
sys.exit(0)
'''
        (tool_dir / "usagetool.py").write_text(script)
        
        self.registry = ToolRegistry(
            config_path=self.temp_path / ".toolregistryrc",
            db_path=self.temp_path / ".toolregistry" / "registry.db",
            scan_paths=[self.temp_path]
        )
        self.registry.scan()
    
    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.temp_dir)
    
    def test_track_usage(self):
        """Test tracking usage."""
        self.registry._track_usage("UsageTool", "test_action", success=True)
        stats = self.registry.get_usage_stats()
        
        self.assertEqual(stats["total_uses"], 1)
        self.assertEqual(stats["successful"], 1)
    
    def test_usage_stats_empty(self):
        """Test usage stats when empty."""
        stats = self.registry.get_usage_stats()
        # After scan there may be some tracking, so just check structure
        self.assertIn("total_uses", stats)
        self.assertIn("success_rate", stats)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        
        self.registry = ToolRegistry(
            config_path=self.temp_path / ".toolregistryrc",
            db_path=self.temp_path / ".toolregistry" / "registry.db",
            scan_paths=[self.temp_path]
        )
    
    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.temp_dir)
    
    def test_scan_empty_directory(self):
        """Test scanning empty directory."""
        count = self.registry.scan()
        self.assertEqual(count, 0)
    
    def test_scan_nonexistent_path(self):
        """Test scanning nonexistent path."""
        registry = ToolRegistry(
            config_path=self.temp_path / ".toolregistryrc",
            db_path=self.temp_path / ".toolregistry" / "registry.db",
            scan_paths=[Path("/nonexistent/path")]
        )
        count = registry.scan()
        self.assertEqual(count, 0)
    
    def test_search_empty_query(self):
        """Test search with empty query."""
        results = self.registry.search("")
        self.assertEqual(len(results), 0)
    
    def test_search_special_characters(self):
        """Test search with special characters."""
        results = self.registry.search("@#$%")
        self.assertEqual(len(results), 0)
    
    def test_launch_nonexistent_tool(self):
        """Test launching nonexistent tool."""
        returncode, stdout, stderr = self.registry.launch("NonexistentTool")
        self.assertEqual(returncode, 1)
        self.assertIn("not found", stderr.lower())
    
    def test_ecosystem_health_no_tools(self):
        """Test health report with no tools."""
        health = self.registry.ecosystem_health()
        self.assertEqual(health["total_tools"], 0)
        self.assertIn("No tools discovered", health.get("status", ""))
    
    def test_recommend_no_tools(self):
        """Test recommendations with no tools."""
        results = self.registry.recommend("send a message")
        self.assertEqual(len(results), 0)


class TestRecommendations(unittest.TestCase):
    """Test tool recommendation functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        
        # Create tools with specific purposes
        tools = [
            ("MessageTool", "Send messages to other agents"),
            ("MonitorTool", "Monitor system health"),
            ("TaskTool", "Manage tasks and queues"),
        ]
        
        for name, desc in tools:
            tool_dir = self.temp_path / name
            tool_dir.mkdir()
            (tool_dir / f"{name.lower()}.py").write_text(f'"""{name} - {desc}"""\nVERSION = "1.0"')
            (tool_dir / "README.md").write_text(f"# {name}\n\n{desc}")
        
        self.registry = ToolRegistry(
            config_path=self.temp_path / ".toolregistryrc",
            db_path=self.temp_path / ".toolregistry" / "registry.db",
            scan_paths=[self.temp_path]
        )
        self.registry.scan()
    
    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.temp_dir)
    
    def test_recommend_message_task(self):
        """Test recommendations for messaging task."""
        results = self.registry.recommend("send a message")
        self.assertGreaterEqual(len(results), 1)
    
    def test_recommend_monitor_task(self):
        """Test recommendations for monitoring task."""
        results = self.registry.recommend("monitor health")
        self.assertGreaterEqual(len(results), 1)
    
    def test_recommend_returns_limited(self):
        """Test recommendations return max 5 results."""
        results = self.registry.recommend("tool")
        self.assertLessEqual(len(results), 5)


# ============== TEST RUNNER ==============

def run_tests():
    """Run all tests with nice output."""
    print("=" * 70)
    print("TESTING: ToolRegistry v1.0")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestToolMetadata))
    suite.addTests(loader.loadTestsFromTestCase(TestToolRegistry))
    suite.addTests(loader.loadTestsFromTestCase(TestQualityScoring))
    suite.addTests(loader.loadTestsFromTestCase(TestCategoryDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestExport))
    suite.addTests(loader.loadTestsFromTestCase(TestEcosystemHealth))
    suite.addTests(loader.loadTestsFromTestCase(TestUsageTracking))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestRecommendations))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 70)
    print(f"RESULTS: {result.testsRun} tests")
    print(f"[OK] Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    if result.failures:
        print(f"[FAIL] Failed: {len(result.failures)}")
    if result.errors:
        print(f"[ERROR] Errors: {len(result.errors)}")
    print("=" * 70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
