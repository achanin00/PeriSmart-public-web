# PeriSmart Public Website Information Architecture and Content Model

**Level-2 Design Specification (L2)**  
**Version 1.0** | March 2026

---

## 1. Purpose

This document defines the recommended information architecture, page structure, messaging pattern, and content boundaries for the PeriSmart public website.

It translates the high-level requirements in `spec/public-web/l1_Public_Website_Requirements.md` into a concrete page model for later HTML implementation.

---

## 2. Reference-Site Pattern Summary

The three reference sites suggest a common public-site structure:
- a strong hero with concise AI/operations language
- clear product explanation near the top
- modular sections for outcomes, workflow, and trust
- repeated demo/contact CTA
- restrained top-level navigation

Patterns worth adopting:
- outcome-led hero messaging
- product explainer sections with simple visual placeholders
- trust sections for privacy, deployment, or clinical fit
- consistent CTA repetition

Patterns to avoid for PeriSmart v1:
- customer logo walls without customers
- physician or hospital references without proof
- broader safety/education/surgeon-review positioning
- claims for modules not in PeriSmart specs

---

## 3. Recommended Sitemap

### Core Pages
1. `/index.html` - Home
2. `/platform.html` - Platform
3. `/how-it-works.html` - How It Works
4. `/privacy-deployment.html` - Privacy & Deployment
5. `/contact.html` - Contact / Request Demo

### Optional Later Pages
- `/faq.html`
- `/case-studies.html`
- `/resources.html`

These optional pages should not be part of v1 unless actual content exists.

---

## 4. Global Navigation Model

### Header
- Logo
- Home
- Platform
- How It Works
- Privacy & Deployment
- Contact
- Primary CTA button: `Request a Demo`

### Footer
- Short PeriSmart description
- Repeat of primary links
- Contact email
- Legal placeholders:
  - Privacy
  - Terms

If legal pages do not yet exist, they can remain plain placeholders until provided.

---

## 5. Homepage Structure

### 5.1 Goal

The homepage should answer five questions quickly:
1. What is PeriSmart?
2. Who is it for?
3. How does it work at a high level?
4. Why is it credible and safe to deploy?
5. What should I do next?

### 5.2 Recommended Section Order

### Section 1: Hero
- Headline focused on real-time OR visibility and coordination
- Short subhead focused on operational value
- Primary CTA: `Request a Demo`
- Secondary CTA: `See How It Works`
- Adjacent visual area:
  - either a product illustration
  - or the homepage video placeholder

### Section 2: Explainer Video Placeholder
- 16:9 poster frame
- short label such as `See PeriSmart in action`
- caption: product overview video coming soon
- short summary beneath the frame

### Section 3: Core Value Pillars
- Real-time visibility
- Predictive runway
- Event-driven communication
- Operational insights

Each pillar should be written in business language, not deep technical language.

### Section 4: How PeriSmart Fits the OR Day
- Import schedule context
- Detect milestones and room-state changes
- Update predicted timelines
- Notify the right teams earlier
- Learn from historical performance

This section should feel like a simple workflow, not an engineering diagram.

### Section 5: Privacy and Deployment Snapshot
- Edge-based de-identification
- De-identified cloud storage and analytics
- Existing schedule-system integration
- No full scheduling rip-and-replace
- Use the externally created privacy illustration asset at `images/public-web/illustrations/privacy-illustration.png` as the primary visual for this section

### Section 6: Who It Helps
- Charge nurse / flow coordinator
- Perioperative operations manager
- Anesthesia lead
- Pre-op / PACU coordination staff
- OR leadership

### Section 7: Final CTA Band
- Short closing statement
- Primary CTA: `Request a Demo`
- Secondary CTA: `Contact Us`

---

## 6. Platform Page

### 6.1 Goal

The Platform page should give more detail on what PeriSmart does without turning into technical documentation.

### 6.2 Recommended Sections

### Section 1: Intro
- one-paragraph platform summary

### Section 2: Capability Blocks
- Day-of execution board
- Notifications and smart routing
- Live room visibility
- Analytics and insights
- Schedule-context integration

### Section 3: What PeriSmart Does Not Replace
- hospital scheduling systems
- existing operational workflows

This is important because the product is integration-oriented, not replacement-oriented.

### Section 4: Audience-Oriented Outcomes
- less status chasing
- earlier coordination
- fewer manual calls and texts
- better visibility into delays and turnover

### Section 5: CTA
- request a walkthrough or demo

---

## 7. How It Works Page

### 7.1 Goal

Show the operating model in a simple sequence that a hospital buyer can understand in under two minutes.

### 7.2 Recommended Flow

### Step 1: Bring in the day's schedule
- FHIR, HL7v2, CSV, or manual entry for demos and edge cases

### Step 2: Capture what is actually happening
- camera-based room awareness
- milestone/event detection
- planned vs actual reconciliation

### Step 3: Update the operational picture
- real-time room status
- predicted case progression
- upcoming turnover and delay risk

### Step 4: Alert the right teams
- notification subscriptions by room, area, service line, or surgeon

### Step 5: Learn over time
- analytics for utilization, turnover, delays, and schedule accuracy

### 7.3 Recommended Visual Style
- simple numbered cards or horizontal process band
- no dense architecture diagrams in v1

---

## 8. Privacy & Deployment Page

### 8.1 Goal

This page should reduce buyer anxiety around cameras, PHI, and hospital deployment complexity.

### 8.2 Recommended Sections

### Section 1: Privacy-First Overview
- faces and sensitive elements are de-identified before cloud upload
- raw video stays local to the edge buffer
- raw audio is not retained in cloud

### Section 2: Edge and Cloud Roles
- edge handles de-identification and local processing
- cloud handles analytics, event inference, storage of de-identified video, and operational coordination features
- The page should pair this copy with `images/public-web/illustrations/privacy-illustration.png`, which shows the privacy concept through a stylized de-identified OR camera view rather than an abstract systems diagram

### Section 3: Integration Approach
- PeriSmart imports schedule context from existing systems
- Epic-optional, not Epic-dependent
- no need to replace incumbent schedulers

### Section 4: Deployment Practicality
- outbound connectivity model
- rapid implementation target
- site readiness and camera planning support

### Section 5: Trust CTA
- invite privacy/compliance or IT stakeholders to contact the team

---

## 9. Contact / Request Demo Page

### 9.1 Goal

Provide a simple conversion path that works without custom application logic.

### 9.2 Recommended Content
- short intro paragraph
- contact email
- demo request form (name, work email, organization, role, free-text interest)
- short checklist of what a demo conversation can cover

### 9.3 Form Handling

The demo request form posts to Formspree (formspree.io), a third-party form endpoint service for static sites. Formspree handles submission storage, spam filtering, and email notification to the PeriSmart team. No custom backend is required.

Key integration details:
- form action URL uses a Formspree endpoint ID
- a hidden `_next` field redirects the user to a branded thank-you page after submission
- if the Formspree endpoint is not yet configured, the form panel is automatically disabled via JavaScript (greyed out, inputs disabled)

---

## 10. Messaging Framework

### 10.1 Core headline territory

Recommended message territory:
- real-time OR execution visibility
- better prediction of what happens next
- earlier coordination across perioperative teams
- privacy-conscious deployment

### 10.2 Supporting proof territory

Allowed proof styles for v1:
- product architecture facts
- deployment model facts
- integration flexibility facts
- workflow outcomes stated qualitatively

Avoid:
- named outcomes without customer evidence
- percentages that imply public validation
- competitor-comparison tables on the public website

---

## 11. Content Blocks to Exclude

Do not include the following in v1:
- customer logo strip
- physician testimonial carousel
- hospital reference quotes
- surgical safety checklist module
- educational case-library language
- mobile app download prompts
- blog feed
- investor-style market sizing section

These may become relevant later, but they weaken credibility now.

---

## 12. Suggested Copy Themes by Audience

### Perioperative leadership
- see the current state of every room
- coordinate earlier with fewer manual interventions
- improve throughput with better operational visibility

### IT and compliance
- edge-based de-identification
- integration with existing scheduling systems
- practical deployment without full system replacement

### Surgeons and clinical stakeholders
- lightweight visibility into today's cases
- more predictable room readiness and start timing

---

## 13. Visual Content Guidance

Recommended asset types for v1:
- abstracted product mockups
- simple timeline or board illustrations
- deployment/process diagrams in plain language
- explainer-video placeholder art
- approved marketing illustrations from `images/public-web/illustrations/`

### Approved illustration mapping
- Homepage hero: `images/public-web/illustrations/hero-or-board-illustration.svg`
- Platform page support visual: `images/public-web/illustrations/case-detail-illustration.svg`
- Privacy & Deployment page primary visual: `images/public-web/illustrations/privacy-illustration.png`
- Analytics support visual: `images/public-web/illustrations/turnover-analytics-illustration.svg`

Avoid:
- highly specific UI promises if the design is not finalized
- photos of identifiable patients
- visuals that suggest clinical decision support or intraoperative guidance

---

## 14. Recommendation Summary

The public website should feel:
- modern
- operational
- credible
- intentionally narrow

It should look complete, but not overbuilt. The best v1 is a clear static marketing site that explains PeriSmart well and leaves room for richer proof later.
