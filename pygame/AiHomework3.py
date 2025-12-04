import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import numpy as np

# 1. Pandas dataframe 객체로 읽어들인다.
df = pd.read_csv('Ai3Data/Data/Iris2.csv')

# 2. 데이터를 출력한다.
print("--- 데이터 확인 (상위 5개 행) ---")
print(df.head())
print("\n--- 데이터 정보 ---")
df.info()

# 3. Matplotlib을 사용하여 산점도를 2개 이상 그린다.
# 각 클래스 별로 색깔을 다르게 표시한다.
plt.figure(figsize=(12, 5))

# 산점도 1: sepal_length vs sepal_width
plt.subplot(1, 2, 1)
scatter1 = plt.scatter(df['sepal_length'], df['sepal_width'], c=df['class'], cmap='viridis')
plt.title('Sepal Length vs Sepal Width by Class')
plt.xlabel('Sepal Length (cm)')
plt.ylabel('Sepal Width (cm)')
plt.legend(*scatter1.legend_elements(), title='Class')

# 산점도 2: petal_length vs petal_width
plt.subplot(1, 2, 2)
scatter2 = plt.scatter(df['petal_length'], df['petal_width'], c=df['class'], cmap='viridis')
plt.title('Petal Length vs Petal Width by Class')
plt.xlabel('Petal Length (cm)')
plt.ylabel('Petal Width (cm)')
plt.legend(*scatter2.legend_elements(), title='Class')

plt.tight_layout()
plt.savefig('iris_scatter_plots.png')
plt.close()

# 4. Pandas를 사용하여 데이터를 분리 및 병합한다.
# 각 클래스 별로 50개 중 30개는 학습 데이터로, 20개는 테스트 데이터로 사용한다.

# 클래스별로 데이터를 분리
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

# 학습 데이터 및 테스트 데이터 병합
df_train = pd.concat([train_0, train_1, train_2])
df_test = pd.concat([test_0, test_1, test_2])

# 특성과 타겟 변수 분리
features = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
X_train = df_train[features]
y_train = df_train['class']
X_test = df_test[features]
y_test = df_test['class']

print("\n--- 학습 데이터 크기 ---")
print(f"총 샘플 수: {len(X_train)} (Class 0: {len(train_0)}, Class 1: {len(train_1)}, Class 2: {len(train_2)})")
print("\n--- 테스트 데이터 크기 ---")
print(f"총 샘플 수: {len(X_test)} (Class 0: {len(test_0)}, Class 1: {len(test_1)}, Class 2: {len(test_2)})")

# 5. scikit-learn을 사용하여 3개 이상의 기계 학습 알고리즘을 적용하고 정확도를 비교한다.
models = {
    "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Support Vector Machine (RBF)": SVC(random_state=42)
}

accuracy_results = {}

print("\n--- 기계 학습 모델 학습 및 정확도 확인 ---")
for name, model in models.items():
    # 학습 데이터로 학습
    model.fit(X_train, y_train)

    # 테스트 데이터로 정확도 확인
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    accuracy_results[name] = accuracy
    print(f"{name}: 정확도 = {accuracy:.4f}")

print("\n--- 정확도 비교 ---")
for name, accuracy in accuracy_results.items():
    print(f"{name}: {accuracy:.4f}")

# 정확도 결과를 DataFrame으로 변환 및 저장
results_df = pd.DataFrame(accuracy_results.items(), columns=['Model', 'Accuracy'])
results_df_sorted = results_df.sort_values(by='Accuracy', ascending=False)

print("\n--- 정렬된 정확도 결과 ---")
print(results_df_sorted)

# 결과 CSV 저장
results_df_sorted.to_csv('iris_ml_accuracy_results.csv', index=False)