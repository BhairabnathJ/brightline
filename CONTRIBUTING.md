# Contributing to Brightline Logistics

Welcome! You work on Brightline the same way you would on a real engineering
team: pick up a ticket, branch off `main`, open a pull request, and let the
grader tell you whether your change is correct. This guide walks through that
loop end to end.

The workflow is:

**branch → pull request → hidden tests → AI review → fix → pass → XP**

## 1. Start from a known-good `main`

Before you begin, make sure your checkout of `main` is clean and the visible
tests pass:

```bash
git checkout main
git pull
pytest
```

A green run on `main` is your baseline. Every ticket branch starts from here.

## 2. Create a branch for your ticket

Each ticket has a branch name assigned to it (for example,
`ticket/l1-pagination`). Create your working branch from `main` using that name:

```bash
git checkout main
git checkout -b ticket/l1-pagination
```

**Branch-naming convention:** name your branch `ticket/<short-slug>`, where
`<short-slug>` is the slug for the ticket you are working on (for example,
`ticket/l1-pagination`, `ticket/l2-eta-timezone`, `ticket/l3-route-eta`). Use
the branch name the ticket specifies so the grader can find your work.

Do your work on this branch. Commit as you go:

```bash
git add <files you changed>
git commit -m "Fix shipment pagination boundary"
```

## 3. Open a pull request

When you're ready to submit, push your branch and open a pull request against
the repository's default branch, `main`:

1. Push your branch to the remote and set up tracking:

   ```bash
   git push -u origin ticket/l1-pagination
   ```

2. Open a pull request with your branch as the source and `main` as the base
   (the default branch). Give it a clear title and describe what you changed.

## 4. Grading happens on your pull request

**Opening a pull request submits your branch for grading.** Once the PR is
open, the submitted branch is evaluated by **hidden tests** — a dedicated test
suite that checks the ticket's acceptance criteria.

These hidden tests are **not present in this repository.** You will not find
them in `tests/` or anywhere else in the Brightline codebase; they live
server-side and run against your PR. The visible tests in `tests/` are your
local sanity check, but passing them does not guarantee the hidden tests pass —
they cover the specific behavior the ticket asks for.

After grading, you'll also receive an AI code review with feedback on your
change.

## 5. If the hidden tests fail, iterate on the same branch

**When the hidden tests fail, your pull request is marked as needing changes.**
To fix it:

1. Make your changes locally on the **same branch**.
2. Commit and push more commits to that branch:

   ```bash
   git add <files you changed>
   git commit -m "Address failing boundary case"
   git push
   ```

Pushing further commits to the same branch **re-triggers grading** on the
existing pull request. Repeat this fix → push → re-grade loop until the hidden
tests pass.

When the hidden tests pass, the ticket is complete and you're awarded its XP.
Then it's on to the next ticket.
