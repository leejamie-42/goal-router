import asyncio
from app.models.schemas import GeneratePlanRequest
from app.router import generate_plan_endpoint

async def test():
    request = GeneratePlanRequest(
        goal="Learn to play jazz piano improvisation",
        context="I can read sheet music but have no improv experience"
    )
    
    try:
        response = await generate_plan_endpoint(request)
        print(f"Success! Generated {len(response.weekly_breakdown)}-week plan")
        print(f"Category: {response.category}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test())