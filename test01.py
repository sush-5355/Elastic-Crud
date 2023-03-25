import asyncio
from utilities.CRUD import create

data = {
    'name':'sushant',
    'age': 28
}
async def test():
    res = await create(index_name='dummy', mapping=data)
    print(res)

asyncio.run(test())