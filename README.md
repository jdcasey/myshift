# myshift

PagerDuty schedule management CLI tools.

## Installation

Clone this repository and install in development mode:

```bash
pip install -e .
```

This will install the `myshift` command-line tool.

## Running in a Container

You can run myshift in a container using the pre-built image from quay.io or build it yourself using the provided `Containerfile` (Fedora-based).

### Using the pre-built image

The container image is available at `quay.io/jdcasey/myshift`. You can run it with:

```bash
podman run -it --rm -v /path/to/spre-config.yaml:/etc/myshift/spre-config.yaml quay.io/jdcasey/myshift
# or
docker run -it --rm -v /path/to/spre-config.yaml:/etc/myshift/spre-config.yaml quay.io/jdcasey/myshift
```

### Building the container yourself

If you prefer to build the container locally:

```bash
podman build -t myshift .
# or
docker build -t myshift .
```

Then run it with:

```bash
podman run -it --rm -v /path/to/spre-config.yaml:/etc/myshift/spre-config.yaml myshift
# or
docker run -it --rm -v /path/to/spre-config.yaml:/etc/myshift/spre-config.yaml myshift
```

The container will start directly in the myshift REPL. You can use all the same commands as described below.

## Generating the Configuration File

To generate a sample configuration file, run:

```bash
myshift override --print-sample-config
```

This will print a sample `spre-config.yaml` to standard output. Save this file to one of the following standard locations:

- **Linux:**
  - `/etc/spre-config.yaml`
  - `~/.config/spre-config.yaml`
  - `./spre-config.yaml`
- **macOS:**
  - `/Library/Application Support/spre-config.yaml`
  - `~/Library/Application Support/spre-config.yaml`
  - `~/.config/spre-config.yaml`
  - `./spre-config.yaml`

### Configuration Parameters

- `pagerduty_token`: **(required)** Your PagerDuty API token. This is required for all API operations.
- `pagerduty_base_url`: The base URL for the PagerDuty API. The default is `https://api.pagerduty.com`.
- `schedule_id`: (optional) The default PagerDuty schedule ID to use if not specified on the command line.

Example configuration:

```yaml
pagerduty_token: PASTE_YOUR_PD_API_TOKEN_HERE
pagerduty_base_url: https://api.pagerduty.com
# schedule_id: PASTE_YOUR_SCHEDULE_ID_HERE
```

## Using the Sub-Commands

### Override Command

The `override` sub-command allows you to override a sequence of scheduled shifts for a PagerDuty schedule.

**Example:**
```bash
myshift override --user-email new.oncall@example.com \
                --target-user-email old.oncall@example.com \
                --start-date 2024-07-01 \
                --dry-run
```
- `--user-email`: The email address of the user who will be assigned to the override.
- `--target-user-email`: The email address of the user whose scheduled shifts will be overridden.
- `--start-date`: The first day to check for scheduled shifts to override.
- `--dry-run`: Show what would be overridden, but do not make any changes.

If you omit `--dry-run`, the overrides will be created in PagerDuty.

You can also use `--user-id` and `--target-user-id` if you know the PagerDuty user IDs.

If you do not specify the schedule ID on the command line, it will be read from the configuration file if present.

---

### Upcoming Command

The `upcoming` sub-command shows upcoming on-call shifts for a specific user in the configured schedule.

**Example:**
```bash
myshift upcoming --user-email someone@example.com --weeks 6
```
- `--user-email` or `--user-id`: Specify the user whose upcoming shifts you want to see.
- `--weeks`: Number of weeks to look ahead (default: 4).

---

### Plan Command

The `plan` sub-command prints all on-call shifts for the configured schedule in the coming N weeks, for all users.

**Example:**
```bash
myshift plan --weeks 8
```
- `--weeks`: Number of weeks to look ahead (default: 4).

---

### REPL Command

The `repl` sub-command starts an interactive shell where you can run any of the above sub-commands as commands, with the same arguments as the CLI.

**Example:**
```bash
myshift repl
```

Once inside the REPL, you can type commands like:
```
(myshift) override --user-email new.oncall@example.com --target-user-email old.oncall@example.com --start-date 2024-07-01 --dry-run
(myshift) upcoming --user-email someone@example.com --weeks 6
(myshift) plan --weeks 8
(myshift) exit
```
Type `help` or `?` in the REPL for a list of available commands.

---

For more options, run:

```bash
myshift <sub-command> --help
```

## Git Hooks

This project includes git hooks to enforce commit message standards. The hooks are stored in the `git-hooks` directory and can be installed using one of the following methods:

### Automatic Installation

Run the following command in the project root:

```bash
git config core.hooksPath git-hooks
```

### Manual Installation

Copy the hooks from the `git-hooks` directory to your `.git/hooks` directory:

```bash
cp git-hooks/* .git/hooks/
chmod +x .git/hooks/*
```

### Commit Message Standards

The project follows the [Conventional Commits](https://www.conventionalcommits.org/) specification. Each commit message should follow this format:

```
<type>(<scope>): <description>
```

#### Types

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools
- `ci`: Changes to CI configuration files and scripts

#### Scopes

- `cli`: Command-line interface changes
- `config`: Configuration changes
- `api`: API-related changes
- `container`: Container-related changes
- `deps`: Dependency updates
- `docs`: Documentation changes

#### Examples

```bash
feat(cli): add new command for schedule management
fix(api): handle rate limiting errors gracefully
docs(docs): update contributing guidelines
chore(deps): update pdpyras to latest version
```

When a commit message doesn't meet these standards, the hook will:
1. Show the error message
2. Display the current commit message
3. Offer options to:
   - Edit the message (opens git commit editor)
   - Abort the commit
   - Force the commit despite validation errors 