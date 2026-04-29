

import asyncio
import requests
from typing import List
from xml.etree import ElementTree

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator



def get_pydantic_ai_docs_urls() -> List[str]:
    """
    Récupère toutes les URLs depuis le sitemap XML de Pydantic AI.
    URL du sitemap : https://ai.pydantic.dev/sitemap.xml

    Returns:
        List[str]: Liste des URLs trouvées
    """
    sitemap_url = "https://ai.pydantic.dev/sitemap.xml"
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()

        root = ElementTree.fromstring(response.content)

   
        namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [loc.text for loc in root.findall(".//ns:loc", namespace)]

        return urls
    except Exception as e:
        print(f"Erreur lors de la récupération du sitemap : {e}")
        return []




async def crawl_sequential(urls: List[str]):
    """
    Crawle toutes les URLs de façon séquentielle.
    Réutilise la même session navigateur pour plus d'efficacité.
    """
    print("\n=== Crawl Séquentiel avec Réutilisation de Session ===\n")


    browser_config = BrowserConfig(
        headless=True,
        extra_args=[
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--no-sandbox",
        ],
    )

  
    crawl_config = CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator()
    )

  
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()

    success_count = 0
    fail_count = 0

    try:
       
        session_id = "session1"

        for i, url in enumerate(urls, 1):
            result = await crawler.arun(
                url=url,
                config=crawl_config,
                session_id=session_id,
            )

            if result.success:
                success_count += 1
                md_length = len(result.markdown.raw_markdown)
                print(f"[{i:3}/{len(urls)}]  {url}")
                print(f"          Markdown : {md_length} caractères")
            else:
                fail_count += 1
                print(f"[{i:3}/{len(urls)}]  {url}")
                print(f"          Erreur : {result.error_message}")

    finally:
       
        await crawler.close()
        print(f"\n── Résumé ──────────────────────────────────────────")
        print(f"   Succès  : {success_count}")
        print(f"   Échecs  : {fail_count}")
        print(f"   Total   : {len(urls)}")



async def main():
    urls = get_pydantic_ai_docs_urls()

    if urls:
        print(f" {len(urls)} URLs trouvées dans le sitemap")
        await crawl_sequential(urls)
    else:
        print("Aucune URL trouvée dans le sitemap.")


if __name__ == "__main__":
    asyncio.run(main())
