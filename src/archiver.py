import os

def archive_report(chat_name: str):
    files = [
        f"./reports/{chat_name}.report.json",
        f"./reports/photos/{chat_name}"
    ]

    file_string = " ".join(files)
    
    os.makedirs("./reports/archives", exist_ok=True)
    cmd = f"zip -r ./reports/archives/{chat_name}.zip -Z deflate -9 {file_string}"

    os.system(cmd)

if __name__ == "__main__":
    archive_report(
        "Thoughts"
    )