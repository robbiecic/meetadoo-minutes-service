# NoteIt-Minutes-API

# - Add Minute
# - Get a specific minute
# - Get My Minute History including those im tagged in


# Will need to tag the person creating it by email address
# Will need to add the datetime of the meeting
# Will need to add the participants
# - Tag Participants - will return an the user name if exists, other will just tag their email
#
# - Archive/Close Minute
# - Create Minute Action
# - Complete Minute Action
# - Cancel Minute Action


# Potential Data Model
# Meeting ID
# Date of meeting
# Creator
# Tagged people - array
# Title
# Sub Title
# Body
# Attachments
# Actions: Array of Object [1 - {Creator, Assignee, Task, Open/Closed}, 2 - {Creator, Assignee, Task, Open/Closed} ]
