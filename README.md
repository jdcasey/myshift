# myshift

PagerDuty schedule management CLI tools.

## Installation

### From Source

```bash
git clone https://github.com/jdcasey/myshift.git
cd myshift
pip install -e .
```

### From Container

```bash
# Using podman
podman run -it --rm -v /path/to/myshift.yaml:/etc/myshift.yaml quay.io/jdcasey/myshift

# Using docker
docker run -it --rm -v /path/to/myshift.yaml:/etc/myshift.yaml quay.io/jdcasey/myshift
```

### From PyPI

```bash
pip install myshift
```

## Configuration

The tool requires a configuration file. You can generate a sample configuration file by running:

```bash
myshift override --print-sample-config
```

This will print a sample `myshift.yaml` to standard output. Save this file to one of the following standard locations:

### Linux
- `/etc/myshift.yaml`
- `~/.config/myshift.yaml`
- `./myshift.yaml`

### macOS
- `/Library/Application Support/myshift.yaml`
- `~/Library/Application Support/myshift.yaml`
- `~/.config/myshift.yaml`
- `./myshift.yaml`

## Usage

### Container Usage

```bash
# Using podman
podman run -it --rm -v /path/to/myshift.yaml:/etc/myshift.yaml myshift

# Using docker
docker run -it --rm -v /path/to/myshift.yaml:/etc/myshift.yaml myshift
```

**NOTE::** When you run in container mode, the `repl` command will be used.

### Command Line Usage

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