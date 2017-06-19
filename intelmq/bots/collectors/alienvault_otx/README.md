- Install the library from GitHub, as there is no package in PyPi:
  ```language
  pip install -r REQUIREMENTS.txt
   ```
** Runtime Parameter Configuration
    - "api_key": register on the website to get one
    - "modified_pulses_only": get only modified pulses instead of all, set to it to true or false, default false
    - "interval": if "modified_pulses_only" is set, define the time in hours (integer value) to get modified pulse since then, default 24 hours