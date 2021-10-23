import sys
import pandas as pd
import math
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelBinarizer, LabelEncoder

def main():
	args = sys.argv[1:]
	if len(args) != 2:
		print("well thats just not ok")
	train = pd.read_csv(args[0], header=None)
	test = pd.read_csv(args[1], header=None)
	test_x = pd.DataFrame(test.iloc[:, :-1])
	y = pd.DataFrame(test.iloc[:, -1])
	test_x = test_x.apply(LabelEncoder().fit_transform)
	y = y.apply(LabelEncoder().fit_transform).to_numpy()
	t_y = pd.DataFrame(train.iloc[:, -1]).apply(LabelEncoder().fit_transform).to_numpy()

	y_preds = {}
	t_y_preds = {}


	for j in range(2, 501):
		for i in range(1, j):
			train_sample = train.sample(frac=1.0, replace=True).reset_index(drop=True)
			train_x = pd.DataFrame(train_sample.iloc[:, :-1])
			train_y = pd.DataFrame(train_sample.iloc[:, -1])
			train_x = train_x.apply(LabelEncoder().fit_transform)
			train_y = train_y.apply(LabelEncoder().fit_transform)

			tree = DecisionTreeClassifier(max_features = 4)
			tree.fit(train_x, train_y)
			preds = tree.predict(test_x)
			t_preds = tree.predict(train_x)
			for i in range(len(preds)):
				if i in y_preds.keys():
					y_preds[i].append(preds[i])
				else:
					y_preds[i] = []
					y_preds[i].append(preds[i])
			for i in range(len(t_preds)):
				if i in t_y_preds.keys():
					t_y_preds[i].append(t_preds[i])
				else:
					t_y_preds[i] = []
					t_y_preds[i].append(t_preds[i])
		train_correct = 0
		test_correct = 0
		for i in range(test.shape[0]):
			if most_common(y_preds.get(i)) == y[i]:
				test_correct += 1
		for i in range(train.shape[0]):
			if most_common(t_y_preds.get(i)) == t_y[i]:
				train_correct += 1
		print("| " + str(j-1) + "             | " + str(test_correct / test.shape[0]) + " | " + str(train_correct / train.shape[0]))
		y_preds.clear()
		t_y_preds.clear()

def most_common(lst):
    return max(set(lst), key=lst.count)


if __name__ == "__main__":
    main()