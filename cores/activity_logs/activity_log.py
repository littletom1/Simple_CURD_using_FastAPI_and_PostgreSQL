from cores.databases.connection import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text, desc
from cores.enums import activity_log_enum
from functools import wraps
from datetime import date, datetime
from cores.enums.activity_log_enum import ACTIVITY_LOG_QUEUE

# import json
session: Session = next(get_db())
def get_activity_log(causer_id = None, subject_type= None, subject_id = None, event = None, order = 'asc', is_get_first = False):
    from cores.activity_logs.activity_log_model import ActivityLog
    query = session.query(ActivityLog)
    if causer_id:
        query = query.filter(ActivityLog.causer_id == causer_id)
    if subject_type:
        query = query.filter(ActivityLog.subject_type == subject_type)
    if subject_id:
        query = query.filter(ActivityLog.subject_id == subject_id)
    if event:
        query = query.filter(ActivityLog.event == event)
    query = query.order_by(text(f'id {order}'))
    if is_get_first:
        return query.first()
    result = query.all()
    return session.close()
# def send_queue_to_write_activity_log(func):
#     @wraps(func)
#     async def wrapped_function(*args, **kwargs):
#         print(123, kwargs['request'])
#         FibonacciRpcClient().send_message(
#             method='post',
#             routing_key=worker_enum.ACTIVITY_LOG_QUEUE,
#             body=dict(kwargs['request'])
#         )
#         return await func(**kwargs)
#     return wrapped_function

def send_queue_to_write_activity_log(current_user_id: int, event: str, subject: dict, routing_key = ACTIVITY_LOG_QUEUE, subject_type = None):
    from cores.rabbitmq.rpc_client import FibonacciRpcClient
    data = {
        'current_user_id': current_user_id,
        'event': event,
        'subject': subject,
        'subject_type': subject_type,
    }
    FibonacciRpcClient().send_message(
        method='post',
        routing_key=routing_key,
        body=data
    )

def write_activity_log(current_user_id: int, event: str, subject, subject_type = None, log_name: str = 'default'):
    from cores.activity_logs.activity_log_model import ActivityLog
    if type(subject) is not dict:
        subject_type = subject.__table__.name
        subject = subject.__dict__
        del subject['_sa_instance_state']

    properties = {}
    subject_id = subject['id']
    if event == activity_log_enum.EVENT_DELETED:
        pass
    else:
        if 'created_at' in subject:
            if isinstance(subject['created_at'], (datetime, date)):
                subject['created_at'] = subject['created_at'].isoformat()
        if 'updated_at' in subject:
            if isinstance(subject['updated_at'], (datetime, date)):
                subject['updated_at'] = subject['updated_at'].isoformat()
        if 'deleted_at' in subject:
            if isinstance(subject['deleted_at'], (datetime, date)):
                subject['deleted_at'] = subject['deleted_at'].isoformat()


        properties['attributes'] = subject

    old = {}
    if event == activity_log_enum.EVENT_UPDATED:
        old_log = get_activity_log(current_user_id, subject_type, subject_id, None, 'desc', True)
        if old_log:
            content = old_log.properties
            old = content['attributes']
        # email_file.write(content)

    if old:
        properties['old'] = old
    # properties = json.dumps(properties)

    activity_log = ActivityLog(
        event=event,
        log_name=log_name,
        causer_id=current_user_id,
        subject_type=subject_type,
        subject_id=subject_id,
        properties=properties,
    )
    session.add(activity_log)
    session.commit()
    session.close()
