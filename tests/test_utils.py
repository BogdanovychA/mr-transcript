import logging
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from mr_transcript.utils import get_video_id

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class GetVideoIdTests(unittest.TestCase):
    def test_accepts_supported_youtube_url_formats(self) -> None:
        cases = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "http://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtube.com/watch?v=dQw4w9WgXcQ",
            "https://www.youtube.com/watch?feature=shared&v=dQw4w9WgXcQ",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL1234567890",
            "https://m.youtube.com/watch?v=dQw4w9WgXcQ&t=1s",
            "https://youtu.be/dQw4w9WgXcQ",
            "http://youtu.be/dQw4w9WgXcQ",
            "https://www.youtube.com/embed/dQw4w9WgXcQ?start=1",
            "https://www.youtube.com/shorts/dQw4w9WgXcQ",
        ]

        for url in cases:
            with self.subTest(url=url):
                actual = get_video_id(url)
                logger.info("Valid YouTube URL accepted: %s -> %s", url, actual)
                self.assertEqual(actual, "dQw4w9WgXcQ")

    def test_rejects_non_youtube_domains(self) -> None:
        self.assertEqual(
            get_video_id("https://example.com/notyoutube/dQw4w9WgXcQ"),
            "",
        )

    def test_rejects_ids_that_are_not_exactly_eleven_characters(self) -> None:
        cases = [
            "https://www.youtube.com/watch?v=abcdefghij",
            "https://www.youtube.com/watch?v=abcdefghijkl",
            "https://youtu.be/abcdefghij",
            "https://youtu.be/abcdefghijkl",
        ]

        for url in cases:
            with self.subTest(url=url):
                self.assertEqual(get_video_id(url), "")


if __name__ == "__main__":
    unittest.main()
