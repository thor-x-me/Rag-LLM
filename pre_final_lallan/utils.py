import json
import os
from github import Github, Auth
from langchain_core.documents import Document


def write_to_json(data, filename):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            existing_data = json.load(file)
        # Check if the email already exists in the file
        if "user" in data:
            existing_emails = [
                entry["user"] for entry in existing_data if "user" in entry
            ]
            if data["user"] in existing_emails:
                return
        existing_data.append(data)
        with open(filename, "w") as file:
            json.dump(existing_data, file, indent=4)
    else:
        with open(filename, "w") as file:
            json.dump([data], file, indent=4)


def fc(user_id):
    email_filename = "queries" + f"\{user_id}.json"
    return email_filename


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def unstructure_docs(auth_token: str):
    auth = Auth.Token(auth_token)
    g = Github(auth=auth)
    repo = g.get_repo("LucknowAI/Lucknow-LLM")
    contents = repo.get_contents("lucknowllm/data/Unstructured_data")
    text = []
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            text.append(Document(page_content=file_content.decoded_content))
    return text


def create_document_list_from_local(path):
    document_list = []
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                with open(os.path.join(root, file), "r") as f:
                    document_list.append(Document(page_content=f.read()))
    elif os.path.isfile(path):
        with open(path, "r") as f:
            document_list.append(Document(page_content=f.read()))
    else:
        print("The path provided is not a valid file or directory")
    return document_list