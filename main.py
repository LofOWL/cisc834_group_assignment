from lib import Repository
from lib import ResearchQuestion
import os
import pandas as pd
from tqdm import tqdm


def all():
    # repositories = os.listdir("repositories")
    data = list()
    repositories = ['cpsign-service-management']
    for repository in tqdm(repositories):
        rp = Repository(path="/home/lofowl/Desktop/cisc834_group/mining/repositories/"+repository)
        RQ = ResearchQuestion(rp)
        print(f"done {repository}")
        data.append([repository,RQ.RQ1_1(),RQ.RQ1_2(),RQ.RQ1_3(),RQ.RQ1_4(),RQ.RQ2_1(),RQ.RQ2_2(),RQ.RQ2_3(),RQ.RQ2_4(),RQ.RQ3_1()])
    df = pd.DataFrame(data=data,columns=["repository","RQ1_1","RQ1_2","RQ1_3","RQ1_4","RQ2_1","RQ2_2","RQ2_3","RQ2_4","RQ3_1"])
    df.to_csv("/home/lofowl/Desktop/cisc834_group/mining/data3.csv",index=False)

if __name__ == "__main__":
    all()