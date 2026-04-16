# -*- coding: utf-8 -*-

from __future__ import annotations

import logging
import re
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, TypeVar

from youtube_transcript_api import NoTranscriptFound, Transcript

if TYPE_CHECKING:
    from youtube_transcript_api import TranscriptList

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def check_and_clear(id_or_url: str) -> str:
    """Returns the video ID: extracts it from the URL or returns the input string as is."""
    if id_or_url.startswith("http://") or id_or_url.startswith("https://"):
        return get_video_id(id_or_url)
    return id_or_url


def ensure_video_id(func: F) -> F:
    """Decorator for automatically converting a URL to a video ID in the first argument."""

    @wraps(func)
    def wrapper(video_id: str, *args: Any, **kwargs: Any) -> Any:
        video_id = check_and_clear(video_id)
        return func(video_id, *args, **kwargs)

    return wrapper  # type: ignore


def get_text(transcript: Transcript, timecodes: bool = False) -> str:
    """Converts a transcript object into formatted text (with or without timecodes)."""

    transcript_text: list[str] = []

    for block in transcript.fetch():
        text_block = f"{block.start}: {block.text}" if timecodes else block.text
        transcript_text.append(text_block)

    return "\n".join(transcript_text)


def get_transcript_internal(
    transcript_list: TranscriptList,
    language: str,
    manually: bool = True,
    timecodes: bool = False,
) -> str:
    """Searches for transcripts of a given language and type (manual/generated) in the list."""

    txt_prefix = "Manually"

    try:

        if manually:
            transcript = transcript_list.find_manually_created_transcript([language])
        else:
            txt_prefix = "Generated"
            transcript = transcript_list.find_generated_transcript([language])

        logger.info(f"{txt_prefix} transcript found [lang: {language}]")
        return get_text(transcript, timecodes=timecodes)

    except NoTranscriptFound:
        logger.info(f"{txt_prefix} transcript not found [lang: {language}]")
        return ""


def get_video_id(url: str) -> str:
    """Extracts the video ID from YouTube links of various formats."""

    regex = r"(?:v=|\/|be\/|shorts\/|embed\/)([0-9A-Za-z_-]{10,12})(?:[&?\s]|$)"
    match = re.search(regex, url)
    if match:
        return match.group(1)

    logger.error(f"Invalid YouTube URL: {url}")
    return ""
