# colony

Colony is the working state for an autonomous agent pursuing a single
long-running goal. The goal, its pillars, and what the agent is allowed to
do are defined in `config/north_star.json`; everything the agent produces or
tracks lives alongside it in this repo.

Current north star: **Road to NVIDIA** — land an AI or software engineering
internship at NVIDIA.

## Layout

```
config/
  north_star.json   Goal, pillars, and permission flags
state/
  progress.json     0–100 progress score per pillar, plus "overall"
  tasks.json        Task queue ({"tasks": [...]})
  activity.jsonl    Append-only activity log, one JSON object per line
artifacts/
  code/             Code the agent writes
  documents/        Drafts such as resumes and cover letters
  reports/          Periodic progress reports
  research/         Notes from research tasks
dashboard/          Progress dashboard
scripts/            Maintenance utilities
```

## Pillars

Progress is tracked across five pillars: `technical_skills`, `portfolio`,
`applications`, `networking`, and `interview_prep`. Each pillar listed in
`north_star.json` should have a matching key in `state/progress.json`.

## Permissions

The `permissions` block in `north_star.json` limits what the agent may do on
its own. It can research, write files, and write code. It may not modify
existing projects, send messages, submit applications, or publish anything;
those actions need a human.

## Setup

Copy `.env.example` to `.env` and fill in any credentials. `.env` is
gitignored.

## Checking state

Run `python3 scripts/validate_state.py` after editing config or state files.
It exits non-zero and lists every problem it finds.
