# oshi
An asynchronous osu API wrapper made in python 

## Example(s)

   ```py
   import oshi
   import asyncio


   async def main() -> None:
      auth = oshi.Authentication(CLIENT_ID, "CLIENT_SECRET")

      async with oshi.Client(auth) as client:
         map = await client.get_beatmap(id=1222063)
         print(map.url)

   asyncio.run(main())
   ```


## Development
_For developers_
If you plan on contributing please open an issue beforehand

## Contributors

- [an-dyy](https://github.com/an-dyy) - creator and maintainer

