import aiohttp
import asyncio

url="https://jntuhresults.herokuapp.com/api/results/18E51A04"
url2="/4-2"

def get_tasks(session):
    tasks=[]
    for i in range(11,100):
        tasks.append(session.get(url+str(i)+url2,ssl=False))
    return tasks
async def getting_the_grades():
        async with aiohttp.ClientSession() as session:
            tasks=get_tasks(session)
            responses =await asyncio.gather(*tasks)
            session.close()
        return await responses

print(asyncio.run(getting_the_grades()))