# ========================================
# PHẦN 3. ÁP DỤNG CÔNG CỤ / THUẬT TOÁN
# ========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

print("=== PHẦN 3. ÁP DỤNG CÔNG CỤ / THUẬT TOÁN ===")
print("Đang tải dữ liệu sạch...")

# Đọc dữ liệu đã được làm sạch
df = pd.read_csv('data/clean/products_clean.csv')
print(f"✅ Đã tải {len(df):,} sản phẩm từ dữ liệu sạch")

# ========================================
# 3.1. KỸ THUẬT OLAP / VISUALIZATION
# ========================================
print("\n📊 3.1. KỸ THUẬT OLAP / VISUALIZATION")
print("=" * 60)

# Tính doanh thu (price × quantity_sold)
df['revenue'] = df['price'] * df['quantity_sold']
print(f"✅ Đã tính doanh thu cho {len(df)} sản phẩm")

# OLAP Query 1: Doanh thu trung bình theo brand
print("\n\n OLAP Query 1: Doanh thu trung bình theo brand")
revenue_by_brand = df.groupby('brand')['revenue'].agg(['mean', 'sum', 'count']).round(0)
revenue_by_brand.columns = ['Doanh_thu_TB', 'Tong_doanh_thu', 'So_san_pham']
top_brands = revenue_by_brand.sort_values('Tong_doanh_thu', ascending=False).head(10)
print(top_brands)

# OLAP Query 2: Trung bình rating_average theo fulfillment_type
print("\n⭐ OLAP Query 2: Trung bình rating theo fulfillment_type")
rating_by_fulfillment = df.groupby('fulfillment_type')['rating_average'].agg(['mean', 'count']).round(2)
rating_by_fulfillment.columns = ['Rating_TB', 'So_san_pham']
print(rating_by_fulfillment)

# OLAP Query 3: Sản phẩm được yêu thích nhất theo price_segment
print("\n❤️ OLAP Query 3: Favourite_count trung bình theo price_segment")
favourite_by_segment = df.groupby('price_segment')['favourite_count'].agg(['mean', 'sum', 'count']).round(1)
favourite_by_segment.columns = ['Favourite_TB', 'Tong_favourite', 'So_san_pham']
print(favourite_by_segment)

# Pivot Table: Doanh thu theo brand và fulfillment_type
print("\n📋 Pivot Table: Doanh thu theo brand và fulfillment_type (Top 5 brands)")
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

print("\n📈 Đang tạo biểu đồ OLAP...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('📊 PHÂN TÍCH OLAP - BUSINESS INTELLIGENCE', fontsize=16, fontweight='bold', y=1.08)

# 1. Bar chart: Top 10 thương hiệu có doanh thu cao nhất
top_10_brands = df.groupby('brand')['revenue'].sum().nlargest(10)
axes[0, 0].bar(range(len(top_10_brands)), top_10_brands.values, color='skyblue')
axes[0, 0].set_title('Top 10 Thương hiệu - Tổng Doanh thu', fontweight='bold')
axes[0, 0].set_xlabel('Thương hiệu')
axes[0, 0].set_ylabel('Doanh thu (VNĐ)')
axes[0, 0].tick_params(axis='x', rotation=45)
axes[0, 0].set_xticks(range(len(top_10_brands)))
axes[0, 0].set_xticklabels(top_10_brands.index, rotation=45, ha='right')

# 2. Scatter plot: Giá vs Rating vs Số lượng bán
scatter = axes[0, 1].scatter(df['price']/1000, df['rating_average'], 
                           s=df['quantity_sold']*2, alpha=0.6, c=df['revenue']/1000, cmap='viridis')
axes[0, 1].set_title('Giá vs Rating (size=quantity, color=revenue)', fontweight='bold')
axes[0, 1].set_xlabel('Giá (nghìn VNĐ)')
axes[0, 1].set_ylabel('Rating Average')
plt.colorbar(scatter, ax=axes[0, 1], label='Revenue (nghìn VNĐ)')

# 3. Boxplot: Rating theo fulfillment_type
fulfillment_data = [df[df['fulfillment_type'] == ft]['rating_average'].values 
                   for ft in df['fulfillment_type'].unique()]
fulfillment_labels = df['fulfillment_type'].unique()
axes[1, 0].boxplot(fulfillment_data, labels=fulfillment_labels)
axes[1, 0].set_title('⭐ So sánh Rating theo Fulfillment Type', fontweight='bold')
axes[1, 0].set_xlabel('Fulfillment Type')
axes[1, 0].set_ylabel('Rating Average')
axes[1, 0].tick_params(axis='x', rotation=45)

# 4. Doanh thu theo price_segment
segment_revenue = df.groupby('price_segment')['revenue'].sum()
axes[1, 1].pie(segment_revenue.values, labels=segment_revenue.index, autopct='%1.1f%%', startangle=90)
axes[1, 1].set_title('Phân bố Doanh thu theo Price Segment', fontweight='bold')

plt.tight_layout()
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('data/clean/olap_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ Đã lưu biểu đồ OLAP: 'data/clean/olap_analysis.png'")

# ========================================
# 3.2. KỸ THUẬT DATA MINING
# ========================================
print("\n🔍 3.2. KỸ THUẬT DATA MINING - CLUSTERING")
print("=" * 60)

# Chuẩn bị dữ liệu cho clustering
print("\n📋 Chuẩn bị dữ liệu cho clustering...")
clustering_features = ['price', 'rating_average', 'quantity_sold', 'favourite_count']
X = df[clustering_features].copy()
X = X.fillna(0)  # Thay thế NaN bằng 0

print("📊 Thống kê dữ liệu trước khi chuẩn hóa:")
print(X.describe().round(2))

# Chuẩn hóa dữ liệu
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("✅ Đã chuẩn hóa dữ liệu bằng StandardScaler")

# Tìm số cluster tối ưu bằng Silhouette Score
print("\n🔍 Tìm số cluster tối ưu:")
silhouette_scores = []
K_range = range(2, 8)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    cluster_labels = kmeans.fit_predict(X_scaled)
    silhouette_avg = silhouette_score(X_scaled, cluster_labels)
    silhouette_scores.append(silhouette_avg)
    print(f"   K={k}: Silhouette Score = {silhouette_avg:.3f}")

# Chọn K tốt nhất
best_k = K_range[np.argmax(silhouette_scores)]
print(f"\n✅ Số cluster tối ưu: K = {best_k} (Silhouette Score = {max(silhouette_scores):.3f})")

# Thực hiện clustering với K tối ưu
final_kmeans = KMeans(n_clusters=best_k, random_state=42)
df['cluster'] = final_kmeans.fit_predict(X_scaled)

print(f"\n📊 Phân bố cluster:")
cluster_counts = df['cluster'].value_counts().sort_index()
for cluster, count in cluster_counts.items():
    print(f"   Cluster {cluster}: {count:,} sản phẩm ({count/len(df)*100:.1f}%)")

# Mô tả từng cluster
print(f"\n📋 MÔ TẢ CÁC CLUSTER:")
print("=" * 50)

cluster_summary = df.groupby('cluster')[clustering_features + ['revenue']].agg(['mean', 'median']).round(0)

for i in range(best_k):
    cluster_data = df[df['cluster'] == i]
    print(f"\n🎯 CLUSTER {i} ({len(cluster_data):,} sản phẩm):")
    print(f"   Giá TB: {cluster_data['price'].mean():,.0f} VNĐ")
    print(f"   Rating TB: {cluster_data['rating_average'].mean():.2f}")
    print(f"   Số lượng bán TB: {cluster_data['quantity_sold'].mean():.1f}")
    print(f"   Favourite TB: {cluster_data['favourite_count'].mean():.1f}")
    print(f"   Doanh thu TB: {cluster_data['revenue'].mean():,.0f} VNĐ")
    
    # Đặc điểm cluster
    if cluster_data['price'].mean() < df['price'].mean():
        if cluster_data['rating_average'].mean() < df['rating_average'].mean():
            print(f"   Đặc điểm: Sản phẩm GIÁ RẺ, RATING THẤP, bán ít")
        else:
            print(f"   Đặc điểm: Sản phẩm GIÁ RẺ, RATING TỐT, giá trị tốt")
    else:
        if cluster_data['rating_average'].mean() > df['rating_average'].mean():
            print(f"   Đặc điểm: Sản phẩm CAO CẤP, RATING CAO, chất lượng premium")
        else:
            print(f"   Đặc điểm: Sản phẩm TẦM TRUNG, rating trung bình")

print(f"\n📈 Đang tạo biểu đồ Data Mining...")

# Tạo figure cho Data Mining visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('🔍 PHÂN TÍCH DATA MINING - CLUSTERING', fontsize=16, fontweight='bold')

# 1. Scatter plot: Price vs Quantity_sold với màu theo cluster
colors = plt.cm.tab10(np.linspace(0, 1, best_k))
for i in range(best_k):
    cluster_data = df[df['cluster'] == i]
    axes[0, 0].scatter(cluster_data['price']/1000, cluster_data['quantity_sold'], 
                      c=colors[i], label=f'Cluster {i}', alpha=0.6)
axes[0, 0].set_title('Giá vs Số lượng bán (theo Cluster)', fontweight='bold')
axes[0, 0].set_xlabel('Giá (nghìn VNĐ)')
axes[0, 0].set_ylabel('Số lượng bán')
axes[0, 0].legend()

# 2. Biểu đồ cột: Rating trung bình theo cluster
cluster_rating = df.groupby('cluster')['rating_average'].mean()
axes[0, 1].bar(cluster_rating.index, cluster_rating.values, color=colors)
axes[0, 1].set_title('Rating trung bình theo Cluster', fontweight='bold')
axes[0, 1].set_xlabel('Cluster')
axes[0, 1].set_ylabel('Rating Average')

# 3. Biểu đồ cột: Giá trung bình theo cluster
cluster_price = df.groupby('cluster')['price'].mean()
axes[1, 0].bar(cluster_price.index, cluster_price.values/1000, color=colors)
axes[1, 0].set_title('Giá trung bình theo Cluster', fontweight='bold')
axes[1, 0].set_xlabel('Cluster')
axes[1, 0].set_ylabel('Giá (nghìn VNĐ)')

# 4. Scatter plot 3D-like: Price vs Rating với size theo quantity_sold
for i in range(best_k):
    cluster_data = df[df['cluster'] == i]
    axes[1, 1].scatter(cluster_data['price']/1000, cluster_data['rating_average'], 
                      s=cluster_data['quantity_sold']*3, c=colors[i], 
                      label=f'Cluster {i}', alpha=0.6)
axes[1, 1].set_title('Giá vs Rating (size=quantity)', fontweight='bold')
axes[1, 1].set_xlabel('Giá (nghìn VNĐ)')
axes[1, 1].set_ylabel('Rating Average')
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('data/clean/clustering_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ Đã lưu biểu đồ Clustering: 'data/clean/clustering_analysis.png'")

# Lưu kết quả clustering
df.to_csv('data/clean/products_with_clusters.csv', index=False, encoding='utf-8')
print("✅ Đã lưu dữ liệu có cluster: 'data/clean/products_with_clusters.csv'")

print(f"\n🎯 TỔNG KẾT PHẦN 3:")
print("=" * 50)
print("✅ OLAP: Đã phân tích doanh thu, rating theo brand/fulfillment/segment")
print("✅ Data Mining: Đã phân cụm sản phẩm thành các nhóm chiến lược")
print("✅ Visualization: Đã tạo biểu đồ minh họa kết quả")
print("✅ Sẵn sàng cho báo cáo và đề xuất chiến lược kinh doanh!")