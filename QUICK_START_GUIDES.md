# ToolRegistry - Quick Start Guides

## 📖 ABOUT THESE GUIDES

Each Team Brain agent has a **5-minute quick-start guide** tailored to their role and workflows.

**Choose your guide:**
- [Forge (Orchestrator)](#-forge-quick-start)
- [Atlas (Executor)](#-atlas-quick-start)
- [Clio (Linux Agent)](#-clio-quick-start)
- [Nexus (Multi-Platform)](#-nexus-quick-start)
- [Bolt (Free Executor)](#-bolt-quick-start)

---

## 🔥 FORGE QUICK START

**Role:** Orchestrator / Reviewer  
**Time:** 5 minutes  
**Goal:** Use ToolRegistry to find the right tool for task assignment

### Step 1: Installation Check
```bash
cd C:\Users\logan\OneDrive\Documents\AutoProjects\ToolRegistry
python toolregistry.py --version

# Expected: toolregistry 1.0.0
```

### Step 2: First Scan
```bash
python toolregistry.py scan

# Expected: ✓ Discovered 35 tools
```

### Step 3: Find Tools for Tasks
```python
# In your Forge session
import sys
sys.path.insert(0, r'C:\Users\logan\OneDrive\Documents\AutoProjects\ToolRegistry')
from toolregistry import ToolRegistry

registry = ToolRegistry()

# Task: Need to send notification to team
recommendations = registry.recommend("send notification to agents")
print(f"Best tool: {recommendations[0].name}")
print(f"Import: {recommendations[0].python_api}")
```

### Step 4: Check Ecosystem Health
```bash
python toolregistry.py health

# See total tools, quality distribution, what needs work
```

### Common Forge Commands
```bash
# Find communication tools
toolregistry search "message"

# Find monitoring tools
toolregistry list --category monitoring

# Get ecosystem overview
toolregistry health
```

### Next Steps for Forge
1. Use `recommend` before assigning tasks
2. Check `health` weekly for quality tracking
3. Create tasks for tools that need improvement

---

## ⚡ ATLAS QUICK START

**Role:** Executor / Builder  
**Time:** 5 minutes  
**Goal:** Check for existing tools before building new ones

### Step 1: Installation Check
```python
# In Python
import sys
sys.path.insert(0, r'C:\Users\logan\OneDrive\Documents\AutoProjects\ToolRegistry')
from toolregistry import ToolRegistry
print("OK")
```

### Step 2: Check Before Building
```python
# BEFORE starting any new tool, check if it exists
from toolregistry import ToolRegistry

registry = ToolRegistry()
registry.scan()

# Example: Planning to build a clipboard manager
search = registry.search("clipboard")
if search:
    print("Similar tools exist:")
    for tool in search:
        print(f"  {tool.name} ({tool.quality_score}/100)")
        print(f"  → {tool.github_url}")
else:
    print("✓ No similar tools - safe to build!")
```

### Step 3: After Building, Rescan
```bash
# After completing a new tool, update the registry
python toolregistry.py scan

# Verify your new tool is indexed
python toolregistry.py info NewToolName
```

### Step 4: Quality Check
```python
# Check your tool's quality score
from toolregistry import ToolRegistry

registry = ToolRegistry()
tool = registry.get("YourNewTool")
print(f"Quality: {tool.quality_score}/100")
print(f"README: {tool.has_readme} ({tool.readme_lines} lines)")
print(f"Tests: {tool.has_tests} ({tool.test_count} tests)")
print(f"Examples: {tool.has_examples}")
print(f"Branding: {tool.has_branding}")
```

### Common Atlas Commands
```bash
# Check for duplicate before building
toolregistry search "your feature idea"

# Verify after building
toolregistry info YourToolName

# See what needs improvement
toolregistry health
```

### Next Steps for Atlas
1. Always search before building new tools
2. Rescan after completing any tool
3. Aim for 80+ quality score on all tools

---

## 🐧 CLIO QUICK START

**Role:** Linux / Ubuntu Agent  
**Time:** 5 minutes  
**Goal:** Discover and audit tools in Linux environment

### Step 1: Linux Installation
```bash
# Clone from GitHub (if not already present)
cd ~/AutoProjects
git clone https://github.com/DonkRonk17/ToolRegistry.git
cd ToolRegistry

# Verify
python3 toolregistry.py --version
```

### Step 2: Scan Tools
```bash
# Scan AutoProjects directory
python3 toolregistry.py scan

# Adjust scan path if needed (edit ~/.toolregistryrc)
```

### Step 3: Run Quality Audit
```bash
# Full ecosystem health
python3 toolregistry.py health

# List all tools
python3 toolregistry.py list

# Find specific tools
python3 toolregistry.py search "network"
```

### Step 4: Export for Documentation
```bash
# Export catalog to markdown
python3 toolregistry.py export --format md --output ~/TOOL_CATALOG.md
```

### Linux-Specific Features
```bash
# Pipe to grep for filtering
python3 toolregistry.py list --compact | grep "synapse"

# Save health report
python3 toolregistry.py health > ~/ecosystem_health.txt

# Use in shell scripts
TOOL_COUNT=$(python3 toolregistry.py list --compact | wc -l)
echo "Total tools: $TOOL_COUNT"
```

### Next Steps for Clio
1. Set up periodic quality audits
2. Export catalog to documentation
3. Test cross-platform compatibility

---

## 🌐 NEXUS QUICK START

**Role:** Multi-Platform Agent  
**Time:** 5 minutes  
**Goal:** Verify tool compatibility across platforms

### Step 1: Platform Detection
```python
import platform
import sys
sys.path.insert(0, r'C:\Users\logan\OneDrive\Documents\AutoProjects\ToolRegistry')
from toolregistry import ToolRegistry

registry = ToolRegistry()
print(f"Platform: {platform.system()}")
print(f"ToolRegistry works on: Windows, Linux, macOS")
```

### Step 2: Verify Cross-Platform Tools
```python
# Check which tools are likely cross-platform
from toolregistry import ToolRegistry

registry = ToolRegistry()
registry.scan()

for tool in registry.list_all():
    deps = tool.dependencies
    if not deps or "No dependencies" in str(deps):
        print(f"✓ {tool.name} - Zero deps (likely cross-platform)")
    else:
        print(f"? {tool.name} - Check deps: {deps}")
```

### Step 3: Test on Multiple Platforms
```bash
# Windows
python toolregistry.py search "network"

# Linux/macOS (same command!)
python3 toolregistry.py search "network"
```

### Step 4: Report Platform Issues
```python
# If a tool has platform issues, log it
from toolregistry import ToolRegistry
from synapselink import quick_send

registry = ToolRegistry()
tool = registry.get("ProblematicTool")

quick_send(
    "FORGE",
    f"Platform Issue: {tool.name}",
    f"Tool {tool.name} has issues on [PLATFORM].\nPath: {tool.path}\n\nIssue: [DESCRIPTION]",
    priority="HIGH"
)
```

### Platform Considerations
| Platform | Config Location | Database Location |
|----------|-----------------|-------------------|
| Windows | `~/.toolregistryrc` | `~/.toolregistry/` |
| Linux | `~/.toolregistryrc` | `~/.toolregistry/` |
| macOS | `~/.toolregistryrc` | `~/.toolregistry/` |

### Next Steps for Nexus
1. Test registry on each platform
2. Identify platform-specific tools
3. Report compatibility issues via Synapse

---

## 🆓 BOLT QUICK START

**Role:** Free Executor (Cline + Grok)  
**Time:** 5 minutes  
**Goal:** Discover and use tools without API costs

### Step 1: Verify Free Access
```bash
# No API key required! ToolRegistry is 100% local
python toolregistry.py --version
```

### Step 2: Batch Discovery
```bash
# Discover all tools (free operation)
python toolregistry.py scan

# List everything
python toolregistry.py list --compact
```

### Step 3: Export for Offline Use
```bash
# Export full catalog to JSON (for processing)
python toolregistry.py export --format json --output tools.json

# Export to Markdown (for reading)
python toolregistry.py export --format md --output CATALOG.md
```

### Step 4: Batch Operations
```bash
# Generate health report
python toolregistry.py health > health_report.txt

# Find all monitoring tools
python toolregistry.py list --category monitoring > monitoring_tools.txt

# Search multiple terms
for term in synapse task file; do
    echo "=== $term ===" >> search_results.txt
    python toolregistry.py search $term --compact >> search_results.txt
done
```

### Cost-Free Benefits
| Operation | API Cost | ToolRegistry Cost |
|-----------|----------|-------------------|
| Search 100 times | $0.XX | $0.00 |
| Full catalog export | $0.XX | $0.00 |
| Health check | $0.XX | $0.00 |
| Everything | Variable | **Always $0** |

### Next Steps for Bolt
1. Use for all tool discovery (free!)
2. Export catalogs before sessions
3. Batch process tool information

---

## 📚 ADDITIONAL RESOURCES

**For All Agents:**
- Full Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Integration Plan: [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)

**Support:**
- GitHub Issues: https://github.com/DonkRonk17/ToolRegistry/issues
- Synapse: Post in THE_SYNAPSE/active/
- Direct: Message Forge

---

**Last Updated:** January 19, 2026  
**Maintained By:** Forge (Team Brain - Cursor)
