# import asyncio
# from app.models.schemas import GeneratePlanRequest
# from app.router import generate_plan_endpoint

# async def test():
#     request = GeneratePlanRequest(
#         goal="Learn to play jazz piano improvisation",
#         context="I can read sheet music but have no improv experience"
#     )

#     try:
#         response = await generate_plan_endpoint(request)
#         print(f"Success! Generated {len(response.weekly_breakdown)}-week plan")
#         print(f"Category: {response.category}")
#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     asyncio.run(test())


import asyncio
import logging
from app.models.schemas import GeneratePlanRequest
from app.router import generate_plan_endpoint

# Only show INFO level and above (hide DEBUG)
logging.basicConfig(
    level=logging.WARNING,  # ← Changed from DEBUG to WARNING
    format="%(levelname)s - %(message)s",
)


async def test():
    request = GeneratePlanRequest(
        goal="Learn to play jazz piano improvisation",
        context="I can read sheet music but have no improv experience",
    )

    try:
        print("\nTesting AI Personal Productivity Router...\n")
        response = await generate_plan_endpoint(request)

        print(f"✅ Success! Generated {len(response.weekly_breakdown)}-week plan")
        print(f"📁 Category: {response.category}")
        print(f"⏱️  Total hours: {response.total_estimated_hours}")
        print(f"\n📅 Weekly Breakdown:")
        for week in response.weekly_breakdown:
            print(f"\n  Week {week.week_number}: {week.focus_area}")
            for task in week.tasks:
                milestone = "🎯" if task.milestone else "  "
                print(f"    {milestone} {task.task} ({task.estimated_hours}h)")

        print(f"\n📚 Resources:")
        for resource in response.resources:
            print(f"  - {resource.title} ({resource.resource_type})")
            print(f"    {resource.url}")

        print(f"\n🔧 Metadata:")
        print(f"  Model: {response.metadata.get('model')}")
        print(f"  Tokens: {response.metadata.get('tokens_used', {}).get('total')}")
        print(f"  Mock mode: {response.metadata.get('mock_mode', False)}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test())


# import asyncio
# import logging
# from app.models.schemas import GeneratePlanRequest
# from app.router import generate_plan_endpoint

# # Enable debug logging
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )

# async def test():
#     request = GeneratePlanRequest(
#         goal="Learn to play jazz piano improvisation",
#         context="I can read sheet music but have no improv experience"
#     )

#     try:
#         response = await generate_plan_endpoint(request)
#         print(f"\n✅ Success! Generated {len(response.weekly_breakdown)}-week plan")
#         print(f"Category: {response.category}")
#         print(f"Total hours: {response.total_estimated_hours}")
#         print(f"\nFirst week focus: {response.weekly_breakdown[0].focus_area}")
#     except Exception as e:
#         print(f"\n❌ Error: {e}")
#         # Print full stack trace
#         import traceback
#         traceback.print_exc()

# if __name__ == "__main__":
#     asyncio.run(test())
