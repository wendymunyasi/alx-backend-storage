#!/usr/bin/env python3
"""Module for task 11
"""


def schools_by_topic(mongo_collection, topic):
    """Function that returns the list of school having a specific topic.

    Args:
        mongo_collection (pymongo.collection.Collection): collection to analyze
        topic (str): topic searched.

    Returns:
        list: school having a specific topic.
    """
    topic_filter = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    return [doc for doc in mongo_collection.find(topic_filter)]
