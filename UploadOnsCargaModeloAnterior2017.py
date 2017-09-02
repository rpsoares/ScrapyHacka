import boto3
ACCESS_KEY = ''
SECRET_KEY =  ''
input = "onsCargaModeloAnterior2017.json"
bucketName = "hackadirtyfiles"
key = "Carga/onsCargaModeloAnterior2017.json"

s3_client = boto3.client(
	's3',
	aws_access_key_id=ACCESS_KEY,
	aws_secret_access_key=SECRET_KEY
)
# Upload the file to S3
s3_client.upload_file(input, bucketName, key)

# Download the file from S3
#s3_client.download_file('MyBucket', 'hello-remote.txt', 'hello2.txt')
#print(open('hello2.txt').read())