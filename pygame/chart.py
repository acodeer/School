import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

# 1. 데이터 불러오기
df = pd.read_csv('Ai3Data/Data/Iris2.csv')
df['class'] = df['class'].astype(int)  # 혹시 문자열이면 정수형으로 변환

# 2. 특징 선택 (petal_length, petal_width만 사용)
X = df[['petal_length', 'petal_width']].values
y = df['class'].values

# 3. 모델 정의
models = {
    "KNN (k=5)": KNeighborsClassifier(n_neighbors=5),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "SVM (RBF)": SVC(kernel='rbf', random_state=42)
}

# 4. 결정 경계 시각화용 설정
x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                     np.arange(y_min, y_max, 0.02))

# 5. 그래프 출력
plt.figure(figsize=(18, 5))
cmap = plt.cm.Set1

for i, (name, model) in enumerate(models.items(), 1):
    # 모델 학습
    model.fit(X, y)

    # 예측 수행 (결정 경계용)
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # 그래프 출력
    plt.subplot(1, 3, i)
    plt.contourf(xx, yy, Z, alpha=0.3, cmap=cmap)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap, edgecolor='k')
    plt.title(name)
    plt.xlabel('Petal Length (cm)')
    plt.ylabel('Petal Width (cm)')

plt.suptitle("Iris Data - Decision Boundaries by Different Models", fontsize=15)
plt.tight_layout()
plt.show()
