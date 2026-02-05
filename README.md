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

## Contributing

PRs welcome! To add a skill, create a new directory under `skills/` with a `SKILL.md` file.

## License

[MIT](LICENSE)

[agent-skills]: https://agentskills.io
[claude-code]: https://docs.anthropic.com/en/docs/claude-code
[skills-docs]: https://docs.anthropic.com/en/docs/claude-code/skills
[plugins-docs]: https://docs.anthropic.com/en/docs/claude-code/plugins
