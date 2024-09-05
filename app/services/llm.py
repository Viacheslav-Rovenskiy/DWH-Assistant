import os
import json
import requests


SCHEMA_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "schema", "dbml_schema.dbml"
)
PROMPT_PATH = os.path.join(os.path.dirname(__file__), "prompts", "ygpt.txt")
API_KEY = os.getenv("YANDEX_API_KEY")
FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")

def natural_language_to_sql(prompt, debug_mode=False):
    """
    Sends a user query to YandexGPT via Yandex Cloud API using an API key. 
    Returns a structured response including the model's answer or an error message.

    Parameters
    ----------
    user_query : str
        The user's query in natural language.

    Returns
    -------
    dict
        A dictionary with the processing status, the model's answer, 
        and an error description if applicable.
    """
    if debug_mode:
        result_text = llm_debug_answer()
        print("* Model response:", result_text)
    else:
        system_prompt, prompt = generate_prompt(prompt)
        
        # Creating the URL of the model
        model_uri = f"gpt://{FOLDER_ID}/yandexgpt/latest"
        
        # Headers for query
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {API_KEY}",
            "x-folder-id": f"{FOLDER_ID}",
        }
        # Data for query
        data = {
            "modelUri": model_uri,
            "completionOptions": {
                "stream": False,
                "temperature": 0.3,
                "maxTokens": 2000,
            },
            "messages": [
                {
                    "role": "system",
                    "text": system_prompt,
                },
                {
                    "role": "user",
                    "text": prompt,
                },
            ],
        }

        # Sending a POST request to the API
        response = requests.post(
            "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
            headers=headers,
            data=json.dumps(data),
            timeout=60
        )

        # Processing the response
        if response.status_code != 200:
            return {
                "status": "failure",
                "sql": "",
                "error_description": "Error from YandexGPT API.",
                "raw_response": response.text,
            }

        print("* Model response:", response.text)
        response_data = response.json()
        result_text = (
            response_data.get("result", {})
            .get("alternatives", [{}])[0]
            .get("message", {})
            .get("text", "")
        )

    try:
        print(result_text)
        result_json = json.loads(result_text)
        if result_json.get("sql"):
            return {
                "status": "success",
                "sql": result_json["sql"],
                "error_description": "",
                "raw_response": result_text,
            }
        else:
            return {
                "status": "failure",
                "sql": "",
                "error_description": result_json.get(
                    "error_description", "No SQL query provided."
                ),
                "raw_response": result_text,
            }

    except json.JSONDecodeError:
        return {
            "status": "failure",
            "sql": "",
            "error_description": "Failed to parse model response.",
            "raw_response": result_text,
        }


def generate_prompt(user_query):
    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema_data = file.read()

    with open(PROMPT_PATH, "r", encoding="utf-8") as file:
        system_prompt = file.read()

    system_prompt = system_prompt.replace("{schema_data}", schema_data)
    system_prompt = system_prompt.replace('"\{user_query\}"', "")
    system_prompt = system_prompt.replace("User's request", "")

    print()

    return system_prompt, user_query


def llm_debug_answer():
    sql_text = (
        "SELECT u.full_name, COUNT(o.id) AS order_count, "
        "MAX(o.created_at) AS last_purchase "
        "FROM simulator.karpovexpress_users u "
        "JOIN simulator.karpovexpress_orders o "
        "ON u.id = o.user_id GROUP BY u.full_name "
        "ORDER BY order_count DESC LIMIT 5"
    )

    return f'{{ "sql": "{sql_text}", "error_description": "" }}'