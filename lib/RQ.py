from lib.repository import Repository
from datetime import datetime

def relate_count(commits,*args):
    relate_commits = 0
    for commit in commits:
        try:
            for arg in args:
                if arg in commit[0]:
                    print(commit[0])
                    relate_commits += 1
                    break
        except:
            pass
    return relate_commits

def get_related_commits_date(self):
    self.rp.refresh()
    commits = self.rp.get_git_commits()
    touch_commits = list()
    for commit in commits:
        self.rp.set_to_commit(commit)
        files = self.rp.get_all_relate_files("pfs")
        if len(files) != 0:
            touch_commits.append(commit)
    
    date_commits = [self.rp.get_commit_date(commit)[:-6] for commit in touch_commits]
    date_commits = [datetime.strptime(date,"%Y-%m-%d %H:%M:%S") for date in  date_commits]
    return date_commits

class ResearchQuestion:

    def __init__(self,repo:Repository):
        self.rp = repo

    def RQ1_1(self):
        # Number of pachyderm-related commits
        # generalfusion-pachyderm: 0
        # yellow-pachyderm: 3
        self.rp.refresh()
        commits = self.rp.get_git_commits()
        related_commits = list()
        for commit in commits:
            diff = self.rp.get_commit_diff(commit).split("\n")
            ifTouch = False
            for lines in diff:
                if any(arg in lines.lower() for arg in ['+','-']) and any(keyword in lines.lower() for keyword in ['pachyderm','pfs']):
                    related_commits.append(commit)
                    ifTouch = True
                    break
                if ifTouch: break
        return len(related_commits)

    def RQ1_2(self):
        # Total number of merge PRs
        # generalfusion-pachyderm PRs: 0
        # yellow-pachyderm: 0
        self.rp.refresh()
        commits = self.rp.get_git_commits()
        merge_commits = list()
        for commit in commits:
            message = self.rp.get_commit_message(commit)
            if "merge pull request" in message.lower():
                merge_commits.append(commit)
        return len(merge_commits)

    def RQ1_3(self):
        # Number of pachyderm-related files
        # generalfusion-pachyderm : 3
        # yellow-pachyderm : 2
        files = self.rp.get_all_relate_files('pfs')
        return len(files)

    def RQ1_4(self):

        # Total number of files
        # generalfusion-pachyderm : 23
        # yellow-pachyderm : 14
        return len(self.rp.get_all_files())

    def RQ2_1(self):
        # Number of days of pachyderm usage
        # generalfusion-pacyhderm : 
        # yellow-pachyderm : 
        date_commits = get_related_commits_date(self)
        date_commits.sort()
        usage_date = date_commits[-1] - date_commits[1]
        return usage_date.days
        


    def RQ2_2(self):
        # Number of days between creation of repository and adoption of pachyderm
        # generalfusion-pacyhderm :
        # yellow-pachyderm :   
        
        commits = self.rp.get_git_commits()
        date_commits = get_related_commits_date(self)
        date_commits.sort()

        commits = [self.rp.get_commit_date(commit)[:-6] for commit in commits]
        commits = [datetime.strptime(date,"%Y-%m-%d %H:%M:%S") for date in commits]
        commits.sort()
        return (date_commits[0] - commits[0]).days

    def RQ2_3(self):
        # Number of days between release of pachyderm and adoption into repository
        # generalfusioni-pachyderm : 
        # yellow-pachyderm :
        release_date = datetime.strptime("2014-11-29 00:00:00","%Y-%m-%d %H:%M:%S")
        date_commits = get_related_commits_date(self)
        date_commits.sort()

        return (date_commits[0] - release_date).days

    def RQ2_4(self):
        # Percentage of Pachyderm commits 
        # generalfusion-pachyderm: 0%
        # yellow-pachyderm: 13%
        self.rp.refresh()
        commits = self.rp.get_git_commits()

        related_commits = list()
        for commit in commits:
            diff = self.rp.get_commit_diff(commit).split("\n")
            ifTouch = False
            for lines in diff:
                if any(arg in lines.lower() for arg in ['+','-']) and any(keyword in lines.lower() for keyword in ['pachyderm','pfs']):
                    related_commits.append(commit)
                    ifTouch = True
                    break
                if ifTouch: break
        
        return len(related_commits)/len(commits)

    def RQ3_1(self):
        # All Bug Commit Message
        self.rp.refresh()
        commits = self.rp.get_git_commits()
        fix_bug_commits = list()
        for commit in commits:
            message = self.rp.get_commit_message(commit)
            for arg in ["fix","bug"]:
                if arg in message.lower():
                    fix_bug_commits.append(commit)
                    break
        
        relate_bug_commit = list()
        for commit in fix_bug_commits:
            diff = self.rp.get_commit_diff(commit).split("\n")
            ifTouch = False
            for lines in diff:
                if any(arg in lines.lower() for arg in ['+','-']) and any(keyword in lines.lower() for keyword in ['pachyderm','pfs']):
                    relate_bug_commit.append(commit)
                    ifTouch = True
                    break
                if ifTouch: break
        
        return len(relate_bug_commit)
            


    def __str__(self):
        return f'''{self.rp.path}\nRQ1.1 Number of pachyderm-related commits:{self.RQ1_1()}
        \nRQ1.2 Total number of merged PRs:{self.RQ1_2()}
        \nRQ1.3 Number of pachyderm-related files:{self.RQ1_3()}
        \nRQ1.4 Total number of files:{self.RQ1_4()}
        \nRQ2.1 Number of days of pachyderm usage:{self.RQ2_1()}
        \nRQ2.2 Number of days between creation of repository and adoption of pachyderm:{self.RQ2_2()}
        \nRQ2.3 Number of days between release of pachyderm and adoption into repository:{self.RQ2_3()}
        \nRQ2.4 Percentage of Pachyderm commits:{self.RQ2_4()}
        \nRQ3.1 Number of related bug commits:{self.RQ3_1()}'''
