import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn as sk

df = pd.read_csv('Ai3Data/data/iris2.csv')
print(df.head(5))
print(df.info())

df_class_0 = df[df['class'] == 0]
df_class_1 = df[df['class'] == 1]
df_class_2 = df[df['class'] == 2]

# 학습 데이터 (30개씩)
train_0 = df_class_0.head(30)
train_1 = df_class_1.head(30)
train_2 = df_class_2.head(30)

# 테스트 데이터 (20개씩)
test_0 = df_class_0.tail(20)
test_1 = df_class_1.tail(20)
test_2 = df_class_2.tail(20)

model = {
    'KNN': sk.neighbors.KNeighborsClassifier(),
    'DecisionTree': sk.tree.DecisionTreeClassifier(),
    'SVM': sk.svm.SVC()
}

train_data = pd.concat([train_0, train_1, train_2])
test_data = pd.concat([test_0, test_1, test_2])
X_train = train_data.drop('class', axis=1)
y_train = train_data['class']
X_test = test_data.drop('class', axis=1)
y_test = test_data['class']

for name, clf in model.items():
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy = sk.metrics.accuracy_score(y_test, y_pred)
    print(f"{name} 정확도: {accuracy:.4f}")

# 산점도 그리기 (테스트 데이터만)
plt.figure(figsize=(12, 5))

# 1️⃣ Sepal Length vs Width
plt.subplot(1, 2, 1)
scatter1 = plt.scatter(
    df['sepal_length'],
    df['sepal_width'],
    c=df['class'],
    cmap='viridis'
)
plt.title('Sepal Length vs Sepal Width (Test Data)')
plt.xlabel('Sepal Length (cm)')
plt.ylabel('Sepal Width (cm)')
plt.legend(*scatter1.legend_elements(), title='Class')

# 2️⃣ Petal Length vs Width
plt.subplot(1, 2, 2)
scatter2 = plt.scatter(
    df['petal_length'],
    df['petal_width'],
    c=df['class'],
    cmap='viridis'
)
plt.title('Petal Length vs Petal Width (Test Data)')
plt.xlabel('Petal Length (cm)')
plt.ylabel('Petal Width (cm)')
plt.legend(*scatter2.legend_elements(), title='Class')

plt.tight_layout()
plt.savefig('iris_test_scatter_plots.png')
plt.close()

#실제 값 vs 예측 값 비교
print("\n===== 모델별 예측 비교 =====\n")

predictions = {}
for name, clf in model.items():
    predictions[name] = clf.predict(X_test)

print("Idx\tKNN\tAct\tDT\tAct\tSVM\tAct")
print("-" * 50)

for idx in range(len(y_test)):
    actual = y_test.iloc[idx]
    knn_pred = predictions['KNN'][idx]
    dt_pred = predictions['DecisionTree'][idx]
    svm_pred = predictions['SVM'][idx]

    print(f"{idx}\t{knn_pred}\t{actual}\t{dt_pred}\t{actual}\t{svm_pred}\t{actual}")



