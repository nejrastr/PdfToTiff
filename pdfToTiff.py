import os
import requests

API_KEY = "strsevicnejra@gmail.com_qm8l450IgVIK0M3Pjlx1Xn0Q0m17x7OI0O1cLPz6T7z0Ngb8wQ850n3Ffr8yHi9j"

BASE_URL = "https://api.pdf.co/v1"

SourceDirectory = "./pdf/"
DestinationDirectory = "./tiff/"
ProcessedDirectory = "./processed/"
Pages = ""
Password = ""

def main():
    for filename in os.listdir(SourceDirectory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(SourceDirectory, filename)
            uploadedFileUrl = uploadFile(pdf_path)
            if uploadedFileUrl:
                convertPdfToImage(uploadedFileUrl, filename)
                # Move processed file to 'processed' directory
                os.makedirs(ProcessedDirectory, exist_ok=True)
                processed_file = os.path.join(ProcessedDirectory, filename)
                os.replace(pdf_path, processed_file)


def convertPdfToImage(uploadedFileUrl, filename):
    parameters = {
        "password": Password,
        "pages": Pages,
        "url": uploadedFileUrl
    }

    url = "{}/pdf/convert/to/tiff".format(BASE_URL)

    response = requests.post(url, data=parameters, headers={"x-api-key": API_KEY})
    if response.status_code == 200:
        json = response.json()

        if not json["error"]:
            resultFileUrl = json["url"]

            r = requests.get(resultFileUrl, stream=True)
            if r.status_code == 200:
                os.makedirs(DestinationDirectory, exist_ok=True)
                destination_file = os.path.join(DestinationDirectory, os.path.splitext(filename)[0] + ".tiff")
                with open(destination_file, 'wb') as file:
                    for chunk in r:
                        file.write(chunk)
                print(f"Result file saved as \"{destination_file}\".")
            else:
                print(f"Request error: {response.status_code} {response.reason}")
        else:
            print(json["message"])
    else:
        print(f"Request error: {response.status_code} {response.reason}")


def uploadFile(fileName):
    url = "{}/file/upload/get-presigned-url?contenttype=application/octet-stream&name={}".format(
        BASE_URL, os.path.basename(fileName))

    response = requests.get(url, headers={"x-api-key": API_KEY})
    if response.status_code == 200:
        json = response.json()

        if not json["error"]:
            uploadUrl = json["presignedUrl"]
            uploadedFileUrl = json["url"]

            with open(fileName, 'rb') as file:
                requests.put(uploadUrl, data=file, headers={"x-api-key": API_KEY, "content-type": "application/octet-stream"})

            return uploadedFileUrl
        else:
            print(json["message"])
    else:
        print(f"Request error: {response.status_code} {response.reason}")

    return None


if __name__ == '__main__':
    main()
