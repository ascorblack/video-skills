# Delivering the sound, keys and spending [Audio]

## How to deliver the sound

- Attach the file, an address for listening and the measurements: duration, loudness, peak, timecodes of events.
- Write honestly if you did not listen yourself and relied only on measurements.
- Do not delete or replace earlier versions: every new version is a new file.

## Keys and spending on generation

- Read the key only into the process that calls the API. Never print it, do not write it into logs, files and reports. Check the results by searching for the characteristic prefix of the key.
- Count the spending by the accounting, not from memory: other people could have used the same key. The budget ceiling must be checked in code before each generation.
- The file with keys must be excluded from version control. Check this, do not take it on trust.
