
timew.timewarrior module
************************

**class timew.timewarrior.TimeWarrior(bin='timew', simulate=False)**

   Bases: ``object``

   **annotate(id, annotation)**

      Add annotation to an existing interval

      :Parameters:
         *  **id** (*int*) – The Timewarrior id

         *  **annotation** (*str*) – Annotation text to be set

   **cancel()**

      If there is an open interval, it is abandoned.

   **cont(id)**

      Resumes tracking of closed intervals.

      :Parameters:
         **id** (*int*) – The Timewarrior id to be continued

   **delete(id)**

      Deletes an interval.

      :Parameters:
         **id** (*int*) – The Timewarrior id to be deleted

   **export(ids=None, start_time=None, end_time=None, tags=None)**

      export timewarrior entries by list of integer IDs, or with
      optional tags and for optional interval, default all entries in
      the database

      :Parameters:
         *  **intervals** (*list* [*int*], *optional*) – list of IDs
            to export, exclusive of other options

         *  **start_time** (*datetime*, *optional*) – start of
            interval to list entries for.

         *  **end_time** (*datetime*, *optional*) – end of interval to
            list entries for.

         *  **tags** (*list*, *optional*) – dump only events with
            matching tag(s)

      Returns a list of database entries formatted like the following:

      ::

         [{"id": 1, "start": "20190123T092300Z",
           "tags": ["watering new plants","gardening"]},
          {"id" : 2, "start": "20190123T085000Z", "end": "20190123T092256Z",
           "tags": ["helped plant roses","gardening"]}]

      the above contains a started (but not ended) entry with id=1;
      and an ended entry with id=2

   **join(id1, id2)**

      Joins two intervals, by using the earlier of the two start
      times, and the later of the two end times, and the combined set
      of tags.

      :Parameters:
         *  **id1** (*int*) – The first Timewarrior id to be joined

         *  **id2** (*int*) – The second Timewarrior id to be joined

   **lengthen(id, duration)**

      Defer the end date of a closed interval.

      :Parameters:
         *  **id** (*int*) – The Timewarrior id

         *  **duration** (*timew.Duration*) – The duration to lengthen
            the interval by

   **list(start_time=None, end_time=None)**

      export the timewarrior entries for interval

      :Parameters:
         *  **start_time** (*datetime*, *optional*) – start of
            interval to list entries for.

         *  **end_time** (*datetime*, *optional*) – start of interval
            to list entries for.

      Returns a list of database entries formatted like the following:

      ::

         [{"id": 1, "start": "20190123T092300Z",
           "tags": ["watering new plants","gardening"]},
          {"id" : 2, "start": "20190123T085000Z", "end": "20190123T092256Z",
           "tags": ["helped plant roses","gardening"]}]

      the above contains a started (but not ended) entry with id=1;
      and an ended entry with id=2

   **modify(start_or_end, id, time)**

      Changes the start or end of an interval.

      :Parameters:
         *  **start_or_end** (*str*) – “start” or “end”

         *  **id** (*int*) – The Timewarrior id

         *  **time** (*datetime*) – The new start or end time for the
            interval

   **move(id, time)**

      Reposition an interval at a new start time.

      :Parameters:
         *  **id** (*int*) – The Timewarrior id

         *  **time** (*datetime*) – The new start time for the
            interval

   **shorten(id, duration)**

      Advance the end date of a closed interval.

      :Parameters:
         *  **id** (*int*) – The Timewarrior id

         *  **duration** (*timew.Duration*) – The duration to shorten
            the interval by

   **split(id)**

      Splits an interval into two equally sized adjacent intervals,
      having the same tags.

      :Parameters:
         **id** (*int*) – The Timewarrior id to split

   **start(time=None, tags=None)**

      Begins tracking using the current time with any specified set of
      tags.

      :Parameters:
         *  **time** (*datetime*) – The time to start the interval

         *  **tags** (*list* [*str*]) – The list of tags to apply to
            the interval

   **stop(tags=None)**

      Stops tracking time. If tags are specified, then they are no
      longer tracked. If no tags are specified, all tracking stops.

      :Parameters:
         *  **tags** (*list*) – The Timewarrior id

         *  **tags** – The list of tags to stop tracking

   **summary(start_time=None, end_time=None)**

      export the timewarrior entries for interval

      :Parameters:
         *  **start_time** (*datetime*, *optional*) – start of
            interval to list entries for.

         *  **end_time** (*datetime*, *optional*) – start of interval
            to list entries for.

      Returns a list of database entries formatted like the following:

      ::

         [{"id": 1, "start": "20190123T092300Z",
           "tags": ["watering new plants","gardening"]},
          {"id" : 2, "start": "20190123T085000Z", "end": "20190123T092256Z",
           "tags": ["helped plant roses","gardening"]}]

      the above contains a started (but not ended) entry with id=1;
      and an ended entry with id=2

   **tag(id, tags)**

      Adds a tag to an interval.

      :Parameters:
         *  **id** (*int*) – The Timewarrior id

         *  **tags** (*list*) – The list of tags to add to the
            interval

   **track(start_time, end_time=None, tags=None)**

      The track command is used to add tracked time in the past.
         Perhaps you forgot to record time, or are just filling in old
         entries.

      :Parameters:
         *  **start_time** (*datetime*) – The task start time.

         *  **end_time** (*datetime*, *optional*) – The task end time.
            (required if duration not given)

         *  **duration** (*timew.Timedelta*, *optional*) – The task
            duration. (required if task not given)

         *  **tags** (*list* [*str*]) – The tags

      :Raises:
         **TimewarriorError** – Timew command errors

   **untag(id, tags)**

      Remove a tag from an interval

      :Parameters:
         *  **id** (*int*) – The Timewarrior id

         *  **tag** (*str*) – The tag to remove
