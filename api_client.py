import requests
from pathlib import Path
import pandas as pd
import json

class InventoryAPIClient:
    """Handles communications with the DummyJSON Products API."""
    
    def __init__(self, base_url: str = "https://dummyjson.com/products"):
        self.base_url = base_url
        # Initializing a session preserves connections and optimizes performance
        self.session = requests.Session()

    def fetch_page(self, limit: int = 30, skip: int = 0) -> dict:
        """Fetch a single page of product data using query parameters."""
        params = {
            "limit": limit,
            "skip": skip
        }
        
        response = self.session.get(self.base_url, params=params)
        # Automatically raises an HTTPError for 4xx or 5xx status codes
        response.raise_for_status() 
        
        # Returns the full parsed JSON dictionary: {"products": [...], "total": X, "skip": Y, "limit": Z}
        return response.json()

    def fetch_all_products(self, batch_size: int = 30) -> list[dict]:
        """Paginate through all endpoints until all inventory items are retrieved."""
        all_products = []
        skip = 0
        
        while True:
            # 1. Fetch the current page dictionary
            data = self.fetch_page(limit=batch_size, skip=skip)
            
            # 2. Extract the actual products list from the response payload
            products = data.get("products", [])
            if not products:
                break
                
            all_products.extend(products)
            
            # 3. Update the offset or break if we have retrieved everything
            total = data.get("total", 0)
            skip += batch_size
            
            if skip >= total:
                break
                
        return all_products

class InventoryReportGenerator:
    """Transforms raw product API data into structured business reports."""
    
    def __init__(self, raw_data: list[dict]):
        # Load raw_data into a pandas DataFrame attribute
        self.df = pd.DataFrame(raw_data)
        
    def process_inventory(self, low_stock_threshold: int = 10) -> pd.DataFrame:
        """Calculate discounted prices and identify low-stock items."""
        if self.df.empty:
            return self.df
            
        # Calculate 'discounted_price' = price * (1 - discountPercentage / 100)
        self.df['discounted_price'] = self.df['price'] * (1 - self.df['discountPercentage'] / 100)
        
        # Add boolean column 'low_stock_warning' if stock < low_stock_threshold
        self.df['low_stock_warning'] = self.df['stock'] < low_stock_threshold
        
        # Select and reorder relevant columns
        columns_order = [
            'id', 'title', 'price', 'discountPercentage', 
            'discounted_price', 'stock', 'low_stock_warning'
        ]
        # Dynamically filter columns to only include what exists in the data
        existing_columns = [col for col in columns_order if col in self.df.columns]
        
        self.df = self.df[existing_columns]
        return self.df  # Fixed: Added the missing return statement

    def export_csv(self, destination: str | Path) -> None:
        """Export the processed DataFrame to CSV format."""
        self.df.to_csv(destination, index=False)
        
    def export_summary_metrics(self, destination: str | Path) -> None:
        """Export high-level metrics (total inventory value, item count) as JSON."""
        if self.df.empty:
            metrics = {"total_inventory_value": 0.0, "total_item_count": 0}
        else:
            # Value = stock * discounted_price (or regular price depending on preference)
            total_value = (self.df['stock'] * self.df['discounted_price']).sum()
            total_items = int(self.df['stock'].sum())
            
            metrics = {
                "total_inventory_value": float(round(total_value, 2)),
                "total_item_count": total_items
            }
            
        with open(destination, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=4)


