import aiohttp
import asyncio
import os
import aiofiles


async def download_image(session, url, folder, filename):
    async with session.get(url) as response:
        if response.status == 200:
            async with aiofiles.open(os.path.join(folder, filename),
                                     'wb') as f:
                await f.write(await response.read())

            print(f"Downloaded: {filename}")


async def main(num_images, folder):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(num_images):
            url = f"https://picsum.photos/200/300?random={i}"
            filename = f"image_{i}.jpg"
            tasks.append(download_image(session, url, folder, filename))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    num_images = 5  # Количество изображений для загрузки
    download_folder = "artifacts/images"
    os.makedirs(download_folder, exist_ok=True)
    asyncio.run(main(num_images, download_folder))
