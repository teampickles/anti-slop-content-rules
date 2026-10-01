# Anti-Slop Content Rules

Private Pickles content standard. Version 1.0.0. Canonical instructions are English, with Russian examples; usage guidance is bilingual.

Use [CONTENT-RULES.md](CONTENT-RULES.md) for articles, explainers, newsletters, posts, commercial copy and interface wording. It contains 26 copy rules, eight editorial rules, examples and complete notices. It requires no software project, build, deployment or engineering team for writing tasks.

> Read CONTENT-RULES.md. Write or edit the supplied material for the specified audience and channel. Preserve facts, author intent and natural language. Verify consequential claims and return the finished text with material unresolved facts separately.

## По-русски

Скачайте [CONTENT-RULES.md](CONTENT-RULES.md) и передайте агенту с задачей и исходными материалами. Для работы над статьёй достаточно этого файла. Он охватывает голос автора, конкретику, русские и английские штампы, источники, структуру, редактуру, публикацию и актуальность. Само хранение файла не гарантирует, что агент его прочитал: прикрепите его или явно укажите путь.

Для разработки сайтов и приложений используйте отдельный [репозиторий разработки](https://github.com/teampickles/anti-slop-design-rules). Когда сайт нужно и разработать, и наполнить текстами, подключайте оба стандарта по назначению.

## Maintenance

Edit rules/ and run:

```sh
python3 scripts/build_bundle.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Build scripts maintain this package; they do not impose engineering tasks on authors. [Ownership and synchronization](SYNC.md). [Migration record](MIGRATION.md). [License](LICENSE), [notices](NOTICE.md). Keep this approach and assets private; existing historical license terms remain intact.
