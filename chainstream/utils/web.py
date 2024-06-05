from typing import List
import requests
from urllib.parse import urlparse


def related_links(query: str, tool) -> List[str]:
    def string_to_object_array(string):
        """Converts a string with snippets in square brackets to a list of dictionaries.

        Args:
        string: The string to convert.

        Returns:
        A list of dictionaries, where each dictionary represents a snippet with its content, title, and link (if available).
        """
        # Remove leading and trailing characters (square brackets)
        string = string[1:-1]

        # Split the string by double square brackets (representing individual snippets)
        snippets = string.split("], [")

        # Convert each snippet string to a dictionary using try-except for potential missing keys
        object_array = []
        for snippet in snippets:
            try:
                # Extract data (content is everything before ", title:")
                data = snippet.split(", title:")
                content = data[0].strip()[8:]  # Remove quotes and leading "snippet:"
                # Extract title and link (assuming the format is consistent)
                title_link = data[1].strip()
                title, link = title_link.split(", link:")
            except IndexError:  # Handle cases where title or link is missing
                content = snippet.strip()[8:]  # Extract only content
                title = "NA"
                link = "NA"

            # Create a dictionary and add it to the array
            obj = {
                "content": content,
                "title": title.strip(),  # Only remove leading/trailing spaces
                "link": link.strip(),  # Only remove leading/trailing spaces
            }
            object_array.append(obj)

        return object_array

    try:
        array = string_to_object_array(
            tool.run(query, num_results=5 if tool.name == "bing_search" else None)
        )
        for i, obj in enumerate(array):
            array[i] = obj["link"]
    except BaseException as e:
        print(e)
        return []
    return array


def is_pdf_link(url):
    """Checks if the URL points to a PDF file using Content-Type header."""
    try:
        response = requests.head(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        content_type = response.headers.get("Content-Type", None)
        return content_type and content_type.lower() == "application/pdf"
    except requests.exceptions.RequestException:
        # Handle potential errors during request
        return False


def is_youtube_link(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc in ("www.youtube.com", "youtube.com") and (
        parsed_url.path == "/watch" or parsed_url.path.startswith("/playlist")
    )


def is_arxiv_link(url):
    import urllib.parse

    parsed_url = urllib.parse.urlparse(url)
    return parsed_url.netloc == "arxiv.org"
