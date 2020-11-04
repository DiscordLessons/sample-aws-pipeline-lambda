import boto3
import time

client = boto3.client('cloudformation')
client_lambda = boto3.client('lambda')

def lambda_handler(event, context):
    try:
        client_lambda.update_function_code(
              FunctionName='prodLambdaFunction',
              S3Bucket='bwijayaw-riiid-production',
              S3Key='python_function.zip',
          )
        client.create_change_set(
            StackName='prodStack',
            TemplateURL='https://bwijayaw-riiid-production.s3.us-east-2.amazonaws.com/prod-lambda-cf.yml',
            ChangeSetName='prodChangeSet',
            ChangeSetType='IMPORT',
            ResourcesToImport=[
                {
                    'ResourceType': 'AWS::Lambda::Function',
                    'LogicalResourceId': 'ProdLambdaFunction',
                    'ResourceIdentifier': {
                        'FunctionName': 'prodLambdaFunction'
                    }
                },
            ]
        )
        time.sleep(5)
        client.execute_change_set(
            ChangeSetName='prodChangeSet',
            StackName='prodStack'
        )
        print("Function code updated. Creating stack.")
        return
    except:
        print("Function code updated. Stack is already running.")
        return

