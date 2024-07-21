import base64
import json
from openai import OpenAI

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your local image file
image_path = "sample3.png"  # Change this to the correct image file as needed

# Getting the base64 string
base64_image = encode_image(image_path)

# Set your API key
api_key = os.getenv("OPENAI_API_KEY")  # Replace with your actual API key

# Create the OpenAI client with the API key
client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "이미지에서 표를 추출하여 값을 JSON 형식으로 반환해주세요. JSON에는 헤더와 행이 구조화된 데이터로 포함되어야 합니다."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    },
                },
            ],
        }
    ],
    max_tokens=1000,
)

# Print the raw content from the response for debugging
raw_content = response.choices[0].message.content.strip()
print("Raw content from API:", raw_content)

# Extract JSON content from the response
json_start = raw_content.find('{')
json_end = raw_content.rfind('}') + 1
json_content = raw_content[json_start:json_end]

# Save the JSON content to a file
json_file_path = "output_table.json"
with open(json_file_path, "w", encoding="utf-8") as json_file:
    json_file.write(json_content)

print(f"JSON content saved to {json_file_path}")
