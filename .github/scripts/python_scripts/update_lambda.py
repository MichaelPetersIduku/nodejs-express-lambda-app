import boto3
import sys
import json

from utils import fetch_lambda

lambda_client = boto3.client('lambda')

if len(sys.argv) < 2:
    sys.exit("Please specify a branch name")
branch_name = sys.argv[1]

with open("./config/lambda_layers.json") as f:
    layersConfig = json.load(f)

aws_layers = []
lambda_layers = []

if branch_name == "master":
    lambda_name = "Ethereum-API"
elif branch_name == "staging":
    lambda_name = "Staging-Ethereum-API"
elif branch_name == "dev":
    lambda_name = "Staging-Ethereum-API-dev"
else:
    lambda_name = f"Staging-Ethereum-API-{branch_name}"


try:
    response = lambda_client.list_layers()
    aws_layers = response["Layers"]
    while "NextMarker" in response:
        response = lambda_client.list_layers(
            Marker=response["NextMarker"]
        )
        aws_layers += response["Layers"]
except Exception as e:
    print(f"Error listing layers: {e}")


for aws_layer in aws_layers:
    for layer in layersConfig.keys():
        layerConfig = layersConfig[layer]
        if layerConfig["LayerName"] == aws_layer["LayerName"] and layerConfig["Version"] == aws_layer["LatestMatchingVersion"]["Version"]:
            lambda_layers.append(
                aws_layer["LatestMatchingVersion"]["LayerVersionArn"])


try:
    lambda_found = fetch_lambda(lambda_name)
    if not lambda_found:
        sys.exit("Lambda does not exist")
    else:
        response = lambda_client.update_function_configuration(
            FunctionName=lambda_name,
            Layers=lambda_layers,
            MemorySize=8192,
            Timeout=650
        )
        print("Updated lambda configuration")
except Exception as error:
    print(f"Error updating Lambda configuration: {error}")
