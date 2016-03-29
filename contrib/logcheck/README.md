# logcheck ruleset

logcheck is a simple and effective log monitoring tool checking for known and
unknown patterns in the logfiles. The given rules do ignore all messages with
loglevels INFO and DEBUG, and parts of tracebacks. ERROR and CRITICAL are
treated as violations, WARNINGS are thus normal irregular log messages.
