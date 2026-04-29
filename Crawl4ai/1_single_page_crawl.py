
import asyncio
from crawl4ai import AsyncWebCrawler


async def main():
  
    async with AsyncWebCrawler() as crawler:
        print("Crawling: https://ai.pydantic.dev/")
        print("-" * 60)

        result = await crawler.arun(
            url="https://ai.pydantic.dev/",
        )

        if result.success:
            print(f"✅ Succès !")
            print(f"Longueur du Markdown : {len(result.markdown)} caractères\n")
            print("── Aperçu (500 premiers caractères) ──────────────────")
            print(result.markdown[:500])
            print("...")
        else:
            print(f" Échec : {result.error_message}")


if __name__ == "__main__":
    asyncio.run(main())


