# patcon-skills

A collection of reusable [agent skills][agent-skills] for use with [Claude Code][claude-code].

## What are skills?

Skills are markdown files that extend what your AI coding agent can do. Each one contains instructions that get loaded into context when relevant -- reusable prompts your agent can discover and apply automatically.

This repo follows the [Agent Skills][agent-skills] open standard, which works across multiple AI tools.

To learn more:

- [Agent Skills standard][agent-skills] -- the open spec this repo follows
- [Skills in the Claude Code docs][skills-docs] -- how skills work, where they live, and how to configure them

## Usage

Copy any skill directory into your own project:

```sh
cp -r skills/example /path/to/your-project/.claude/skills/example
```

Or use this repo as a [Claude Code plugin][plugins-docs]:

```sh
# from your project
claude plugin add patcon/patcon-skills
```

## Structure

Each skill is a directory under `skills/` with a `SKILL.md` entrypoint:

```
skills/
  example/
    SKILL.md        # Instructions (required)
    ...             # Optional supporting files
```

See the [skill directory layout docs][skills-docs] for details on supporting files, frontmatter options, and more.

## Future skill ideas

Potential skills to extract or create:

- **patcon-interest-assessor** — Encodes patcon's research interests and preferences for evaluating whether a paper, project, or link is worth deeper attention. Includes: keywords to skim for (PCA, clustering, UMAP, dimensional reduction, etc.), what makes something interesting (new math applied to opinion data, datasets, passive/emergent mapping), what's less interesting (papers that critique discrete mechanisms in favor of LLM nuance, papers pushing active consensus-building), and output formats (Roam page template). Currently embedded in `polis-scouring` under "User Preferences" but is general enough to be its own skill, reusable across different scouring/research workflows.
- **roam-reader** — Read and query patcon's Roam Research graph. Roam doesn't have a public API, so this would likely need to work via JSON export (Roam can export the full graph as JSON), an MCP server wrapping that export, or possibly the unofficial Roam backend API. Useful for checking whether a paper/author/concept already has a page before creating a new one, and for finding related notes.
- **roam-writer** — Create or update pages in patcon's Roam Research graph. Even harder than reading — options might include: generating Roam-flavored markdown for manual paste (current approach), automating paste via AppleScript/clipboard, using the Roam `SmartBlocks` or `roam/render` extension APIs, or an MCP server that writes via Roam's backend. Would enable the scouring workflow to save interesting papers directly into Roam without manual copy-paste.

## Contributing

PRs welcome! To add a skill, create a new directory under `skills/` with a `SKILL.md` file.

## License

[MIT](LICENSE)

[agent-skills]: https://agentskills.io
[claude-code]: https://docs.anthropic.com/en/docs/claude-code
[skills-docs]: https://docs.anthropic.com/en/docs/claude-code/skills
[plugins-docs]: https://docs.anthropic.com/en/docs/claude-code/plugins
