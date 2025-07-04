import os
import boto3
from jinja2 import Environment, FileSystemLoader
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
SENDER = os.getenv("SES_SENDER")

ses_client = boto3.client(
    "ses",
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

# Jinja2 template engine
env = Environment(loader=FileSystemLoader('templates'))

def send_email(recipient, subject, template_name, context):
    try:
        # Render template
        template = env.get_template(template_name)
        html_body = template.render(context)
        text_body = context.get("text", "This is a plain text fallback.")

        response = ses_client.send_email(
            Source=SENDER,
            Destination={'ToAddresses': [recipient]},
            Message={
                'Subject': {'Data': subject},
                'Body': {
                    'Text': {'Data': text_body},
                    'Html': {'Data': html_body}
                }
            }
        )
        return {"status": "success", "message_id": response['MessageId']}
    except ClientError as e:
        return {"status": "error", "message": e.response['Error']['Message']}
    except Exception as ex:
        return {"status": "error", "message": str(ex)}

