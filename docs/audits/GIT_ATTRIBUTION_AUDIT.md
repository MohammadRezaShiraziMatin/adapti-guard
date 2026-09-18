# Git attribution audit (read-only + experimental rewrite prep)

**Date (UTC):** 2026-09-18  
**Repository:** `https://github.com/mohammadreza583/adapti-guard`  
**Working copy:** `/workspace` (Cloud Agent checkout; local path `~/projects/adapti-guard` on owner machine should be the same remote)  
**Canonical identity (target):** `MohammadReza S M <121524262+Mohammadreza583@users.noreply.github.com>`

**Suspicious identities reviewed:**

| Identity | Email |
|----------|--------|
| Cursor Agent | `cursoragent@cursor.com` |
| cursor[bot] | `206951365+cursor[bot]@users.noreply.github.com` |
| MohammadReza (placeholder) | `your-email@example.com` |
| Adapti-Guard Research | `research@localhost` |

**Rules applied:** No force-push; no change to frozen file **content**; backup created; experimental rewrite only in `/tmp/adapti-guard-attribution-exp` (not pushed).

---

## 1. Current state (workspace, pre-rewrite)

| Field | Value |
|--------|--------|
| Current branch | `cursor/q2-publication-hardening-f6f3` |
| HEAD | `6ac7d69b57f78f35152a2b569bee3adc54b93674` |
| `main` tip | `e6b31942779c9cef7628ae22abdc220680b2f3db` |
| Remote | `origin` → `github.com/mohammadreza583/adapti-guard` |
| Total commits (`--all`) | **199** |
| Merge commits | **5** |
| Tags | **0** |
| Local branches | **6** |
| Remote-tracking branches | **76** |

### Author counts (`git shortlog -sne --all`)

| Count | Author |
|------:|--------|
| 179 | Cursor Agent `<cursoragent@cursor.com>` |
| 8 | MohammadReza `<your-email@example.com>` |
| 6 | MohammadReza S M `<121524262+Mohammadreza583@users.noreply.github.com>` |
| 4 | Adapti-Guard Research `<research@localhost>` |
| 2 | cursor[bot] `<206951365+cursor[bot]@users.noreply.github.com>` |

### Commits with suspicious author **or** committer (unique SHAs)

**193 / 199** commits touch at least one suspicious email on author or committer.

**6 commits** already have canonical author email and non-suspicious committer (GitHub `noreply@github.com` on PR merges):

- `612f577118a19949b4862a3b27b801db8c7eef65`
- `f00270903faed55e6d12259605c0dc0e63c31e8d`
- `5a7684835fe57303f7786c51719973ea168c1210`
- `cde70eaf0289feeb3ddac0633ecc90f897622921` (if present on all refs)
- `5e688103ed3f3097d69e4563a20aae0150b5e149`
- `e6b31942779c9cef7628ae22abdc220680b2f3db`

*(Shortlog double-counts across refs; unique SHA count is authoritative.)*

### Merge commits

```
e6b3194 Merge pull request #57 …
860a11f merge main into live evaluation gate branch
5e68810 Merge pull request #56 …
b56b435 Merge pull request #53 …
d08d839 Merge pull request #48 …
```

GitHub merge commits keep committer `GitHub <noreply@github.com>` — **do not rewrite** committer to canonical (preserves platform semantics).

---

## 2. Backup (no force-push)

| Artifact | Path | SHA-256 |
|----------|------|---------|
| Full `--all` bundle | `/opt/cursor/artifacts/adapti-guard-pre-attribution-rewrite-20260918T111644Z.bundle` | `af4ef14132047a9a9411605dd27b0368a7bbef81ceec29fa9678443813ec7cd5` |

Restore check (read-only): `git clone /opt/cursor/artifacts/adapti-guard-pre-attribution-rewrite-20260918T111644Z.bundle adapti-guard-restored`

Experimental rewrite clone: `/tmp/adapti-guard-attribution-exp` (disposable; **not** pushed).

---

## 3. Commit SHAs referenced in scientific provenance

Historical **git commit IDs** are embedded in docs and experiment artifacts (file **content** SHAs are separate and unchanged by attribution rewrite).

### High-impact pointers

| SHA | Role |
|-----|------|
| `b075df0f5ec5ad11ede76ac4e4079cade15208f1` | Q2 evidence commit (manifest, docs, run dir name suffix) |
| `612f577118a19949b4862a3b27b801db8c7eef65` | Early eval / frozen eval_v1 manifest |
| `35833a64b35a98d596d729c3fa7687e3228381ca` | Phase5 / FINAL_RESEARCH_MANIFEST |
| `a2681e928fe2235a2dd9265cd25072193bdff359` | Phase-1 confirmatory live lock |
| `46bffe142be334260f767a98c2201ca273c24f71` | Detector v4 / VNEXT docs |
| `eaa1f029d3fd524fd3c5beeea6e02329adee7d20` | Layer A diagnostic manuscript |
| `7e401714f97a95fc16a718291e7ec499297b2931` | Stage-B code (run dir `…_7e401714` not in git) |

Also cited in many `docs/research/q2_publication_package/*`, `MANUSCRIPT_FINAL.md`, `FINAL_SUBMISSION_READINESS.json`, `experiments/real_llm_eval/P3_DETECTOR_COMPARISON/p3_stage_c_q2_…/manifest.json`, and numerous `experiments/**/config.json` / `provenance.json` files.

**Frozen dataset file hashes (P1/P2/Q2 predictions, vnext pack, etc.) do not depend on git commit metadata** — only on file bytes. Offline tests such as `test_frozen_pack_hash_unchanged` remain valid after rewrite.

---

## 4. Does history rewrite harm scientific provenance?

| Layer | After attribution-only rewrite |
|--------|------------------------------|
| **Tree / blob content** | Unchanged (verified: `git diff old_sha new_sha` empty for sampled pairs). |
| **Recorded `git_commit` in manifests & docs** | **Stale** — every rewritten commit gets a new SHA; descendants all change. |
| **Run directory names** (e.g. `…_b075df0f`) | Unchanged on disk; still refer to **old** short hash by design. |
| **External citations / PR links** | GitHub PR merge SHAs (e.g. `b56b435`, `d08d839`) would change if history is force-pushed. |

**Conclusion:** Rewrite is **safe for code and frozen bytes**, but **not provenance-neutral** unless you add a **published old→new SHA map** and/or a controlled update pass on `git_commit` fields (that update pass would be a **separate, explicit** human-approved docs/manifest change — not done here).

---

## 5. Commits eligible for attribution change

| Email | Commits as author (`--author`) | Action |
|--------|-------------------------------|--------|
| `cursoragent@cursor.com` | 179 | → canonical |
| `your-email@example.com` | 8 | → canonical |
| `research@localhost` | 4 | → canonical **if owner confirms** local placeholder (see §6) |
| `206951365+cursor[bot]@users.noreply.github.com` | 2 (PR merge authors) | → canonical author; keep GitHub committer |

**~191 commits** have author metadata changed; **~193** rows if counting committer-only suspicious emails.

---

## 6. Adapti-Guard Research `<research@localhost>`

Four early commits (examples):

- `804659ce…` — `docs: finalize research README`
- `27c84b2c…`, `8be47c88…`, `68e66def…`

No evidence this is a third party; pattern matches **local git `user.email` placeholder** on the owner machine before GitHub noreply was configured. **Included in experimental rewrite**, but **owner must confirm** before production rewrite.

---

## 7. Rewrite risk summary

| Risk | Severity | Mitigation |
|------|----------|------------|
| Stale `git_commit` in Q2/Phase manifests | **High** | Ship `/opt/cursor/artifacts/git_attribution_sha_map_*.txt`; optional follow-up doc update with human sign-off |
| Force-push coordination (76 remote branches) | **High** | Single maintenance window; notify collaborators; use `--force-with-lease` only after approval |
| GitHub PR/merge SHA links break | **Medium** | Expected; archive pre-rewrite bundle |
| Accidental blob change | **Low** | Verified empty diff old vs new commit pairs |
| Bash `case` on `cursor[bot]` email | **Medium** | `[bot]` is a character class in `case` — use `if [ "$GIT_AUTHOR_EMAIL" = "206951365+cursor[bot]@users.noreply.github.com" ]` (see §9) |

---

## 8. Experimental rewrite (local only)

**Branch:** `cursor/git-attribution-rewrite-test-f6f3` in `/tmp/adapti-guard-attribution-exp`  
**Tool:** `git filter-branch --env-filter` (suspicious emails → canonical; GitHub committer untouched)

### Results on `cursor/q2-publication-hardening-f6f3` lineage (149 commits)

| Metric | Before | After |
|--------|--------|--------|
| Authors on branch | Mostly Cursor / placeholders | **148** canonical, **1** cursor[bot] (bash `case` bug) |
| Branch tip | `6ac7d69b57f78f35152a2b569bee3adc54b93674` | `9af998b81f8c121bf021024007f287a1d6519c1f` |
| Q2 evidence commit | `b075df0f5ec5ad11ede76ac4e4079cade15208f1` | `19cadfd5799a3026598df4d1ca9c3a5ea5c79fa6` |
| Tree at tip vs old tip | — | **Identical** (`git diff` empty) |

Full old→new map (branch): `/opt/cursor/artifacts/git_attribution_sha_map_q2_hardening_branch.txt` (**149** pairs).

### Post-rewrite checks (experiment clone)

| Check | Result |
|--------|--------|
| `pytest tests/ -m "not stage_b"` | **489 passed**, 8 skipped |
| `test_frozen_pack_hash_unchanged` | **PASS** |
| Frozen Q2 manifest file SHA-256 (workspace) | `915632dac1be39ec8ebd490225c0899ba2acacf493edcfc8a43ceb6d84fa0cc6` (unchanged on disk in workspace; same bytes in rewritten tree) |

---

## 9. Recommended production procedure (requires your explicit approval)

**Do not run on `main` until you confirm.** Use the bundle backup first.

### 9.1 Fresh mirror and rewrite (fixed bot email handling)

```bash
cd /path/to/safe/directory
git clone --mirror git@github.com:mohammadreza583/adapti-guard.git adapti-guard.git
cd adapti-guard.git

export FILTER_BRANCH_SQUELCH_WARNING=1
git filter-branch -f --env-filter '
CANON_NAME="MohammadReza S M"
CANON_EMAIL="121524262+Mohammadreza583@users.noreply.github.com"
fix_author() {
  case "$1" in
    cursoragent@cursor.com|your-email@example.com|research@localhost) return 0 ;;
  esac
  [ "$1" = "206951365+cursor[bot]@users.noreply.github.com" ] && return 0
  return 1
}
if fix_author "$GIT_AUTHOR_EMAIL"; then
  export GIT_AUTHOR_NAME="$CANON_NAME"
  export GIT_AUTHOR_EMAIL="$CANON_EMAIL"
fi
if fix_author "$GIT_COMMITTER_EMAIL"; then
  export GIT_COMMITTER_NAME="$CANON_NAME"
  export GIT_COMMITTER_EMAIL="$CANON_EMAIL"
fi
' --tag-name-filter cat -- --all
```

Prefer **`git filter-repo`** (with `--email-callback` or mailmap) if installed — clearer and faster than `filter-branch`.

### 9.2 Verify before any push

```bash
git shortlog -sne origin/main   # expect essentially one human author + GitHub committer on merges
git diff <OLD_TIP> <NEW_TIP>    # must be empty for each branch tip
pytest tests/ -q
python3 -m pytest tests/test_vnext_adapt_artifact_schema.py::test_frozen_pack_hash_unchanged -q
# Generate full SHA map: git log refs/original/... vs rewritten refs
```

### 9.3 Publish to GitHub (only after your OK)

```bash
git push --force-with-lease origin --all
git push --force-with-lease origin --tags   # none today
```

Then publish `git_attribution_sha_map_*.txt` in `docs/audits/` and add a short **provenance errata** note listing that embedded `git_commit` strings refer to pre-rewrite SHAs unless updated in a follow-up PR.

### 9.4 Optional: omit `research@localhost` until confirmed

Remove `research@localhost` from `fix_author` if you want a conservative first pass (4 commits stay as-is).

---

## 10. Answers to final checklist

| Question | Answer |
|----------|--------|
| **Is rewrite safe?** | **Conditionally yes** for file integrity and tests; **not** safe for provenance strings unless you add SHA map + optional manifest/doc follow-up. |
| **How many commits change attribution?** | **~191–193** metadata rewrites; **all descendant SHAs** change (149 on current feature branch alone). |
| **Which SHAs change?** | All non-root commits on rewritten branches; examples: `6ac7d69…`→`9af998b8…`, `b075df0f…`→`19cadfd5…`. See map file. |
| **What provenance is affected?** | Every `git_commit` / `evidence_commit` field pointing at old SHAs; GitHub PR merge links; run folder suffixes still mean old short hash. |
| **Tests / integrity after experiment?** | **Yes** — 489 passed; frozen pack hash test passed; trees identical. |
| **Final commands?** | §9 — backup bundle already at `/opt/cursor/artifacts/…`; filter + verify + **force-with-lease only with your approval**. |

---

**Status:** AUDIT COMPLETE · experimental rewrite validated locally · **no remote history changed** · **awaiting owner confirmation** before production rewrite and push.
