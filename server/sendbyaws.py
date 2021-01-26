import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = "ap-southeast-1"

# The character encoding for the email.
CHARSET = "UTF-8"

def send(sender, receiver, subject, body, attachment=""):
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    # Create a multipart/mixed parent container.
    msg = MIMEMultipart('mixed')
    # Add subject, from and to lines.
    msg['Subject'] = subject 
    msg['From'] = sender 
    msg['To'] = receiver

    # Create a multipart/alternative child container.
    msg_body = MIMEMultipart('alternative')

    # Encode the text and HTML content and set the character encoding. This step is
    # necessary if you're sending a message with characters outside the ASCII range.
    htmlpart = MIMEText(body.encode(CHARSET), 'text', CHARSET)

    # Add the text and HTML parts to the child container.
    msg_body.attach(htmlpart)

    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    msg.attach(msg_body)
    
    if len(attachment) > 0 :
        # Define the attachment part and encode it using MIMEApplication.
        att = MIMEApplication(open(attachment, 'rb').read())

        # Add a header to tell the email client to treat this part as an attachment,
        # and to give the attachment a name.
        att.add_header('Content-Disposition','attachment',filename=os.path.basename(attachment))

        # Add the attachment to the parent container.
        msg.attach(att)
        
    print(msg)
    try:
        #Provide the contents of the email.
        response = client.send_raw_email(
            Source=sender,
            Destinations=[
                receiver
            ],
            RawMessage={
                'Data':msg.as_string(),
            }
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

if __name__ == "__main__":
    from sys import argv, exit

    def usage():
        print("""sendbyaws usage:
python sendbyasw.py <from> <to> <subject> <text body> <path of attachment>""")
        
    print("Number of argv=",len(argv))
    
    if not len(argv) > 4:
        usage()
        exit(64)
        
    send(argv[1], argv[2], argv[3], argv[4], argv[5])
    print("done")
