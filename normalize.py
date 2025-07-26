import re

def normalize_text(text):
    """
    Normalize text by converting to lowercase and removing special characters.
    Returns the normalized string.
    """
    if not text:
        return ""
    # Convert to lowercase and remove special characters, keeping letters, numbers, and spaces
    normalized = re.sub(r'[^a-z0-9\s]', '', text.lower().strip())
    return normalized

def normalize_tags(tags):
    """
    Normalize a list of tags by applying normalize_text to each tag.
    Returns a list of normalized tags.
    """
    if not tags:
        return []
    return [normalize_text(tag) for tag in tags]