import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import numpy as np

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

df = pd.read_csv("atp3.csv", index_col=6, sep=',', decimal=".")
df = df.dropna(axis=0)
df2 = df.infer_objects()

# le = LabelEncoder()
# df2 = df2.apply(le.fit_transform)

nominal_data = ["p1_main_hand", "p2_main_hand", "court_type", "court_base" ]
df2 = pd.get_dummies(df2,columns=nominal_data)

print(df2)

#
# input = ["ranking_diff", "age_diff", "weight_diff", "height_diff", "p1_main_hand_Ambidextrous",
# "p1_main_hand_Left-Handed", "p1_main_hand_Right-Handed", "p2_main_hand_Left-Handed", "p2_main_hand_Right-Handed",
# "court_type_I", "court_type_O", "court_base_Carpet", "court_base_Clay", "court_base_Hard"]
# output = "result"
#
# x_train, x_test, y_train, y_test = train_test_split(df2[input], df2[output], test_size=0.25, random_state=789)
#
# dt = DecisionTreeClassifier()
# dt.fit(x_train, y_train)
#
# print(dt.predict(np.array([6, 8, 3, 18, 2, 1, 1, 1]).reshape(1, -1))) # 1
# print(dt.predict(np.array([5, 5, 8, 3, 2, 1, 1, 1]).reshape(1, -1))) # 0