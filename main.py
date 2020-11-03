import pandas as pd

results = pd.read_csv("presidential_results.csv")
states = pd.read_csv("states.csv")

distr = pd.DataFrame(results.loc[results.year==2016].groupby("state").candidatevotes.sum())
distr["elector"] = None

for i,r in states.iterrows():
    try:
        distr["elector"].at[r.state] = r.electors
    except:
        pass
distr["elector"].at["District of Columbia"] = 3

vote_per_seat = distr.apply(lambda x: x.candidatevotes/x.elector, axis=1).sort_values()

n = 0
bad_state = []
while n <= distr.elector.sum()//2:
    state = str(vote_per_seat.index[0])
    bad_state.append(state)
    vote_per_seat.drop(state, inplace=True)
    n += distr.elector[state]

min_voters_needed = distr.loc[bad_state].candidatevotes.sum()/distr.candidatevotes.sum()

res = results.loc[results.year==2016]
a = res.loc[[c in ['Trump, Donald J.', 'Clinton, Hillary'] for c in res.candidate]].groupby(by=["state", "candidate"]).candidatevotes.sum()

distr["winner"] = ''
distr["margin"] = 0.0
for s in distr.index:
    distr.at[s, "winner"] = a[s].idxmax()
    distr.at[s, "margin"] = a[s].max()/(a[s].min()+a[s].max())
