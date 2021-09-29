# Singular EC2 worker node

This stack provides the ability to start an EC2 instance by placing the instance ID on a SQS queue.
The idea is that the EC2 instance will be started up, perform some processing and when done, shut itself down.

For example by placing a batch of files in S3 could trigger a Lambda event that could put the message in the queue for the EC2 to start.
The EC2 will then pull all the files that it can find in the S3 bucket and process them and when done shut itself down.

This Cloud Formation stack deploys a Lambda and SQS queue. 
A message in the format { "instance_id" : "i-0ec080a6ece65fc40" } can be placed in the queue that will trigger the lambda that will attempt to start the EC2 instance.
The EC2 instance will need to start processing automatically when it starts up and shuts itself down when there is nothing to process anymore.

## Requirements
1.  The AWS CLI is required to deploy the Lambda function and SQS queue using the deployment instructions.
2.  The AWS CLI should be configured with valid credentials to create the CloudFormation stack, lambda function, and related resources.  You must also have rights to upload new objects to the S3 bucket you specify in the deployment steps.  
3.  An EC2 instance that are configured to process until there is nothing more to process and then shut down.   
    
## Deploy 

1. Clone the singular_worker github repository to your computer using the following command:

       git clone https://github.com/tobievdmerwe/singular_worker
       
2. Configure the AWS CLI with credentials for your AWS account.  

3. Package the deployment

       aws cloudformation package \
        --template-file infrastructure.yaml \
        --s3-bucket <bucket name> \
        --s3-prefix singularWorker  \
        --output-template-file infrastructure-packaged.yaml 

4. Deploy the stack

       aws cloudformation deploy \
        --template-file infrastructure-packaged.yaml \
        --stack-name singularWorker \
        --region <region where the EC2s are deployed ie eu-west-1>  \
        --capabilities CAPABILITY_IAM 