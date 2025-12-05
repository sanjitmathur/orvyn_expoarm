#.\.venv\Scripts\Activate.ps1
#python ML_Python.py

import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

print("Generating dummy data...")

X_rest = np.random.rand(100, 4) * 10 
y_rest = np.zeros(100)

X_fist = np.random.rand(100, 4) * 50 + 40
y_fist = np.ones(100)

X_ext = np.random.rand(100, 4) * 30 + 10
y_ext = np.full(100, 2)

X = np.concatenate((X_rest, X_fist, X_ext))
y = np.concatenate((y_rest, y_fist, y_ext))

clf = svm.SVC(kernel='linear', decision_function_shape='ovr')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
clf.fit(X_train, y_train)

print(f"Model Accuracy: {accuracy_score(y_test, clf.predict(X_test)) * 100:.2f}%")

print("\n--- COPY THE CODE BELOW INTO YOUR TEENSY SKETCH ---\n")

weights = clf.coef_
intercept = clf.intercept_

print(f"// Number of Classes: {len(clf.classes_)}")
print(f"// Number of Features: {weights.shape[1]}")

print("float svm_weights[NUM_CLASSES][NUM_FEATURES] = {")
for i, row in enumerate(weights):
    line = "    {" + ", ".join([f"{w:.4f}" for w in row]) + "}"
    if i < len(weights) - 1:
        line += ","
    print(line)
print("};")

print("float svm_bias[NUM_CLASSES] = {")
line = "    " + ", ".join([f"{b:.4f}" for b in intercept])
print(line)
print("};")