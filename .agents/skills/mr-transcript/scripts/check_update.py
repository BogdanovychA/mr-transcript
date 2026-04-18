import logging
import os
import io
import urllib.request

logger = logging.getLogger(__name__)

def get_remote_content(repo_url: str):
    try:
        with urllib.request.urlopen(repo_url, timeout=5) as response:
            content = response.read().decode('utf-8')
            return content
    except Exception as e:
        logger.error(f"Error getting remote content: {e}")
        return None


def get_local_content():

    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        skill_path = os.path.join(base_dir, "SKILL.md")

        with open(skill_path, 'r', encoding='utf-8') as f:
            return f.read()

    except Exception as e:
        logger.error(f"Error getting local content: {e}")
        return None

def read_source(source: io.StringIO):

    result = {}
    first_line = next(source, None)

    if first_line is None or first_line.strip() != "---":
        return result

    for line in source:

        line = line.strip()

        if line == "---":
            break

        if ":" in line:
            key, value = line.split(":", 1)
            key=key.strip()
            value = value.strip()
            result[key] = value

    return result

def get_owner_and_repo(repository: str):

    suffix = repository.removeprefix("https://github.com/")
    owner, repo = suffix.split("/", 1)
    repo = repo.strip("/")

    return owner, repo

def main():

    local_content = get_local_content()
    local_data = read_source(io.StringIO(local_content))

    if not local_data:
        print("Could not retrieve local data from SKILL.md.")
        return

    try:
        local_version = local_data["version"]
        repository = local_data["repository"]
        skill_name = local_data["name"]
    except KeyError:
        print("Could not retrieve local data from SKILL.md.")
        return

    owner, repo = get_owner_and_repo(repository)

    repo_raw = f"https://raw.githubusercontent.com/{owner}/{repo}/main/.agents/skills/{skill_name}/SKILL.md"

    remote_content = get_remote_content(repo_raw)
    remote_data = read_source(io.StringIO(remote_content))

    if not remote_data:
        print("Could not retrieve remote data from SKILL.md.")
        return

    try:
        remote_version = remote_data["version"]
    except KeyError:
        print("Could not retrieve remote data from SKILL.md.")
        return

    if remote_version > local_version:
        print(
            f"A new version of the skill is available: {remote_version} (current: {local_version})."
        )
        print(
            f"Please update the skill using the command: npx skills add {owner}/{repo} --skill {skill_name}"
        )
    else:
        print(f"Skill is up to date (version {local_version}).")


if __name__ == "__main__":
    main()
