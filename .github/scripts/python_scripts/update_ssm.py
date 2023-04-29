import boto3
import sys

from utils import fetch_lambda, create_parameter

ssm = boto3.client('ssm')
lambda_client = boto3.client('lambda')

if len(sys.argv) < 2:
    sys.exit("Please specify a branch name")
branch_name = sys.argv[1]


lambda_found = fetch_lambda(f"Staging-Ethereum-API-{branch_name}")
if not lambda_found:
    sys.exit("Lambda does not exist")
else:
    function_arn = lambda_found["FunctionArn"]
    parameterName = f"EthereumAPIAppsync_{branch_name}_LAMBDA_ARN"
    try:
        response = create_parameter(
            name=parameterName,
            value=function_arn,
            type='String',
            overwrite=True
        )
        print(f"Parameter: {parameterName} is created")
    except Exception as error:
        print(f"Could not create parameter: {error}")
