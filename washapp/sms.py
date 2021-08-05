import os
from twilio.rest import Client as messageClient


def request_created_sms(client, request, laundry_basket):

    phone_number = client.phone_number
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    laundry_man = request.laundry_man
    date_required = laundry_basket.date_required
    cost = laundry_basket.get_total_cost()
    user = messageClient(account_sid, auth_token)

    message = user.messages \
        .create(
            body=f'Hello {client.client.username}\n your request to {laundry_man.laundry_man.username} on \
                    {date_required} has been successfully created \n Laundry worth #{cost}. Thank you for choosing us.',
            from_=f'{os.environ["phone_number"]}',
            to=f'+234{phone_number}'
    )

    if message.sid:
        print(message.sid)
        return
    else:
        print('an error occurred')
        return


def random_created_sms(client, request, laundry_basket):

    phone_number = client.phone_number
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    laundry_man = request.laundry_man
    date_required = laundry_basket.date_required
    cost = laundry_basket.get_total_cost()
    user = messageClient(account_sid, auth_token)

    message = user.messages \
        .create(
            body=f'Hello {client.client.username}\n your request has been paired to {laundry_man.laundry_man.username} on \
                    {date_required} \n Laundry worth #{cost}. Thank you for choosing us.',
            from_=f'{os.environ["phone_number"]}',
            to=f'+234{phone_number}'
    )

    if message.sid:
        print(message.sid)
        return
    else:
        print('an error occurred')
        return


def send_request_sms(laundry_man, request, laundry_basket):

    phone_number = laundry_man.phone_number
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = request.client
    date_required = laundry_basket.date_required
    cost = laundry_basket.get_total_cost()
    user = messageClient(account_sid, auth_token)

    message = user.messages \
        .create(
            body=f'Hello {laundry_man.laundry_man.username}\n {client.client.username} has requested your services on \
                {date_required}\n Laundry worth #{cost}, Jump into your office to view request   ',
            from_=f'{os.environ["phone_number"]}',
            to=f'+234{phone_number}'
        )

    if message.sid:
        print(message.sid)
        return
    else:
        print('an error occurred')
        return


def laundry_accepted_sms(client, request, laundry_basket, accepted):

    phone_number = client.phone_number
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    laundry_man = request.laundry_man
    date_required = laundry_basket.date_required
    cost = laundry_basket.get_total_cost()
    user = messageClient(account_sid, auth_token)

    if accepted == 'True':
        message = user.messages \
            .create(
                body=f'Hello {client.client.username}\n your request to {laundry_man.laundry_man.username} on \
                        {date_required} for #{cost} has been accepted \n jumping to your dashboard to make payments \
                         and  proceed',
                from_=f'{os.environ["phone_number"]}',
                to=f'+234{phone_number}'
        )
    elif accepted == 'False':
        message = user.messages \
            .create(
                body=f'Hello {client.client.username}\n Sorry {laundry_man.laundry_man.username} the laundryman would \
                        be unavailable on {date_required} to handle your request. \n Please visit your dashboard to \
                         request another agent. \n Or you can try our random select feature to pair automatically.',
                from_=f'{os.environ["phone_number"]}',
                to=f'+234{phone_number}'
        )

    if message.sid:
        print(message.sid)
        return
    else:
        print('an error occurred')
        return


def payment_made_sms(laundry_man, request, laundry_basket):
    phone_number = laundry_man.phone_number
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = request.client
    date_required = laundry_basket.date_required
    user = messageClient(account_sid, auth_token)

    message = user.messages \
        .create(
            body=f'Hello {laundry_man.laundry_man.username}\n {client.client.username} has made payments on your  \
                   accepted laundry for {date_required}\n You have been successfully booked.',
            from_=f'{os.environ["phone_number"]}',
            to=f'+234{phone_number}'
    )

    if message.sid:
        print(message.sid)
        return
    else:
        print('an error occurred')
        return
