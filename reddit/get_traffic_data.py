
import time
import datetime
import json
import pickle
import praw


def execute_every(f, wait, max_count=10):
    starttime = time.time()
    i = 0
    while i < max_count:
        i += 1
        print("[+] tick {}".format(i))
        try:
            f()
        except:
            print('something went wrong')
        time.sleep(wait - ((time.time()-starttime) % wait))
    print("[+] done!")

def get_reddit():
    with open('credentials.json', 'r') as f:
        creds = json.load(f)
    reddit = praw.Reddit(**creds)
    return reddit

class DataGetter(object):
    def __init__(self, reddit, subreddit='politics', post_count=2):
        self.reddit = reddit
        self.subreddit = subreddit
        self.post_count=post_count
        self.ids, self.post_info = self.get_new_post_ids()
        self.data = {}

    def get_new_post_ids(self):
        sub = self.reddit.subreddit(self.subreddit)
        new = sub.new()
        new_list = [next(new) for _ in range(self.post_count)]
        ids = [s.id for s in new_list]
        info = {s.id: 
                    {
                        'title': s.title,
                        'author': s.author,
                        'domain': s.domain,
                        'url': s.url,
                        'created_time': s.created
                    }
                    for s in new_list}
        return ids, info

    def get_submission_data_now(self):
        t = time.time()
        dt = datetime.datetime.fromtimestamp(t)
        dt = dt.replace(microsecond=0, second=0)
        dtstr = dt.strftime('%x-%X')
        print('  [+] getting submission data for {}'.format(dt))
        def grab_data(sid):
            s = self.reddit.submission(id=sid)
            data = {
                    'score': s.score,
                    'upvotes': s.ups,
                    'downvotes': s.downs,
                    'num_comments': s.num_comments,
                    'num_reports': s.num_reports,
                    'view_count': s.view_count
                    }
            return data
        data = {sid: grab_data(sid) for sid in self.ids}
        self.data[dtstr] = data
        print('  [+] done!')
                    
    def get_submission_data(self, wait=300, count=(12*24)):
        execute_every(self.get_submission_data_now, wait, count)

def get_a_whole_bunch():
    dg = DataGetter(reddit=get_reddit(), post_count=100)
    dg.get_submission_data(wait=300, count=(12*8))
    # dg.get_submission_data(wait=3, count=2)
    with open('data.p', 'wb') as f:
        pickle.dump(dg.data, f)
    with open('data.json', 'w') as f:
        json.dump(dg.data, f)



if __name__ == '__main__':
    # create a new reddit instance if it doesn't already exist
    # get_a_whole_bunch()
    try:    reddit
    except: reddit = get_reddit()

    # dg = DataGetter(reddit=reddit)



