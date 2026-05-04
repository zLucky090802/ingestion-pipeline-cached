"""
LlamaIndex Documentation Crawler using Crawl4AI

This script crawls the LlamaIndex documentation site and saves each page
as a clean markdown file, optimized for RAG/LLM ingestion.

Why Crawl4AI instead of BeautifulSoup?
1. LlamaIndex docs is a JavaScript SPA (Astro/Starlight) - BS4 can't render JS
2. The site uses clean URLs (/python/framework/) not .html files
3. Crawl4AI provides built-in markdown generation for LLM workflows
4. Deep crawling handles the 400+ page navigation tree automatically

Usage:
    uv run python download_docs.py
"""

import asyncio
from pathlib import Path
from urllib.parse import urlparse

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CrawlerRunConfig,
    BFSDeepCrawlStrategy,
    DefaultMarkdownGenerator,
    FilterChain,
    URLPatternFilter,
    PruningContentFilter,
)

# Configuration
BASE_URL = "https://developers.llamaindex.ai/python/framework/"
OUTPUT_DIR = Path("./llamaindex-docs")
MAX_DEPTH = 5  # Full site coverage


async def crawl_llamaindex_docs():
    """Crawl LlamaIndex documentation and save as markdown files."""

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Browser configuration - headless Chromium
    browser_config = BrowserConfig(
        headless=True,
        verbose=True
    )

    # URL filtering - only crawl Python docs, skip query strings and anchors
    # FilterChain combines multiple filters - URL must pass ALL filters
    url_filter = FilterChain(filters=[
        # Include only Python documentation pages (glob pattern)
        URLPatternFilter(
            patterns=["*developers.llamaindex.ai/python/*"],
            use_glob=True,
            reverse=False  # Include matching URLs
        ),
    ])

    # Deep crawl strategy - BFS (Breadth-First Search) to get all pages
    # This is a real CS concept: BFS explores all neighbors at current depth
    # before moving to nodes at the next depth level
    deep_crawl = BFSDeepCrawlStrategy(
        max_depth=MAX_DEPTH,
        filter_chain=url_filter,
        include_external=False,  # Stay within the domain
    )

    # Content filter to remove navigation/sidebar noise
    # PruningContentFilter uses text density analysis to keep only main content
    # This is critical for RAG - we don't want nav menus polluting our embeddings
    content_filter = PruningContentFilter(
        threshold=0.48,  # Default threshold for content relevance
        threshold_type="fixed",
    )

    # Crawler configuration with markdown generation + content filtering
    crawl_config = CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator(
            content_filter=content_filter  # Filter out nav/sidebar noise
        ),
        deep_crawl_strategy=deep_crawl,
        verbose=True
    )

    print("=" * 60)
    print("LlamaIndex Documentation Crawler")
    print("=" * 60)
    print(f"Target: {BASE_URL}")
    print(f"Output: {OUTPUT_DIR.absolute()}")
    print(f"Strategy: BFS Deep Crawl (max_depth={MAX_DEPTH})")
    print("-" * 60)
    print("Starting crawl... This will take 5-10 minutes.\n")

    async with AsyncWebCrawler(config=browser_config) as crawler:
        results = await crawler.arun(
            BASE_URL,
            config=crawl_config
        )

        # Handle both single result and list of results
        if not isinstance(results, list):
            results = [results]

        saved_count = 0
        failed_count = 0

        for i, result in enumerate(results):
            if result.success and result.markdown:
                # Use fit_markdown (filtered content) for RAG-optimized output
                # This removes navigation, sidebars, footers - keeping only main content
                md_result = result.markdown
                content = md_result.fit_markdown if md_result.fit_markdown else md_result.raw_markdown

                if content:
                    # Create filename from URL path
                    # e.g., /python/framework/rag/ -> python_framework_rag.md
                    parsed = urlparse(result.url)
                    path_parts = [p for p in parsed.path.strip("/").split("/") if p]
                    filename = "_".join(path_parts) if path_parts else "index"
                    filename = f"{filename}.md"

                    # Save markdown file
                    filepath = OUTPUT_DIR / filename
                    filepath.write_text(content, encoding="utf-8")
                    print(f"[{i+1:3d}] Saved: {filename} ({len(content):,} chars)")
                    saved_count += 1
                else:
                    print(f"[{i+1:3d}] Empty: {result.url}")
                    failed_count += 1
            else:
                error_msg = getattr(result, 'error_message', 'Unknown error')
                print(f"[{i+1:3d}] Failed: {result.url} - {error_msg}")
                failed_count += 1

    # Summary
    print("\n" + "=" * 60)
    print("Crawl Complete!")
    print("=" * 60)
    print(f"Pages saved: {saved_count}")
    print(f"Pages failed: {failed_count}")
    print(f"Output directory: {OUTPUT_DIR.absolute()}")
    print(f"Total files: {len(list(OUTPUT_DIR.glob('*.md')))}")


if __name__ == "__main__":
    asyncio.run(crawl_llamaindex_docs())
