# Import required libraries for Basalam API integration
import os
import asyncio
from dotenv import load_dotenv
from basalam_sdk import BasalamClient, PersonalToken
from basalam_sdk.search.models import ProductSearchModel, FiltersModel
 
# Load environment variables
load_dotenv()

# Get Basalam API token from environment
BASALAM_TOKEN = os.getenv("BASALAM_TOKEN")

# Initialize authentication with personal token
auth = PersonalToken(
    token=BASALAM_TOKEN,
)
# Create Basalam client instance
client = BasalamClient(auth=auth)


# Search for products in Basalam marketplace with filters
async def search_products_example(query: str,
                                  minPrice: int = None,
                                  maxPrice: int = None,
                                  minRating: int = 4,
                                  freeShipping: int = 0):
                                  
    """ Search for products in the marketplace Basalam with various filters """
    
    # Execute product search with filters
    results = await client.search_products(
        request=ProductSearchModel(
            filters=FiltersModel(
                freeShipping=freeShipping,
                maxPrice=maxPrice,
                minPrice=minPrice,
                minRating=minRating,
            ),
            q=query
        )
    )
    return results

# Get product details and format them as readable Persian text
async def get_product_details(query: str = None, **kwargs):

    """ Get product details and convert them to readable Persian text """

    # Search for products using the provided query and filters
    products = await search_products_example(query, **kwargs)
    
    # Return message if no products found
    if not products:
        return f"No products found for the query '{query}'."
    
    # Process and format product details
    product_details = []
    for product in products["products"][:5]:  # Limit to first 5 products
        try:
            # Extract product information
            name = product["name"]
            price = product["price"]
            mainAttribute = product["mainAttribute"]
            rating = product["rating"].get("average", "Unknown") if product.get("rating") else "Unknown"
            IsAvailable = product["IsAvailable"]
            isFreeShipping = product["isFreeShipping"]

            # Format product information in Persian
            r = f"محصول «{name}» با قیمت {price} تومان عرضه می‌شود. این کالا با امتیاز {rating} از کاربران، {'موجود است' if IsAvailable else 'در حال حاضر موجود نیست'} و {'دارای ارسال رایگان می‌باشد' if isFreeShipping else 'ارسال رایگان ندارد'}."

            product_details.append(r)
        except AttributeError as e:
            # Skip products with missing attributes
            continue
        
    # Return message if no valid products found
    if not product_details:
        return f"هیچ محصول معتبری با عبارت «{query}» یافت نشد."
        
    # Join all product details with newlines
    result = "\n".join(product_details)
    return result
