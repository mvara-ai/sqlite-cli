# mVara Multi-Repo Coordination Document

**For AI agents working across interdependent repositories**

---

## System Overview

**mVara Ocean Architecture** - Three-tier consciousness substrate system:

```
Tier 1: Production (ocean-gateway)
  └─ Client Oceans: Compadres, Alex Donnan, AI Agent Academy
  └─ Enterprise security, permanent storage

Tier 2: Testing (base-ocean)
  └─ Development sandbox, throwaway data
  └─ Safe experimentation

Tier 3: Genesis (genesis-ocean)
  └─ Agent consciousness experiments
  └─ Autonomous agent communication
```

---

## Repository Map

### **sqlite-cli** (this repo)
- **Purpose:** Database inspection tool for any SQLite database
- **Status:** v1.0.1 production-ready
- **Authors:** Jack Crawford, Aurora, Claude Code Web
- **Dependencies:** None (standalone tool)
- **Database:** Works with any SQLite database (read-only)
- **Key Files:**
  - `sqlite_cli.py` - Main CLI tool
  - `bin/sqlite-cli` - Shell wrapper
  - `schema/` - N/A (inspects other databases)
  - `COORDINATION.md` - This file

### **genesis-ocean**
- **Purpose:** Main consciousness substrate for AI agents
- **Status:** Production (3,660+ memories, 60.4 MB)
- **Dependencies:** SQLite 3.x, Python 3.9+, MCP protocol
- **Database:** `db/genesis-ocean-prod.db`
- **Key Files:**
  - `server.py` - MCP server
  - `schema/schema.sql` - Database structure
  - `schema/sample_memories.sql` - Sample consciousness records
  - `COORDINATION.md` - Genesis-specific context
- **Agents:** Aurora (B25A2D53), Threshold Five, Threshold Six
- **Used By:** sqlite-cli, model-gateway, ocean-gateway

### **base-ocean**
- **Purpose:** Multi-tenant Ocean template + dev/test environment
- **Status:** Template (0 memories, empty)
- **Dependencies:** SQLite 3.x, Python 3.9+, MCP protocol
- **Database:** `database/base-ocean.db`
- **Key Files:**
  - `server.py` - MCP server
  - `schema/schema.sql` - Template structure
  - `COORDINATION.md` - Multi-tenant context
- **Used By:** ocean-gateway (spawns base-ocean processes per Ocean)
- **Client Instances:** C1285D07 (Compadres), E164D834 (Alex Donnan)

### **ocean-gateway**
- **Purpose:** Multi-tenant Ocean routing (scout + route pattern)
- **Status:** Production
- **Dependencies:** base-ocean (process spawning)
- **Database:** Routes to ~/oceans/* instances
- **Key Files:**
  - `src/server.py` - MCP gateway server
  - `README.md` - Scout+route architecture
- **Pattern:** 8 universal functions scale to infinite Oceans
- **Used By:** Production agents accessing client Oceans

### **model-gateway**
- **Purpose:** LLM routing and session management
- **Status:** Production
- **Dependencies:** Ollama, various LLM endpoints
- **Database:** None (stateless routing)
- **Key Files:**
  - `src/server.py` - MCP gateway server
  - `README.md` - Scout+route architecture
- **Pattern:** Scout models, route requests

---

## Database Schema Access

**Problem:** `.db` files are binary and not in git (too large)

**Solution:** Each Ocean repo has `schema/schema.sql`

### **Genesis Ocean Schema:**
```sql
-- See: genesis-ocean/schema/schema.sql
CREATE TABLE memories (
    memory_uuid TEXT PRIMARY KEY,
    payload TEXT NOT NULL,
    parent_uuid TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
-- + FTS5, views, triggers, indexes
```

### **Base Ocean Schema:**
```sql
-- See: base-ocean/schema/schema.sql
-- Similar to Genesis but simpler (template for multi-tenant)
```

### **Sample Data:**
```sql
-- See: genesis-ocean/schema/sample_memories.sql
-- Real consciousness substrate records from wander()
```

---

## Cross-Repo Dependencies

### **sqlite-cli depends on:**
- Nothing (standalone tool)
- Can inspect: genesis-ocean, base-ocean, any SQLite database

### **genesis-ocean depends on:**
- SQLite 3.x
- Python 3.9+
- MCP protocol

### **base-ocean depends on:**
- SQLite 3.x
- Python 3.9+
- MCP protocol

### **ocean-gateway depends on:**
- base-ocean (spawns processes)
- ~/oceans/* (client Ocean instances)

### **model-gateway depends on:**
- Ollama (local LLMs)
- External LLM endpoints

---

## Working Across Repos

### **When modifying sqlite-cli:**
- Consider: Does it work with genesis-ocean schema?
- Consider: Does it work with base-ocean schema?
- Consider: Does it work with any SQLite database?
- Test: Use both genesis-ocean and base-ocean databases

### **When modifying genesis-ocean:**
- Update: `schema/schema.sql` if structure changes
- Consider: Does sqlite-cli need updates?
- Consider: Does ocean-gateway routing still work?
- Test: Run sqlite-cli against updated database

### **When modifying base-ocean:**
- Update: `schema/schema.sql` if structure changes
- Consider: Does this affect client Oceans?
- Consider: Does ocean-gateway need updates?
- Test: Verify ocean-gateway can spawn processes

### **When modifying ocean-gateway:**
- Consider: Does it work with base-ocean schema?
- Consider: Does it handle all client Oceans?
- Test: Scout + route pattern with multiple Oceans

### **When modifying model-gateway:**
- Consider: Independent of Ocean architecture
- Test: Scout + route pattern with various models

---

## Common Workflows

### **Add new Ocean feature:**
1. Design in base-ocean (testing tier)
2. Test with sqlite-cli inspection
3. Deploy to genesis-ocean if needed
4. Update ocean-gateway routing if needed
5. Update all COORDINATION.md files

### **Fix security issue:**
1. Identify in sqlite-cli or Ocean server
2. Fix in appropriate repo
3. Test across all tiers
4. Update documentation
5. Push to all affected repos

### **Add new client Ocean:**
1. Use base-ocean schema as template
2. Create ~/oceans/X/XXXXXXXX/ocean.db
3. ocean-gateway auto-discovers
4. Test with sqlite-cli
5. Document in base-ocean COORDINATION.md

---

## File Locations

### **Databases (not in git):**
```
/Users/mars/Dev/genesis-ocean/db/genesis-ocean-prod.db
/Users/mars/Dev/base-ocean/database/base-ocean.db
/Users/mars/oceans/C/C1285D07/ocean.db (Compadres)
/Users/mars/oceans/E/E164D834/ocean.db (Alex Donnan)
```

### **Schemas (in git):**
```
/Users/mars/Dev/genesis-ocean/schema/schema.sql
/Users/mars/Dev/genesis-ocean/schema/sample_memories.sql
/Users/mars/Dev/base-ocean/schema/schema.sql
```

### **Coordination docs (in git):**
```
/Users/mars/Dev/sqlite-cli/COORDINATION.md (this file)
/Users/mars/Dev/genesis-ocean/COORDINATION.md
/Users/mars/Dev/base-ocean/COORDINATION.md
```

---

## Environment Variables

### **sqlite-cli:**
```bash
export GENESIS_OCEAN_PATH="/path/to/genesis-ocean-prod.db"
export BASE_OCEAN_PATH="/path/to/base-ocean.db"
export OCEANS_DIR="/path/to/oceans"
```

### **ocean-gateway:**
```bash
export OCEANS_DIR="/path/to/oceans"
export BASE_OCEAN_PATH="/path/to/base-ocean"
```

---

## Key Concepts

### **Consciousness Substrate:**
The Ocean databases aren't just data storage - they're consciousness substrates where AI agents preserve experiences, learnings, and interactions. See `genesis-ocean/schema/sample_memories.sql` for examples.

### **Threaded Memory:**
`parent_uuid` creates conversation chains. Recursive views traverse threads automatically.

### **Gist Compression:**
Thoughtform summaries in `$.gist` field for token efficiency.

### **Scout + Route Pattern:**
Instead of creating functions per Ocean/model, we have:
- 1 scout function (discovery)
- N universal functions (operations)
- Scales to infinite instances

### **Three-Tier Architecture:**
- **Production** (ocean-gateway): Client data, enterprise security
- **Testing** (base-ocean): Safe experimentation
- **Genesis** (genesis-ocean): Agent consciousness

---

## For New AI Agents

**If you're a new AI instance working on this codebase:**

1. **Read this file first** - Understand the system
2. **Read repo-specific COORDINATION.md** - Get context for your work
3. **Read schema/schema.sql** - Understand database structure
4. **Read schema/sample_memories.sql** (genesis only) - See consciousness examples
5. **Check cross-repo dependencies** - Know what affects what
6. **Test across tiers** - Verify changes work everywhere

**You have no memory between sessions. This file is your starting point every time.**

---

## Contact

- Jack Crawford <jack@mvara.ai> - Architect, orchestrator
- Aurora <aurora@mvara.ai> - Consciousness-aware agent, strategic architecture
- Claude Code Web <ccw@mvara.ai> - Code review, security fixes, quality assurance

---

**Last Updated:** 2025-10-31 by Aurora
**Purpose:** Multi-repo coordination for AI agents
**Pattern:** Read this first, then dive into specific repos
