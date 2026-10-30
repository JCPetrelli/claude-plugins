# Claude Code plugins by Jacopo Castellano

[![sync](https://github.com/JCPetrelli/claude-plugins/actions/workflows/sync.yml/badge.svg)](https://github.com/JCPetrelli/claude-plugins/actions/workflows/sync.yml) [![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

One [Claude Code](https://claude.com/claude-code) plugin marketplace for five tools. Add it once, then install the plugins you want.

```
/plugin marketplace add JCPetrelli/claude-plugins
/plugin install brickwise@jcpetrelli
```

<!-- plugins:start -->
| Plugin | What it does | Version | Install |
|---|---|---|---|
| [Brickwise](https://github.com/JCPetrelli/brickwise) | Explains a codebase or any topic as an interactive 3D brick model | [1.0.0](https://github.com/JCPetrelli/brickwise/releases/tag/v1.0.0) | `/plugin install brickwise@jcpetrelli` |
| [Rubricai](https://github.com/JCPetrelli/rubricai) | Cleans up and completes the macOS Contacts address book, one reviewed plan at a time | 0.1.0 (main) | `/plugin install rubricai@jcpetrelli` |
| [Bookmarkwise](https://github.com/JCPetrelli/bookmarkwise) | Cleans up Chrome bookmarks in your own style, through a reviewed plan and a one-off extension | [0.1.0](https://github.com/JCPetrelli/bookmarkwise/releases/tag/v0.1.0) | `/plugin install bookmarkwise@jcpetrelli` |
| [tab-tag](https://github.com/JCPetrelli/tab-tag) | Gives each session's iTerm2 tab a colour and a one- or two-word name | 0.2.0 (main) | `/plugin install tab-tag@jcpetrelli` |
| [close-tab](https://github.com/JCPetrelli/close-tab) | Say "close the session" and Claude Code finishes, then closes its iTerm2 tab | [1.0.0](https://github.com/JCPetrelli/close-tab/releases/tag/v1.0.0) | `/plugin install close-tab@jcpetrelli` |
<!-- plugins:end -->

Each plugin lives in its own repository, with its code, tests, issues and releases. This repository holds only the list. When a tool gets a new release, the list follows it within a day, so `/plugin marketplace update jcpetrelli` brings you the new version.

---

## Brickwise

Explains a codebase, an architecture or any complicated topic as an interactive 3D brick model. Each concept is a brick, related bricks form a sub-assembly, and a brick's size shows how complex its concept is. Explode the model, take one group apart, click a brick for a short explanation and an example.

![Clicking a brick opens its explanation](https://raw.githubusercontent.com/JCPetrelli/brickwise/main/docs/images/popup.jpg)

[Live demos](https://jcpetrelli.github.io/brickwise/) · [Repository](https://github.com/JCPetrelli/brickwise) · `/plugin install brickwise@jcpetrelli`

## Rubricai

Cleans up and completes the macOS Contacts address book: exact copies, same-person merges, entity resolution by name, Title Case, and people who are missing from Contacts but appear in Apple Mail and WhatsApp Desktop. You talk, Claude runs the tools, and nothing changes until you approve a plan. Every change writes a vCard undo file first.

![Rubricai: dedupe, merge and complete macOS Contacts](https://raw.githubusercontent.com/JCPetrelli/rubricai/main/docs/images/social-preview.png)

[Repository](https://github.com/JCPetrelli/rubricai) · `/plugin install rubricai@jcpetrelli`

## Bookmarkwise

Cleans up your Chrome bookmarks in your own style. Claude asks how you like bookmarks named, organized and pruned, shows the plan as tables, and changes nothing until you say yes. A tiny one-off extension then applies the plan through Chrome itself, after a backup and a check that nothing changed since the plan was made. Undo comes from the backup.

![Say "clean up my bookmarks": duplicates and junk links disappear, titles get your naming style](https://raw.githubusercontent.com/JCPetrelli/bookmarkwise/main/docs/bookmarkwise.gif)

[Repository](https://github.com/JCPetrelli/bookmarkwise) · `/plugin install bookmarkwise@jcpetrelli`

## tab-tag

Gives every Claude Code session's iTerm2 tab its own colour and a one- or two-word name from the first prompt, so you can tell five open sessions apart without clicking through them.

![Five identical tabs get a colour each, then a name from the first prompt](https://raw.githubusercontent.com/JCPetrelli/tab-tag/main/docs/demo.gif)

[Repository](https://github.com/JCPetrelli/tab-tag) · `/plugin install tab-tag@jcpetrelli`

## close-tab

End your last message with "close the session". Claude Code finishes the work, writes one short line, then closes its own iTerm2 tab. If a step fails or a decision is needed, the tab stays open.

![Say "close the session" and the iTerm2 tab closes](https://raw.githubusercontent.com/JCPetrelli/close-tab/main/docs/close-tab.png)

[Repository](https://github.com/JCPetrelli/close-tab) · `/plugin install close-tab@jcpetrelli`

---

## Updates

- `/plugin marketplace update jcpetrelli` fetches the newest list; `/plugin` shows what can be updated.
- A plugin with releases is pinned to its latest release tag. A plugin without releases follows its main branch.
- A GitHub Action ([sync.yml](.github/workflows/sync.yml)) checks the five repositories every day and on demand. When a new release or version appears, it updates [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) and the table above, and commits the change.

## Maintaining this list

- Add or remove a plugin in [`plugins.json`](plugins.json), then run `python3 scripts/sync.py`. Do not edit `marketplace.json` or the table by hand: the sync rewrites them.
- Releasing a tool: bump `version` in its `.claude-plugin/plugin.json`, tag it (`v1.2.0`) and publish a GitHub release. The next sync picks it up; run the workflow by hand ("Run workflow") to do it at once.
- `python3 scripts/sync.py --check` exits 1 when the files are out of date.

## License

MIT. Each plugin has its own license in its repository.
