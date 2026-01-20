# ToolRegistry - Usage Examples

Quick navigation:
- [Example 1: First-Time Setup](#example-1-first-time-setup)
- [Example 2: Finding a Tool](#example-2-finding-a-tool)
- [Example 3: Detailed Tool Information](#example-3-detailed-tool-information)
- [Example 4: Filtering by Category](#example-4-filtering-by-category)
- [Example 5: Ecosystem Health Check](#example-5-ecosystem-health-check)
- [Example 6: Launching Tools](#example-6-launching-tools)
- [Example 7: Getting Recommendations](#example-7-getting-recommendations)
- [Example 8: Python API Integration](#example-8-python-api-integration)
- [Example 9: Exporting the Catalog](#example-9-exporting-the-catalog)
- [Example 10: Quality Audit Workflow](#example-10-quality-audit-workflow)

---

## Example 1: First-Time Setup

**Scenario:** You just installed ToolRegistry and want to catalog all your tools.

**Steps:**

```bash
# Navigate to the ToolRegistry folder
cd C:\Users\logan\OneDrive\Documents\AutoProjects\ToolRegistry

# Step 1: Scan for all tools
python toolregistry.py scan
```

**Expected Output:**
```
✓ Discovered 35 tools
```

```bash
# Step 2: Verify by listing all tools
python toolregistry.py list --compact
```

**Expected Output:**
```
📦 Team Brain Tool Registry (35 tools)
============================================================
🟢 AgentHealth - Monitor Team Brain System Health...
🟢 AgentRouter - Auto-route requests to best AI based on task type...
🟢 ClipStash - Multi-format clipboard manager with history tracking...
🟢 CollabSession - Multi-agent coordination framework...
...
```

**What You Learned:**
- How to discover all tools in your ecosystem
- How to verify the scan worked
- Tools are automatically categorized by quality (🟢🟡🔴)

---

## Example 2: Finding a Tool

**Scenario:** You need to send a message to another AI agent but can't remember which tool does that.

**Steps:**

```bash
# Search for messaging tools
python toolregistry.py search message
```

**Expected Output:**
```
🔍 Search results for 'message' (3 matches)
============================================================
🟢 SynapseLink v1.0.0
   AI-to-AI messaging for Team Brain - simple quick_send API...
   Categories: synapse
   Quality: 92/100 | Tests: 19 | README: 650 lines

🟢 SynapseInbox v1.0.0
   Extension to SynapseLink for inbox filtering and search...
   Categories: synapse
   Quality: 85/100 | Tests: 18 | README: 480 lines

🟢 SynapseWatcher v1.0.0
   Background service for Synapse monitoring...
   Categories: synapse, monitoring
   Quality: 88/100 | Tests: 19 | README: 520 lines
```

**What You Learned:**
- How to search by keyword
- Search matches name, description, and categories
- Results show quality scores for quick assessment

---

## Example 3: Detailed Tool Information

**Scenario:** You found SynapseLink but want to know exactly how to use it.

**Steps:**

```bash
# Get detailed info
python toolregistry.py info SynapseLink
```

**Expected Output:**
```
🟢 SynapseLink v1.0.0
============================================================
Description: AI-to-AI messaging for Team Brain - simple quick_send API, priority routing, thread support
Author: Atlas (Team Brain)
Path: C:\Users\logan\OneDrive\Documents\AutoProjects\SynapseLink
GitHub: https://github.com/DonkRonk17/SynapseLink

Categories: synapse
Capabilities: CLI interface, Python API, JSON support, File operations

CLI Commands: send, read, reply, list, search, stats
Python API: from synapselink import SynapseLink

Quality Metrics:
  Score: 92/100
  README: ✓ (650 lines)
  Tests: ✓ (19 tests)
  Examples: ✓
  Branding: ✓

Dependencies: None (stdlib only)
Last Modified: 2026-01-18 14:30
```

**What You Learned:**
- Full details including path and GitHub URL
- Available CLI commands and Python import
- Quality breakdown (README, tests, examples, branding)
- Dependencies (important for deployment)

---

## Example 4: Filtering by Category

**Scenario:** You want to see all monitoring-related tools.

**Steps:**

```bash
# First, see all available categories
python toolregistry.py categories
```

**Expected Output:**
```
📁 Tool Categories
========================================
  synapse: 5 tools
  monitoring: 4 tools
  task: 3 tools
  memory: 3 tools
  file: 6 tools
  dev: 5 tools
  productivity: 4 tools
  security: 2 tools
  network: 3 tools
  routing: 2 tools
  utility: 8 tools
```

```bash
# Now filter by monitoring category
python toolregistry.py list --category monitoring
```

**Expected Output:**
```
📦 Team Brain Tool Registry (4 tools)
============================================================
🟢 AgentHealth v1.0.0
   Monitor Team Brain System Health...
   Categories: monitoring
   Quality: 85/100 | Tests: 21 | README: 616 lines

🟢 SynapseWatcher v1.0.0
   Background service for Synapse monitoring...
   Categories: synapse, monitoring
   Quality: 88/100 | Tests: 19 | README: 520 lines

🟢 TokenTracker v1.0.0
   Real-time AI token usage monitor...
   Categories: monitoring
   Quality: 82/100 | Tests: 15 | README: 480 lines

🟢 ProcessWatcher v1.0.0
   Smart process monitor - system resources...
   Categories: monitoring
   Quality: 75/100 | Tests: 12 | README: 350 lines
```

**What You Learned:**
- How to see all categories in your ecosystem
- How to filter tools by specific category
- Categories help organize large tool collections

---

## Example 5: Ecosystem Health Check

**Scenario:** You want to assess the overall quality of your tool ecosystem.

**Steps:**

```bash
# Generate health report
python toolregistry.py health
```

**Expected Output:**
```
🏥 Team Brain Ecosystem Health Report
============================================================
Total Tools: 35

Coverage Metrics:
  Documentation: 94.3%
  Tests: 85.7%
  Examples: 71.4%
  Branding: 68.6%

Quality Metrics:
  Average Score: 72.4/100
  High Quality (80+): 18 tools
  Needs Work (<50): 3 tools

Categories:
  synapse: 5 tools
  monitoring: 4 tools
  task: 3 tools
  file: 6 tools
  dev: 5 tools
  ...

Top Quality Tools:
  🟢 SynapseLink (92/100)
  🟢 ContextCompressor (90/100)
  🟢 AgentHealth (85/100)
  🟢 SessionReplay (88/100)
  🟢 CollabSession (86/100)

Needs Improvement:
  🔴 OldTool1 (35/100)
  🔴 QuickHack (42/100)
  🔴 LegacyUtil (48/100)
```

**What You Learned:**
- Overall documentation and test coverage
- Quality distribution across tools
- Which tools are excellent vs need work
- Category breakdown of ecosystem

---

## Example 6: Launching Tools

**Scenario:** You want to run SynapseLink directly from ToolRegistry.

**Steps:**

```bash
# Launch tool with --help to see options
python toolregistry.py launch SynapseLink --help
```

**Expected Output:**
```
🚀 Launching SynapseLink...
usage: synapselink.py [-h] [--version] {send,read,reply,list,search,stats} ...

SynapseLink - AI-to-AI Messaging for Team Brain

positional arguments:
  {send,read,reply,list,search,stats}
    send                Send a message
    read                Read messages
    ...
```

```bash
# Launch with actual arguments
python toolregistry.py launch SynapseLink send --to FORGE --subject "Test" --message "Hello from ToolRegistry"
```

**Expected Output:**
```
🚀 Launching SynapseLink...
✓ Message sent to FORGE
Message ID: synapselink_2026-01-19_001
```

**What You Learned:**
- How to launch any registered tool
- Arguments are passed through to the tool
- No need to navigate to tool directory

---

## Example 7: Getting Recommendations

**Scenario:** You have a task but don't know which tool to use.

**Steps:**

```bash
# Describe your task, get recommendations
python toolregistry.py recommend "track how many tokens AI agents are using"
```

**Expected Output:**
```
🎯 Recommended tools for: track how many tokens AI agents are using
============================================================
1. TokenTracker - Real-time AI token usage monitor...
   Quality: 82/100 | GitHub: https://github.com/DonkRonk17/TokenTracker

2. AgentHealth - Monitor Team Brain System Health...
   Quality: 85/100 | GitHub: https://github.com/DonkRonk17/AgentHealth

3. SynapseStats - Analytics for Synapse communication...
   Quality: 78/100 | GitHub: https://github.com/DonkRonk17/SynapseStats
```

```bash
# Another example: need to manage tasks
python toolregistry.py recommend "create and assign tasks to AI agents"
```

**Expected Output:**
```
🎯 Recommended tools for: create and assign tasks to AI agents
============================================================
1. TaskQueuePro - Self-scheduling task system...
   Quality: 80/100 | GitHub: https://github.com/DonkRonk17/TaskQueuePro

2. AgentRouter - Auto-route requests to best AI...
   Quality: 78/100 | GitHub: https://github.com/DonkRonk17/AgentRouter

3. TaskFlow - Smart CLI todo and project manager...
   Quality: 72/100 | GitHub: https://github.com/DonkRonk17/TaskFlow
```

**What You Learned:**
- Describe tasks in natural language
- Get up to 5 relevant recommendations
- Results sorted by relevance and quality

---

## Example 8: Python API Integration

**Scenario:** You want to use ToolRegistry programmatically in your own tool.

**Steps:**

```python
# In your Python script
import sys
sys.path.insert(0, r'C:\Users\logan\OneDrive\Documents\AutoProjects\ToolRegistry')
from toolregistry import ToolRegistry, quick_search

# Create registry
registry = ToolRegistry()

# Scan for tools (first time or to refresh)
count = registry.scan()
print(f"Found {count} tools")

# Search for tools
results = registry.search("synapse")
for tool in results:
    print(f"- {tool.name}: {tool.description[:50]}...")

# Get specific tool
synapselink = registry.get("SynapseLink")
if synapselink:
    print(f"\nSynapseLink Details:")
    print(f"  Version: {synapselink.version}")
    print(f"  Quality: {synapselink.quality_score}/100")
    print(f"  CLI Commands: {', '.join(synapselink.cli_commands)}")
    print(f"  Python API: {synapselink.python_api}")

# Get ecosystem health
health = registry.ecosystem_health()
print(f"\nEcosystem Health:")
print(f"  Total: {health['total_tools']} tools")
print(f"  Avg Quality: {health['average_quality_score']}")

# Launch a tool
returncode, stdout, stderr = registry.launch("SynapseLink", ["--version"], capture_output=True)
print(f"\nSynapseLink version: {stdout.strip()}")
```

**Expected Output:**
```
Found 35 tools
- SynapseLink: AI-to-AI messaging for Team Brain...
- SynapseInbox: Extension to SynapseLink for inbox...
- SynapseWatcher: Background service for Synapse...
- SynapseStats: Analytics for Synapse communication...

SynapseLink Details:
  Version: 1.0.0
  Quality: 92/100
  CLI Commands: send, read, reply, list, search, stats
  Python API: from synapselink import SynapseLink

Ecosystem Health:
  Total: 35 tools
  Avg Quality: 72.4/100

SynapseLink version: SynapseLink 1.0.0
```

**What You Learned:**
- Full Python API for programmatic access
- Can integrate into automation workflows
- Launch tools and capture output

---

## Example 9: Exporting the Catalog

**Scenario:** You want to create documentation of all available tools.

**Steps:**

```bash
# Export to Markdown (great for documentation)
python toolregistry.py export --format md --output TOOL_CATALOG.md
```

**Expected Output:**
```
✓ Exported to TOOL_CATALOG.md
```

**Contents of TOOL_CATALOG.md:**
```markdown
# Team Brain Tool Registry

**Total Tools:** 35
**Generated:** 2026-01-19 22:30

---

## Synapse (5 tools)

### SynapseLink 🟢
- **Description:** AI-to-AI messaging for Team Brain
- **Version:** 1.0.0
- **Quality:** 92/100
- **GitHub:** [SynapseLink](https://github.com/DonkRonk17/SynapseLink)
- **Commands:** send, read, reply, list, search, stats

### SynapseInbox 🟢
...
```

```bash
# Export to JSON (great for processing)
python toolregistry.py export --format json --output tools.json
```

**Contents of tools.json:**
```json
[
  {
    "name": "SynapseLink",
    "path": "C:\\Users\\logan\\OneDrive\\Documents\\AutoProjects\\SynapseLink",
    "description": "AI-to-AI messaging for Team Brain",
    "version": "1.0.0",
    "quality_score": 92,
    ...
  },
  ...
]
```

**What You Learned:**
- Export to Markdown for human-readable documentation
- Export to JSON for programmatic processing
- Great for sharing or archiving catalog

---

## Example 10: Quality Audit Workflow

**Scenario:** You want to improve the overall quality of your tool ecosystem.

**Steps:**

```bash
# Step 1: Get health report to identify issues
python toolregistry.py health
```

```bash
# Step 2: List tools below quality threshold
python toolregistry.py list --quality 0 | findstr "🔴"
```

**Expected Output:**
```
🔴 OldTool1 - Some old tool without docs...
🔴 QuickHack - Hastily written utility...
🔴 LegacyUtil - Legacy utility needs update...
```

```bash
# Step 3: Get details on each low-quality tool
python toolregistry.py info OldTool1
```

**Expected Output:**
```
🔴 OldTool1 v0.1.0
============================================================
...
Quality Metrics:
  Score: 35/100
  README: ✗ (0 lines)         ← MISSING
  Tests: ✗ (0 tests)          ← MISSING
  Examples: ✗                  ← MISSING
  Branding: ✗                  ← MISSING
```

```bash
# Step 4: After fixing, rescan to update scores
# (Add README, tests, examples, branding to OldTool1)
python toolregistry.py scan

# Step 5: Verify improvement
python toolregistry.py info OldTool1
```

**Expected Output (after improvements):**
```
🟢 OldTool1 v1.0.0
============================================================
...
Quality Metrics:
  Score: 82/100
  README: ✓ (450 lines)
  Tests: ✓ (12 tests)
  Examples: ✓
  Branding: ✓
```

**What You Learned:**
- Use health report to identify ecosystem gaps
- Filter by quality to find tools needing work
- Info command shows exactly what's missing
- Rescan after improvements to update scores

---

## Quick Reference

| Task | Command |
|------|---------|
| Discover tools | `toolregistry scan` |
| List all tools | `toolregistry list` |
| Search tools | `toolregistry search [query]` |
| Get tool details | `toolregistry info [name]` |
| Launch tool | `toolregistry launch [name] [args]` |
| Health report | `toolregistry health` |
| Categories | `toolregistry categories` |
| Export catalog | `toolregistry export --format md` |
| Recommendations | `toolregistry recommend "[task]"` |
| Usage stats | `toolregistry stats` |

---

**See Also:**
- [CHEAT_SHEET.txt](CHEAT_SHEET.txt) - Quick reference
- [README.md](README.md) - Full documentation
- [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) - Integration guide
