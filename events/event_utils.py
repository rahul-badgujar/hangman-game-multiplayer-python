import pickle

from events.event_base import Event


def encode_event(event: Event)->bytes:
    return pickle.dumps(event)

def decode_event(encoded_event)->Event:
    return pickle.loads(encoded_event)