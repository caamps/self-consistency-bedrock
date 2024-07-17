import boto3 
import json
import time

session = boto3.Session()


# Initialize boto3 clients
iam_client = session.client('iam')
sts_client = session.client('sts')
lambda_client = session.client('lambda')
bedrock = boto3.client('bedrock-agent')


##########################################################################################

# Create IAM role for lambda functions

account_id = sts_client.get_caller_identity()["Account"]
region = session.region_name

lambda_role_name = 'FlowsLambdaRole'

assume_role_policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

lambda_role_response = iam_client.create_role(
    RoleName=lambda_role_name,
    AssumeRolePolicyDocument=json.dumps(assume_role_policy_document),
    Description='IAM role for Lambda function with basic execution permissions'
)

lambda_role_arn = lambda_role_response['Role']['Arn']

iam_client.attach_role_policy(
    RoleName=lambda_role_name,
    PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
)


print(f'Role ARN: {lambda_role_arn}')
print('Role created and policies attached successfully.')
print('Waiting for IAM role to propagate...')
time.sleep(10)

################################################################################
#Create lambda functions

with open('packages/generate-prompts.zip', 'rb') as f:
    generate_prompts_zip_content = f.read()

generate_prompts_function = lambda_client.create_function(
    FunctionName='generate-prompts',
    Runtime='python3.12',
    Role=lambda_role_arn,
    Handler='lambda_function.lambda_handler',
    Code={
        'ZipFile': generate_prompts_zip_content
    },
    Timeout=30,
    MemorySize=128,
    Publish=True
)

generate_prompts_function_arn = generate_prompts_function['FunctionArn']

print(f"Lambda function ARN: {generate_prompts_function_arn}")


with open('packages/evaluate-results.zip', 'rb') as f:
    evaluate_results_zip_content = f.read()

evaluate_results_function = lambda_client.create_function(
    FunctionName='evaluate-results',
    Runtime='python3.12',
    Role=lambda_role_arn,
    Handler='lambda_function.lambda_handler',
    Code={
        'ZipFile': evaluate_results_zip_content
    },
    Timeout=30,
    MemorySize=128,
    Publish=True
)

evaluate_results_function_arn = evaluate_results_function['FunctionArn']
print(f"Lambda function ARN: {evaluate_results_function_arn}")

permission_generate_prompts = lambda_client.add_permission(
    FunctionName='generate-prompts',
    StatementId='permission-generate-prompts',
    Action='lambda:InvokeFunction',
    Principal='bedrock.amazonaws.com'
)

permission_evaluate_results = lambda_client.add_permission(
    FunctionName='evaluate-results',
    StatementId='permission-evaluate-results',
    Action='lambda:InvokeFunction',
    Principal='bedrock.amazonaws.com'
)

###############################################################################
#Create bedrock flows execution role

bedrock_role_name = 'BedrockFlowsRole'
policy_name_1 = 'BedrockGetFlowPolicy'
policy_name_2 = 'BedrockInvokeModelPolicy'

get_flow_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "bedrock:GetFlow",
            "Resource": [
                f"arn:aws:bedrock:{region}:{account_id}:flow/*"
            ]
        }
    ]
}

invoke_model_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "bedrock:InvokeModel",
            "Resource": [
                f"arn:aws:bedrock:{region}::foundation-model/*"
            ]
        }
    ]
}

bedrock_assume_role_policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "bedrock.amazonaws.com"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "aws:SourceAccount": account_id
                },
                "ArnLike": {
                    "aws:SourceArn": f"arn:aws:bedrock:{region}:{account_id}:flow/*"
                }
            }
        }
    ]
}

bedrock_role_response = iam_client.create_role(
    RoleName=bedrock_role_name,
    AssumeRolePolicyDocument=json.dumps(bedrock_assume_role_policy_document),
    Description='IAM role for Bedrock InvokeModel with specific permissions'
)

bedrock_role_arn = bedrock_role_response['Role']['Arn']

iam_client.put_role_policy(
    RoleName=bedrock_role_name,
    PolicyName=policy_name_1,
    PolicyDocument=json.dumps(get_flow_policy)
)

iam_client.put_role_policy(
    RoleName=bedrock_role_name,
    PolicyName=policy_name_2,
    PolicyDocument=json.dumps(invoke_model_policy)
)

print(f'Role ARN: {bedrock_role_arn}')
print('Role created and policies attached successfully.')
print('Waiting for IAM role to propagate...')
time.sleep(10)

####################################################################
with open('definition.json', 'r') as file:
    definition = json.load(file)

definition = json.dumps(definition, ensure_ascii=False)
definition = definition.replace('arn:aws:lambda:region:111222333444:function:nome-da-funcao-1', generate_prompts_function_arn).replace('arn:aws:lambda:region:111222333444:function:nome-da-funcao-2', evaluate_results_function_arn)
definition = json.loads(definition)

response = bedrock.create_flow(
    definition=definition,
    name='self-consistency-flow',
    executionRoleArn=bedrock_role_arn
    )
print("Bedrock flow created successfully.")
