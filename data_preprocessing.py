import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')



df = pd.read_csv('vietnamese_tiki_products_backpacks_suitcases.csv')

desc_stats = df.describe(include='all').T
original_count = len(df)
missing_data = df.isnull().sum()
df = df.dropna(subset=['id', 'name', 'price'])
df = df[df['price'] > 0]
df = df[df['quantity_sold'] >= 0]
df['brand'] = df['brand'].fillna('Unknown').str.lower().str.strip()
df['current_seller'] = df['current_seller'].fillna('Unknown').str.lower().str.strip()
df['fulfillment_type'] = df['fulfillment_type'].fillna('Unknown').str.lower().str.strip()
df['discount_rate'] = np.where(
	df['original_price'] > 0,
	1 - df['price'] / df['original_price'],
	0
)
bins = [0, 100000, 500000, 2000000, float('inf')]
labels = ['<100k', '100k-500k', '500k-2M', '>2M']
df['price_segment'] = pd.cut(df['price'], bins=bins, labels=labels)

df['rating_average'] = df['rating_average'].astype(float)
df['quantity_sold'] = df['quantity_sold'].astype(int)

print("\n💾 BƯỚC 5: Xuất dữ liệu sạch")
import os
os.makedirs('data/clean', exist_ok=True)
df.to_csv('data/clean/products_clean.csv', index=False, encoding='utf-8')
print("✅ Đã xuất dữ liệu sạch ra 'data/clean/products_clean.csv'")