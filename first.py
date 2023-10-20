import os
import requests
from creds import API_KEY  

class PDFProcessor:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = "https://api.ilovepdf.com/v1"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def combine_pdfs(self, pdf_files, output_path):
        endpoint = f"{self.base_url}/tasks"
        task_data = {
            "tasks": [{"tool": "merge", "params": {"files": pdf_files}},
            ],
        }
        response = requests.post(endpoint, json=task_data, headers=self.headers)
        print(response.text)
        if response.status_code == 200:
            task_id = response.json()["task"]
            download_url = f"{self.base_url}/tasks/{task_id}/download"
            response = requests.get(download_url, stream=True)
            if response.status_code == 200:
                with open(output_path, "wb") as pdf_output:
                    for chunk in response.iter_content(1024):
                        pdf_output.write(chunk)
                return True
        return False

    def extract_pages(self, pdf_file, start_page, end_page, output_path):
        endpoint = f"{self.base_url}/tasks"
        task_data = {
            "tasks": [{"tool": "split", "params": {"start_page": start_page, "end_page": end_page}},
            ],
        }
        response = requests.post(endpoint, json=task_data, headers=self.headers)
        if response.status_code == 200:
            task_id = response.json()["task"]
            download_url = f"{self.base_url}/tasks/{task_id}/download"
            response = requests.get(download_url, stream=True)
            if response.status_code == 200:
                with open(output_path, "wb") as pdf_output:
                    for chunk in response.iter_content(1024):
                        pdf_output.write(chunk)
                return True
        return False

    def remove_password(self, pdf_file, output_path):
        endpoint = f"{self.base_url}/tasks"
        task_data = {
            "tasks": [{"tool": "protect", "params": {"password": "", "encrypt": "false"}},
            ],
        }
        response = requests.post(endpoint, json=task_data, headers=self.headers)
        if response.status_code == 200:
            task_id = response.json()["task"]
            download_url = f"{self.base_url}/tasks/{task_id}/download"
            response = requests.get(download_url, stream=True)
            if response.status_code == 200:
                with open(output_path, "wb") as pdf_output:
                    for chunk in response.iter_content(1024):
                        pdf_output.write(chunk)
                return True
        return False

    def extract_text(self, pdf_file, txt_file):
        endpoint = f"{self.base_url}/tasks"
        task_data = {
            "tasks": [{"tool": "text", "params": {}},
            ],
        }
        response = requests.post(endpoint, json=task_data, headers=self.headers)
        if response.status_code == 200:
            task_id = response.json()["task"]
            download_url = f"{self.base_url}/tasks/{task_id}/download"
            response = requests.get(download_url, stream=True)
            if response.status_code == 200:
                with open(txt_file, "wb") as text_output:
                    for chunk in response.iter_content(1024):
                        text_output.write(chunk)
                return True
        return False

    def images_to_pdf(self, image_files, output_path):
        endpoint = f"{self.base_url}/tasks"
        task_data = {
            "tasks": [{"tool": "image2pdf", "params": {"files": image_files}},
            ],
        }
        response = requests.post(endpoint, json=task_data, headers=self.headers)
        if response.status_code == 200:
            task_id = response.json()["task"]
            download_url = f"{self.base_url}/tasks/{task_id}/download"
            response = requests.get(download_url, stream=True)
            if response.status_code == 200:
                with open(output_path, "wb") as pdf_output:
                    for chunk in response.iter_content(1024):
                        pdf_output.write(chunk)
                return True
        return False

if __name__ == "__main__":
    pdf_processor = PDFProcessor()

    while True:
        print("\nPDF Processing Options:")
        print("1. Combine PDF files")
        print("2. Extract pages from a PDF")
        print("3. Remove PDF password")
        print("4. Extract text from a PDF")
        print("5. Convert images to PDF")
        print("6. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            pdf_files = input("Enter PDF files to combine (comma-separated): ").split(",")
            output_path = input("Enter the output PDF file name: ")
            if pdf_processor.combine_pdfs(pdf_files, output_path):
                print("PDFs combined successfully.")
            else:
                print("PDF combination failed.")

        elif choice == "2":
            pdf_file = input("Enter the source PDF file: ")
            start_page = int(input("Enter the start page: "))
            end_page = int(input("Enter the end page: "))
            output_path = input("Enter the output PDF file name: ")
            if pdf_processor.extract_pages(pdf_file, start_page, end_page, output_path):
                print("Pages extracted successfully.")
            else:
                print("Page extraction failed.")

        elif choice == "3":
            pdf_file = input("Enter the source PDF file: ")
            output_path = input("Enter the output PDF file name: ")
            if pdf_processor.remove_password(pdf_file, output_path):
                print("PDF password removed successfully.")
            else:
                print("Password removal failed.")

        elif choice == "4":
            pdf_file = input("Enter the source PDF file: ")
            txt_file = input("Enter the output text file name: ")
            if pdf_processor.extract_text(pdf_file, txt_file):
                print("Text extracted successfully.")
            else:
                print("Text extraction failed.")

        elif choice == "5":
            image_files = input("Enter image files to convert (comma-separated): ").split(",")
            output_path = input("Enter the output PDF file name: ")
            if pdf_processor.images_to_pdf(image_files, output_path):
                print("Images converted to PDF successfully.")
            else:
                print("Image to PDF conversion failed.")

        elif choice == "6":
            print("Exiting the PDF Processor. Bye , Take Care!")
            break

        else:
            print("Invalid choice. Please select a valid option.")
