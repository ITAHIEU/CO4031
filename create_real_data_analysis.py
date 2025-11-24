#!/usr/bin/env python3
"""
Real data analysis script for GitHub Actions deployment
Connects to MySQL database and creates visualizations from actual data
"""

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
import warnings
import os

warnings.filterwarnings('ignore')

def main():
    # Set matplotlib backend
    plt.switch_backend('Agg')
    
    # Create data directory
    os.makedirs('data/clean', exist_ok=True)
    
    print("🔌 Connecting to MySQL database...")
    
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='root_password',
        database='ProductDW'
    )
    
    # Query real data from staging table (has real Vietnamese Tiki data)
    query = """
    SELECT 
        id as product_id,
        name as product_name,
        brand as brand_name,
        category as category_name,
        current_seller as seller_name,
        price as price,
        rating_average as rating,
        review_count,
        quantity_sold,
        COALESCE((original_price - price) / original_price * 100, 0) as discount_percent
    FROM STAGING_Products
    WHERE price > 0 AND rating_average >= 0
    LIMIT 5000;
    """
    
    df = pd.read_sql(query, conn)
    conn.close()
    
    print(f'📊 Loaded {len(df)} products from database')
    
    # Save clean data
    df.to_csv('data/clean/products_clean.csv', index=False)
    
    # Create OLAP Analysis Chart
    print("📈 Creating OLAP analysis charts...")
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Revenue by Brand (top 15)
    brand_revenue = df.groupby('brand_name')['price'].sum().nlargest(15)
    ax1.barh(brand_revenue.index, brand_revenue.values / 1e6, color='skyblue')
    ax1.set_title('💰 Top 15 Brands by Revenue (Million VND)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Revenue (Million VND)')
    
    # Price vs Rating scatter plot
    ax2.scatter(df['price']/1000, df['rating'], alpha=0.6, color='coral', s=30)
    ax2.set_title('📊 Price vs Rating Analysis', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Price (Thousand VND)')
    ax2.set_ylabel('Rating')
    
    # Category Distribution
    category_counts = df['category_name'].value_counts().head(8)
    colors = plt.cm.Set3(np.linspace(0, 1, len(category_counts)))
    ax3.pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%', 
            startangle=90, colors=colors)
    ax3.set_title('📦 Top Categories Distribution', fontsize=14, fontweight='bold')
    
    # Top Sellers by Revenue
    seller_revenue = df.groupby('seller_name')['price'].sum().nlargest(10)
    ax4.bar(range(len(seller_revenue)), seller_revenue.values / 1e6, color='lightgreen')
    ax4.set_title('🚚 Top 10 Sellers by Revenue', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Seller Rank')
    ax4.set_ylabel('Revenue (Million VND)')
    ax4.set_xticks(range(len(seller_revenue)))
    ax4.set_xticklabels([f'S{i+1}' for i in range(len(seller_revenue))], rotation=45)
    
    plt.tight_layout()
    plt.savefig('data/clean/olap_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✅ OLAP analysis chart created')
    
    # K-means Clustering Analysis on real data
    print("🤖 Running K-means clustering analysis...")
    if len(df) > 10:  # Only cluster if we have enough data
        features = ['price', 'rating', 'review_count', 'discount_percent']
        X = df[features].fillna(0)  # Fill NaN values
        
        # Remove outliers (optional)
        Q1 = X.quantile(0.25)
        Q3 = X.quantile(0.75)
        IQR = Q3 - Q1
        X_filtered = X[~((X < (Q1 - 1.5 * IQR)) | (X > (Q3 + 1.5 * IQR))).any(axis=1)]
        
        if len(X_filtered) > 10:
            # Standardize features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X_filtered)
            
            # Apply K-means
            n_clusters = min(7, max(2, len(X_filtered)//100))  # Dynamic cluster number
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            clusters = kmeans.fit_predict(X_scaled)
            
            # Add clusters back to original dataframe
            cluster_df = X_filtered.copy()
            cluster_df['cluster'] = clusters
            
            # Save clustered data
            result_df = df.loc[X_filtered.index].copy()
            result_df['cluster'] = clusters
            result_df.to_csv('data/clean/products_with_clusters.csv', index=False)
            
            # Create clustering visualization
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
            
            # Cluster scatter plot
            scatter = ax1.scatter(cluster_df['price']/1000, cluster_df['rating'], 
                                c=cluster_df['cluster'], cmap='viridis', alpha=0.7, s=40)
            ax1.set_title('💡 K-means Clustering: Price vs Rating', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Price (Thousand VND)')
            ax1.set_ylabel('Rating')
            plt.colorbar(scatter, ax=ax1, label='Cluster ID')
            
            # Cluster distribution
            cluster_counts = pd.Series(clusters).value_counts().sort_index()
            ax2.bar(cluster_counts.index, cluster_counts.values, color='orange', alpha=0.8)
            ax2.set_title('📊 Cluster Size Distribution', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Cluster ID')
            ax2.set_ylabel('Number of Products')
            
            # Average price by cluster
            cluster_price = cluster_df.groupby('cluster')['price'].mean()
            ax3.bar(cluster_price.index, cluster_price.values / 1000, color='lightcoral', alpha=0.8)
            ax3.set_title('💰 Average Price by Cluster', fontsize=14, fontweight='bold')
            ax3.set_xlabel('Cluster ID')
            ax3.set_ylabel('Average Price (Thousand VND)')
            
            # Average rating by cluster
            cluster_rating = cluster_df.groupby('cluster')['rating'].mean()
            ax4.bar(cluster_rating.index, cluster_rating.values, color='lightblue', alpha=0.8)
            ax4.set_title('⭐ Average Rating by Cluster', fontsize=14, fontweight='bold')
            ax4.set_xlabel('Cluster ID')
            ax4.set_ylabel('Average Rating')
            
            plt.tight_layout()
            plt.savefig('data/clean/clustering_analysis.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f'✅ Clustering analysis completed with {n_clusters} clusters')
        else:
            print('⚠️  Data too small after outlier removal')
    else:
        print('⚠️  Insufficient data for clustering analysis')
    
    print('🎉 Real data analysis completed successfully!')

if __name__ == "__main__":
    main()