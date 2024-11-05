import os
import logging
import boto3

from datetime import datetime
from pyhtml2pdf import converter

logger = logging.getLogger()
logger.setLevel("INFO")

BUCKET_NAME = 'wkhtmltopdfhtmlcontent'
INPUT_FILE_NAME = 'sample_website.html'
OUTPUT_FILE_NAME_PREFIX = '/tmp/output.html'
OUTPUT_FILE_EXTENSION = 'pdf'

def generate_pdf_from_html() -> None:
    logger.info("Started generate_pdf_from_html function.")

    result = get_pdf_from_html()
    logger.info("Pdf has been generated.")

    output_file_name = get_output_file_name()

    save_file_locally(output_file_name, result)
    logger.info(f"File: {output_file_name} has been saved locally.")

    save_file_to_s3(output_file_name)
    logger.info(f"File: {output_file_name} has been saved in S3: {BUCKET_NAME}.")

def get_pdf_from_html() -> bytes:
    source: str = get_source_of_input_file()
    timeout: int = 2
    install_driver: bool = True
    print_options: dict = get_print_options()

    return converter.__get_pdf_from_html(source, timeout, install_driver, print_options)

def get_source_of_input_file() -> str:
    path = os.path.abspath(INPUT_FILE_NAME)
    return f'file:///{path}'

def get_output_file_name() -> str:
    curr_time = datetime.now()
    formatted_time = curr_time.strftime("%Y%m%d%H%M%S%f")
    random_prefix = f'{OUTPUT_FILE_NAME_PREFIX}_{formatted_time}'
    return f'{random_prefix}.{OUTPUT_FILE_EXTENSION}'

def get_print_options() -> dict:
    return {
        "scale" : 1
    }

def save_file_locally(output_file_name: str, result: bytes) -> None:
    with open(output_file_name, "wb") as file:
        file.write(result)

def save_file_to_s3(output_file_name: str) -> None:
    s3 = boto3.client("s3")
    path_generated_file = os.path.abspath(output_file_name)
    s3.upload_file(Filename=path_generated_file, Bucket=BUCKET_NAME, Key=output_file_name)
