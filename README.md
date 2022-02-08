# Speedtest

Run a speedtest from the CLI and plot results.

Requires Python 3.6.


## Required Hack:

Until I decide to actually update speedtest-cli, apply this hack:

```diff
diff --git a/.venv-speedtest/lib/python3.6/site-packages/speedtest.py.bak b/.venv-speedtest/lib/python3.6/site-packages/speedtest.py
index cb4a374..22d90f2 100644
--- a/.venv-speedtest/lib/python3.6/site-packages/speedtest.py.bak
+++ b/.venv-speedtest/lib/python3.6/site-packages/speedtest.py
@@ -796,7 +796,7 @@ class Speedtest(object):
             client = get_attributes_by_tag_name(root, 'client')

         ignore_servers = list(
-            map(int, server_config['ignoreids'].split(','))
+            int(c) for c in server_config['ignoreids'].split(',') if c
         )

         ratio = int(upload['ratio'])
```

See https://github.com/sivel/speedtest-cli/commit/cadc68b5aef20f28648072cf07a8f155639b81dd


## Installation

1.  Make a venv: `python -m venv .venv-speedtest`.
    + It's recommended to use `pyenv` to set your python version to 3.6.
    + The venv **must** be called `.venv-speedtest`.
2.  `pip install -r requirements.txt`


## Running

Make sure to:

1. Set `run_speedtest.sh` to executable:

   ```
   chmod u+x run_speedtest.sh
   ```

2. Set up the cron task: (`/etc/crontab`)

   ```
   42 * * * * username /home/username/speedtest/run_speedtest.sh
   ```

3. Make the data file:

   ```
   speedtest --csv-headers > results.csv
   ```

