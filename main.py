import requests
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Github activity parser")
    parser.add_argument("-u", "--user", nargs="+", metavar="user", type=str)
    parser.add_argument("-t", "--token", nargs="+", metavar="token", type=str)
    args = parser.parse_args()
    return args


def get_request(user, token):
    request = requests.get(f"https://api.github.com/users/{user}/events",
                           headers={"Authorization": token})
    if request.status_code == 200:
        return request
    else:
        print("Error: Site returned", request.status_code)
        quit()


args = get_args()
try:
    user = args.user[0]
except TypeError:
    print("Error: User must be specified")
    quit()
    
if args.token is None:
    token = None
else:
    token = args.token[0]
request = get_request(user, token)

user_events = request.json()
for events in user_events:
    repo = events["repo"]["url"]
    payload = events["payload"]
    
    match events["type"]:
        case "CommitCommentEvent":
            print(f"- created a commit comment in {repo}")
        case "CreateEvent":
            print(f"- created {payload["ref_type"]} in {repo}")
        case "DeleteEvent":
            print(f"- deleted {payload["ref_type"]} in {repo}")
        case "ForkEvent":
            print(f"- forked {repo}")
        case "GollumEvent":
            print(f"- created a wiki in {repo}")
        case "IssueCommentEvent":
            print(f"- {payload["action"]} the issue in {repo}")    
        case "IssuesEvent":
            print(f"- {payload["action"]} the issue in {repo}")
        case "MemberEvent": 
            print(f"- {payload["member"]} {payload["action"]} to {repo}")
        case "PublicEvent":
            print(f"- made {repo} public")
        case "PullRequestEvent":
            if payload["action"] == "review_requested":
                print(f"- requested review for pull request {payload["number"]} in {repo}")
            elif payload["action"] == "review_request_removed":
                print(f"- review request for pull request {payload["number"]} removed in {repo}")
            else:
                print(f"- {payload["action"]} {payload["number"]} pull request in {repo}")
        case "PullRequestReviewEvent":
            print(f"- {payload["action"]} pull request review in {repo}")
        case "PullRequestCommentEvent":
            print(f"- {payload["action"]} pull request review comment in {repo}")
        case "PullRequestReviewThreadEvent":
            print(f"- marked {payload["thread"]} as {payload["action"]} in {repo}")
        case "PushEvent":
            print(f"- pushed (id: {payload["push_id"]}) {payload["size"]} commit(s) in {repo}")
        case "ReleaseEvent":
            print(f"- {payload["action"]} in {repo}")
        case "SponsorshipEvent":
            print(f"- {payload["action"]} in {repo}")
        case "WatchEvent":
            print(f"- {payload["action"]} in {repo}")
