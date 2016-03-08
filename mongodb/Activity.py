#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from pymongo import MongoClient


class Activity:
    def __init__(self):
        pass

    @staticmethod
    def convert_activity(address_old, port_old, address_new, port_new):
        # old database connection
        client = MongoClient(address_old, port_old)
        travel1 = client.travel1

        # new database connection
        client = MongoClient(address_new, port_new)
        travel2 = client.travel2

        # old collection latest activities
        activities = travel1.activities
        activity_new = travel2.activity

        # clean former data
        activity_new.remove()

        for activity_old in activities.find():
            _id = activity_old['_id']
            title = activity_old['title']

            if 'cover_image' in activity_old:
                cover_image = activity_old['cover_image']
            else:
                cover_image = None

            post = {
                '_id': _id,  # 活动ID
                'title': title,  # 活动主题
                'cover_image': cover_image  # 活动封面
            }
            activity_new.insert(post)

    @staticmethod
    def get_city_activity(address_old, port_old):
        # old database connection
        client = MongoClient(address_old, port_old)
        travel1 = client.travel1

        # old collection city
        latest_city = travel1.latestcity

        kv_city_activity = {}
        for city in latest_city.find():
            city_id = city['_id']

            if 'activity_labels' in city:
                activity_labels = city['activity_labels']
                if len(activity_labels) > 0:
                    activity_list = []
                    for activity in activity_labels:
                        activity_list.append(activity['_id'])
                    kv_city_activity[city_id] = activity_list

        return kv_city_activity

