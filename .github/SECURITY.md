# Security Policy

## Reporting a vulnerability or a data concern

**Do not** open a public GitHub issue for security problems or for personal data you find in this repository.

Instead, email support@promptingcompany.com with:

- what you found and where (file and line, or commit)
- how to reproduce it, if it applies
- the potential impact

We respond within 48 hours and agree a timeline for the fix with you.

## What this repository holds

- Task definitions, prompts, answer keys and graders for Monid Bench, and each published run's output and grade. No credentials: runs read the Monid, Treg, Apify and model keys from your own environment.
- Public web data only: Google search volumes and results (keyword-research), company facts from SEC 10-K filings and company websites (company-data), and public SaaS pricing pages snapshotted from a US network (pricing).
- Public social media posts that mention a brand (social-listening). Each row keeps the post's link, its author's public handle and its text as the agent found it, so the grade can be checked. Some posts include contact details their authors published.

If you are named or quoted in this repository and want to be removed, email the same address.

## Security measures

- Runs use keys made for this benchmark, stored in a password manager and never committed.
- The snapshot workflow has read-only repository access and pins its actions to a commit.

## Bug bounty

We do not currently run a bug bounty program.

---

**Contact:** support@promptingcompany.com
