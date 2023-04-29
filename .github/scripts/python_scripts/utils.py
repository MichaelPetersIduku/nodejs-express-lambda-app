import boto3

ssm = boto3.client('ssm')
lambda_client = boto3.client('lambda')


def fetch_lambda(name):
    lambdaFunc = ''
    try:
        response = lambda_client.get_function(FunctionName=name)
        if response["Configuration"]["FunctionName"] == name:
            lambdaFunc = response["Configuration"]
    except Exception as error:
        print(f"This function: {name} does not exist")
        print(f"Error fetching function: {error}")
    finally:
        return lambdaFunc


def get_parameter(name):
    try:
        response = ssm.get_parameter(Name=name)
    except Exception as e:
        print("Could not fetch parameters")
        print(f"Error: {e}")
        return ""

    return response["Parameter"]["Value"]


def create_parameter(name, value, type, overwrite):
    try:
        response = ssm.put_parameter(
            Name=name,
            Value=value,
            Type=type,
            Overwrite=overwrite
        )
    except Exception as error:
        print(f"Error creating parameter: {error}")
