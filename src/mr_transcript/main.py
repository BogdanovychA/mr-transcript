# -*- coding: utf-8 -*-

import logging

from youtube_transcript_api import VideoUnavailable, YouTubeTranscriptApi

from .utils import ensure_video_id, get_transcript_internal

logger = logging.getLogger(__name__)


@ensure_video_id
def get_transcript(video_id: str, language: str, timecodes: bool = False) -> str:
    """
    Retrieves the full transcript text for a specified YouTube video.

    The function automatically processes both direct video IDs and full links.
    The search is performed in two stages: first, manually created transcripts are sought,
    and if they are unavailable, YouTube's auto-generated ones are used.

    Args:
        video_id (str): Video identifier (11 characters) or a full link to it.
        language (str): Language code (e.g., 'uk', 'en', 'pl').
        timecodes (bool): If True, adds timestamps (start time) to each text block.

    Returns:
        str: Full transcript text. Returns an empty string in case of an error
             or if transcripts for the specified language are not found.
    """

    client = YouTubeTranscriptApi()

    try:

        transcript_list = client.list(video_id)

        result = get_transcript_internal(
            transcript_list, language, manually=True, timecodes=timecodes
        )
        if result:
            return result

        result = get_transcript_internal(
            transcript_list, language, manually=False, timecodes=timecodes
        )

        if result:
            return result
        else:
            logger.info(
                f"No transcripts (manual or generated) found for language '{language}' in video {video_id}"
            )
            return ""

    except VideoUnavailable:
        logger.error(f"Video not found. Video id: {video_id}")
        return ""

    except Exception:
        logger.exception("Unexpected error in get_transcript")
        return ""


@ensure_video_id
def get_languages(video_id: str) -> dict[str, str]:
    """
    Returns a list of all available transcript languages for a specified video.

    Helps determine which language codes can be used in the get_transcript function.

    Args:
        video_id (str): Video identifier or a full link to it.

    Returns:
        dict[str, str]: A dictionary where the key is the language code (e.g., 'en')
                        and the value is the full language name (e.g., 'English').
                        Returns an empty dictionary in case of an error.
    """

    client = YouTubeTranscriptApi()
    result: dict[str, str] = {}

    try:
        transcript_list = client.list(video_id)

        for transcript in transcript_list:
            if transcript.language and isinstance(transcript.language, str):
                lang, *_ = transcript.language.split()
                result[transcript.language_code] = lang

        return result

    except VideoUnavailable:
        logger.error(f"Video not found. Video id: {video_id}")
        return {}

    except Exception:
        logger.exception("Unexpected error in get_languages")
        return {}
