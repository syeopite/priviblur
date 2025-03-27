import subprocess


# Taken from the Invidious Project
# CURRENT_BRANCH = subprocess.run(
#     "git branch --show-current".split(),
#     stdout=subprocess.PIPE
# ).stdout.decode("utf-8").strip()

CURRENT_COMMIT = (
    subprocess.run(
        "git rev-list HEAD --max-count=1 --abbrev-commit".split(), stdout=subprocess.PIPE
    )
    .stdout.decode("utf-8")
    .strip()
)

# CURRENT_VERSION = subprocess.run(
#     "git log -1 --format=%ci".split(),
#     stdout=subprocess.PIPE
# ).stdout.decode("utf-8").split()[0].replace("-", ".")

CURRENT_VERSION = "v0.4.0-dev"

PROJECT_VERSION = f"{CURRENT_VERSION}"
VERSION = f"{CURRENT_VERSION}-{CURRENT_COMMIT}"
