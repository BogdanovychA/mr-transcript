# mr-transcript

[![DOI](https://zenodo.org/badge/1212408609.svg)](https://doi.org/10.5281/zenodo.19630758) [![PyPI Downloads](https://static.pepy.tech/personalized-badge/mr-transcript?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=BLUE&left_text=downloads)](https://pepy.tech/projects/mr-transcript)

A convenient wrapper for the `youtube-transcript-api` library designed to retrieve YouTube video transcripts quickly and reliably.

## Key Features

*   **Automatic URL Handling:** Supports various YouTube link formats, including `youtube.com`, `youtu.be`, `shorts`, and `embed`.
*   **Intelligent Search:** The package first looks for manually created transcripts; if they are unavailable, it automatically switches to YouTube's auto-generated ones.
*   **Timecodes:** Option to add timestamps to each text block.
*   **Language List:** Quickly retrieve a dictionary of all available languages for a specific video.
*   **Type Safety:** Full support for type annotations for better development experience.

## Installation

Install the package via `pip`:

```bash
pip install mr-transcript
```

Or using `uv`:

```bash
uv add mr-transcript
```

## Quick Start

```python
from mr_transcript import get_transcript, get_languages

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# 1. Check available languages
languages = get_languages(url)
print(f"Available languages: {languages}")

# 2. Retrieve transcript text (e.g., in English)
if "en" in languages:
    text = get_transcript(url, language="en", timecodes=True)
    print(text[:500])  # Prints the first 500 characters
```

## AI Agent Skill

This repository includes a specialized skill for AI agents (like Gemini CLI). It helps the agent provide expert assistance with Python coding, URL parsing, and integrating this library into your projects.

To install the skill, run:
```bash
npx skills add BogdanovychA/mr-transcript --skill "mr-transcript"
```

## Function Descriptions

### `get_transcript(video_id, language, timecodes=False)`
Retrieves the full transcript text.
*   `video_id`: Video ID or a full link.
*   `language`: Language code (e.g., 'en', 'uk').
*   `timecodes`: If `True`, adds the start time to each text block.

### `get_languages(video_id)`
Returns a dictionary of all available languages for the video.
*   Format: `{"language_code": "language_name"}` (e.g., `{"en": "English"}`).

## Requirements

*   Python >= 3.10
*   [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) >= 1.2.4

## License

This project is licensed under the MIT License.
