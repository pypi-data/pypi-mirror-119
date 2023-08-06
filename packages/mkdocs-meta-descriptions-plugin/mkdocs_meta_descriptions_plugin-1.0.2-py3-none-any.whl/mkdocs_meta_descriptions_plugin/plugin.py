import re
from html import escape

from bs4 import BeautifulSoup
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin

from .export import Export


class MetaDescription(BasePlugin):

    config_scheme = (
        ("export_csv", config_options.Type(bool, default=False)),
    )

    def __init__(self):
        self._headings_pattern = re.compile("<h[2-6]", flags=re.IGNORECASE)
        self._pages = []

    def _get_first_paragraph_text(self, html):
        # Strip page subsections to improve performance
        html = re.split(self._headings_pattern, html, maxsplit=1)[0]
        # Select first paragraph directly under body
        first_paragraph = BeautifulSoup(html, "html.parser").select_one("p:not(div.admonition > p)")
        if first_paragraph is not None:
            # Found the first paragraph, return stripped and escaped text
            return escape(first_paragraph.get_text().strip())
        else:
            # Didn't find the first paragraph
            return ""

    def on_page_content(self, html, page, config, files):
        if page.meta.get("description", None):
            # Skip pages that already have an explicit meta description
            pass
        else:
            # Create meta description based on the first paragraph of the page
            first_paragraph_text = self._get_first_paragraph_text(html)
            if len(first_paragraph_text) > 0:
                page.meta["description"] = first_paragraph_text
        return html

    def on_post_page(self, output, page, config):
        if self.config.get("export_csv", False):
            # Collect pages to export meta descriptions to CSV file
            self._pages.append(page)
        return output

    def on_post_build(self, config):
        if self.config.get("export_csv", False):
            # Export meta descriptions to CSV file
            Export(self._pages, config).write_csv()
