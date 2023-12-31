import os
import asyncio
from typing import Callable
from google.cloud import pubsub_v1
from google.pubsub_v1 import PullRequest
from google.oauth2.service_account import Credentials


if os.environ.get("ENV", "PROD") == "DEV":
    creds = Credentials.from_service_account_info(
        {
            "type": os.environ["GOOGLE_CLOUD_TYPE"],
            "project_id": os.environ["GOOGLE_CLOUD_PROJECT"],
            "private_key_id": os.environ["GOOGLE_CLOUD_PRIVATE_KEY_ID"],
            "private_key": os.environ["GOOGLE_CLOUD_PRIVATE_KEY"],
            "client_email": os.environ["GOOGLE_CLOUD_CLIENT_EMAIL"],
            "client_id": os.environ["GOOGLE_CLOUD_CLIENT_ID"],
            "auth_uri": os.environ["GOOGLE_CLOUD_AUTH_URI"],
            "token_uri": os.environ["GOOGLE_CLOUD_TOKEN_URI"],
            "auth_provider_x509_cert_url": os.environ[
                "GOOGLE_CLOUD_AUTH_PROVIDER_X509_CERT_URL"
            ],
            "client_x509_cert_url": os.environ["GOOGLE_CLOUD_CLIENT_X509_CERT_URL"],
        }
    )

    create_candidate_sub = pubsub_v1.SubscriberClient(credentials=creds)
else:
    create_candidate_sub = pubsub_v1.SubscriberClient()

CANDIDATE_CREATION_SUBSCRIPTION_NAME = os.environ[
    "CANDIDATE_CREATION_SUBSCRIPTION_NAME"
]
CANDIDATE_CREATION_SUB_PATH = create_candidate_sub.subscription_path(
    os.environ["GOOGLE_CLOUD_PROJECT"], CANDIDATE_CREATION_SUBSCRIPTION_NAME
)


async def pull_messages(
    subscriber: pubsub_v1.SubscriberClient, subscription_path: str, handler: Callable
) -> None:
    while True:
        try:
            pull_request = PullRequest(subscription=subscription_path, max_messages=10)
            response = subscriber.pull(request=pull_request, timeout=2)
        except Exception as e:
            await asyncio.sleep(15)
            continue

        for received_message in response.received_messages:
            try:
                await handler(received_message.message.data)
                subscriber.acknowledge(
                    subscription=subscription_path, ack_ids=[received_message.ack_id]
                )
            except Exception as e:
                print(f"Error processing message: {e}")

        await asyncio.sleep(15)
