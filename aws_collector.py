import boto3
import json
from datetime import datetime

def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def collect_aws_iam_data():
    print("[+] Starting AWS IAM data collection...")
    
    iam_client = boto3.client('iam')
    
    iam_data = {
        "users": [],
        "roles": [],
        "policies": []
    }

    try:
        # Collect IAM Users
        paginator = iam_client.get_paginator('list_users')
        for page in paginator.paginate():
            for user in page['Users']:
                user_name = user['UserName']
                attached_policies = iam_client.list_attached_user_policies(UserName=user_name)['AttachedPolicies']
                
                iam_data["users"].append({
                    "UserName": user_name,
                    "Arn": user['Arn'],
                    "AttachedPolicies": attached_policies
                })

        # Collect IAM Roles and Trust Policies
        paginator = iam_client.get_paginator('list_roles')
        for page in paginator.paginate():
            for role in page['Roles']:
                role_name = role['RoleName']
                attached_policies = iam_client.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']
                
                iam_data["roles"].append({
                    "RoleName": role_name,
                    "Arn": role['Arn'],
                    "AssumeRolePolicyDocument": role['AssumeRolePolicyDocument'],
                    "AttachedPolicies": attached_policies
                })

        # Save collected data to JSON file
        output_file = "aws_iam_data.json"
        with open(output_file, "w") as f:
            json.dump(iam_data, f, indent=4, default=datetime_serializer)
            
        print(f"[✔] Success! IAM data saved to '{output_file}'.")

    except Exception as e:
        print(f"[❌] Error occurred: {str(e)}")

if __name__ == "__main__":
    collect_aws_iam_data()