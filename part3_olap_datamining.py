import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, mean_squared_error, r2_score, classification_report, accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.svm import SVR, SVC
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
import warnings
warnings.filterwarnings('ignore')

print("=== PHAN 3. AP DUNG CONG CU / THUAT TOAN ===")
print("Dang tai du lieu sach...")

# Doc du lieu da duoc lam sach
df = pd.read_csv('data/clean/products_clean.csv')
print(f"Da tai {len(df):,} san pham tu du lieu sach")

# ========================================
# 3.1. KY THUAT OLAP / VISUALIZATION
# ========================================
print("\n3.1. KY THUAT OLAP / VISUALIZATION")
print("=" * 60)

# Tinh doanh thu (price × quantity_sold)
df['revenue'] = df['price'] * df['quantity_sold']
print(f"Da tinh doanh thu cho {len(df)} san pham")

# OLAP Query 1: Doanh thu trung binh theo brand
print("\n\nOLAP Query 1: Doanh thu trung binh theo brand")
revenue_by_brand = df.groupby('brand')['revenue'].agg(['mean', 'sum', 'count']).round(0)
revenue_by_brand.columns = ['Doanh_thu_TB', 'Tong_doanh_thu', 'So_san_pham']
top_brands = revenue_by_brand.sort_values('Tong_doanh_thu', ascending=False).head(10)
print(top_brands)

# OLAP Query 2: Trung binh rating_average theo fulfillment_type
print("\nOLAP Query 2: Trung binh rating theo fulfillment_type")
rating_by_fulfillment = df.groupby('fulfillment_type')['rating_average'].agg(['mean', 'count']).round(2)
rating_by_fulfillment.columns = ['Rating_TB', 'So_san_pham']
print(rating_by_fulfillment)

# OLAP Query 3: San pham duoc yeu thich nhat theo price_segment
print("\nOLAP Query 3: Favourite_count trung binh theo price_segment")
favourite_by_segment = df.groupby('price_segment')['favourite_count'].agg(['mean', 'sum', 'count']).round(1)
favourite_by_segment.columns = ['Favourite_TB', 'Tong_favourite', 'So_san_pham']
print(favourite_by_segment)

# Pivot Table: Doanh thu theo brand va fulfillment_type
print("\nPivot Table: Doanh thu theo brand va fulfillment_type (Top 5 brands)")
top5_brands = df.groupby('brand')['revenue'].sum().nlargest(5).index
df_top5 = df[df['brand'].isin(top5_brands)]
pivot_revenue = df_top5.pivot_table(
    values='revenue', 
    index='brand', 
    columns='fulfillment_type', 
    aggfunc='sum', 
    fill_value=0
).round(0)
print(pivot_revenue)

print("\nDang tao bieu do OLAP...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('PHAN TICH OLAP - BUSINESS INTELLIGENCE', fontsize=16, fontweight='bold', y=1.08)

# 1. Bar chart: Top 10 thuong hieu co doanh thu cao nhat
top_10_brands = df.groupby('brand')['revenue'].sum().nlargest(10)
axes[0, 0].bar(range(len(top_10_brands)), top_10_brands.values, color='skyblue')
axes[0, 0].set_title('Top 10 Thuong hieu - Tong Doanh thu', fontweight='bold')
axes[0, 0].set_xlabel('Thuong hieu')
axes[0, 0].set_ylabel('Doanh thu (VND)')
axes[0, 0].tick_params(axis='x', rotation=45)
axes[0, 0].set_xticks(range(len(top_10_brands)))
axes[0, 0].set_xticklabels(top_10_brands.index, rotation=45, ha='right')

# 2. Scatter plot: Gia vs Rating vs So luong ban
scatter = axes[0, 1].scatter(df['price']/1000, df['rating_average'], 
                           s=df['quantity_sold']*2, alpha=0.6, c=df['revenue']/1000, cmap='viridis')
axes[0, 1].set_title('Gia vs Rating (size=quantity, color=revenue)', fontweight='bold')
axes[0, 1].set_xlabel('Gia (nghin VND)')
axes[0, 1].set_ylabel('Rating Average')
plt.colorbar(scatter, ax=axes[0, 1], label='Revenue (nghin VND)')

# 3. Boxplot: Rating theo fulfillment_type
fulfillment_data = [df[df['fulfillment_type'] == ft]['rating_average'].values 
                   for ft in df['fulfillment_type'].unique()]
fulfillment_labels = df['fulfillment_type'].unique()
axes[1, 0].boxplot(fulfillment_data, labels=fulfillment_labels)
axes[1, 0].set_title('So sanh Rating theo Fulfillment Type', fontweight='bold')
axes[1, 0].set_xlabel('Fulfillment Type')
axes[1, 0].set_ylabel('Rating Average')
axes[1, 0].tick_params(axis='x', rotation=45)

# 4. Doanh thu theo price_segment
segment_revenue = df.groupby('price_segment')['revenue'].sum()
axes[1, 1].pie(segment_revenue.values, labels=segment_revenue.index, autopct='%1.1f%%', startangle=90)
axes[1, 1].set_title('Phan bo Doanh thu theo Price Segment', fontweight='bold')

plt.tight_layout()
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('data/clean/olap_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print("Da luu bieu do OLAP: 'data/clean/olap_analysis.png'")

# ========================================
# 3.2. KY THUAT DATA MINING
# ========================================
print("\n3.2. KY THUAT DATA MINING - CLUSTERING")
print("=" * 60)

# Chuan bi du lieu cho clustering
print("\nChuan bi du lieu cho clustering...")
clustering_features = ['price', 'rating_average', 'quantity_sold', 'favourite_count']
X = df[clustering_features].copy()
X = X.fillna(0)  # Thay the NaN bang 0

print("Thong ke du lieu truoc khi chuan hoa:")
print(X.describe().round(2))

# Chuan hoa du lieu
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("Da chuan hoa du lieu bang StandardScaler")

# Tim so cluster toi uu bang Silhouette Score
print("\nTim so cluster toi uu:")
silhouette_scores = []
K_range = range(2, 8)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    cluster_labels = kmeans.fit_predict(X_scaled)
    silhouette_avg = silhouette_score(X_scaled, cluster_labels)
    silhouette_scores.append(silhouette_avg)
    print(f"   K={k}: Silhouette Score = {silhouette_avg:.3f}")

# Chon K tot nhat
best_k = K_range[np.argmax(silhouette_scores)]
print(f"\nSo cluster toi uu: K = {best_k} (Silhouette Score = {max(silhouette_scores):.3f})")

# Thuc hien clustering voi K toi uu
final_kmeans = KMeans(n_clusters=best_k, random_state=42)
df['cluster'] = final_kmeans.fit_predict(X_scaled)

print(f"\nPhan bo cluster:")
cluster_counts = df['cluster'].value_counts().sort_index()
for cluster, count in cluster_counts.items():
    print(f"   Cluster {cluster}: {count:,} san pham ({count/len(df)*100:.1f}%)")

# Mo ta tung cluster
print(f"\nMO TA CAC CLUSTER:")
print("=" * 50)

cluster_summary = df.groupby('cluster')[clustering_features + ['revenue']].agg(['mean', 'median']).round(0)

for i in range(best_k):
    cluster_data = df[df['cluster'] == i]
    print(f"\nCLUSTER {i} ({len(cluster_data):,} san pham):")
    print(f"   Gia TB: {cluster_data['price'].mean():,.0f} VND")
    print(f"   Rating TB: {cluster_data['rating_average'].mean():.2f}")
    print(f"   So luong ban TB: {cluster_data['quantity_sold'].mean():.1f}")
    print(f"   Favourite TB: {cluster_data['favourite_count'].mean():.1f}")
    print(f"   Doanh thu TB: {cluster_data['revenue'].mean():,.0f} VND")
    
    # Dac diem cluster
    if cluster_data['price'].mean() < df['price'].mean():
        if cluster_data['rating_average'].mean() < df['rating_average'].mean():
            print(f"   Dac diem: San pham GIA RE, RATING THAP, ban it")
        else:
            print(f"   Dac diem: San pham GIA RE, RATING TOT, gia tri tot")
    else:
        if cluster_data['rating_average'].mean() > df['rating_average'].mean():
            print(f"   Dac diem: San pham CAO CAP, RATING CAO, chat luong premium")
        else:
            print(f"   Dac diem: San pham TAM TRUNG, rating trung binh")

print(f"\nDang tao bieu do Data Mining...")

# Tao figure cho Data Mining visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('PHAN TICH DATA MINING - CLUSTERING', fontsize=16, fontweight='bold')

# 1. Scatter plot: Price vs Quantity_sold voi mau theo cluster
colors = plt.cm.tab10(np.linspace(0, 1, best_k))
for i in range(best_k):
    cluster_data = df[df['cluster'] == i]
    axes[0, 0].scatter(cluster_data['price']/1000, cluster_data['quantity_sold'], 
                      c=colors[i], label=f'Cluster {i}', alpha=0.6)
axes[0, 0].set_title('Gia vs So luong ban (theo Cluster)', fontweight='bold')
axes[0, 0].set_xlabel('Gia (nghin VND)')
axes[0, 0].set_ylabel('So luong ban')
axes[0, 0].legend()

# 2. Bieu do cot: Rating trung binh theo cluster
cluster_rating = df.groupby('cluster')['rating_average'].mean()
axes[0, 1].bar(cluster_rating.index, cluster_rating.values, color=colors)
axes[0, 1].set_title('Rating trung binh theo Cluster', fontweight='bold')
axes[0, 1].set_xlabel('Cluster')
axes[0, 1].set_ylabel('Rating Average')

# 3. Bieu do cot: Gia trung binh theo cluster
cluster_price = df.groupby('cluster')['price'].mean()
axes[1, 0].bar(cluster_price.index, cluster_price.values/1000, color=colors)
axes[1, 0].set_title('Gia trung binh theo Cluster', fontweight='bold')
axes[1, 0].set_xlabel('Cluster')
axes[1, 0].set_ylabel('Gia (nghin VND)')

# 4. Scatter plot 3D-like: Price vs Rating voi size theo quantity_sold
for i in range(best_k):
    cluster_data = df[df['cluster'] == i]
    axes[1, 1].scatter(cluster_data['price']/1000, cluster_data['rating_average'], 
                      s=cluster_data['quantity_sold']*3, c=colors[i], 
                      label=f'Cluster {i}', alpha=0.6)
axes[1, 1].set_title('Gia vs Rating (size=quantity)', fontweight='bold')
axes[1, 1].set_xlabel('Gia (nghin VND)')
axes[1, 1].set_ylabel('Rating Average')
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('data/clean/clustering_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print("Da luu bieu do Clustering: 'data/clean/clustering_analysis.png'")

# Luu ket qua clustering
df.to_csv('data/clean/products_with_clusters.csv', index=False, encoding='utf-8')
print("Da luu du lieu co cluster: 'data/clean/products_with_clusters.csv'")

# ========================================
# 3.3. DU DOAN VA PHAN TICH NANG CAO
# ========================================
print("\n3.3. DU DOAN VA PHAN TICH NANG CAO")
print("=" * 60)

# Chuan bi du lieu cho machine learning
print("\nChuan bi du lieu cho Machine Learning...")

# Tao cac bien phu thuoc cho du doan
df['price_category'] = pd.cut(df['price'], bins=4, labels=['Gia_thap', 'Gia_TB', 'Gia_cao', 'Gia_rat_cao'])
df['revenue_per_item'] = df['revenue'] / (df['quantity_sold'] + 1)  # Tranh chia cho 0

# Encode categorical variables
le_brand = LabelEncoder()
le_category = LabelEncoder()
le_seller = LabelEncoder()

df['brand_encoded'] = le_brand.fit_transform(df['brand'].astype(str))
df['category_encoded'] = le_category.fit_transform(df['category'].astype(str))
df['seller_encoded'] = le_seller.fit_transform(df['current_seller'].astype(str))

# Tao features cho ML
features_for_ml = ['price', 'rating_average', 'review_count', 'quantity_sold', 'brand_encoded', 
                   'category_encoded', 'seller_encoded', 'discount_rate']
X_ml = df[features_for_ml].fillna(0)

print(f"Features cho ML: {len(features_for_ml)} features")
print(f"So mau du lieu: {len(X_ml)}")

# ========================================
# 3.3.1. DU DOAN DOANH THU (REVENUE PREDICTION)
# ========================================
print("\n3.3.1. DU DOAN DOANH THU - ADVANCED REGRESSION MODELS")
print("-" * 55)

y_revenue = df['revenue']
X_train_rev, X_test_rev, y_train_rev, y_test_rev = train_test_split(
    X_ml, y_revenue, test_size=0.2, random_state=42
)

# Chuan hoa du lieu
scaler_rev = StandardScaler()
X_train_rev_scaled = scaler_rev.fit_transform(X_train_rev)
X_test_rev_scaled = scaler_rev.transform(X_test_rev)

print("Training cac mo hinh du doan doanh thu...")

# Dictionary luu ket qua cac model
revenue_models = {}
revenue_scores = {}

# Model 1: Random Forest
rf_rev = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
rf_rev.fit(X_train_rev, y_train_rev)
rf_pred = rf_rev.predict(X_test_rev)
revenue_models['Random Forest'] = rf_rev
revenue_scores['Random Forest'] = {
    'R2': r2_score(y_test_rev, rf_pred),
    'RMSE': np.sqrt(mean_squared_error(y_test_rev, rf_pred))
}

# Model 2: Gradient Boosting
gb_rev = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
gb_rev.fit(X_train_rev, y_train_rev)
gb_pred = gb_rev.predict(X_test_rev)
revenue_models['Gradient Boosting'] = gb_rev
revenue_scores['Gradient Boosting'] = {
    'R2': r2_score(y_test_rev, gb_pred),
    'RMSE': np.sqrt(mean_squared_error(y_test_rev, gb_pred))
}

# Model 3: Neural Network (MLP)
mlp_rev = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=1000, random_state=42)
mlp_rev.fit(X_train_rev_scaled, y_train_rev)
mlp_pred = mlp_rev.predict(X_test_rev_scaled)
revenue_models['Neural Network'] = mlp_rev
revenue_scores['Neural Network'] = {
    'R2': r2_score(y_test_rev, mlp_pred),
    'RMSE': np.sqrt(mean_squared_error(y_test_rev, mlp_pred))
}

# Model 4: Support Vector Regression
svr_rev = SVR(kernel='rbf', C=100, gamma=0.001)
svr_rev.fit(X_train_rev_scaled, y_train_rev)
svr_pred = svr_rev.predict(X_test_rev_scaled)
revenue_models['Support Vector'] = svr_rev
revenue_scores['Support Vector'] = {
    'R2': r2_score(y_test_rev, svr_pred),
    'RMSE': np.sqrt(mean_squared_error(y_test_rev, svr_pred))
}

# Model 5: K-Nearest Neighbors
knn_rev = KNeighborsRegressor(n_neighbors=5)
knn_rev.fit(X_train_rev_scaled, y_train_rev)
knn_pred = knn_rev.predict(X_test_rev_scaled)
revenue_models['K-Neighbors'] = knn_rev
revenue_scores['K-Neighbors'] = {
    'R2': r2_score(y_test_rev, knn_pred),
    'RMSE': np.sqrt(mean_squared_error(y_test_rev, knn_pred))
}

print("\nKET QUA DU DOAN DOANH THU:")
for model_name, scores in revenue_scores.items():
    print(f"{model_name:15}: R2 = {scores['R2']:.3f}, RMSE = {scores['RMSE']:,.0f}")

# Tim model tot nhat
best_model_name = max(revenue_scores.keys(), key=lambda x: revenue_scores[x]['R2'])
print(f"\nMo hinh tot nhat cho du doan doanh thu: {best_model_name}")

# Feature importance (Random Forest)
feature_importance = pd.DataFrame({
    'feature': features_for_ml,
    'importance': rf_rev.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTAM QUAN TRONG CUA FEATURES:")
for _, row in feature_importance.head(5).iterrows():
    print(f"   {row['feature']:20}: {row['importance']:.3f}")

# ========================================
# 3.3.2. PHAN LOAI SAN PHAM (CLASSIFICATION)
# ========================================
print("\n3.3.2. PHAN LOAI SAN PHAM - ADVANCED CLASSIFICATION")
print("-" * 50)

# Tao target cho classification (rating categories)
df['rating_class'] = pd.cut(df['rating_average'], 
                           bins=[-0.1, 0, 2, 4, 5], 
                           labels=['Khong_danh_gia', 'Thap', 'Trung_binh', 'Cao'])

y_class = df['rating_class'].fillna('Khong_danh_gia')
X_train_cls, X_test_cls, y_train_cls, y_test_cls = train_test_split(
    X_ml, y_class, test_size=0.2, random_state=42, stratify=y_class
)

X_train_cls_scaled = scaler_rev.fit_transform(X_train_cls)
X_test_cls_scaled = scaler_rev.transform(X_test_cls)

print("Training cac mo hinh phan loai...")

# Dictionary luu ket qua classification
class_models = {}
class_scores = {}

# Classification Model 1: Random Forest
rf_cls = RandomForestClassifier(n_estimators=100, random_state=42)
rf_cls.fit(X_train_cls, y_train_cls)
rf_cls_pred = rf_cls.predict(X_test_cls)
class_models['Random Forest'] = rf_cls
class_scores['Random Forest'] = accuracy_score(y_test_cls, rf_cls_pred)

# Classification Model 2: Neural Network
mlp_cls = MLPClassifier(hidden_layer_sizes=(50, 25), max_iter=1000, random_state=42)
mlp_cls.fit(X_train_cls_scaled, y_train_cls)
mlp_cls_pred = mlp_cls.predict(X_test_cls_scaled)
class_models['Neural Network'] = mlp_cls
class_scores['Neural Network'] = accuracy_score(y_test_cls, mlp_cls_pred)

# Classification Model 3: Support Vector Machine
svm_cls = SVC(kernel='rbf', random_state=42)
svm_cls.fit(X_train_cls_scaled, y_train_cls)
svm_cls_pred = svm_cls.predict(X_test_cls_scaled)
class_models['Support Vector'] = svm_cls
class_scores['Support Vector'] = accuracy_score(y_test_cls, svm_cls_pred)

# Classification Model 4: K-Nearest Neighbors
knn_cls = KNeighborsClassifier(n_neighbors=7)
knn_cls.fit(X_train_cls_scaled, y_train_cls)
knn_cls_pred = knn_cls.predict(X_test_cls_scaled)
class_models['K-Neighbors'] = knn_cls
class_scores['K-Neighbors'] = accuracy_score(y_test_cls, knn_cls_pred)

print("\nKET QUA PHAN LOAI RATING:")
for model_name, score in class_scores.items():
    print(f"{model_name:15}: Accuracy = {score:.3f}")

best_class_model = max(class_scores.keys(), key=lambda x: class_scores[x])
print(f"\nMo hinh tot nhat cho phan loai: {best_class_model}")

# ========================================
# 3.3.3. CUSTOMER LIFETIME VALUE & MARKET BASKET ANALYSIS
# ========================================
print("\n3.3.3. CUSTOMER LIFETIME VALUE & BUSINESS INSIGHTS")
print("-" * 50)

# Tinh CLV dua tren cluster
cluster_metrics = df.groupby('cluster').agg({
    'revenue': ['mean', 'sum', 'count'],
    'rating_average': 'mean',
    'quantity_sold': ['mean', 'sum'],
    'price': 'mean'
}).round(2)

cluster_metrics.columns = ['Revenue_Mean', 'Revenue_Sum', 'Customer_Count', 
                          'Avg_Rating', 'Qty_Mean', 'Qty_Sum', 'Price_Mean']

# Tinh CLV Score
cluster_metrics['CLV_Score'] = (
    cluster_metrics['Revenue_Mean'] * 
    cluster_metrics['Avg_Rating'] * 
    cluster_metrics['Qty_Mean'] / 1000
).round(0)

print("\nCUSTOMER LIFETIME VALUE BY CLUSTER:")
for i, row in cluster_metrics.iterrows():
    print(f"Cluster {i}: CLV = {row['CLV_Score']:8.0f}, Customers = {row['Customer_Count']:4.0f}, "
          f"Avg Revenue = {row['Revenue_Mean']:10,.0f}")

# Brand Performance Analysis
brand_performance = df.groupby('brand').agg({
    'revenue': 'sum',
    'rating_average': 'mean',
    'quantity_sold': 'sum',
    'id': 'count'
}).round(2)
brand_performance.columns = ['Total_Revenue', 'Avg_Rating', 'Total_Quantity', 'Product_Count']
brand_performance = brand_performance.sort_values('Total_Revenue', ascending=False)

print("\nTOP 5 BRANDS PERFORMANCE:")
for brand, row in brand_performance.head(5).iterrows():
    print(f"{brand:15}: Revenue = {row['Total_Revenue']:12,.0f}, Rating = {row['Avg_Rating']:.2f}, "
          f"Products = {row['Product_Count']:3.0f}")

# ========================================
# 3.3.4. VISUALIZATION CHO ADVANCED ANALYTICS
# ========================================
print("\n3.3.4. ADVANCED ANALYTICS VISUALIZATION")
print("-" * 45)

fig, axes = plt.subplots(3, 2, figsize=(16, 18))
fig.suptitle('MACHINE LEARNING & PREDICTIVE ANALYTICS', fontsize=16, fontweight='bold')

# 1. Model Performance Comparison (Revenue)
models = list(revenue_scores.keys())
r2_scores = [revenue_scores[m]['R2'] for m in models]
axes[0, 0].bar(models, r2_scores, color=['red', 'green', 'blue', 'orange', 'purple'])
axes[0, 0].set_title('Model Performance - Revenue Prediction (R2)', fontweight='bold')
axes[0, 0].set_ylabel('R2 Score')
axes[0, 0].tick_params(axis='x', rotation=45)

# 2. Classification Accuracy Comparison
class_names = list(class_scores.keys())
class_acc = list(class_scores.values())
axes[0, 1].bar(class_names, class_acc, color=['darkred', 'darkgreen', 'darkblue', 'darkorange'])
axes[0, 1].set_title('Classification Accuracy Comparison', fontweight='bold')
axes[0, 1].set_ylabel('Accuracy')
axes[0, 1].tick_params(axis='x', rotation=45)

# 3. Feature Importance
axes[1, 0].barh(feature_importance.head(6)['feature'], 
               feature_importance.head(6)['importance'], color='coral')
axes[1, 0].set_title('Feature Importance (Random Forest)', fontweight='bold')
axes[1, 0].set_xlabel('Importance')

# 4. Actual vs Predicted Revenue (Best Model)
best_model = revenue_models[best_model_name]
if best_model_name in ['Neural Network', 'Support Vector', 'K-Neighbors']:
    best_pred = best_model.predict(X_test_rev_scaled)
else:
    best_pred = best_model.predict(X_test_rev)

axes[1, 1].scatter(y_test_rev, best_pred, alpha=0.5, color='green')
axes[1, 1].plot([y_test_rev.min(), y_test_rev.max()], 
               [y_test_rev.min(), y_test_rev.max()], 'r--', lw=2)
axes[1, 1].set_title(f'Actual vs Predicted Revenue ({best_model_name})', fontweight='bold')
axes[1, 1].set_xlabel('Actual Revenue')
axes[1, 1].set_ylabel('Predicted Revenue')

# 5. CLV by Cluster
axes[2, 0].bar(cluster_metrics.index, cluster_metrics['CLV_Score'], color='purple', alpha=0.7)
axes[2, 0].set_title('Customer Lifetime Value by Cluster', fontweight='bold')
axes[2, 0].set_xlabel('Cluster')
axes[2, 0].set_ylabel('CLV Score')

# 6. Brand Revenue Distribution (Top 10)
top_brands = brand_performance.head(10)
axes[2, 1].pie(top_brands['Total_Revenue'], labels=top_brands.index, 
              autopct='%1.1f%%', startangle=90)
axes[2, 1].set_title('Revenue Distribution - Top 10 Brands', fontweight='bold')

plt.tight_layout()
plt.savefig('data/clean/advanced_analytics.png', dpi=300, bbox_inches='tight')
plt.show()

print("Da luu bieu do Advanced Analytics: 'data/clean/advanced_analytics.png'")

# Luu ket qua ML
ml_results = pd.DataFrame({
    'Model_Type': ['Regression'] * len(revenue_scores) + ['Classification'] * len(class_scores),
    'Model_Name': list(revenue_scores.keys()) + list(class_scores.keys()),
    'Score': [revenue_scores[m]['R2'] for m in revenue_scores.keys()] + list(class_scores.values()),
    'Metric': ['R2'] * len(revenue_scores) + ['Accuracy'] * len(class_scores)
})
ml_results.to_csv('data/clean/ml_results.csv', index=False)
print("Da luu ket qua ML: 'data/clean/ml_results.csv'")

# Luu CLV results
cluster_metrics.to_csv('data/clean/cluster_clv_analysis.csv')
print("Da luu phan tich CLV: 'data/clean/cluster_clv_analysis.csv'")

print(f"\nTONG KET PHAN 3 NANG CAO:")
print("=" * 50)
print("OLAP: Da phan tich doanh thu, rating theo brand/fulfillment/segment")
print("Data Mining: Da phan cum san pham thanh cac nhom chien luoc")
print("Machine Learning: Da xay dung 5 mo hinh du doan doanh thu")
print("Classification: Da xay dung 4 mo hinh phan loai rating")
print("Predictive Analytics: Da tinh toan Customer Lifetime Value")
print("Business Intelligence: Da phan tich hieu suat thuong hieu")
print("Advanced Visualization: Da tao dashboard ML hoan chinh")
print(f"Mo hinh tot nhat - Revenue: {best_model_name} (R2={revenue_scores[best_model_name]['R2']:.3f})")
print(f"Mo hinh tot nhat - Classification: {best_class_model} (Acc={class_scores[best_class_model]:.3f})")
print("San sang cho bao cao va de xuat chien luoc kinh doanh nang cao!")