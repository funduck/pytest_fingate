"""Скрипт управления Fingate
Нужен, чтобы тестам было кого дёргать и чтобы в Fingate были данные"""

import os
import sys
import time
from db import cursor

class WarmupError(Exception):
    pass

class WarmupTimeoutError(WarmupError):
    pass

def warmup(uploads, backups, timeout=30):
    """Exports tables with data from database to Fingate files
    Then waits until files are loaded
    If timeout is exceeded then raises WarmupTimeoutError"""

    wait_files = {}
    evac_files = {}

    for data in [
        {
        'table': "Accounts",
        'filetype': "accounts",
        'fields': ['account','terminal_device_id','imsi','msisdn','account_closed','terminal_device_closed','date_from','date_to','deleted','load_id','marketing_category_id','contract_closed','customer_id','contract_number','service_provider_id']
        }
        ]:
        billings = {}

        with cursor() as cur:
            cur.execute(f"SELECT * FROM public.\"{data['table']}\"")
            for record in cur:
                rows = []
                if record['billing'] in billings:
                    rows = billings[record['billing']]
                else:
                    billings[record['billing']] = rows

                line = ''
                for field in data['fields']:
                    line = line + f",\"{record[field]}\""
                rows.append(f"[{line[1:]}]")

        print("Test data:", billings)

        for b in billings:
            fname = f"warmup_MR{b}_{data['filetype']}_2000-01-01"
            wait_files[fname] = True
            evac_files[fname] = True

            for failed_file in [uploads + '/' + fname + '.gz', backups + '/' + fname + '.gz']:
                if os.path.exists(failed_file):
                    print("Found .gz file, removing", failed_file)
                    os.remove(failed_file)

            print(f"Put file {fname} to uploads: {uploads}")
            f = open(uploads + '/' + fname + '.csv', 'w')
            f.write(';'.join(data['fields']))
            f.write('\n')

            for l in billings[b]:
                f.write(l)
                f.write('\n')
 
            f.close()

    print("Waiting for files to be loaded...")

    done = False
    step = 1
    while done is False and timeout > 0:
        time.sleep(step)
        #print(timeout)
        timeout -= step
        done = True
        for fname in wait_files:
            if wait_files[fname] is False:
                continue
            if os.path.exists(uploads + '/' + fname + '.csv') or os.path.exists(uploads + '/' + fname + '.load'):
                done = False
            else:
                if os.path.exists(uploads + '/' + fname + '.gz') or os.path.exists(backups + '/' + fname + '.gz'):
                    print(f"File {fname} load failed")
                    sys.exit(1)
                print(f"File {fname} loaded")
                wait_files[fname] = False

    if done is True:
        print("\033[92m", "Success! All files loaded", "\033[0m")
        return
    else:
        print("\033[91m", "Failure! Warmup timed out. Not loaded:", wait_files, "\033[0m")
        raise WarmupTimeoutError

def clear():
    """Clear Fingate databases"""
    # TODO
    pass
