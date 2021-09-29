# This Lambda takes instance-ids from the SQS queue and start the instance(s).
# SQS message format : { "instance_id" : "i-0ec080a6ece65fc40" }
import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Lambda handler
def lambda_handler(event, context):

    try:
       ec2 = boto3.resource('ec2')
       logger.info('Event info: {}'.format(event))

       for record in event['Records']:
          body = record['body']
          event_body = json.loads(body)    
          instance_id = event_body['instance_id']
          try:
             instance = ec2.Instance(instance_id)
             logger.info("Instance State {}".format(instance.state['Name']))
             if instance.state['Name'] == 'running':
                 logger.info("Instance is already running, nothing to do.")
             elif instance.state['Name'] in ['stopping']:
                 logger.info("Waiting for instance to stop")
                 instance.wait_until_stopped()
                 logger.info("Starting instance {}".format(instance_id))
                 instance.start()
                 instance.wait_until_running()
                 logger.info("Instance State {}".format(instance.state['Name']))
             elif instance.state['Name'] in ['shutting-down', 'pending']:
                 logger.info("Cannot reboot machines that are in this state.")
             elif instance.state['Name'] == 'stopped':
                 logger.info("Starting instance {}".format(instance_id))
                 instance.start()
                 instance.wait_until_running()
                 logger.info("Instance State {}".format(instance.state['Name']))
          except Exception as e:
             logger.error('Could not start instance {}'.format(e))
             raise
    except Exception as e:
        logger.error('An exception has happened: {}'.format(e))
        raise