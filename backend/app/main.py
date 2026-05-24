import asyncio

from app.config.companies import COMPANIES
from app.ai_agents.orchestration.referral_runner import run_referral_pipeline
from app.ai_agents.orchestration.runner import run_job_filtering_agent
from app.crawlers.greenhouse import GreenhouseCrawler
from app.crawlers.workday import WorkdayCrawler
from app.crawlers.lever import LeverCrawler
from app.crawlers.ashby import AshbyCrawler
from app.db.connection import AsyncSessionLocal
from app.db.repository import JobRepository
from app.parsers.validators import is_relevant_job, is_good_location, is_fresher_job
from app.utils.logger import logger
from app.parsers.job_normalizer import (
    normalize_greenhouse_job,
    normalize_lever_job,
    normalize_workday_job,
    normalize_ashby_job
)

def get_crawler(company):
    provider = company["provider"]
    if provider == "greenhouse":
        return GreenhouseCrawler()
    if provider == "lever":
        return LeverCrawler()
    if provider == "workday":
        return WorkdayCrawler()
    if provider == "ashby":
        return AshbyCrawler()
    
    raise Exception(f"Unsupported provider: {provider}")

async def process_company(company, user_id: int):
    try:
       

        if company["provider"] == "workday":
            result = await crawler.fetch_jobs(company["base_url"])
        else:
            result = await crawler.fetch_jobs(company["token"])

        if not result.success:
            return

        raw_jobs = result.jobs
        
        async with AsyncSessionLocal() as session:
            repository = JobRepository(session)

            for raw_job in raw_jobs:
                try:
                    if company["provider"] == "greenhouse":
                        normalized = normalize_greenhouse_job(raw_job, company_name=company["name"])
                    elif company["provider"] == "lever":
                        normalized = normalize_lever_job(raw_job, company_name=company["name"])
                    elif company["provider"] == "workday":
                        normalized = normalize_workday_job(raw_job, company_name=company["name"])
                    elif company["provider"] == "ashby":
                        normalized = normalize_ashby_job(raw_job, company_name=company["name"])
                    else:
                        continue

                    if not normalized:
                        continue

                    title = normalized.get("title", "")
                    if not is_relevant_job(title):
                        continue

                    location = normalized.get("location", "")
                    if not is_good_location(location):
                        continue

                    await repository.save_job(normalized, user_id=user_id)
                    

                except Exception as job_err:
                    
                    continue

    except Exception as e:
        logger.error(f"Critical error processing company {company.get('name', 'Unknown')}: {e}")

async def main(user_id: int):
    tasks = [
        process_company(company, user_id)
        for company in COMPANIES
    ]

    await asyncio.gather(*tasks)
    
    try:
        await run_job_filtering_agent()
        await run_referral_pipeline(user_id=user_id)
    except Exception as e:
        logger.error(f"Error in post-processing pipeline: {e}")

if __name__ == "__main__":
    asyncio.run(main())