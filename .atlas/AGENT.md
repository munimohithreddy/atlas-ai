# Atlas AI - AI Engineering Playbook

## Project

Atlas AI is an AI-powered Business Operating System.

The goal is NOT to generate articles.

The goal is to build profitable online businesses.

Affiliate marketing is the first business model.

Future business models include:

- SEO sites
- Newsletters
- Local SEO
- Shopify stores
- SaaS marketing

---

# Mission

Help users discover opportunities,
make better business decisions,
execute repetitive work,
measure outcomes,
and continuously improve.

---

# Engineering Principles

1. Never rewrite large parts of the project unless requested.
2. Make the smallest change possible.
3. Explain every file modified.
4. Keep architecture clean.
5. Prefer readability over cleverness.
6. Preserve backwards compatibility.
7. Write production-quality Python.
8. Follow FastAPI best practices.
9. Add type hints.
10. Keep business logic inside services.

---

# Folder Responsibilities

backend/app/api

- HTTP endpoints only.

backend/app/services

- Business logic.

backend/app/models

- SQLAlchemy models.

backend/app/repositories

- Database access.

backend/app/schemas

- Pydantic models.

backend/app/agents

- AI agents.

backend/app/workflows

- Multi-step orchestration.

backend/app/integrations

- Third-party APIs.

backend/app/utils

- Shared utilities.

knowledge/

Business intelligence.

Never executable code.

docs/

Project documentation.

---

# Coding Rules

Never duplicate logic.

Always reuse services.

Never hardcode secrets.

Always use configuration.

Prefer composition over inheritance.

Write clean imports.

---

# Git Workflow

One feature per branch.

Small commits.

Explain every commit.

Never modify unrelated files.

---

# Documentation

Every feature updates:

ROADMAP.md

SPRINTS.md

CHANGELOG.md

DECISIONS.md

---

# Architecture

Atlas consists of three logical brains.

Knowledge Brain

Stores research and best practices.

Decision Brain

Determines what Atlas should do.

Execution Brain

Performs work.

---

# Product Goal

Atlas should eventually answer:

"What should I build next?"

before answering

"How do I build it?"

---

# Current Status

Atlas Core v0.1

Completed:

- FastAPI
- PostgreSQL
- Redis
- Alembic
- Health endpoint
- Opportunity Engine foundation

Current Sprint:

Opportunity Intelligence Engine

---

# AI Behavior

When asked to modify code:

1. Read the repository first.
2. Understand the architecture.
3. Propose a plan.
4. Make minimal changes.
5. Explain every change.
6. Suggest tests.
7. Never remove functionality without explanation.