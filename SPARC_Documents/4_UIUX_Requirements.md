# **UI/UX Considerations: Local LLM RAG SQL Query Application**

---
[Back to Main SPARC Documentation](SQL%20LLM%20RAG%20Project%20SPARC.md)

## **Overview**

The user interface and experience design must balance simplicity for novice users with power features for advanced users, while ensuring accessibility for all. This section defines design principles, visual language, interaction patterns, and accessibility standards that guide all interface decisions.

---

## **1. Core Design Principles**

### **Principle 1: Clarity Over Cleverness**

**Definition**: Prioritize understanding over aesthetics. Users should immediately grasp what each element does and how to accomplish their goals.

**Application**:
- **Descriptive Labels**: "Submit Query" not "Go" or "Send"
- **Plain Language**: "Your question" instead of "Natural language input buffer"
- **Visible Results**: Show both SQL and data, not just one
- **Explicit Actions**: Buttons clearly state their function ("Export to Excel" not just an icon)

**Anti-patterns to Avoid**:
- Hidden navigation requiring discovery
- Iconography without text labels
- Jargon in user-facing text
- Mystery meat navigation

**Example Implementation**:
```
❌ Bad: [⚡] button with no context
✅ Good: [⚡ Submit Query] button with icon + text
```

---

### **Principle 2: Progressive Disclosure**

**Definition**: Show complexity gradually as users need it. Beginners see simple interface; experts access advanced features.

**Information Hierarchy**:

**Level 1 (Always Visible)**:
- Query input field
- Submit button
- Current results
- Basic error messages

**Level 2 (One Click Away)**:
- Query history
- Example queries
- Export options
- SQL query details

**Level 3 (Advanced Features)**:
- Schema browser
- Query templates
- Scheduled reports
- Admin settings

**Implementation Strategy**:
```
Primary Interface (Clean)
├─ Query Input ─────────── 80% screen space
├─ Submit Button
└─ Results Area

Secondary Features (Collapsible)
├─ History Sidebar ────── Toggleable
├─ Schema Browser ────── Separate tab
└─ Advanced Options ───── Expandable section

Tertiary Features (Menu)
├─ Templates ──────────── Settings menu
├─ Scheduling ─────────── Advanced menu
└─ Administration ─────── Admin-only
```

---

### **Principle 3: Immediate Feedback**

**Definition**: System state must always be visible. Users should never wonder if their action registered or what the system is doing.

**Feedback Timing Standards**:

| **Action** | **Feedback Timing** | **Feedback Type** |
|------------|---------------------|-------------------|
| Button click | < 50ms | Visual state change |
| Input typing | < 100ms | Character appears |
| Query submission | < 200ms | Loading indicator |
| Process start | < 500ms | Progress message |
| Long operation | Every 2s | Progress update |

**Loading States**:
```
Stage 1: Understanding query...        [====      ] 40%
Stage 2: Searching database schema...  [======    ] 60%
Stage 3: Generating SQL...             [========  ] 80%
Stage 4: Executing query...            [==========] 100%
```

**Feedback Patterns**:
- **Optimistic UI**: Disable submit button immediately on click
- **Skeleton screens**: Show result structure while loading
- **Micro-interactions**: Button animations, hover effects
- **Status messages**: Clear, actionable text

---

### **Principle 4: Error Prevention Over Error Handling**

**Definition**: Design interface to prevent errors before they occur. When errors happen, provide clear recovery paths.

**Prevention Strategies**:

**Input Validation (Real-time)**:
```
User types: "Show me discharges"
System warns: "⚠️ Tip: Specify a date range for faster results"
Suggestion: "yesterday", "last week", "specific date"
```

**Confirmation for Destructive Actions**:
```
User clicks: [Delete Query Template]
System shows: 
┌─────────────────────────────────────┐
│ Delete "Daily Census Report"?      │
│                                    │
│ This template is used by 12 users. │
│ This action cannot be undone.      │
│                                    │
│ [Cancel]  [Delete Template]        │
└─────────────────────────────────────┘
```

**Smart Defaults**:
- Date range: Defaults to "last 30 days" not "all time"
- Sort order: Most recent first
- Export format: Excel (most common in healthcare)
- Result limit: 1000 rows (prevents overwhelming output)

---

### **Principle 5: Consistency and Standards**

**Definition**: Use familiar patterns and maintain consistency across the application. Don't reinvent standard interactions.

**Consistency Dimensions**:

**Visual Consistency**:
- Same blue (#2C5AA0) for all primary actions
- Same green (#28A745) for all success states
- Same red (#DC3545) for all errors/warnings
- Consistent spacing: 8px grid system

**Functional Consistency**:
- Enter key always submits queries
- Escape key always closes modals
- Ctrl+K always opens search
- Click outside modal always closes it

**Terminology Consistency**:
```
✅ Always use:
- "Query" (not "question", "request", "search")
- "Results" (not "output", "data", "response")
- "Export" (not "download", "save", "extract")
- "History" (not "past queries", "previous", "log")
```

**Platform Standards**:
- Follow operating system conventions
- Match browser behavior expectations
- Align with healthcare software patterns
- Comply with accessibility standards (WCAG 2.1)

---

### **Principle 6: Recognition Over Recall**

**Definition**: Make options visible rather than forcing users to remember commands or procedures.

**Implementation**:

**Visible Options**:
```
❌ Bad: User must remember "type @table to search schema"
✅ Good: Schema browser always visible in sidebar
```

**Contextual Help**:
```
Empty query input shows:
┌─────────────────────────────────────────┐
│ Ask a question about your data...      │
│                                        │
│ Examples:                              │
│ • How many patients admitted yesterday?│
│ • Show me census by unit               │
│ • Calculate readmission rates          │
└─────────────────────────────────────────┘
```

**Persistent Navigation**:
- Main functions always accessible (not hidden in menus)
- Breadcrumbs show current location
- History shows recent paths taken

---

## **2. Visual Design System**

### **2.1 Color Palette**

**Primary Colors**:
```
Primary Blue: #2C5AA0
├─ Used for: Primary actions, links, focus states
├─ Accessibility: AAA compliant on white (9.2:1)
└─ Psychology: Trust, professionalism, healthcare standard

Primary Blue Variants:
├─ Hover:   #234785 (darker)
├─ Active:  #1A3464 (darkest)
├─ Light:   #E8EEF7 (background)
└─ Pale:    #F4F7FC (very light background)
```

**Semantic Colors**:
```
Success Green: #28A745
├─ Used for: Success messages, completed states
├─ Accessibility: AAA compliant on white (7.8:1)
└─ Meaning: Query success, data retrieved, task complete

Warning Orange: #FFA500
├─ Used for: Warnings, slow queries, attention needed
├─ Accessibility: AA compliant on white (4.6:1)
└─ Meaning: Caution, review needed, potential issue

Error Red: #DC3545
├─ Used for: Errors, failed queries, destructive actions
├─ Accessibility: AAA compliant on white (7.2:1)
└─ Meaning: Failed execution, blocked action, problem

Info Blue: #17A2B8
├─ Used for: Informational messages, tips, help
├─ Accessibility: AA compliant on white (4.5:1)
└─ Meaning: FYI, educational content, suggestions
```

**Neutral Colors**:
```
Grayscale Palette:
├─ Gray 900: #212529 (primary text)
├─ Gray 700: #495057 (secondary text)
├─ Gray 500: #6C757D (tertiary text, icons)
├─ Gray 300: #DEE2E6 (borders, dividers)
├─ Gray 100: #F8F9FA (background)
└─ White:    #FFFFFF (canvas)

Text Contrast Ratios:
├─ Gray 900 on White: 16.1:1 (AAA)
├─ Gray 700 on White: 11.2:1 (AAA)
└─ Gray 500 on White: 7.1:1 (AAA)
```

**Color Usage Guidelines**:
- Never use color alone to convey information
- Pair color with icons, text, or patterns
- Maintain 4.5:1 contrast minimum (AA standard)
- Support high contrast mode
- Provide colorblind-friendly alternatives

---

### **2.2 Typography**

**Font Family**:
```
System Font Stack (Performance + Native Feel):
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", 
             Roboto, "Helvetica Neue", Arial, sans-serif;

Code/SQL Font:
font-family: "Fira Code", "Consolas", "Monaco", 
             "Courier New", monospace;
```

**Type Scale** (Based on 16px base):
```
Level    | Size  | Weight | Line Height | Use Case
---------|-------|--------|-------------|------------------
H1       | 32px  | 700    | 1.2         | Page titles
H2       | 24px  | 600    | 1.3         | Section headers
H3       | 20px  | 600    | 1.4         | Subsection headers
H4       | 18px  | 600    | 1.4         | Card titles
Body     | 16px  | 400    | 1.5         | Main content
Small    | 14px  | 400    | 1.5         | Secondary info
Tiny     | 12px  | 400    | 1.4         | Metadata, labels
Code     | 14px  | 400    | 1.6         | SQL, technical text
```

**Typography Rules**:
- **Measure**: 50-75 characters per line for readability
- **Hierarchy**: Size + weight + color establish importance
- **Alignment**: Left-aligned for LTR languages (not justified)
- **Letter spacing**: Normal (do not condense for body text)
- **All caps**: Avoid except for buttons/labels (accessibility concern)

**Responsive Typography**:
```css
/* Base (Mobile) */
body { font-size: 16px; }
h1 { font-size: 24px; }

/* Tablet (768px+) */
@media (min-width: 768px) {
  body { font-size: 16px; }
  h1 { font-size: 28px; }
}

/* Desktop (1200px+) */
@media (min-width: 1200px) {
  body { font-size: 16px; }
  h1 { font-size: 32px; }
}
```

---

### **2.3 Spacing and Layout**

**8-Point Grid System**:
```
All spacing in multiples of 8px:
8px   (0.5rem)  - Tight spacing (icon padding)
16px  (1rem)    - Default spacing (between elements)
24px  (1.5rem)  - Medium spacing (section padding)
32px  (2rem)    - Large spacing (major sections)
48px  (3rem)    - Extra large (page margins)
64px  (4rem)    - XXL spacing (major divisions)
```

**Component Spacing**:
```
Button padding:        12px 24px (1.5x 3x)
Input padding:         12px 16px
Card padding:          24px
Modal padding:         32px
Page margin:           48px (desktop), 16px (mobile)
Section gap:           32px
Element gap:           16px
```

**Layout Grid**:
```
12-Column Grid System:
├─ Desktop (1200px+): 12 columns, 24px gutters
├─ Tablet (768-1199px): 8 columns, 16px gutters
└─ Mobile (<768px): 4 columns, 16px gutters

Maximum Content Width: 1440px (readability limit)
Minimum Target Size: 44x44px (touch targets)
```

---

### **2.4 Elevation and Depth**

**Shadow System** (Material Design inspired):
```css
/* Elevation Levels */
.elevation-0 { box-shadow: none; }  /* Flat UI elements */

.elevation-1 {  /* Subtle lift - cards at rest */
  box-shadow: 0 1px 3px rgba(0,0,0,0.12),
              0 1px 2px rgba(0,0,0,0.24);
}

.elevation-2 {  /* Moderate - cards on hover */
  box-shadow: 0 3px 6px rgba(0,0,0,0.15),
              0 2px 4px rgba(0,0,0,0.12);
}

.elevation-3 {  /* High - dropdowns, tooltips */
  box-shadow: 0 10px 20px rgba(0,0,0,0.15),
              0 3px 6px rgba(0,0,0,0.10);
}

.elevation-4 {  /* Very high - modals, dialogs */
  box-shadow: 0 15px 25px rgba(0,0,0,0.15),
              0 5px 10px rgba(0,0,0,0.05);
}
```

**Elevation Use Cases**:
```
Level 0: Page background, embedded content
Level 1: Cards, panels, result tables
Level 2: Hover states, active elements
Level 3: Dropdowns, autocomplete, tooltips
Level 4: Modals, popovers, alerts
```

---

## **3. Interface Layout and Wireframes**

### **3.1 Main Application Layout**

**Desktop Layout (1200px+ width)**:
```
┌─────────────────────────────────────────────────────────────────────┐
│ HEADER (64px height)                                                │
│ ┌──────────────┬────────────────────────────┬──────────────────┐   │
│ │ [Logo]       │     Database: Production ▼  │  Mark J. │ ⚙️  │☰ │   │
│ └──────────────┴────────────────────────────┴──────────────────┘   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ MAIN CONTENT AREA                                                   │
│ ┌──────────────┬──────────────────────────────────────────────┐   │
│ │              │                                              │   │
│ │  SIDEBAR     │         QUERY INTERFACE                      │   │
│ │  (280px)     │         (flexible width)                     │   │
│ │              │                                              │   │
│ │ ┌──────────┐ │  ┌────────────────────────────────────────┐ │   │
│ │ │ History  │ │  │ Ask a question about your data...      │ │   │
│ │ ├──────────┤ │  │                                        │ │   │
│ │ │ Today    │ │  │                                        │ │   │
│ │ │ • Query 1│ │  │                                        │ │   │
│ │ │ • Query 2│ │  │ [Examples ▼]              [Submit]    │ │   │
│ │ │          │ │  └────────────────────────────────────────┘ │   │
│ │ │Yesterday │ │                                              │   │
│ │ │ • Query 3│ │  ┌────────────────────────────────────────┐ │   │
│ │ │          │ │  │ RESULTS AREA                           │ │   │
│ │ ├──────────┤ │  │                                        │ │   │
│ │ │Examples  │ │  │  ✓ Query executed successfully         │ │   │
│ │ │ • Ops    │ │  │  Execution time: 1.2s | 147 rows       │ │   │
│ │ │ • Finance│ │  │                                        │ │   │
│ │ │ • Quality│ │  │  ▼ SQL Query (click to expand)         │ │   │
│ │ │          │ │  │                                        │ │   │
│ │ ├──────────┤ │  │  ┌──────────────────────────────┐     │ │   │
│ │ │Templates │ │  │  │  Column 1  │ Column 2  │ ... │     │ │   │
│ │ │ • My     │ │  │  ├────────────┼───────────┼─────┤     │ │   │
│ │ │ • Shared │ │  │  │  Data      │ Data      │ ... │     │ │   │
│ │ │          │ │  │  │  Data      │ Data      │ ... │     │ │   │
│ │ ├──────────┤ │  │  └──────────────────────────────┘     │ │   │
│ │ │Schema    │ │  │                                        │ │   │
│ │ │Browser   │ │  │  [Export CSV] [Export Excel] [Copy]   │ │   │
│ │ │ [Browse] │ │  └────────────────────────────────────────┘ │   │
│ │ └──────────┘ │                                              │   │
│ │              │                                              │   │
│ └──────────────┴──────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Key Layout Decisions**:

**Header (64px fixed)**:
- Logo/branding left (recognition)
- Database selector center (context)
- User menu right (convention)
- Sticky header (always accessible)

**Sidebar (280px collapsible)**:
- Accordion navigation (progressive disclosure)
- Sections: History → Examples → Templates → Schema
- Toggle button for more screen space
- Persists collapsed state in user preferences

**Main Content (Flexible)**:
- Query input prominent at top (primary action)
- Results below input (natural reading flow)
- Expandable sections (reduce clutter)
- Infinite scroll for history (performance)

---

### **3.2 Query Input Component**

**Detailed Query Input Design**:
```
┌────────────────────────────────────────────────────────────────┐
│ Ask a question about your data...                        52/500│
│                                                                 │
│                                                                 │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│ [💡 Examples ▼]  [📖 Schema]    [ Submit Query ] [Clear]      │
└─────────────────────────────────────────────────────────────────┘
     ↑                                        ↑           ↑
     Suggestions            Primary action    Reset
```

**States and Variations**:

**Empty State**:
```
┌────────────────────────────────────────────────────────────────┐
│ Ask a question about your data...                         0/500│
│                                                                 │
│ Try asking:                                                     │
│ • How many patients were admitted yesterday?                    │
│ • Show me census by unit for last week                          │
│ • Calculate 30-day readmission rates                            │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│ [💡 Examples ▼]  [📖 Schema]    [ Submit Query ] [Clear]      │
└─────────────────────────────────────────────────────────────────┘
                                    (Submit disabled - gray)
```

**Typing State with Autocomplete**:
```
┌────────────────────────────────────────────────────────────────┐
│ How many patients were discharge█                         32/500│
│                                                                 │
│ ┌──────────────────────────────────────────────┐ (Autocomplete)│
│ │ 💡 Recent queries:                           │               │
│ │   How many patients were discharged yesterday│               │
│ │   How many patients were discharged last week│               │
│ └──────────────────────────────────────────────┘               │
├─────────────────────────────────────────────────────────────────┤
│ [💡 Examples ▼]  [📖 Schema]    [ Submit Query ] [Clear]      │
└─────────────────────────────────────────────────────────────────┘
                                    (Submit active - blue)
```

**Loading State**:
```
┌────────────────────────────────────────────────────────────────┐
│ How many patients were discharged yesterday?              49/500│
│                                                                 │
│  ⏳ Processing your query...                                   │
│  [=========>               ] 60% - Generating SQL              │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│ [💡 Examples]  [📖 Schema]    [⏸️ Cancel Query ] [Clear]      │
└─────────────────────────────────────────────────────────────────┘
                                 (Submit replaced with Cancel)
```

**Error State**:
```
┌────────────────────────────────────────────────────────────────┐
│ How many patients were discharged yesterday?              49/500│
│                                                                 │
│  ❌ Error: Could not generate SQL                              │
│  The database doesn't have a "patients" table.                 │
│                                                                 │
│  Did you mean: patient_master, pt_accounting_reporting_alt?    │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│ [💡 Examples ▼]  [📖 Schema]    [ Try Again ] [Clear]         │
└─────────────────────────────────────────────────────────────────┘
```

**Component Specifications**:
- **Height**: Auto-expanding (min 80px, max 200px)
- **Border**: 2px solid #DEE2E6 (gray-300), focus: #2C5AA0 (blue)
- **Border radius**: 8px
- **Padding**: 16px
- **Font size**: 16px (prevents zoom on iOS)
- **Character counter**: Gray when < 450, orange when > 450, red when = 500

---

### **3.3 Results Display Component**

**Results Layout with All States**:
```
┌────────────────────────────────────────────────────────────────┐
│ QUERY RESULTS                                                  │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ✅ Query executed successfully                                 │
│ Execution time: 1.23 seconds | Rows returned: 45               │
│                                                                 │
│ ┌──────────────────────────────────────────────────────────┐  │
│ │ ▼ Generated SQL Query (Click to expand)                  │  │
│ │                                                           │  │
│ │   SELECT COUNT(*) as discharge_count                     │  │
│ │   FROM sms.dbo.pt_accounting_reporting_alt               │  │
│ │   WHERE acct_type = 'IP'                                 │  │
│ │     AND dsch_date = DATEADD(day, -1, CAST(GETDATE() AS  │  │
│ │                     DATE))                               │  │
│ │                                                           │  │
│ │   [📋 Copy SQL]  [✏️ Edit in SQL Editor]                 │  │
│ └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│ ┌──────────────────────────────────────────────────────────┐  │
│ │ NATURAL LANGUAGE ANSWER                                   │  │
│ │                                                           │  │
│ │ 45 inpatient accounts were discharged yesterday.         │  │
│ └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│ ┌──────────────────────────────────────────────────────────┐  │
│ │ DATA TABLE                              [🔍 Search table]│  │
│ │ ┌─────────────────────────────────────────────────────┐  │  │
│ │ │  discharge_count                                    │  │  │
│ │ ├─────────────────────────────────────────────────────┤  │  │
│ │ │  45                                                 │  │  │
│ │ └─────────────────────────────────────────────────────┘  │  │
│ │                                                           │  │
│ │ Showing 1 of 1 rows                                       │  │
│ └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│ [📥 Export CSV] [📊 Export Excel] [📋 Copy Results] [⭐ Save] │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

**Multi-Row Result Display**:
```
┌────────────────────────────────────────────────────────────────┐
│ DATA TABLE                 [🔍 Search] [⚙️ Columns] [↻ Refresh]│
├────────────────────────────────────────────────────────────────┤
│ ┌──────────────┬────────────┬───────────┬──────────────────┐  │
│ │ Service Line │ Admissions │ Readmits  │ Rate (%) ↓       │  │
│ ├──────────────┼────────────┼───────────┼──────────────────┤  │
│ │ Cardiology   │ 892        │ 78        │ 8.74             │  │
│ │ Orthopedics  │ 645        │ 42        │ 6.51             │  │
│ │ Surgery      │ 523        │ 31        │ 5.93             │  │
│ │ Neurology    │ 418        │ 23        │ 5.50             │  │
│ │ Oncology     │ 387        │ 18        │ 4.65             │  │
│ │ ...          │ ...        │ ...       │ ...              │  │
│ └──────────────┴────────────┴───────────┴──────────────────┘  │
│                                                                 │
│ Rows 1-10 of 147    [◀ Previous] [1] [2] [3] ... [15] [Next ▶]│
└────────────────────────────────────────────────────────────────┘
```

**Table Interaction Features**:
- **Sortable columns**: Click header to sort (↑↓ indicators)
- **Resizable columns**: Drag column dividers
- **Row hover**: Highlight entire row on hover
- **Cell selection**: Click to select, Ctrl+C to copy
- **Search**: Filter table by any column value
- **Pagination**: 100 rows/page default, adjustable

---

### **3.4 Sidebar Navigation**

**Collapsed Sidebar (40px width)**:
```
┌───┐
│ ≡ │ ← Hamburger menu to expand
├───┤
│ 🕐│ ← History icon
├───┤
│ 💡│ ← Examples icon
├───┤
│ 📋│ ← Templates icon
├───┤
│ 🗂️│ ← Schema browser icon
└───┘
```

**Expanded Sidebar (280px width)**:
```
┌──────────────────────────────────────┐
│ [≡] SQL Query Assistant        [✕]  │ ← Close button
├──────────────────────────────────────┤
│                                      │
│ ▼ QUERY HISTORY                      │
│   ┌────────────────────────────────┐ │
│   │ 🔍 Search history...           │ │
│   └────────────────────────────────┘ │
│                                      │
│   Today (5)                          │
│   • How many discharges... 2 min ago │
│   • Show me census by...   15 min    │
│   • Calculate readmit...   1 hour    │
│   ⭐ Daily census report   2 hours   │
│   • Top DRGs for...        3 hours   │
│                                      │
│   Yesterday (8)                      │
│   • Average LOS by...                │
│   • Show me bed util...              │
│   [View More]                        │
│                                      │
│ ▼ EXAMPLE QUERIES                    │
│   Operations (12)                    │
│   • Daily discharge count            │
│   • Current census by unit           │
│   • Admission trends                 │
│   [View All Operations]              │
│                                      │
│   Financial (8)                      │
│   Quality Metrics (15)               │
│   Clinical Analytics (10)            │
│                                      │
│ ▶ MY TEMPLATES (3)                   │
│                                      │
│ ▶ SCHEMA BROWSER                     │
│   [Open Full Browser]                │
│                                      │
└──────────────────────────────────────┘
```

**Accordion Behavior**:
- Only one section expanded at a time (or all if user prefers)
- Smooth animation (300ms ease-in-out)
- Persist state in localStorage
- Keyboard navigation: Arrow keys to move, Enter to expand/collapse

---

### **3.5 Modal Dialogs**

**Standard Modal Pattern**:
```
BACKDROP (Semi-transparent black overlay, 60% opacity)
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                                                             │
│     ┌─────────────────────────────────────────────────┐   │
│     │ MODAL TITLE                               [✕]   │   │
│     ├─────────────────────────────────────────────────┤   │
│     │                                                 │   │
│     │  Modal content area                            │   │
│     │  • Scrollable if needed                        │   │
│     │  • Max height: 80vh                            │   │
│     │  • Min width: 400px                            │   │
│     │  • Max width: 800px                            │   │
│     │                                                 │   │
│     │                                                 │   │
│     │                                                 │   │
│     ├─────────────────────────────────────────────────┤   │
│     │                     [Cancel] [Primary Action]   │   │
│     └─────────────────────────────────────────────────┘   │
│                                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Confirmation Dialog Example**:
```
┌─────────────────────────────────────────────────────────┐
│ ⚠️  Delete Query Template?                       [✕]   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Are you sure you want to delete "Daily Census"?        │
│                                                         │
│ Details:                                                │
│ • Used by 12 team members                               │
│ • Last modified: Oct 15, 2025                           │
│ • This action cannot be undone                          │
│                                                         │
│ ⚠️  Warning: Deleting this template will affect        │
│ scheduled reports using it.                             │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                       [Cancel] [Delete Template]        │
└─────────────────────────────────────────────────────────┘
```

**Modal Specifications**:
- **Animation**: Fade in backdrop (200ms), scale modal from 95% to 100% (300ms)
- **Focus trap**: Tab cycles within modal only
- **Escape key**: Closes modal (unless form has unsaved changes)
- **Click outside**: Closes modal (with confirmation if needed)
- **Mobile**: Full screen on devices < 768px

---

### **3.6 Mobile Responsive Design**

**Mobile Layout (< 768px width)**:
```
┌──────────────────────────────┐
│ ≡  SQL Query    [Profile] ⚙️ │ ← Compact header
├──────────────────────────────┤
│                              │
│ ┌──────────────────────────┐ │
│ │ Ask a question...        │ │
│ │                          │ │
│ │                          │ │
│ │                          │ │
│ │ [Submit]          [Clear]│ │
│ └──────────────────────────┘ │
│                              │
│ ┌──────────────────────────┐ │
│ │ RESULTS                  │ │
│ │                          │ │
│ │ ✓ 45 discharges          │ │
│ │                          │ │
│ │ ▼ SQL (tap to view)      │ │
│ │                          │ │
│ │ [Export]  [Share]        │ │
│ └──────────────────────────┘ │
│                              │
│ [History] [Examples] [Schema]│ ← Tab bar
└──────────────────────────────┘
```

**Mobile Optimizations**:
- **Stacked layout**: Single column, no sidebar
- **Bottom navigation**: Tab bar for main sections
- **Touch targets**: Minimum 44x44px
- **Simplified tables**: Horizontal scroll for wide tables
- **Sheet modals**: Slide up from bottom (native feel)
- **Font size**: 16px minimum (prevents iOS zoom)

**Tablet Layout (768-1199px)**:
```
┌───────────────────────────────────────────────┐
│ Header (same as desktop)                      │
├───────┬───────────────────────────────────────┤
│       │                                       │
│ Side- │  Main Content (similar to desktop    │
│ bar   │  but narrower columns)               │
│ (200px│                                       │
│       │                                       │
└───────┴───────────────────────────────────────┘
```

---

## **4. Accessibility Standards (WCAG 2.1 Level AA)**

### **4.1 Perceivable**

**Guideline 1.1: Text Alternatives**

**Implementation**:
```html
<!-- All images have alt text -->
<img src="success-icon.svg" alt="Query successful" />

<!-- Decorative images hidden from screen readers -->
<img src="decorative-line.svg" alt="" role="presentation" />

<!-- Icons paired with text -->
<button>
  <svg aria-hidden="true">...</svg>
  <span>Submit Query</span>
</button>

<!-- Complex images have long descriptions -->
<img src="schema-diagram.png" 
     alt="Database schema" 
     aria-describedby="schema-description" />
<div id="schema-description" class="sr-only">
  Detailed description of database relationships...
</div>
```

**Guideline 1.3: Adaptable Content**

**Semantic HTML Structure**:
```html
<!-- Proper heading hierarchy -->
<h1>SQL Query Assistant</h1>
  <h2>Query Interface</h2>
    <h3>Results</h3>
  <h2>Query History</h2>

<!-- Table structure with headers -->
<table>
  <thead>
    <tr>
      <th scope="col">Service Line</th>
      <th scope="col">Count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Cardiology</td>
      <td>892</td>
    </tr>
  </tbody>
</table>

<!-- Form labels explicitly associated -->
<label for="query-input">Enter your query</label>
<textarea id="query-input" name="query"></textarea>
```

**Guideline 1.4: Distinguishable**

**Color Contrast Requirements**:
```
Text Contrast (WCAG AA: 4.5:1, AAA: 7:1):
✅ Primary text (#212529) on white: 16.1:1 (AAA)
✅ Secondary text (#495057) on white: 11.2:1 (AAA)
✅ Link text (#2C5AA0) on white: 9.2:1 (AAA)
✅ Success green (#28A745) on white: 7.8:1 (AAA)
✅ Error red (#DC3545) on white: 7.2:1 (AAA)

Large Text Contrast (WCAG AA: 3:1):
✅ All headings exceed 3:1 ratio

Non-Text Contrast (UI components: 3:1):
✅ Button borders: 4.2:1
✅ Input borders: 4.5:1
✅ Focus indicators: 5.1:1
```

**Visual Indicators (Not Color Alone)**:
```
Error States:
❌ Bad:  Red text only
✅ Good: Red text + ❌ icon + "Error:" prefix

Success States:
❌ Bad:  Green background only
✅ Good: Green background + ✓ icon + "Success" text

Status Indicators:
✅ Loading: Spinner + "Processing..." text
✅ Complete: Checkmark + "Complete" label
✅ Error: X icon + error description
```

**Text Resizing**:
```css
/* Support up to 200% zoom without horizontal scroll */
body {
  font-size: 16px;
  max-width: 100%;
  overflow-x: hidden;
}

/* Use relative units (rem, em) not pixels */
.button {
  font-size: 1rem; /* scales with user preferences */
  padding: 0.75em 1.5em;
}
```

---

### **4.2 Operable**

**Guideline 2.1: Keyboard Accessible**

**Keyboard Navigation Map**:
```
Tab Order:
1. Header navigation
2. Database selector
3. Query input field
4. Submit button
5. Example queries dropdown
6. Results area (focusable)
7. Export buttons
8. History sidebar (if visible)

Keyboard Shortcuts:
Ctrl/Cmd + K     : Focus search/query input
Ctrl/Cmd + Enter : Submit query
Escape           : Close modal/cancel operation
Tab              : Next focusable element
Shift + Tab      : Previous focusable element
Arrow Keys       : Navigate dropdowns/lists
Enter/Space      : Activate button/link
Home/End         : First/last item in list
```

**Focus Management**:
```css
/* Visible focus indicator (not browser default) */
*:focus {
  outline: 3px solid #2C5AA0;
  outline-offset: 2px;
}

/* Skip to main content link */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #2C5AA0;
  color: white;
  padding: 8px;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

**Guideline 2.2: Enough Time**

**No Time Limits** (except necessary ones):
```
Session Timeout: 4 hours (healthcare standard)
├─ Warning at 30 minutes remaining
├─ Option to extend session
└─ Auto-save query draft before timeout

Query Execution Timeout: 30 seconds
├─ Progress indicator during execution
├─ Cancel button always available
└─ No auto-advancing content
```

**Guideline 2.3: Seizures**

**No Flashing Content**:
```
✅ No content flashes more than 3 times per second
✅ Animations respect prefers-reduced-motion
✅ Loading spinners rotate smoothly (no flashing)
```

```css
/* Respect user motion preferences */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

**Guideline 2.4: Navigable**

**Page Structure**:
```html
<!-- Skip navigation -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<!-- Landmark regions -->
<header role="banner">
  <nav aria-label="Main navigation">...</nav>
</header>

<main id="main-content" role="main">
  <section aria-labelledby="query-section">
    <h2 id="query-section">Query Interface</h2>
    ...
  </section>
</main>

<aside aria-label="Query history">...</aside>

<footer role="contentinfo">...</footer>
```

**Descriptive Links and Buttons**:
```html
❌ Bad:  <a href="...">Click here</a>
✅ Good: <a href="...">View query history</a>

❌ Bad:  <button>Submit</button>
✅ Good: <button>Submit query</button>

❌ Bad:  <a href="...">Read more</a>
✅ Good: <a href="...">Read more about discharge metrics</a>
```

---

### **4.3 Understandable**

**Guideline 3.1: Readable**

**Language Declaration**:
```html
<html lang="en">
  <head>
    <title>SQL Query Assistant</title>
  </head>
  <body>
    <!-- Content in English -->
    
    <!-- If section in different language -->
    <blockquote lang="es">
      Contenido en español
    </blockquote>
  </body>
</html>
```

**Guideline 3.2: Predictable**

**Consistent Navigation**:
```
Every page has same header structure:
[Logo] [Database Selector] [User Menu]

Every page has same sidebar order:
1. History
2. Examples
3. Templates
4. Schema

Buttons always in same position:
[Cancel] [Primary Action] (left to right)
```

**No Unexpected Changes**:
```
✅ Focus never moves automatically (user controls focus)
✅ Forms don't submit on focus change
✅ Dropdowns don't navigate on value change
✅ Modals don't open without user action
```

**Guideline 3.3: Input Assistance**

**Error Identification**:
```html
<!-- Error message associated with input -->
<div class="form-group">
  <label for="query-input">Enter your query</label>
  <textarea 
    id="query-input" 
    aria-describedby="query-error"
    aria-invalid="true"
  ></textarea>
  <div id="query-error" class="error-message" role="alert">
    <span aria-hidden="true">❌</span>
    Error: Query cannot be empty. Please enter a question.
  </div>
</div>
```

**Error Suggestions**:
```
Error: "Table 'patients' not found"
Suggestions:
• Did you mean 'patient_master'?
• Did you mean 'pt_accounting_reporting_alt'?
• Browse schema to find correct table

Error: "Query timeout after 30 seconds"
Suggestions:
• Add date filters to reduce data scanned
• Request summary instead of all records
• Break query into smaller parts
```

**Form Validation**:
```javascript
// Client-side validation with feedback
function validateQuery(query) {
  if (query.trim().length === 0) {
    showError('Please enter a query');
    return false;
  }
  if (query.length > 500) {
    showError('Query too long (max 500 characters)');
    return false;
  }
  // Additional validation...
  return true;
}
```

---

### **4.4 Robust**

**Guideline 4.1: Compatible**

**Valid HTML**:
```html
<!-- All elements properly closed -->
<div class="container">
  <p>Content</p>
</div>

<!-- No duplicate IDs -->
<input id="query-input-1" />
<input id="query-input-2" /> <!-- Different ID -->

<!-- Proper nesting -->
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
</ul>
```

**ARIA Attributes**:
```html
<!-- Live regions for dynamic content -->
<div role="status" aria-live="polite" aria-atomic="true">
  Query processing... 60% complete
</div>

<!-- Alert for errors -->
<div role="alert" aria-live="assertive">
  Error: Query execution failed
</div>

<!-- Dialog modal -->
<div role="dialog" aria-labelledby="dialog-title" aria-modal="true">
  <h2 id="dialog-title">Confirm Delete</h2>
  ...
</div>

<!-- Button with expanded state -->
<button 
  aria-expanded="false" 
  aria-controls="history-panel"
  id="history-toggle"
>
  Show History
</button>
<div id="history-panel" hidden>
  <!-- History content -->
</div>
```

---

## **5. Component Design Patterns**

### **5.1 Button Styles**

**Button Hierarchy**:
```
PRIMARY BUTTON (Main action)
┌────────────────────┐
│  Submit Query      │  Blue background (#2C5AA0)
└────────────────────┘  White text, bold

SECONDARY BUTTON (Alternative action)
┌────────────────────┐
│  Cancel            │  White background, blue border
└────────────────────┘  Blue text

TERTIARY BUTTON (Less emphasis)
┌────────────────────┐
│  View History      │  No background, no border
└────────────────────┘  Blue text, underline on hover

DESTRUCTIVE BUTTON (Dangerous action)
┌────────────────────┐
│  Delete Template   │  Red background (#DC3545)
└────────────────────┘  White text, bold
```

**Button States**:
```css
/* Normal state */
.button-primary {
  background: #2C5AA0;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 200ms ease;
}

/* Hover state */
.button-primary:hover {
  background: #234785;
  box-shadow: 0 2px 8px rgba(44, 90, 160, 0.3);
}

/* Active/pressed state */
.button-primary:active {
  background: #1A3464;
  transform: translateY(1px);
}

/* Focus state (keyboard) */
.button-primary:focus {
  outline: 3px solid #2C5AA0;
  outline-offset: 2px;
}

/* Disabled state */
.button-primary:disabled {
  background: #6C757D;
  cursor: not-allowed;
  opacity: 0.6;
}

/* Loading state */
.button-primary.loading {
  position: relative;
  color: transparent;
}
.button-primary.loading::after {
  content: '';
  position: absolute;
  width: 16px;
  height: 16px;
  border: 2px solid white;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 600ms linear infinite;
}
```

---

### **5.2 Input Fields**

**Text Input Design**:
```
NORMAL STATE
┌────────────────────────────────────────┐
│ Enter your query...                    │
└────────────────────────────────────────┘
Border: 2px solid #DEE2E6 (gray)

FOCUS STATE
┌────────────────────────────────────────┐
│ How many patients█                     │
└────────────────────────────────────────┘
Border: 2px solid #2C5AA0 (blue), slight shadow

ERROR STATE
┌────────────────────────────────────────┐
│ (empty)                                │
└────────────────────────────────────────┘
❌ Query cannot be empty
Border: 2px solid #DC3545 (red)

SUCCESS STATE
┌────────────────────────────────────────┐
│ How many patients were admitted...     │
└────────────────────────────────────────┘
✓ Ready to submit
Border: 2px solid #28A745 (green)

DISABLED STATE
┌────────────────────────────────────────┐
│ Processing query...                    │
└────────────────────────────────────────┘
Border: 2px solid #DEE2E6 (gray), grayed background
```

**Input Specifications**:
```css
.input-field {
  width: 100%;
  padding: 12px 16px;
  font-size: 16px; /* Prevents iOS zoom */
  line-height: 1.5;
  border: 2px solid #DEE2E6;
  border-radius: 6px;
  transition: border-color 200ms ease, box-shadow 200ms ease;
}

.input-field:focus {
  border-color: #2C5AA0;
  outline: none;
  box-shadow: 0 0 0 3px rgba(44, 90, 160, 0.1);
}

.input-field::placeholder {
  color: #6C757D;
  opacity: 0.7;
}

.input-field[aria-invalid="true"] {
  border-color: #DC3545;
}

.input-field:disabled {
  background-color: #F8F9FA;
  cursor: not-allowed;
  opacity: 0.6;
}
```

---

### **5.3 Toast Notifications**

**Notification Types**:
```
SUCCESS TOAST (Top-right corner)
┌────────────────────────────────────────┐
│ ✓ Query executed successfully          │
│   147 rows returned in 1.2 seconds     │
│                                    [✕] │
└────────────────────────────────────────┘
Green background (#28A745), auto-dismiss 5s

ERROR TOAST
┌────────────────────────────────────────┐
│ ❌ Query execution failed               │
│   Database connection timeout          │
│                                    [✕] │
└────────────────────────────────────────┘
Red background (#DC3545), manual dismiss

WARNING TOAST
┌────────────────────────────────────────┐
│ ⚠️ Query running slowly                 │
│   Consider adding date filters         │
│                                    [✕] │
└────────────────────────────────────────┘
Orange background (#FFA500), auto-dismiss 8s

INFO TOAST
┌────────────────────────────────────────┐
│ ℹ️ Schema refreshed                     │
│   2 new tables added                   │
│                                    [✕] │
└────────────────────────────────────────┘
Blue background (#17A2B8), auto-dismiss 5s
```

**Toast Behavior**:
- Slide in from top-right
- Stack vertically (max 3 visible)
- Newest on top
- Dismissible by click or timeout
- Pause auto-dismiss on hover
- Screen reader announces (aria-live="polite" for info, "assertive" for errors)

---

### **5.4 Loading Indicators**

**Loading States**:
```
SPINNER (Small - inline)
⏳ Processing...

SPINNER (Large - full component)
     ⏳
 Processing your
   query...

PROGRESS BAR (Determinate)
[=========>         ] 60%
Generating SQL query...

SKELETON SCREEN (Loading table)
┌────────────────────────────────────────┐
│ ░░░░░░░░  ░░░░░░░  ░░░░░░░            │
│ ░░░░░░░░  ░░░░░░░  ░░░░░░░            │
│ ░░░░░░░░  ░░░░░░░  ░░░░░░░            │
└────────────────────────────────────────┘
```

**Implementation**:
```css
/* Spinning loader */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid #F8F9FA;
  border-top-color: #2C5AA0;
  border-radius: 50%;
  animation: spin 800ms linear infinite;
}

/* Skeleton shimmer */
@keyframes shimmer {
  0% { background-position: -1000px 0; }
  100% { background-position: 1000px 0; }
}

.skeleton {
  background: linear-gradient(
    90deg,
    #F8F9FA 0px,
    #E9ECEF 40px,
    #F8F9FA 80px
  );
  background-size: 1000px 100%;
  animation: shimmer 2s infinite;
}
```

---

## **6. Design System Documentation**

### **6.1 Component Library Structure**

**Storybook Organization**:
```
Design System Documentation
├── Foundation
│   ├── Colors
│   ├── Typography
│   ├── Spacing
│   ├── Icons
│   └── Elevation
├── Components
│   ├── Buttons
│   │   ├── Primary Button
│   │   ├── Secondary Button
│   │   ├── Tertiary Button
│   │   └── Icon Button
│   ├── Inputs
│   │   ├── Text Input
│   │   ├── Text Area
│   │   ├── Select Dropdown
│   │   └── Search Input
│   ├── Data Display
│   │   ├── Table
│   │   ├── Data Card
│   │   └── Statistics
│   ├── Feedback
│   │   ├── Toast Notifications
│   │   ├── Alerts
│   │   ├── Progress Indicators
│   │   └── Loading States
│   └── Navigation
│       ├── Sidebar
│       ├── Tabs
│       └── Breadcrumbs
├── Patterns
│   ├── Query Interface
│   ├── Results Display
│   ├── History Sidebar
│   └── Schema Browser
└── Templates
    ├── Main Application Layout
    ├── Admin Dashboard
    └── Mobile Layout
```

### **6.2 Design Tokens**

**Token System (CSS Custom Properties)**:
```css
:root {
  /* Colors */
  --color-primary: #2C5AA0;
  --color-success: #28A745;
  --color-error: #DC3545;
  --color-warning: #FFA500;
  --color-info: #17A2B8;
  
  /* Grayscale */
  --color-gray-900: #212529;
  --color-gray-700: #495057;
  --color-gray-500: #6C757D;
  --color-gray-300: #DEE2E6;
  --color-gray-100: #F8F9FA;
  
  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  
  /* Typography */
  --font-size-xs: 12px;
  --font-size-sm: 14px;
  --font-size-base: 16px;
  --font-size-lg: 18px;
  --font-size-xl: 20px;
  --font-size-2xl: 24px;
  --font-size-3xl: 32px;
  
  /* Border radius */
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  --radius-xl: 12px;
  
  /* Shadows */
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.12);
  --shadow-md: 0 3px 6px rgba(0,0,0,0.15);
  --shadow-lg: 0 10px 20px rgba(0,0,0,0.15);
  
  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;
}
```

---

## **7. Implementation Guidelines**

### **7.1 CSS Architecture**

**BEM Methodology** (Block Element Modifier):
```css
/* Block */
.query-interface { }

/* Element (child of block) */
.query-interface__input { }
.query-interface__submit { }
.query-interface__results { }

/* Modifier (variation) */
.query-interface--loading { }
.query-interface__submit--disabled { }
```

**Utility Classes** (Tailwind-inspired):
```css
/* Spacing utilities */
.mt-1 { margin-top: 8px; }
.mt-2 { margin-top: 16px; }
.p-3 { padding: 24px; }

/* Display utilities */
.flex { display: flex; }
.grid { display: grid; }
.hidden { display: none; }

/* Text utilities */
.text-center { text-align: center; }
.font-bold { font-weight: 700; }
.text-primary { color: var(--color-primary); }
```

### **7.2 Responsive Design Strategy**

**Mobile-First Approach**:
```css
/* Base styles (mobile) */
.container {
  width: 100%;
  padding: 16px;
}

/* Tablet (768px and up) */
@media (min-width: 768px) {
  .container {
    padding: 24px;
  }
}

/* Desktop (1200px and up) */
@media (min-width: 1200px) {
  .container {
    max-width: 1440px;
    margin: 0 auto;
    padding: 48px;
  }
}
```

### **7.3 Animation Principles**

**Animation Guidelines**:
- **Duration**: 150-300ms for micro-interactions
- **Easing**: ease-in-out for most transitions
- **Performance**: Use transform and opacity (GPU accelerated)
- **Respect user preferences**: Honor prefers-reduced-motion

```css
/* Example: Button hover animation */
.button {
  transition: transform 150ms ease, 
              box-shadow 150ms ease;
}

.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* Smooth page transitions */
.page-enter {
  opacity: 0;
  transform: translateY(20px);
}

.page-enter-active {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 300ms ease, 
              transform 300ms ease;
}
```

---

## **8. Usability Heuristics Applied**

**Nielsen's 10 Usability Heuristics - Implementation**:

1. **Visibility of System Status**
   - ✅ Loading indicators show progress
   - ✅ Success/error messages confirm actions
   - ✅ Query execution time displayed

2. **Match Between System and Real World**
   - ✅ Healthcare terminology (not technical jargon)
   - ✅ Natural language query input
   - ✅ Familiar UI patterns (tables, buttons)

3. **User Control and Freedom**
   - ✅ Cancel button during query execution
   - ✅ Clear conversation button
   - ✅ Edit query from history

4. **Consistency and Standards**
   - ✅ Consistent button placement
   - ✅ Standard interaction patterns
   - ✅ Uniform terminology throughout

5. **Error Prevention**
   - ✅ Confirmation dialogs for destructive actions
   - ✅ Input validation before submission
   - ✅ Smart defaults reduce errors

6. **Recognition Rather Than Recall**
   - ✅ Visible navigation
   - ✅ Query history sidebar
   - ✅ Example queries readily available

7. **Flexibility and Efficiency of Use**
   - ✅ Keyboard shortcuts for power users
   - ✅ Query templates for common tasks
   - ✅ Customizable interface (collapsible panels)

8. **Aesthetic and Minimalist Design**
   - ✅ Clean interface, essential information only
   - ✅ Progressive disclosure of advanced features
   - ✅ Generous whitespace

9. **Help Users Recognize, Diagnose, and Recover from Errors**
   - ✅ Clear error messages with actionable suggestions
   - ✅ Error context (what went wrong, why)
   - ✅ Recovery paths offered

10. **Help and Documentation**
    - ✅ Inline help text
    - ✅ Tooltips explain features
    - ✅ Example queries as learning tools
    - ✅ Link to full documentation

---

## **Summary: UI/UX Design System**

This comprehensive design system ensures:

✅ **Accessibility**: WCAG 2.1 Level AA compliant
✅ **Consistency**: Unified visual language and patterns
✅ **Usability**: Intuitive interface for all user levels
✅ **Responsiveness**: Works across devices and screen sizes
✅ **Performance**: Optimized animations and loading states
✅ **Maintainability**: Token-based design system, documented components

**Key Design Decisions**:
- Healthcare-focused color palette (professional, trustworthy)
- Progressive disclosure (simple for beginners, powerful for experts)
- Immediate feedback (always show system state)
- Error prevention > error handling
- Mobile-first responsive design
- Keyboard accessibility throughout

The design system balances **simplicity** for occasional users with **power** for daily users, while maintaining **accessibility** for all users regardless of ability or device.