import requests

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
