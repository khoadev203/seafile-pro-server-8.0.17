
## Pubfile

To add pubfile app, in the local_settings.py

    EXTRA_INSTALLED_APPS = (
        ...
        "seahub_extra.pubfile",
        ...
    )
    ENABLE_PUBFILE = True
    
## Search

To add pubfile app, in the local_settings.py

    EXTRA_INSTALLED_APPS = (
        ...
        "seahub_extra.search",
        ...
    )

## Plan & Pay 

Install `dateutil`

    sudo pip install python-dateutil

To add pay app, in the local_settings.py

    EXTRA_INSTALLED_APPS = (
        ...
        'seahub_extra.pay',
        'seahub_extra.plan',
        'paypal.standard.ipn',
        ...
    )
    
    EXTRA_MIDDLEWARE_CLASSES = (
        ...
        'seahub_extra.plan.middleware.PlanMiddleware',
        ...
    )

    PLAN = {
    'Free': {
        'desc': 'Free',
        'storage': 1,           # GB
        'share_link_traffic': 5, # GB/month
        'num_of_groups': 3,
        'group_members': 6,
        },
    'A': {
        'desc': 'Small Team',
        'storage': 100,           # GB
        'share_link_traffic': 100, # GB/month
        'num_of_groups': 8,
        'group_members': 16,
        'pricing': 10,          # $/month
        },
    'B': {
        'desc': 'Large Team',
        'storage': 500,           # GB
        'share_link_traffic': 500, # GB/month
        'num_of_groups': -1,      # no limit
        'group_members': -1,      # no limit
        'pricing': 50,            # $/month
        },
    }
    PAYPAL_RECEIVER_EMAIL = "seafile2012-facilitator@gmail.com"
    ENABLE_PAYMENT = True


Copyright (c) 2012-2016 Seafile Ltd.
