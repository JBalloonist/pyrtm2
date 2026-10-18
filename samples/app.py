#!/usr/bin/env python
"""Command-line sample: list tasks due within the next week."""

import sys

from rtm import createRTM


def getTasksDueWithinWeek(rtm):
    rspTasks = rtm.tasks.getList(filter='dueWithin:"1 week of today"')
    tasks = []
    lists = rspTasks['tasks'].get('list', [])
    if isinstance(lists, dict):
        lists = [lists]
    for lst in lists:
        # XXX: taskseries *may* be a list
        taskseries = lst.get('taskseries', [])
        if isinstance(taskseries, dict):
            taskseries = [taskseries]
        for t in taskseries:
            tasks.append(t['name'])
    return tasks


def main():
    try:
        api_key, secret = sys.argv[1:3]
    except ValueError:
        sys.stderr.write('Usage: app.py APIKEY SECRET [TOKEN]\n')
        return

    token = sys.argv[3] if len(sys.argv) > 3 else None
    rtm = createRTM(api_key, secret, token)

    tasks = getTasksDueWithinWeek(rtm)
    if not tasks:
        print('No tasks due within a week')
    else:
        print('Tasks due within a week:')
        for task in tasks:
            print(f'- {task}')


if __name__ == '__main__':
    main()
