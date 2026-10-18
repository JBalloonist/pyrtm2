# -*- coding: utf-8 -*-

SERVICE_URL = 'https://api.rememberthemilk.com/services/rest/'
AUTH_SERVICE_URL = 'https://www.rememberthemilk.com/services/auth/'

# API spec
API = {
    'auth': {
        'checkToken':
            [('auth_token',), ()],
        'getFrob':
            [(), ()],
        'getToken':
            [('frob',), ()]
    },
    'contacts': {
        'add':
            [('timeline', 'contact'), ()],
        'delete':
            [('timeline', 'contact_id'), ()],
        'getList':
            [(), ()]
    },
    'groups': {
        'add':
            [('timeline', 'group'), ()],
        'addContact':
            [('timeline', 'group_id', 'contact_id'), ()],
        'delete':
            [('timeline', 'group_id'), ()],
        'getList':
            [(), ()],
        'removeContact':
            [('timeline', 'group_id', 'contact_id'), ()],
    },
    'lists': {
        'add':
            [('timeline', 'name',), ('filter',)],
        'archive':
            [('timeline', 'list_id'), ()],
        'delete':
            [('timeline', 'list_id'), ()],
        'getList':
            [(), ()],
        'setDefaultList':
            [('timeline',), ('list_id',)],
        'setName':
            [('timeline', 'list_id', 'name'), ()],
        'unarchive':
            [('timeline', 'list_id'), ()]
    },
    'locations': {
        'getList':
            [(), ()]
    },
    'push': {
        'getSubscriptions':
            [(), ()],
        'getTopics':
            [(), ()],
        'subscribe':
            [('timeline', 'url', 'topics', 'push_format'),
             ('lease_seconds', 'filter')],
        'unsubscribe':
            [('timeline', 'subscription_id'), ()]
    },
    'reflection': {
        'getMethodInfo':
            [('method_name',), ()],
        'getMethods':
            [(), ()]
    },
    'scripts': {
        'add':
            [('timeline', 'name', 'code'), ()],
        'delete':
            [('timeline', 'script_id'), ()],
        'getList':
            [(), ('name',)],
        'run':
            [('timeline', 'script_id'), ()],
        'setCode':
            [('timeline', 'script_id', 'code'), ()],
        'setName':
            [('timeline', 'script_id', 'name'), ()]
    },
    'settings': {
        'getList':
            [(), ()]
    },
    'tags': {
        'getList':
            [(), ()]
    },
    'tasks': {
        'add':
            [('timeline', 'name',),
             ('list_id', 'parse', 'parent_task_id', 'external_id',
              'give_to')],
        'addTags':
            [('timeline', 'list_id', 'taskseries_id', 'task_id', 'tags'),
             ()],
        'complete':
            [('timeline', 'list_id', 'taskseries_id', 'task_id',), ()],
        'delete':
            [('timeline', 'list_id', 'taskseries_id', 'task_id'), ()],
        'getList':
            [(),
             ('list_id', 'filter', 'last_sync', 'callback')],
        'movePriority':
            [('timeline', 'list_id', 'taskseries_id', 'task_id', 'direction'),
             ()],
        'moveTo':
            [('timeline', 'from_list_id', 'to_list_id', 'taskseries_id',
              'task_id'),
             ()],
        'postpone':
            [('timeline', 'list_id', 'taskseries_id', 'task_id'),
             ()],
        'removeTags':
            [('timeline', 'list_id', 'taskseries_id', 'task_id', 'tags'),
             ()],
        'setDueDate':
            [('timeline', 'list_id', 'taskseries_id', 'task_id'),
             ('due', 'has_due_time', 'parse')],
        'setEstimate':
            [('timeline', 'list_id', 'taskseries_id', 'task_id'),
             ('estimate',)],
        'setLocation':
            [('timeline', 'list_id', 'taskseries_id', 'task_id'),
             ('location_id',)],
        'setName':
            [('timeline', 'list_id', 'taskseries_id', 'task_id', 'name'),
             ()],
        'setParentTask':
            [('timeline', 'list_id', 'taskseries_id', 'task_id'),
             ('parent_task_id',)],
        'setPriority':
            [('timeline', 'list_id', 'taskseries_id', 'task_id'),
             ('priority',)],
        'setRecurrence':
            [('timeline', 'list_id', 'taskseries_id', 'task_id'),
             ('repeat',)],
        'setStartDate':
            [('timeline', 'list_id', 'taskseries_id', 'task_id'),
             ('start', 'has_start_time', 'parse')],
        'setTags':
            [('timeline', 'list_id', 'taskseries_id', 'task_id'),
             ('tags',)],
        'setURL':
            [('timeline', 'list_id', 'taskseries_id', 'task_id'),
             ('url',)],
        'uncomplete':
            [('timeline', 'list_id', 'taskseries_id', 'task_id'),
             ()],
    },
    'tasksNotes': {
        'add':
            [('timeline', 'list_id', 'taskseries_id', 'task_id',
              'note_title', 'note_text'), ()],
        'delete':
            [('timeline', 'note_id'), ()],
        'edit':
            [('timeline', 'note_id', 'note_title', 'note_text'), ()]
    },
    'test': {
        'echo':
            [(), ()],
        'login':
            [(), ()]
    },
    'time': {
        'convert':
            [('to_timezone',), ('from_timezone', 'time')],
        'parse':
            [('text',), ('timezone', 'dateformat')]
    },
    'timelines': {
        'create':
            [(), ()]
    },
    'timezones': {
        'getList':
            [(), ()]
    },
    'transactions': {
        'undo':
            [('timeline', 'transaction_id'), ()]
    },
}


# response format
_LIST_COMMON = {
    'list': ['archived', 'deleted', 'id', 'locked', 'name',
             'position', 'smart'],
}

_TASKSERIES_FIELDS = ['created', 'id', 'location_id', 'modified', 'name',
                      'parent_task_id', 'source', 'url']

_TASK_FIELDS = ['added', 'completed', 'deleted', 'due', 'estimate',
                'has_due_time', 'has_start_time', 'id', 'postponed',
                'priority', 'start']

_TASK_COMMON = {
    'list': ['id', {
        'taskseries': [*_TASKSERIES_FIELDS, {
            'tags': [],
            'participants': [],
            'notes': [],
            'task': _TASK_FIELDS,
            },
        ],
        },
    ],
}

_TASK_TAGS = {
    'list': ['id', {
        'taskseries': [*_TASKSERIES_FIELDS, {
            'tags': {
                'tag': [],
            },
            'participants': [],
            'notes': [],
            'task': _TASK_FIELDS,
            },
        ],
        },
    ],
}

_TASK_RRULE = {
    'list': ['id', {
        'taskseries': [*_TASKSERIES_FIELDS, {
            'rrule': ['every'],
            'tags': [],
            'participants': [],
            'notes': [],
            'task': _TASK_FIELDS,
            },
        ],
        },
    ],
}

_TASK_TAGS_RRULE = {
    'list': ['id', {
        'taskseries': [*_TASKSERIES_FIELDS, {
            'rrule': ['every'],
            'tags': {
                'tag': [],
            },
            'participants': [],
            'notes': [],
            'task': _TASK_FIELDS,
            },
        ],
        },
    ],
}

_SCRIPT_COMMON = {
    'script': ['code', 'created', 'id', 'modified', 'name'],
}

_SUBSCRIPTION_COMMON = {
    'subscription': ['expires', 'format', 'id', 'pending', 'url', {
        'topics': {
            'topic': [],
            },
        },
    ],
}

API_RESPONSE = {
    'auth': {
        'checkToken': {
            'auth': {
                'token': [],
                'perms': [],
                'user': ['fullname', 'id', 'username'],
            },
        },
        'getFrob': {
            'frob': [],
        },
        'getToken': {
            'auth': {
                'token': [],
                'perms': [],
                'user': ['fullname', 'id', 'username'],
            },
        },
    },
    'contacts': {
        'add': {
            'contact': ['fullname', 'id', 'username'],
        },
        'delete': [],
        'getList': {
            'contacts': {
                'contact': ['fullname', 'id', 'username'],
            },
        },
    },
    'groups': {
        'add': {
            'group': ['id', 'name', {
                'contacts': [],
                },
            ],
        },
        'addContact': [],
        'delete': [],
        'getList': {
            'groups': {
                'group': ['id', 'name', {
                    'contact': ['id'],
                    },
                ],
            },
        },
        'removeContact': [],
    },
    'lists': {
        'add': _LIST_COMMON,
        'archive': _LIST_COMMON,
        'delete': _LIST_COMMON,
        'getList': {
            'lists': _LIST_COMMON,
        },
        'setDefaultList': [],
        'setName': _LIST_COMMON,
        'unarchive': _LIST_COMMON,
    },
    'locations': {
        'getList': {
            'locations': {
                'location': ['address', 'id', 'latitude', 'longitude',
                             'name', 'viewable', 'zoom'],
            },
        },
    },
    'push': {
        'getSubscriptions': {
            'subscriptions': _SUBSCRIPTION_COMMON,
        },
        'getTopics': {
            'topics': {
                'topic': [],
            },
        },
        'subscribe': _SUBSCRIPTION_COMMON,
        'unsubscribe': [],
    },
    'reflection': {
        'getMethodInfo': {
            'method': [
                'name', 'needslogin', 'needssigning', 'requiredperms',
                {
                    'description': [],
                },
                {
                    'response': [],
                },
                {
                    'arguments': {
                        'artument': ['name', 'optional'],
                    },
                },
                {
                    'errors': {
                        'error': ['code', 'message'],
                    },
                },
            ],
        },
        'getMethods': {
            'methods': {
                'method': [],
            },
        },
    },
    'scripts': {
        'add': _SCRIPT_COMMON,
        'delete': [],
        'getList': {
            'scripts': _SCRIPT_COMMON,
        },
        'run': {
            'execution': ['id'],
        },
        'setCode': _SCRIPT_COMMON,
        'setName': _SCRIPT_COMMON,
    },
    'settings': {
        'getList': {
            'settings': {
                'dateformat': [],
                'defaultlist': [],
                'language': [],
                'timeformat': [],
                'timezone': [],
            },
        },
    },
    'tags': {
        'getList': {
            'tags': {
                'tag': ['name'],
            },
        },
    },
    'tasks': {
        'add': _TASK_COMMON,
        'addTags': _TASK_TAGS,
        'complete': _TASK_COMMON,
        'delete': _TASK_COMMON,
        'getList': {
            'tasks': _TASK_COMMON,
        },
        'movePriority': _TASK_COMMON,
        'moveTo': _TASK_TAGS,
        'postpone': _TASK_COMMON,
        'removeTags': _TASK_TAGS,
        'setDueDate': _TASK_COMMON,
        'setEstimate': _TASK_COMMON,
        'setLocation': _TASK_COMMON,
        'setName': _TASK_COMMON,
        'setParentTask': _TASK_COMMON,
        'setPriority': _TASK_COMMON,
        'setRecurrence': _TASK_RRULE,
        'setStartDate': _TASK_COMMON,
        'setTags': _TASK_TAGS_RRULE,
        'setURL': _TASK_COMMON,
        'uncomplete': _TASK_COMMON,
    },
    'tasksNotes': {
        'add': {
            'note': ['created', 'id', 'modified', 'title'],
        },
        'delete': [],
        'edit': {
            'note': ['created', 'id', 'modified', 'title'],
        },
    },
    'test': {
        'echo': {
            'method': [],
        },
        'login': {
            'user': ["id", {
                "username": [],
                },
            ],
        },
    },
    'time': {
        'convert': {
            'time': ['timezone'],
        },
        'parse': {
            'time': ['precision'],
        },
    },
    'timelines': {
        'create': {
            'timeline': [],
        },
    },
    'timezones': {
        'getList': {
            'timezones': {
                'timezone': ['current_offset', 'dst', 'id', 'name', 'offset'],
            },
        },
    },
    'transactions': {
        'undo': [],
    },
}
