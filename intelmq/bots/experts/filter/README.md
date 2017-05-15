# Filter Bot

The filter bot is capable of filtering specific events.

## Parameters for filtering with key/value attributes:
* `filter_key` - key from data harmonization
* `filter_value` - value for the key
* `filter_action` - action when a message match to the criteria (possible actions: keep/drop)
* `filter_regex` - attribute determines if the `filter_value` shall be treated as regular expression or not.
   If this attribute is not empty, the bot uses python's "search" function to evaluate the filter.

## Parameters for time based filtering:
* `not_before` - events before this time will be dropped
* `not_after` - events after this time will be dropped

Both parameters accept string values describing absolute or relative time:
* absolute
 * basically anything parseable by datetime parser, eg. "2015-09-012T06:22:11+00:00"
 * `time.source` taken from the event will be compared to this value to decide the filter behavior
* relative
 * accepted string formatted like this "<integer> <epoch>", where epoch could be any of following strings (could optionally end with trailing 's'): hour, day, week, month, year
 * time.source taken from the event will be compared to the value (now - relative) to decide the filter behavior

Examples of time filter definition:
* ```"not_before" : "2015-09-012T06:22:11+00:00"``` events older than the specified time will be dropped
* ```"not_after" : "6 months"``` just events older than 6 months will be passed through the pipeline

