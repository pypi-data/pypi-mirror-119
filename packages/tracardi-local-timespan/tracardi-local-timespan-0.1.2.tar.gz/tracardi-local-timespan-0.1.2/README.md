# Tracardi plugin

This code can be run within Tracardi workflow.

# Local time span action

The purpose of this plugin is to check if the local time is within 
defined time span.

This action minds the time zone to the event. Therefore, you must provide 
time zone. By default, time zone is included in browser event context. 


# Configuration

This node requires configuration. In order to read timezone 
you must define path to time zone. Use dot notation to do that.

Moreover, you need to set start and end of the time span. The time slots 
have no default values. 

Example of the configuration:

```json
{
  "timezone": "session@context.time.tz",
  "start": "12:00:00",
  "end": "14:00:00"
}
```

# Input payload

This node does not process input payload.

# Output

Return True or False. Return True if local time is in defined time span.