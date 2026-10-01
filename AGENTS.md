# Maintaining the content standard

Keep this repository private. Preserve licenses and attribution. This repository owns C01–C26 and E01–E08: articles, copy, voice, evidence and publication. Do not add software-delivery rules or apply engineering checks to a user's writing task.

Edit rules/; CONTENT-RULES.md is generated. Keep IDs stable. MUST is scoped correctness, DEFAULT is overridable house style, REVIEW requires judgment. User intent, facts and grammar take precedence. Do not claim authorship detection or rankings.

The development repository consumes C03/C20–C24 as a pinned local snapshot. Changes to these rules require a deliberate synchronization PR there; no runtime download or automatic cross-repository write. See SYNC.md.

After edits run python3 scripts/build_bundle.py, python3 scripts/validate.py and python3 -m unittest discover -s tests -v. Report packaging checks separately from real editorial outcomes.
