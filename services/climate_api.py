from openai import OpenAI
import os
import re

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_climate_data(address):
    try:
        prompt = (
            f"What's the 99% dry-bulb temperature and mean coincident relative humidity in {address}? "
            "Return exactly the format: temperature: 25, humidity: 50"
        )
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message.content
        match = re.search(r"temperature:\s*(\d+(\.\d+)?),\s*humidity:\s*(\d+(\.\d+)?)", content)
        if not match:
            print(f"⚠️ Could not parse OpenAI response: {content}, using fallback values")
            return 37, 0.19  # Fallback values

        temperature = float(match.group(1))
        humidity = float(match.group(3)) / 100  # Convert to decimal
        return temperature, humidity
    except Exception as e:
        print(f"⚠️ Error getting climate data: {str(e)}, using fallback values")
        return 37, 0.19  # Fallback values
