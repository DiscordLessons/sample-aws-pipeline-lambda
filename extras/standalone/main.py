#!/usr/bin/python3

import requests
import json
import subprocess
import sys
import time

# Ensure there is only one argument, a whole number between 1-24.
hours = input("Enter 'h', the past number of hours to parse the HackerNews API:")
try:
    arg = int(hours)
except:
    sys.exit("Please enter a whole number.")

if (arg < 1) or (arg > 24):
    raise Exception("Please enter a whole number between 1 and 24.")

h = 0 # h = past number of hours.
h = arg * 3600 # Taken from input argument then converted to seconds.
stored_count = 0 # Initial value for counting.
highest_count = 0 # Max comment depth.
stored_depth = 0 # Initial value for keeping track of depth.
story_depth = 0 # Depth of the current story.
highest_depth = 0 # Highest depth for a story.
# story_highest = 0 # Story ID with the deepest comment thread. Enable in Lambda
depth = 0 # Tracking how many times the recursive function gets called.
list_count = 0 # Counter to keep track when reaching end of a list.
api_url = "https://hacker-news.firebaseio.com/v0" # Base portion of the url
within_time_range = [] # List of story ids in the past 'h' hours.

# Output a formatted string given a json object as input.
def jprint(object):
    text = json.dumps(object, sort_keys=True, indent=4)
    print(text)
    return

# Recursive function that determines the max depth.
def depth_counter(id, depth):
    global stored_count
    global highest_count
    time.sleep(0.2) # Need a wait timer to prevent too many requests error.
    print("Function 'depth_counter' depth:")
    print(depth)
    # Check each top-level comment for child comments, then check if those have their own child comments
    # until there are no more child comments.
    new_item = requests.get(api_url + "/item/{}.json".format(id))
    if 'kids' in new_item.json():
        print(new_item.json()['kids'])
        for item_id in new_item.json()['kids']:
            print("Item ID:")
            print(item_id)
            time.sleep(0.2)
            # Need to exclude deleted comments, which still appear in the API response for some reason...
            check_deleted = requests.get(api_url + "/item/{}.json".format(item_id))
            if 'deleted' in check_deleted.json():
                continue
            else:
                depth_counter(item_id, depth = depth + 1)
    else:
        if depth >= stored_count:
            highest_count = depth
        stored_count = highest_count
        print("Stored count:")
        print(stored_count)
        print("Highest count:")
        print(highest_count)
        print("Moving on to next item id...")
        print("")
    return highest_count

# Keeps track of the max comment depth and the story id which it belongs to, then prints the output.
def comment_depth():
    global stored_depth
    global story_depth
    for new_item_id in within_time_range:
        print("Story ID:")
        print(new_item_id)
        story_depth = depth_counter(new_item_id, depth = 0)
        if story_depth >= stored_depth:
            highest_depth = story_depth
            story_id_highest = new_item_id
        stored_depth = highest_depth
    print("Story ID with the highest comment depth:")
    print(story_id_highest)
    print("Comment depth:")
    print(stored_depth)
    story = requests.get(api_url + "/item/{}.json".format(story_id_highest))
    jprint(story.json())
    return

def main():
    # Sort through the new stories and create a list, containing stories created in the past 'h' number of hours.
    new_stories = requests.get(api_url + "/newstories.json")
    # Obtain Unix time stamp.
    date = subprocess.Popen(['date', '+%s'],
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    unix_timestamp_str = date.stdout.readline().strip()
    unix_timestamp = int(unix_timestamp_str)
    print("Unix timestamp:")
    print(unix_timestamp)
    time_range = unix_timestamp - h # Current timestamp minus h*3600 gives us the timestamp range to focus on.
    print("Time range:")
    print(time_range)

    # If the story was created within the past 'h' hours AND has at least one comment, add to list.
    for story_id in new_stories.json():
        print(story_id)
        time.sleep(0.2)
        story = requests.get(api_url + "/item/{}.json".format(story_id))
        story_time = story.json()['time']
        if (story_time >= time_range) and ('kids' in story.json()):
            print("Appending story ID to list")
            within_time_range.append(story_id)

    comment_depth()
    return

main()

