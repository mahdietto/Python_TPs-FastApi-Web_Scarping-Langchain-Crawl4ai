"""
TP Crawl4AI — Étape 3 : Crawl Parallèle Ultra-Rapide
Crawle les URLs par lots (batches) en parallèle avec asyncio.gather(),
tout en monitorant la consommation mémoire avec psutil.
"""

import os
import sys
import asyncio
import requests
import psutil
from typing import List
from xml.etree import ElementTree

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode


__location__ = os.path.dirname(os.path.abspath(__file__))
__output__ = os.path.join(__location__, "output")
os.makedirs(__output__, exist_ok=True)




def get_pydantic_ai_docs_urls() -> List[str]:
    """
    Récupère toutes les URLs depuis le sitemap XML de Pydantic AI.

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




async def crawl_parallel(urls: List[str], max_concurrent: int = 3):
   
    print(f"\n=== Crawl Parallèle (max {max_concurrent} simultanés) ===\n")

  
    peak_memory = 0
    process = psutil.Process(os.getpid())

    def log_memory(prefix: str = ""):
        nonlocal peak_memory
        current_mem = process.memory_info().rss  # en bytes
        if current_mem > peak_memory:
            peak_memory = current_mem
        current_mb = current_mem // (1024 * 1024)
        peak_mb = peak_memory // (1024 * 1024)
        print(f"   {prefix}RAM actuelle : {current_mb} MB | Pic : {peak_mb} MB")


    browser_config = BrowserConfig(
        headless=True,
        verbose=False,
        extra_args=[
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--no-sandbox",
        ],
    )

    
    crawl_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)


    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()

    success_count = 0
    fail_count = 0
    total_batches = (len(urls) + max_concurrent - 1) // max_concurrent

    try:
        
        for i in range(0, len(urls), max_concurrent):
            batch = urls[i : i + max_concurrent]
            batch_num = i // max_concurrent + 1
            tasks = []

            print(f"\n── Lot {batch_num}/{total_batches} ({len(batch)} URLs) ──")

           
            for j, url in enumerate(batch):
                session_id = f"parallel_session_{i + j}"
                task = crawler.arun(
                    url=url,
                    config=crawl_config,
                    session_id=session_id,
                )
                tasks.append(task)

       
            log_memory(prefix="Avant  : ")


            results = await asyncio.gather(*tasks, return_exceptions=True)

       
            log_memory(prefix="Après  : ")

            
            for url, result in zip(batch, results):
                if isinstance(result, Exception):
                    print(f"   {url} → {result}")
                    fail_count += 1
                elif result.success:
                    print(f"   {url}")
                    success_count += 1
                else:
                    print(f"   {url} → {result.error_message}")
                    fail_count += 1

    finally:
        print("\nFermeture du crawler...")
        await crawler.close()

        log_memory(prefix="Final  : ")
        print(f"\n── Résumé ──────────────────────────────────────────")
        print(f"   Succès           : {success_count}")
        print(f"   Échecs           : {fail_count}")
        print(f"   Total            : {len(urls)}")
        print(f"   Pic mémoire      : {peak_memory // (1024 * 1024)} MB")




async def main():
    urls = get_pydantic_ai_docs_urls()

    if urls:
        print(f" {len(urls)} URLs trouvées dans le sitemap")
        
        await crawl_parallel(urls, max_concurrent=10)
    else:
        print("Aucune URL trouvée dans le sitemap.")


if __name__ == "__main__":
    asyncio.run(main())
