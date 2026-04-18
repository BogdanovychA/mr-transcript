import os
import re
import urllib.request

# URL of the remote SKILL.md file for version comparison
REPO_URL = "https://raw.githubusercontent.com/BogdanovychA/mr-transcript/main/.agents/skills/mr-transcript/SKILL.md"


def get_version_from_content(content):
    """Extracts the version from the SKILL.md YAML frontmatter."""
    match = re.search(r'version:\s*([0-9.]+)', content)
    if match:
        return match.group(1)
    return None


def get_local_version():
    """Reads the version from the local SKILL.md file."""
    try:
        # Assuming the script is in scripts/ and SKILL.md is in the parent directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        skill_path = os.path.join(base_dir, "SKILL.md")

        if os.path.exists(skill_path):
            with open(skill_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return get_version_from_content(content)
    except Exception as e:
        print(f"Error reading local version: {e}")
    return None


def get_remote_version():
    """Fetches the version from the remote repository."""
    try:
        with urllib.request.urlopen(REPO_URL, timeout=5) as response:
            content = response.read().decode('utf-8')
            return get_version_from_content(content)
    except Exception as e:
        print(f"Error checking for updates: {e}")
    return None


def main():
    local_version = get_local_version()
    remote_version = get_remote_version()

    if not local_version:
        print("Could not retrieve local version from SKILL.md.")
        return

    if not remote_version:
        print("Could not retrieve remote version.")
        return

    if remote_version > local_version:
        print(
            f"A new version of the skill is available: {remote_version} (current: {local_version})."
        )
        print(
            f"Please update the skill using the command: npx skills add BogdanovychA/mr-transcript --skill mr-transcript"
        )
    else:
        print(f"Skill is up to date (version {local_version}).")


if __name__ == "__main__":
    main()
