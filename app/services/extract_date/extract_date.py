import re
from datetime import datetime, timedelta
from typing import Optional

from dateparser import parse as dateparser_parse


class DateExtractorService:
    @classmethod
    def extract_date(
        cls, text: str, default_to_next_day: bool = True
    ) -> Optional[datetime]:
        """Extract date supporting multiple languages automatically"""
        try:
            potential_dates = cls._extract_date_substrings(text)
            for candidate in potential_dates:
                parsed = dateparser_parse(
                    candidate,
                    settings={
                        "PREFER_DAY_OF_MONTH": "first",
                        "PREFER_DATES_FROM": "future",
                        "RELATIVE_BASE": datetime.now(),
                    },
                )
                if parsed:
                    return parsed.replace(hour=0, minute=0, second=0, microsecond=0)
        except Exception as e:
            print("Error parsing date:", e)

        if default_to_next_day:
            tomorrow = datetime.now() + timedelta(days=1)
            return tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)

        return None

    @classmethod
    def _extract_date_substrings(cls, text: str) -> list:
        """Extract potential date substrings from text"""
        candidates = []

        patterns = [
            # DD/MM/YYYY, DD-MM-YYYY, DD.MM.YYYY
            r"\d{1,2}[-/\.]\d{1,2}[-/\.]\d{4}",
            # DD de MES de YYYY (Spanish)
            r"\d{1,2}\s+de\s+[a-z]+\s+de\s+\d{4}",
            # DD MES YYYY (Spanish without 'de')
            r"\d{1,2}\s+[a-z]+\s+\d{4}",
            # MES DD, YYYY (English)
            r"[a-z]+\s+\d{1,2},?\s+\d{4}",
            # Relative dates (tomorrow, next month, etc.)
            r"\b(tomorrow|today|next\s+\w+|in\s+\d+\s+days?)\b",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            candidates.extend(matches)

        sentences = re.split(r"[.!?]", text)
        for sentence in sentences:
            if re.search(r"\d{4}", sentence):
                candidates.append(sentence.strip())

        return list(dict.fromkeys(candidates))


extract_date = DateExtractorService()
