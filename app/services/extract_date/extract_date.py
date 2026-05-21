import re
from datetime import UTC, datetime, timedelta

from dateparser import parse as dateparser_parse


class DateExtractorService:
    def extract_date(
        self, text: str, default_to_next_day: bool = True
    ) -> str | None:
        # Extract date and return RFC 3339 string
        try:
            potential_dates = self._extract_date_substrings(text)
            now = datetime.now()

            for candidate in potential_dates:
                normalize = self._inject_year(candidate, now)

                parsed = dateparser_parse(
                    normalize,
                    settings={
                        "PREFER_DAY_OF_MONTH": "first",
                        "PREFER_DATES_FROM": "future",
                        "RELATIVE_BASE": datetime.now(),
                    },
                )
                if parsed:
                    return (
                        parsed.astimezone(UTC)
                        .replace(microsecond=0)
                        .isoformat()
                        .replace("+00:00", "Z")
                    )

        except Exception as e:
            print("Error parsing date:", e)

        if default_to_next_day:
            tomorrow = datetime.now(UTC) + timedelta(days=1)
            return (
                tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
                .isoformat()
                .replace("+00:00", "Z")
            )

        return None

    def _extract_date_substrings(self, text: str) -> list:
        """Extract potential date substrings from text"""
        candidates = []

        patterns = [
            # DD/MM, DD-MM, DD.MM.
            r"\d{1,2}[-/\.]\d{1,2}",
            # DD de MES (Spanish)
            r"\d{1,2}\s+de\s+[a-z]+",
            # DD MES (English)
            r"[a-z]+\s+\d{1,2}",
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

    def _has_year(self, text: str) -> bool:
        return bool(re.search(r"\b\d{4}\b", text))

    def _inject_year(self, text: str, base_date: datetime) -> str:
        if self._has_year(text):
            return text

        current_year = base_date.year

        if re.match(r"\d{1,2}[-/\.]\d{1,2}$", text):
            return f"{text}/{current_year}"

        if re.match(r"\d{1,2}\s+de\s+[a-z]+$", text, re.IGNORECASE):
            return f"{text} de {current_year}"

        if re.match(r"[a-z]+\s+\d{1,2}$", text, re.IGNORECASE):
            return f"{text}, {current_year}"

        return text


date_extractor = DateExtractorService()
