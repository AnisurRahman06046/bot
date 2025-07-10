import httpx


async def fetch_products(merchant_id: str, access_token: str) -> list[dict]:
    url = f"https://commerzly.onrender.com/api/v1/merchants/{merchant_id}/products"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data.get("products", [])  # ✅ Extract the list
            print(
                "❌ Bitcommerz product fetch failed:",
                response.status_code,
                response.text,
            )
            return []
        except Exception as e:
            print("⚠️ Error fetching Bitcommerz products:", e)
            return []
