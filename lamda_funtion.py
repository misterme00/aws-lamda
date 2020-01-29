import json
import boto3
import requests
import os


js = """
{
  "source": [
    "aws.ec2"
  ],
  "detail-type": [
    "EC2 Instance State-change Notification"
  ],
  "detail": {
    "state": [
      "stopping"
    ],
    "instance-id": [
      ""
    ]
  }
}
"""

cw_events = boto3.client('events')
ec2 = boto3.resource('ec2')

SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']

def lambda_handler(event, context):
    instance_id = event['detail']['instance-id']
    instance = ec2.Instance(instance_id)
    iid = ''.join(instance_id)
    mid = ''.join(instance.image_id)
    ejs={}
    ejs = json.loads(js)
    
    ejs['detail']['instance-id'] = [event['detail']['instance-id']]

    name = "stopping-instance-" + ''.join(instance_id)
    response = instance.create_tags(Tags=[{'Key': 'Ami', 'Value': instance.image_id}])
    response = cw_events.put_rule(
        Name=name,
        RoleArn='arn:aws:iam::534756183248:role/service-role/py-instance-ami-role-3m0yi8b0',
        EventPattern=json.dumps(ejs),
        State='ENABLED')
    pt_response = cw_events.put_targets(
      Rule=name,
      Targets=[
        {
            'Id': "1",
            'Arn': "arn:aws:lambda:us-east-2:534756183248:function:Stopping-Instace",
        },
      ]
    )
    
    sr_arn = ''.join(response['RuleArn'])
    data = { "text": "Instance with image_id " + mid + " has started with stopt-rule ARN " + sr_arn }
    response = requests.post(SLACK_WEBHOOK_URL, json=data, headers={'Content-Type': 'application/json'})
