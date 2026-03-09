# PeriSmart Public Website Requirements

**Level-1 Product Specification (L1)**  
**Version 1.0** | March 2026

---

## 1. Purpose

This specification defines the first public marketing website for **PeriSmart**.

The site exists to:
- explain PeriSmart's value proposition clearly
- establish trust with perioperative buyers and hospital IT stakeholders
- convert interested visitors into demo or contact requests
- stay tightly aligned with current PeriSmart product scope

This is a **public-facing marketing site**, not the application itself.

---

## 2. Scope

### In Scope
- A small static website that presents PeriSmart's purpose, core capabilities, deployment model, and contact/demo CTA
- Messaging informed by public patterns seen on:
  - `https://apella.io/`
  - `https://www.surgicalsafety.com/`
  - `https://www.nsightsurgical.ai/`
- A homepage video placeholder and a defined brief for a future explainer video
- HTML-first structure suitable for straightforward static implementation

### Out of Scope
- Application UI implementation
- Customer portal or login workflow
- Interactive calculators, dashboards, or product simulations
- CMS integration
- Blog, news center, or resource library for v1
- Customer logos, testimonials, named hospital references, or physician endorsements until they exist
- Claims for unsupported or non-MVP capabilities

---

## 3. Product Truth Sources

Public-web content must stay consistent with:
- `spec/l0_MVP_requirements.md`
- `spec/l2_Privacy_Compliance.md`
- `spec/schedule/l1_Case_Scheduling.md`
- `spec/edge/l1_Edge_requirements.md`
- `spec/notifications/l2_Notification_Service.md`
- `spec/competitors.md`
- `spec/ui/l0_CompetitorUI.md`

If those source specs change materially, the public-web specs should be reviewed before implementation.

---

## 4. Website Objectives

### Primary Objectives
1. Communicate that PeriSmart provides real-time visibility into OR execution.
2. Show that PeriSmart helps teams act earlier through prediction and notification.
3. Build trust around privacy, deployment, and integration.
4. Present PeriSmart as operationally valuable without overstating maturity or proof.
5. Drive a clear next action: request a demo, schedule a conversation, or contact the team.

### Secondary Objectives
1. Give enough substance for perioperative leaders to understand the product quickly.
2. Give enough technical confidence for IT and compliance reviewers to stay engaged.
3. Create a clean foundation that can later expand into case studies, FAQ, and resources.

---

## 5. Target Audiences

### Primary Audiences
- Perioperative directors
- Charge nurses and OR flow coordinators
- Perioperative operations managers
- Anesthesia leadership

### Secondary Audiences
- Hospital executives evaluating ROI
- Hospital IT and integration stakeholders
- Privacy and compliance reviewers
- Surgeons evaluating workflow visibility benefits

---

## 6. Positioning

The site should position PeriSmart as:
- an **OR execution intelligence platform**
- focused on **day-of operations**, not full scheduling replacement
- grounded in **camera-derived operational visibility**
- designed for **practical deployment**, including edge-based de-identification and optional EHR integration

The site should not position PeriSmart as:
- a surgical safety checklist product
- a surgical education or video review platform
- a full OR scheduling suite
- a mobile-app-first product
- a system with named customer proof that does not yet exist

---

## 7. Recommended Site Structure

The recommended v1 structure is a **small multi-page static site** with 5 core pages:

1. `Home`
2. `Platform`
3. `How It Works`
4. `Privacy & Deployment`
5. `Contact / Request Demo`

### Rationale
- A single long page would be viable, but a 5-page structure is better for trust-building and easier future expansion.
- This mirrors the clarity of the reference sites without copying their larger content footprint.
- Each page can still be simple enough for hand-authored static HTML.

---

## 8. Content Principles

### 8.1 What the site should emphasize
- Real-time OR visibility
- Planned vs actual vs predicted execution
- Event-driven communication
- Operational analytics and throughput improvement
- Privacy-first deployment
- Epic-optional / integration-flexible design
- Fast implementation and low operational friction

### 8.2 What the site should de-emphasize or avoid
- Deep technical ML detail
- Clinical language that implies decision support
- Anything resembling patient monitoring claims
- Overly specific ROI numbers unless validated for public use
- Broad competitor-style functionality that PeriSmart does not currently support

### 8.3 Tone
- Clear
- Operational
- Trustworthy
- Calm and precise
- Modern, but not flashy for its own sake

---

## 9. Supported Public Claims

The following claims are aligned with current specs and are appropriate for v1:
- PeriSmart gives perioperative teams real-time visibility into OR execution.
- PeriSmart combines planned, actual, and predicted timelines.
- PeriSmart uses camera-based workflow sensing with privacy-first de-identification.
- PeriSmart helps teams coordinate earlier through notifications and operational alerts.
- PeriSmart can import scheduling context from existing systems rather than replacing them.
- PeriSmart is designed for edge-based de-identification and cloud-based analytics/inference.
- PeriSmart is intended for rapid deployment relative to heavier enterprise alternatives.

The following claims should be avoided in v1 unless explicitly approved for public use:
- named customer outcomes
- published percentage improvements presented as PeriSmart customer proof
- autonomous EHR writeback as an active capability
- native mobile app availability
- safety checklist workflows
- surgeon education or video library positioning
- any promise of fully autonomous operation without human override

---

## 10. Functional Requirements

### 10.1 Required global elements
- Consistent header navigation
- Persistent primary CTA: `Request a Demo`
- Secondary CTA: `Contact Us`
- Simple footer with company summary, email/contact path, and legal/privacy placeholders

### 10.2 Required homepage elements
- Hero statement
- Short supporting value proposition
- Primary and secondary CTA
- Placeholder for explainer video
- Core capability overview
- Privacy/integration/deployment trust section
- Audience or use-case section
- Final CTA band

### 10.3 Required supporting page coverage
- Platform page must explain major product capability areas
- How It Works page must explain the operational flow from schedule context to real-time events to team coordination
- Privacy & Deployment page must explain edge de-identification, cloud role, retention posture, and integration approach in business-readable terms
- Contact / Request Demo page must provide a simple lead path that works in a static HTML implementation

### 10.4 Video placeholder requirement
- The homepage must reserve a prominent 16:9 area for a future explainer video.
- Until a video exists, the area should display a poster-style placeholder with concise explanatory text.
- The placeholder must not imply a finished video asset if one does not yet exist.

---

## 11. HTML-Only Implementation Approach

### 11.1 Hosting
- Site is hosted on **Cloudflare Pages** (free tier)
- Source repository: `PeriSmart-public-web` on GitHub
- Custom domain: `peri-smart.com` with DNS managed by Cloudflare
- Cloudflare provides CDN, SSL, and deployment from the GitHub repo

### 11.2 Recommended technical approach
- Static HTML pages
- Shared CSS file(s)
- No framework
- No SPA behavior
- No backend requirement for v1
- No JavaScript required for core browsing

### 11.3 Acceptable lightweight additions
- Mailto link for contact
- External scheduling/demo link
- Embedded hosted video in a later revision, if needed

### 11.4 Not recommended for v1
- Custom lead form backend
- Search
- Animation-heavy front-end libraries
- Content personalization
- Complex scroll effects

---

## 12. Recommended Navigation

Top navigation should be limited to:
- Home
- Platform
- How It Works
- Privacy & Deployment
- Contact
- Request a Demo button

This keeps the site lightweight while still feeling complete.

---

## 13. Non-Goals

The v1 public site should not attempt to:
- match the breadth of mature competitor marketing sites
- simulate the application
- prove product-market fit through references that do not yet exist
- explain every subsystem in the PeriSmart architecture
- support complex lead qualification workflows

The goal is **clarity and credibility**, not content volume.

---

## 14. Delivery Plan

### Phase 1: Specification
- define positioning, structure, and page sections
- define explainer video placeholder and brief

### Phase 2: Static HTML Build
- implement the approved IA in HTML/CSS
- use placeholder assets where needed
- keep content easy to edit by hand

### Phase 3: Content Enrichment
- add real screenshots, diagrams, and product video
- add customer proof and metrics once available
- expand into FAQ, case studies, or resources if needed

---

## 15. Success Criteria

The website is successful if a first-time visitor can quickly understand:
- what PeriSmart is
- who it is for
- how it helps perioperative operations
- why it is privacy-conscious and practical to deploy
- how to request a conversation or demo

---

## 16. Recommendation Summary

The recommended v1 public website is:
- **small**
- **static**
- **HTML-first**
- **content-led**
- **trust-oriented**

It should borrow the structural discipline of Apella, SST, and nSight, while staying strictly inside PeriSmart's actual product scope.
