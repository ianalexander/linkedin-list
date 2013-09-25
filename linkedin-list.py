#!/usr/bin/python

import json
import requests
import csv

# This needs a `leo_auth_token` taken from your web session
LINKEDIN_WEB_COOKIES = dict(
    leo_auth_token='"LIM:54847616:a:21600:1380047125:8e7d114e12e6b5deadc81fe87ffb57c1955aee69"',
)
MY_LINKEDIN_ID = 0


def get_2nd_degree_connections(user_id):
    """Get 2nd degree connections for a given user_id

    Keyword Arguments:
    user_id -- LinkedIn User ID

    Returns a dict containing connection information

    """
    result = []
    if user_id:
        url = 'https://www.linkedin.com/profile/profile-v2-connections?'
        + 'id={}&offset=0&count=1000&distance=1&type=INITIAL'.format(user_id)
        r = requests.get(url, cookies=LINKEDIN_WEB_COOKIES)
        # Encode text to ASCII to avoid encoding issues with .csv
        j = json.loads(r.text.encode('ascii', 'ignore'))
        connections = []
        try:
            connections = j['content']['connections']['connections']
        except KeyError:
            print "Key Error! Dumping body:"
            print r.text
        result = []
        for connection in connections:
            result.append({
                'full_name': connection.get('fmt__full_name', None),
                'headline': connection.get('headline', None),
                'id': connection.get('memberID', None)
                })
    return result

if __name__ == "__main__":
    # get a list of my connections
    print "Getting all my connections..."
    my_connections = get_2nd_degree_connections(MY_LINKEDIN_ID)

    # loop through my connections to get all 2nd degree connections
    print "Getting all 2nd degree connections and writing to output.csv"
    fieldnames = ['id', 'full_name', 'headline']
    with open('output.csv', 'wb') as csvfile:
        cw = csv.DictWriter(csvfile, fieldnames=fieldnames)
        cw.writeheader()
        counter = 0
        length = len(my_connections)
        for connection in my_connections:
            print "[{}/{}] Requesting {}...".format(
                counter, length, connection.get('full_name', '')
                )
            user_connections = get_2nd_degree_connections(
                connection.get('id', None)
            )
            for row in user_connections:
                cw.writerow(row)
            counter += 1
    print "Done!"
