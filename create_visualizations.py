import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Đọc dữ liệu gốc và dữ liệu sạch
df_original = pd.read_csv('vietnamese_tiki_products_backpacks_suitcases.csv')
df_clean = pd.read_csv('data/clean/products_clean.csv')

print("📊 TẠO BIỂU ĐỒ MINH HỌA")
print("=" * 50)

# Thiết lập style
plt.style.use('seaborn-v0_8')
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (15, 10)

# Tạo figure với 2x2 subplots
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('📊 PHÂN TÍCH DỮ LIỆU TRƯỚC VÀ SAU TIỀN XỬ LÝ', fontsize=16, fontweight='bold')

# 1. Histogram giá (price)
axes[0, 0].hist(df_clean['price']/1000, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
axes[0, 0].set_title('📈 Phân phối Giá sản phẩm', fontweight='bold')
axes[0, 0].set_xlabel('Giá (nghìn VNĐ)')
axes[0, 0].set_ylabel('Số lượng sản phẩm')
axes[0, 0].grid(True, alpha=0.3)

# 2. Histogram rating_average
axes[0, 1].hist(df_clean['rating_average'], bins=20, alpha=0.7, color='lightgreen', edgecolor='black')
axes[0, 1].set_title('⭐ Phân phối Điểm đánh giá trung bình', fontweight='bold')
axes[0, 1].set_xlabel('Rating Average')
axes[0, 1].set_ylabel('Số lượng sản phẩm')
axes[0, 1].grid(True, alpha=0.3)

# 3. Phân nhóm giá
price_segment_counts = df_clean['price_segment'].value_counts()
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
axes[1, 0].pie(price_segment_counts.values, labels=price_segment_counts.index, 
               autopct='%1.1f%%', colors=colors, startangle=90)
axes[1, 0].set_title('💰 Phân bố theo nhóm giá', fontweight='bold')

# 4. Tỷ lệ giảm giá
axes[1, 1].hist(df_clean['discount_rate'] * 100, bins=30, alpha=0.7, color='orange', edgecolor='black')
axes[1, 1].set_title('🎯 Phân phối Tỷ lệ giảm giá', fontweight='bold')
axes[1, 1].set_xlabel('Tỷ lệ giảm giá (%)')
axes[1, 1].set_ylabel('Số lượng sản phẩm')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('data/clean/data_analysis_charts.png', dpi=300, bbox_inches='tight')
plt.show()

# Tạo bảng thống kê so sánh
print("\n📋 BẢNG THỐNG KÊ SO SÁNH TRƯỚC/SAU LÀMS SẠCH")
print("=" * 60)

comparison_data = {
    'Chỉ số': [
        'Tổng số sản phẩm',
        'Số thương hiệu',
        'Số người bán',
        'Giá trung bình (VNĐ)',
        'Giá cao nhất (VNĐ)', 
        'Giá thấp nhất (VNĐ)',
        'Rating trung bình',
        'Số sản phẩm có video',
        'Số sản phẩm hỗ trợ trả sau'
    ],
    'Trước làm sạch': [
        f"{len(df_original):,}",
        f"{df_original['brand'].nunique():,}",
        f"{df_original['current_seller'].nunique():,}",
        f"{df_original['price'].mean():,.0f}",
        f"{df_original['price'].max():,}",
        f"{df_original['price'].min():,}",
        f"{df_original['rating_average'].mean():.2f}",
        f"{df_original['has_video'].sum():,}",
        f"{df_original['pay_later'].sum():,}"
    ],
    'Sau làm sạch': [
        f"{len(df_clean):,}",
        f"{df_clean['brand'].nunique():,}",
        f"{df_clean['current_seller'].nunique():,}",
        f"{df_clean['price'].mean():,.0f}",
        f"{df_clean['price'].max():,}",
        f"{df_clean['price'].min():,}",
        f"{df_clean['rating_average'].mean():.2f}",
        f"{df_clean['has_video'].sum():,}",
        f"{df_clean['pay_later'].sum():,}"
    ]
}

comparison_df = pd.DataFrame(comparison_data)
print(comparison_df.to_string(index=False))

# Lưu bảng thống kê
comparison_df.to_csv('data/clean/comparison_statistics.csv', index=False, encoding='utf-8')

print(f"\n✅ Đã lưu biểu đồ: 'data/clean/data_analysis_charts.png'")
print(f"✅ Đã lưu bảng thống kê: 'data/clean/comparison_statistics.csv'")

print("\n🎯 KẾT QUẢ TIỀN XỬ LÝ DỮ LIỆU:")
print("=" * 50)
print("✅ Dữ liệu rất sạch - không có giá trị thiếu hay bất thường")
print("✅ Đã tạo biến discount_rate và price_segment")
print("✅ Đã chuẩn hóa text fields về chữ thường")
print("✅ Đã xuất dữ liệu sạch và biểu đồ phân tích")
print("✅ Sẵn sàng để import vào Data Warehouse!")