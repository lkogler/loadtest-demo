import argparse

from s3_worker import publish

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("message_count", type=int)
    args = parser.parse_args()
    message_count = args.message_count
    print("Publishing '{}' messages".format(message_count))
    publish(message_count)
