import json
import boto3
import requests
import os
import datetime

ec2 = boto3.resource('ec2')
cloudtrail = boto3.client('cloudtrail')

SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']


#endtime = instance.launch_time + interval 

def lambda_handler(event, context):
    instance_id = event['detail']['instance-id']
    instance = ec2.Instance(instance_id)
    endtime = datetime.datetime.now()
    interval = datetime.timedelta(minutes=30)
    starttime = instance.launch_time - interval
    iid = ''.join(instance_id)
    mid = ''.join(instance.image_id)
    
    events = get_events(instance.instance_id,starttime,endtime)
    for event in events['Events']:
        username = event.get("Username")
        ct_event = event.get("CloudTrailEvent")
        event_name = event.get("EventName")
        event_time = event.get("EventTime")
        data = { "text": "Instance with image_id " + mid + " has started with stopt-rule ARN " + "{0} - {1} - {2} - {3}".format(username,ct_event,event_name,event_time) }
        print(data)
        print("testing")
        response = requests.post(SLACK_WEBHOOK_URL, json=data, headers={'Content-Type': 'application/json'})
    
    
    
    
    
    
    
    #sr_arn = ''.join(response['RuleArn'])
    #data = { "text": "Instance with image_id " + mid + " has started with stopt-rule ARN " }
    
    





def get_events(instanceid,st,et):

    try:
        response = cloudtrail.lookup_events(
            LookupAttributes=[
                {
                    'AttributeKey': 'ResourceName',
                    'AttributeValue': instanceid
                },
            ],
            StartTime=st,
            EndTime=et,
            MaxResults=50
        )
    except Exception as e:
        print(e)
        print('Unable to retrieve CloudTrail events for user "{}"'.format(instanceid))
        raise(e)
    return response
