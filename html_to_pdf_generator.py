import os
import shlex
import subprocess

from pyhtml2pdf import converter
import json
import logging
import boto3

logger = logging.getLogger()
logger.setLevel("INFO")

BUCKET_NAME = ''
INPUT_FILE_NAME = '/tmp/input.html'
OUTPUT_FILE_NAME = '/tmp/output.html'
PARAM_FILE_CONTENT_KEY = 'page_content'


def generate_pdf_from_html():
    print("SIEMA :)))")

    # logger.info("Started lambda function")
    # message = 'HELLO FROM LAMBDA'

    # with open(INPUT_FILE_NAME, 'w') as input_file:
    #     input_file.write(event[PARAM_FILE_CONTENT_KEY])

    result = convert_html_to_pdf()

    # command = f'ls -l'
    # args = shlex.split(command)
    # subprocess.run(args)

    s3 = boto3.resource("s3")
    s3.put_object(Bucket=BUCKET_NAME, Key=INPUT_FILE_NAME, Body=result)

    # return {
    #     "statusCode": 200,
    #     "headers": {
    #         "Content-Type": "application/json"
    #     },
    #     "body": json.dumps({
    #         "message ": message
    #     })
    # }



def convert_html_to_pdf():
    # converter.convert('https://pypi.org', 'sample_scale_0_5.pdf', print_options={"scale": 0.5})
    path = os.path.abspath('sample_website.html')
    source = f'file:///{path}'
    target = 'sample_scale_test_XXXX.pdf'
    print_options = {
        "scale" : 1
    }
    # converter.convert(source=source, target='sample_scale_2.pdf', print_options={"scale": 1})
    result = get_pdf_from_html(source=source, print_options=print_options)
    # with open(target, "wb") as file:
    #     file.write(result)
    return result

def get_pdf_from_html(
        source: str,
        timeout: int = 2,
        install_driver: bool = True,
        print_options: dict = {}
):
    return converter.__get_pdf_from_html(source, timeout, install_driver, print_options)