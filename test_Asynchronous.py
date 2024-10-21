# import aiohttp
# import asyncio
# import time

# # Binance API URL to fetch prices
# url = 'https://api.binance.com/api/v3/ticker/price'

# # Function to send a request
# async def fetch(session, url):
#     async with session.get(url) as response:
#         return await response.json()

# # Main function to send 500 requests concurrently
# async def send_requests():
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for _ in range(500):  # Create 500 requests
#             tasks.append(fetch(session, url))
        
#         responses = await asyncio.gather(*tasks)  # Send requests concurrently
#         return responses

# # Measure time
# start_time = time.time()

# # Execute the requests
# responses = asyncio.run(send_requests())

# end_time = time.time()

# # Calculate elapsed time
# elapsed_time = end_time - start_time

# print(f"Total time for 500 requests: {elapsed_time} seconds")


import aiohttp
import asyncio
import time

# Binance API URL
url = 'https://api.binance.com/api/v3/ticker/price'

# Function to send a request
async def fetch(session, url, attempt):
    async with session.get(url) as response:
        elapsed_time = response.headers.get('X-Response-Time', 'Unknown')  # Get elapsed time from header
        print(f"Request number {attempt} with status code: {response.status} and time: {elapsed_time} seconds")  # Print status code and time
        return await response.json()

# Main function to send 500 requests concurrently
async def send_requests():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(500):  # Create 500 requests
            tasks.append(fetch(session, url, i + 1))
        
        responses = await asyncio.gather(*tasks)  # Send requests concurrently
        return responses

# Measure time
start_time = time.time()

# Execute requests
responses = asyncio.run(send_requests())

end_time = time.time()

# Calculate elapsed time
elapsed_time = end_time - start_time

print(f"Total time for 500 requests: {elapsed_time:.2f} seconds")

