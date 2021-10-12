import os
import subprocess

class Repository:

    def __init__(self,path,**args):
        if not path:
            print("wrong")
        self.path = path

    def setAddress(self):
        os.chdir(self.path)

    def refresh(self):
        self.setAddress()
        os.system("git checkout master")

    def set_to_commit(self,commit):
        self.setAddress()
        os.system(f"git checkout -f {commit}")

    def get_commit_diff(self,commits):
        command = f"git show {commits}"
        data = subprocess.getoutput(command)
        return data

    def get_all_relate_files(self,arg):
        self.setAddress()
        # command = "grep -Rnw --include=\*.json --include=\*.yaml . -e 'pfs'"
        command = f"grep -Rnw . -e '{arg}'"
        data = subprocess.getoutput(command)
        list_data = data.split("\n")
        files = list()
        for data in list_data:
            file = data.split(":")[0]
            if file not in files:
                files.append(file)
        return set(files)

    # get touch of files in a commit
    def get_touch_files(self,commit):
        self.setAddress()
        data = subprocess.check_output(['git','show',commit,'--name-only','--format="%H"']).decode("utf-8").split("\n")[1:]
        clean_data = [ele for ele in data if len(ele)]
        return clean_data

    # get the commit message
    def get_commit_message(self,commit):
        self.setAddress()
        # git log --format=%B -n 1
        message = subprocess.check_output(['git','log','-n','1',f'--format="%B"',commit]).decode("utf-8")
        return message

    # get all commits 
    def get_git_commits(self):
        self.setAddress()
        data = subprocess.check_output(['git', 'log', '--format=%H']).decode('utf-8').strip()
        split_commit_message = [data for data in data.split("\n") if len(data)]
        return split_commit_message

    # get all files in current snapshot
    def get_all_files(self):
        # git ls-files
        self.setAddress()
        data = subprocess.check_output(['git','ls-files']).decode('utf-8').strip()
        return data.split("\n")

    def get_commit_date(self,commit):
        # git show -s --format=%ci <commit>
        data = subprocess.getoutput(f"git show -s --format=%ci {commit}")
        return data

if __name__ == "__main__":
    repositories = os.listdir("repositories")
    index = 2
    print(repositories[index])
    rp = Repository(path="/home/lofowl/Desktop/cisc834_group/mining/repositories/"+repositories[index])

    files = rp.get_relate_files('pfs')
    print(len(files))