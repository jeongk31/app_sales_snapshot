import json
from openai import OpenAI

def edit_json_with_gpt(json_file_path, edited_json_file_path, api_key):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    headers = data.get("headers", [])
    rows = data.get("rows", [])

    # Create the OpenAI client with the API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key is not set in environment variables")
    
    client = OpenAI(api_key=api_key)

    # Use GPT-4 to process and suggest column merges and removals
    prompt = f"""
    다음 JSON 데이터에서 표를 추출하여 '명칭', '단가', '수량', '합계'와 같은 의미를 가지는 열만 남기고 나머지 열은 제거하여 JSON 형식으로 반환해주세요. 
    JSON 형식의 데이터만 반환하고 다른 텍스트는 포함하지 마세요.
    JSON 데이터:
    {{
        "headers": {headers},
        "rows": {rows}
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=1500,
    )

    # Print the raw content from the response for debugging
    raw_content = response.choices[0].message.content.strip()
    print("Raw content from API:", raw_content)

    # Clean up the response content
    json_start = raw_content.find('{')
    json_end = raw_content.rfind('}') + 1
    json_content = raw_content[json_start:json_end]

    # Remove any extraneous text around the JSON content
    json_content = json_content.replace("```json", "").replace("```", "").strip()

    try:
        edited_data = json.loads(json_content)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        print("Content received:", json_content)
        return

    # Save the edited JSON content to a new file
    with open(edited_json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(edited_data, json_file, ensure_ascii=False, indent=4)

    print(f"Edited JSON content saved to {edited_json_file_path}")

# Example usage
json_file_path = "sample3.json"
edited_json_file_path = "edited_output_table.json"
edit_json_with_gpt(json_file_path, edited_json_file_path, api_key)
