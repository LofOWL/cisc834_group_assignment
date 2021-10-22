import os
import pandas as pd
import numpy as np
from lib.repository import Repository
from lib.Plot import Plot
from tqdm import tqdm

def repo_pachyderm_files():
    path = "./data/repository_files_short_listed_10.csv"
    df = pd.read_csv(path)
    repo_file = dict()
    for repository,file in np.array(df[['repository','files']]):
        each_file = file.split("\n") if "," not in file else file.split(",")
        filter_files = [file for file in each_file if "." in file]
        files = [file.split("/")[-1] for file in filter_files]
        repository = repository.split("/")[-1]
        repo_file[repository] = files
    return repo_file

def collect_LOS_Pachyderm(rp_files,rp_name):
    rp = Repository(path=f'/home/lofowl/Desktop/cisc834_group/mining/repositories/{rp_name}')
    pachyderm_files = rp_files[rp_name]
    files_commit = {file:[] for file in pachyderm_files}
    files_path = {file:[] for file in pachyderm_files}

    commits = rp.get_all_commits()
    for commit in commits:
        files = rp.get_commit_touch_files(commit)
        for file_path in files:
            file = file_path.split("/")[-1]
            if file in list(files_commit.keys()):
                files_commit[file] = files_commit.get(file) + [commit]
                files_path[file] = files_path.get(file) + [file_path]
    
    # finish files_commit
    # finish files_path
    files_count = {file:[] for file in pachyderm_files}
    for file,commits in files_commit.items():
        if len(commits) > 1:
            i,j = 0,1
            pathes = list(files_path.get(file))
            while j < len(commits):
                try:
                    count = rp.get_file_diff(commits[i],pathes[i],commits[j],pathes[j])
                    files_count[file] = files_count.get(file) +[count]
                except:
                    pass
                i += 1
                j += 1

    print(files_count)
    return (files_commit,files_path,files_count)

def merge(rp_files,rp_name):
    rp = Repository(path=f'/home/lofowl/Desktop/cisc834_group/mining/repositories/{rp_name}')
    pachyderm_files = rp_files[rp_name]
    commits = rp.get_all_commits()
    commits_file_count = {commit:[] for commit in commits}
    commits_count = {commit:[] for commit in commits}
    for commit in commits:
        rp.set_to_commit(commit)
        files = rp.get_all_files()
        #count python
        python_files = [file for file in files if ".py" in file]
        python_count = rp.get_LOC_files(python_files) if python_files else 0
        #count pachyderm
        pdh_files = [file for file in files if any(pf in file for pf in pachyderm_files)]
        pachyderm_count = rp.get_LOC_files(pdh_files) if pdh_files else 0
        commits_file_count[commit] = [len(python_files),len(pdh_files)]
        commits_count[commit] = [python_count,pachyderm_count]
    return commits_file_count,commits_count

def collect_LOS(rp_files,rp_name):
    rp = Repository(path=f'/home/lofowl/Desktop/cisc834_group/mining/repositories/{rp_name}')
    pachyderm_files = rp_files[rp_name]
    commits = rp.get_all_commits()
    commits_count = {commit:[] for commit in commits}
    for commit in commits:
        rp.set_to_commit(commit)
        files = rp.get_all_files()
        #count python
        python_files = [file for file in files if ".py" in file]
        python_count = rp.get_LOC_files(python_files) if python_files else 0
        #count pachyderm
        pdh_files = [file for file in files if any(pf in file for pf in pachyderm_files)]
        pachyderm_count = rp.get_LOC_files(pdh_files) if pdh_files else 0
        commits_count[commit] = [python_count,pachyderm_count]
    return commits_count


def collect_number_of_files(rp_files,rp_name):
    rp = Repository(path=f'/home/lofowl/Desktop/cisc834_group/mining/repositories/{rp_name}')
    pachyderm_files = rp_files[rp_name]
    commits = rp.get_all_commits()
    commits_count = {commit:[] for commit in commits}
    for commit in commits:
        rp.set_to_commit(commit)
        files = rp.get_all_files()
        #count python
        python_files = [file for file in files if ".py" in file]
        #count pachyderm
        phd_files = [file for file in files if any(pf in file for pf in pachyderm_files)]
        commits_count[commit] = [len(python_files),len(phd_files)]
    return commits_count

def files_add_delete_plot(files_count):
    pl = Plot()
    pl.plot(files_count)


if __name__ == "__main__":
    rp_files = repo_pachyderm_files()
    rp_names = list(rp_files.keys())
    for rp_name in tqdm(rp_names):
        cnof,clos = merge(rp_files,rp_name)
        pl = Plot()
        pl.plot_number_lines(cnof,clos,rp_name)

    