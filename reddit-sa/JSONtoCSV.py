import csv
import json
# -*- coding: utf-8 -*-
import sys
import codecs

sys.stdout = codecs.getwriter("iso-8859-1")(sys.stdout, 'xmlcharrefreplace')

#do for each month of year
x = open(r"RC_2009-12.json")
f = csv.writer(open(r"december.csv", "w+", newline=''))

#{"distinguished":null,"id":"7va4","edited":false,"archived":true,"created_utc":"1230768007","gilded":0,"ups":-5,"author":"KiddieFiddler","downs":0,"score":-5,"controversiality":0,"subreddit":"pics","parent_id":"t1_7shm","author_flair_css_class":null,"score_hidden":false,"retrieved_on":1428222113,"link_id":"t3_7mmkw","author_flair_text":null,"subreddit_id":"t5_2qh0u","name":"t1_7va4","body":"**Nigger + Obama. Jailbait + bestof** etc etc"}
i=0
for ln in x.readlines():
    js = json.loads(ln)
    if "[deleted]" not in ln:
        f.writerow([js["id"], js["subreddit"], js["subreddit_id"], js["parent_id"], js["author"], js["created_utc"], js["score"], js["body"].replace('\r\n', ' ').encode("cp437", "ignore")])

