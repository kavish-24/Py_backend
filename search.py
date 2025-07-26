from normalize import normalize_text

def search_jobs_by_query(query, jobs_list):
    """
    Directly search for a normalized query in the title or pre-normalized tags of jobs.
    Returns a list of matching jobs.
    """
    normalized_query = normalize_text(query)  # Normalize the query
    results = []

    for job in jobs_list:
        # Normalize job title for search
        normalized_title = normalize_text(job["title"])
        # Tags are pre-normalized in main.py
        normalized_tags = job["tags"]

        # Direct substring match in title or tags
        if (normalized_query in normalized_title or 
            any(normalized_query in tag for tag in normalized_tags)):
            results.append(job)

    return results