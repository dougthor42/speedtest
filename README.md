# Speedtest

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

