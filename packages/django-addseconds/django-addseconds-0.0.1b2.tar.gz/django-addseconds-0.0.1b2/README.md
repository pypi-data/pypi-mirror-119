[![Build Status](https://api.travis-ci.com/nnseva/django-addseconds.svg?branch=master)](https://travis-ci.com/github/nnseva/django-addseconds)

# Django AddSeconds

The [Django AddSeconds](https://github.com/nnseva/django-addseconds) package provides a number
of useful Django template filters for datetime manipulations.

## Installation

*Stable version* from the PyPi package repository
```bash
pip install django-addseconds
```

*Last development version* from the GitHub source version control system
```
pip install git+git://github.com/nnseva/django-addseconds.git
```

## Configuration

Include the `addseconds` application into the `INSTALLED_APPS` list, like:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    ...
    'addseconds',
    ...
]
```

## Using

Load the library into your template:
```
{% load addseconds %}
```

Use provided template filters as described in the Django documentation.

## Template Filters provided

### addseconds

Adds passed number of seconds to the datetime value, for example:
```
{% load addseconds %}
{{ value|addseconds:3600 }}
```

*Notice* that the `value` passed to the template may be `datetime` value, `date` value, `float`, `int`, or `str`,
all of them are converted to the `datetime`. The `date` value is converted to the `datetime` at midnight.
The `float` or `int` value is converted as a unixtime. The `str` value is converted using
`django.utils.dateparse.parse_datetime` call.

*Notice* that the template filter argument may be `float` as well as `int`.

### parse_datetime

Calls `django.utils.dateparse.parse_datetime`

```
{% load addseconds %}
{{ "2011-11-01 12:13"|parse_datetime }}
```

### parse_date

Calls `django.utils.dateparse.parse_date`

```
{% load addseconds %}
{{ "2011-11-01"|parse_date }}
```

### parse_time

Calls `django.utils.dateparse.parse_time`

```
{% load addseconds %}
{{ "12:13"|parse_time }}
```
