import numpy as np
import pandas as pd
run= pd.read_csv('Rinkesh_running.TXT',sep=',',names=['X','Y','Z'])
run1=pd.read_csv('Yash_running.TXT',sep=',',names=['X','Y','Z'])
run2=pd.read_csv('Ritesh_running.TXT',sep=',',names=['X','Y','Z'])
run3=pd.read_csv('Dhruv_running.TXT',sep=',',names=['X','Y','Z'])
run4=pd.read_csv('Sandeep_running.TXT',sep=',',names=['X','Y','Z'])
run5=pd.read_csv('Rohit_running.TXT',sep=',',names=['X','Y','Z'])
run6=pd.read_csv('Riya_running.TXT',sep=',',names=['X','Y','Z'])
run7=pd.read_csv('Sayan_running.TXT',sep=',',names=['X','Y','Z'])
run=pd.concat([run,run1,run2,run3,run4,run5,run6,run7])
lst=['Running']*6317
run['Result']=lst
walk= pd.read_csv('Rinkesh_walking.TXT',sep=',',names=['X','Y','Z'])
walk1=pd.read_csv('Yash_walking.TXT',sep=',',names=['X','Y','Z'])
walk2=pd.read_csv('Ritesh_walking.TXT',sep=',',names=['X','Y','Z'])
walk3=pd.read_csv('Dhruv_walking.TXT',sep=',',names=['X','Y','Z'])
walk4=pd.read_csv('Sandeep_walking.TXT',sep=',',names=['X','Y','Z'])
walk5=pd.read_csv('Rohit_walking.TXT',sep=',',names=['X','Y','Z'])
walk6=pd.read_csv('Riya_walking.TXT',sep=',',names=['X','Y','Z'])
walk7=pd.read_csv('Sayan_walking.TXT',sep=',',names=['X','Y','Z'])
walk=pd.concat([walk,walk1,walk2,walk3,walk4,walk5,walk6,walk7])
lst1=['Walking']*7924
walk['Result']=lst1
sit=pd.read_csv('Rinkesh_sitting.TXT',sep=',',names=['X','Y','Z'])
sit1=pd.read_csv('Yash_sitting.TXT',sep=',',names=['X','Y','Z'])
sit2=pd.read_csv('Ritesh_sitting.TXT',sep=',',names=['X','Y','Z'])
sit3=pd.read_csv('Dhruv_sitting.TXT',sep=',',names=['X','Y','Z'])
sit4=pd.read_csv('Sandeep_sitting.TXT',sep=',',names=['X','Y','Z'])
sit5=pd.read_csv('Rohit_sitting.TXT',sep=',',names=['X','Y','Z'])
sit6=pd.read_csv('Riya_sitting.TXT',sep=',',names=['X','Y','Z'])
sit7=pd.read_csv('Sayan_sitting.TXT',sep=',',names=['X','Y','Z'])
sit=pd.concat([sit,sit1,sit2,sit3,sit4,sit5,sit6,sit7])
lst2=['Resting']*11839
sit['Result']=lst2
lying=pd.read_csv('Rinkesh_lying.TXT',sep=',',names=['X','Y','Z'])
lying1=pd.read_csv('Yash_lying.TXT',sep=',',names=['X','Y','Z'])
lying2=pd.read_csv('Ritesh_lying.TXT',sep=',',names=['X','Y','Z'])
lying3=pd.read_csv('Dhruv_lying.TXT',sep=',',names=['X','Y','Z'])
lying4=pd.read_csv('Sandeep_lying.TXT',sep=',',names=['X','Y','Z'])
lying5=pd.read_csv('Rohit_lying.TXT',sep=',',names=['X','Y','Z'])
lying6=pd.read_csv('Riya_lying.TXT',sep=',',names=['X','Y','Z'])
lying7=pd.read_csv('Sayan_lying.TXT',sep=',',names=['X','Y','Z'])
lying=pd.concat([lying,lying1,lying2,lying3,lying4,lying5,lying6,lying7])
lst3=['Resting']*10616
lying['Result']=lst3
stand=pd.read_csv('Rinkesh_standing.TXT',sep=',',names=['X','Y','Z'])
stand1=pd.read_csv('Yash_standing.TXT',sep=',',names=['X','Y','Z'])
stand2=pd.read_csv('Ritesh_standing.TXT',sep=',',names=['X','Y','Z'])
stand3=pd.read_csv('Dhruv_standing.TXT',sep=',',names=['X','Y','Z'])
stand4=pd.read_csv('Sandeep_standing.TXT',sep=',',names=['X','Y','Z'])
stand5=pd.read_csv('Rohit_standing.TXT',sep=',',names=['X','Y','Z'])
stand6=pd.read_csv('Riya_standing.TXT',sep=',',names=['X','Y','Z'])
stand7=pd.read_csv('Sayan_standing.TXT',sep=',',names=['X','Y','Z'])
stand=pd.concat([stand,stand1,stand2,stand3,stand4,stand5,stand6,stand7])
lst4=['Resting']*10156
stand['Result']=lst4
merged=pd.concat([walk,run,sit,lying,stand])
from sklearn.preprocessing import StandardScaler
import joblib
scaler=StandardScaler()
scaler.fit(merged.drop('Result',axis=1))
joblib.dump(scaler,'Scaler.pkl')
scaled_feat=scaler.transform(merged.drop('Result',axis=1))
df=pd.DataFrame(scaled_feat,columns=merged.columns[:-1])
from sklearn.neighbors import KNeighborsClassifier
knn=KNeighborsClassifier(n_neighbors=26)
X=df
y=merged['Result']
knn.fit(X,y)
joblib.dump(knn,'Model.pkl')
print("Done")