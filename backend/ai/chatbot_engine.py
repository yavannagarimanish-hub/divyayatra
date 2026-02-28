"""Core AI logic for DivyaYatra chatbot.

This module intentionally keeps the logic lightweight and deterministic so it can
run without external AI providers in local/dev environments.
"""

from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass
class DevotionalIntent:
    """Structured devotional intent extracted from a user message."""

    deity: str | None = None
    location: str | None = None
    travel_preference: str | None = None


# Canonical deity aliases used for lightweight intent extraction.
DEITY_ALIASES: dict[str, tuple[str, ...]] = {
    "Shiva": ("shiva", "mahadev", "shankar", "bholenath"),
    "Vishnu": ("vishnu", "narayana", "hari"),
    "Krishna": ("krishna", "govinda", "kanha"),
    "Rama": ("rama", "ram"),
    "Hanuman": ("hanuman", "anjaneya", "bajrang"),
    "Durga": ("durga", "maa durga", "amman"),
    "Lakshmi": ("lakshmi", "mahalakshmi"),
    "Ganesha": ("ganesha", "ganpati", "vinayaka"),
    "Murugan": ("murugan", "kartikeya", "subramanya"),
    "Ayyappa": ("ayyappa", "sabarimala"),
}

TRAVEL_PREFERENCE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "family": ("family", "kids", "parents"),
    "senior-friendly": ("senior", "elderly", "easy", "comfortable"),
    "budget": ("budget", "cheap", "affordable", "low cost"),
    "festive": ("festival", "utsav", "celebration"),
    "quiet": ("quiet", "peaceful", "calm", "meditation"),
}


def _extract_location(message: str) -> str | None:
    """Extract probable location phrases from a user message."""

    # Prefer patterns like "in Varanasi" / "near Madurai".
    location_match = re.search(r"\b(?:in|near|around|from|at)\s+([a-zA-Z\s]+)", message, re.IGNORECASE)
    if location_match:
        return location_match.group(1).strip().title()

    # Fallback to capitalized words (for users not using prepositions).
    capitals = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", message)
    if capitals:
        return capitals[-1].strip()

    return None


def detect_devotional_intent(message: str) -> DevotionalIntent:
    """Detect deity, location and travel preference from user message."""

    normalized = message.lower()

    detected_deity = None
    for canonical, aliases in DEITY_ALIASES.items():
        if any(alias in normalized for alias in aliases):
            detected_deity = canonical
            break

    detected_preference = None
    for preference, keywords in TRAVEL_PREFERENCE_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            detected_preference = preference
            break

    detected_location = _extract_location(message)

    return DevotionalIntent(
        deity=detected_deity,
        location=detected_location,
        travel_preference=detected_preference,
    )


def build_follow_up_question(intent: DevotionalIntent) -> str:
    """Return the best next conversational question for gathering context."""

    if not intent.deity:
        return "Which deity would you like to center your yatra around?"
    if not intent.location:
        return "Do you have a preferred city or state for this pilgrimage?"
    if not intent.travel_preference:
        return "Do you prefer a family-friendly, budget, or peaceful pilgrimage experience?"
    return "Would you like me to suggest an itinerary and nearby temples as your next step?"
