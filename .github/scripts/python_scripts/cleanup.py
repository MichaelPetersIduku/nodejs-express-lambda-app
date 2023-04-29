'''
 - Delete lambda
 - Delete cloudwatch logs
 - Delete lambda ARN from SSM
 - 
'''

import boto3
import sys

from utils import fetch_lambda

ssm = boto3.client('ssm')
lambda_client = boto3.client('lambda')
logs_client = boto3.client('logs')

if len(sys.argv) < 2:
    sys.exit("Please specify a branch name")
branch_name = sys.argv[1]

lambda_name = f"Staging-Ethereum-API-{branch_name}"

lambda_respone = fetch_lambda(lambda_name)

if lambda_respone:
    try:
        response = lambda_client.delete_function(
            FunctionName=lambda_name
        )
        print(f"Lambda function deleted: {response}")
    except Exception as error:
        print(f"Error deleting lambda: {error}")

try:
    response = logs_client.delete_log_group(
        logGroupName=f"/aws/lambda/{lambda_name}"
    )
    print(f"Lambda function logs deleted: {response}")
except Exception as error:
    print(f"Error deleting log group: {error}")


try:
    response = ssm.delete_parameter(
        Name=f"EthereumAPIAppsync_{branch_name}_LAMBDA_ARN"
    )
    print(f"ARN Parameter entry for lambda deleted: {response}")
except Exception as error:
    print(f"Error deleting ARN parameter entry for lambda: {error}")


try:
    response = ssm.delete_parameter(
        Name=f"EthereumAPI_{branch_name}_APPSYNC_CONFIG"
    )
    print(f"APPSYNC Parameter entry for lambda deleted: {response}")
except Exception as error:
    print(f"Error deleting APPSYNC parameter entry for lambda: {error}")
