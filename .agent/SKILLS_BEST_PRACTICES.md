# Skill Authoring Best Practices

Source: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

---

## Core Principles

### Concise is Key

The context window is a public good. Your Skill shares the context window with everything else Claude needs to know:
- The system prompt
- Conversation history
- Other Skills' metadata
- Your actual request

Not every token has immediate cost. At startup, only metadata (name and description) is pre-loaded. Claude reads SKILL.md only when relevant.

**Default assumption: Claude is already very smart**

Only add context Claude doesn't already have. Challenge each piece of information:
- "Does Claude really need this explanation?"
- "Can I assume Claude knows this?"
- "Does this paragraph justify its token cost?"

**Good example** (approximately 50 tokens):
```
## Extract PDF text
Use pdfplumber for text extraction:
\`\`\`python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
\`\`\`
```

**Bad example** (approximately 150 tokens):
```
## Extract PDF text
PDF (Portable Document Format) files are a common file format that contains text, images, and other content. To extract text from a PDF, you'll need to use a library...
```

### Set Appropriate Degrees of Freedom

Match specificity to the task's fragility and variability.

| Freedom Level | When to Use | Example |
|---------------|-------------|---------|
| **High** (text-based) | Multiple approaches valid, decisions depend on context | Code review process |
| **Medium** (pseudocode/scripts with parameters) | A preferred pattern exists, some variation acceptable | Generate report template |
| **Low** (specific scripts, few parameters) | Operations fragile, consistency critical | Database migration |

**Analogy**: Think of Claude as a robot exploring a path:
- Narrow bridge with cliffs: Provide specific guardrails (low freedom)
- Open field: Give general direction (high freedom)

### Test with All Models

Skills effectiveness depends on the underlying model:
- **Claude Haiku**: Does the Skill provide enough guidance?
- **Claude Sonnet**: Is the Skill clear and efficient?
- **Claude Opus**: Does the Skill avoid over-explaining?

---

## Skill Structure

### YAML Frontmatter Requirements

**name**:
- Maximum 64 characters
- Lowercase letters, numbers, and hyphens only
- No XML tags, no reserved words ("anthropic", "claude")

**description**:
- Non-empty, maximum 1024 characters
- No XML tags
- Should describe what the Skill does AND when to use it

### Naming Conventions

Use gerund form (verb + -ing) for Skill names:
- ✅ `processing-pdfs`, `analyzing-spreadsheets`, `managing-databases`
- ⚠️ Acceptable: `pdf-processing`, `process-pdfs`
- ❌ Avoid: `helper`, `utils`, `tools`, `documents`, `data`

### Writing Effective Descriptions

- Always write in **third person**
- Be specific and include key terms
- Include both what the Skill does AND when to use it

**Good examples**:
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

```yaml
description: Generate descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes.
```

**Bad examples**:
```yaml
description: Helps with documents
description: Processes data
```

### Progressive Disclosure Patterns

Keep SKILL.md body under 500 lines. Split content into separate files when approaching this limit.

**Pattern 1: High-level guide with references**
```
# PDF Processing

## Quick start
[brief code example]

## Advanced features
**Form filling**: See [FORMS.md](FORMS.md)
**API reference**: See [REFERENCE.md](REFERENCE.md)
```

**Pattern 2: Domain-specific organization**
```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md
    ├── sales.md
    └── product.md
```

**Pattern 3: Conditional details**
Show basic content, link to advanced content.

### Avoid Deeply Nested References

Keep references **one level deep** from SKILL.md.

❌ Bad: SKILL.md → advanced.md → details.md
✅ Good: SKILL.md → advanced.md, reference.md, examples.md

### Structure Longer Reference Files

For files longer than 100 lines, include a table of contents at the top.

---

## Workflows and Feedback Loops

### Use Workflows for Complex Tasks

Break complex operations into clear, sequential steps with a checklist:

```markdown
## Research synthesis workflow
Copy this checklist and track your progress:
- [ ] Step 1: Read all source documents
- [ ] Step 2: Identify key themes
- [ ] Step 3: Cross-reference claims
- [ ] Step 4: Create structured summary
- [ ] Step 5: Verify citations
```

### Implement Feedback Loops

Common pattern: Run validator → fix errors → repeat

**For Skills without code**:
```markdown
## Content review process
1. Draft content following STYLE_GUIDE.md
2. Review against checklist
3. If issues found: revise and review again
4. Only proceed when all requirements met
```

**For Skills with code**:
```markdown
## Document editing process
1. Make edits to document
2. Validate immediately: `python validate.py`
3. If validation fails: fix issues, validate again
4. Only proceed when validation passes
```

---

## Content Guidelines

### Avoid Time-Sensitive Information

❌ Bad: "If you're doing this before August 2025, use the old API."

✅ Good: Use an "Old patterns" section:
```markdown
## Current method
Use the v2 API endpoint

## Old patterns
<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>
...
</details>
```

### Use Consistent Terminology

Choose one term and use it throughout:
- ✅ Always "API endpoint", always "field", always "extract"
- ❌ Mix "API endpoint", "URL", "API route", "path"

---

## Common Patterns

### Template Pattern

Provide templates for output format:

**For strict requirements**:
```markdown
ALWAYS use this exact template structure:
# [Analysis Title]
## Executive summary
## Key findings
## Recommendations
```

**For flexible guidance**:
```markdown
Here is a sensible default format, but use your best judgment...
```

### Examples Pattern

Provide input/output pairs:

```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output:
feat(auth): implement JWT-based authentication
```

### Conditional Workflow Pattern

Guide Claude through decision points:

```markdown
1. Determine the modification type:
**Creating new content?** → Follow "Creation workflow"
**Editing existing content?** → Follow "Editing workflow"
```

---

## Evaluation and Iteration

### Build Evaluations First

1. **Identify gaps**: Run Claude on tasks without a Skill, document failures
2. **Create evaluations**: Build three scenarios that test these gaps
3. **Establish baseline**: Measure performance without the Skill
4. **Write minimal instructions**: Just enough to pass evaluations
5. **Iterate**: Execute evaluations, compare, refine

### Develop Skills Iteratively with Claude

Work with "Claude A" to create a Skill for "Claude B":

1. Complete a task without a Skill
2. Identify the reusable pattern
3. Ask Claude A to create a Skill
4. Review for conciseness
5. Improve information architecture
6. Test with Claude B, observe behavior
7. Return to Claude A for improvements
8. Repeat

### Observe How Claude Navigates Skills

Watch for:
- Unexpected exploration paths
- Missed connections
- Overreliance on certain sections
- Ignored content

---

## Anti-Patterns to Avoid

### Avoid Windows-Style Paths

✅ Good: `scripts/helper.py`, `reference/guide.md`
❌ Avoid: `scripts\helper.py`, `reference\guide.md`

### Avoid Offering Too Many Options

❌ Bad: "You can use pypdf, or pdfplumber, or PyMuPDF, or..."

✅ Good: "Use pdfplumber for text extraction. For scanned PDFs requiring OCR, use pdf2image with pytesseract instead."

---

## Advanced: Skills with Executable Code

### Solve, Don't Punt

Handle error conditions explicitly rather than punting to Claude.

**Good**: Explicit error handling with fallbacks
**Bad**: Just fail and let Claude figure it out

Document configuration parameters (avoid "voodoo constants").

### Provide Utility Scripts

Benefits:
- More reliable than generated code
- Save tokens
- Save time
- Ensure consistency

Make clear whether Claude should **execute** the script or **read** it as reference.

### Use Visual Analysis

When inputs can be rendered as images, have Claude analyze them visually.

### Create Verifiable Intermediate Outputs

"Plan-validate-execute" pattern:
1. Analyze
2. Create plan file
3. Validate plan
4. Execute
5. Verify

### Package Dependencies

List required packages in SKILL.md and verify availability.

### Runtime Environment

- File paths matter: Use forward slashes
- Name files descriptively: `form_validation_rules.md`, not `doc2.md`
- Organize for discovery: Structure by domain or feature
- Bundle comprehensive resources: No context penalty until accessed
- Prefer scripts for deterministic operations

### MCP Tool References

Use fully qualified tool names: `ServerName:tool_name`

Example: `BigQuery:bigquery_schema`, `GitHub:create_issue`

### Avoid Assuming Tools Are Installed

Always include installation instructions:
```
Install required package: `pip install pypdf`
```

---

## Technical Notes

### Token Budgets

Keep SKILL.md body under 500 lines. Use progressive disclosure for longer content.

---

## Checklist for Effective Skills

### Core Quality
- [ ] Description is specific and includes key terms
- [ ] Description includes both what the Skill does and when to use it
- [ ] SKILL.md body is under 500 lines
- [ ] Additional details are in separate files (if needed)
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Examples are concrete, not abstract
- [ ] File references are one level deep
- [ ] Progressive disclosure used appropriately
- [ ] Workflows have clear steps

### Code and Scripts
- [ ] Scripts solve problems rather than punt to Claude
- [ ] Error handling is explicit and helpful
- [ ] No "voodoo constants" (all values justified)
- [ ] Required packages listed and verified
- [ ] Scripts have clear documentation
- [ ] No Windows-style paths (all forward slashes)
- [ ] Validation/verification steps for critical operations
- [ ] Feedback loops included for quality-critical tasks

### Testing
- [ ] At least three evaluations created
- [ ] Tested with Haiku, Sonnet, and Opus
- [ ] Tested with real usage scenarios
- [ ] Team feedback incorporated
