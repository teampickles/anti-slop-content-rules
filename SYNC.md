# Ownership and synchronization

This repository is the authoritative source of C01–C26 and E01–E08. The separate private development repository is https://github.com/teampickles/anti-slop-design-rules . It consumes only C03 and C20–C24.

For a shared-rule change: update rules/copy.md here, regenerate CONTENT-RULES.md, test and merge. In an authorized local clone of the development repository run `python3 scripts/sync_copy.py --source /path/to/anti-slop-content-rules`. It requires a clean committed source checkout and records its exact revision plus the six-rule digest. Review the diff, regenerate development bundles, test, and merge a development PR. Never edit the downstream copy by hand. Each repository has an independent version; a synchronization updates the consumer deliberately.

Neither CI nor normal use requires access to the other private repository. No credentials, cross-repository secrets, paid services or background jobs are installed.
