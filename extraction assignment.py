import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import random

# Function to get a random proxy
def get_random_proxy():
    proxies = [
        'http://proxy1:port',
        'http://proxy2:port',
        'http://proxy3:port',
        # Add more proxies as needed
    ]
    return {'http': random.choice(proxies), 'https': random.choice(proxies)}

# Function to scrape product data
def scrape_noon_yoga_products(url, num_products=200):
    products = []
    page = 1

    while len(products) < num_products:
        print(f"Scraping page {page}...")
        response = requests.get(url, proxies=get_random_proxy())
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find product containers
        product_containers = soup.find_all('div', class_='productContainer')

        for container in product_containers:
            title = container.find('h2', class_='productTitle').text.strip()
            price = container.find('span', class_='price').text.strip()
            brand = container.find('span', class_='brand').text.strip() if container.find('span', class_='brand') else 'Unknown'
            seller = container.find('span', class_='seller').text.strip() if container.find('span', class_='seller') else 'Unknown'

            products.append({
                'Title': title,
                'Price': price.replace('AED', '').strip(),
                'Brand': brand,
                'Seller': seller
            })

            if len(products) >= num_products:
                break

        page += 1
        url = f"https://www.noon.com/uae-en/sports-and-outdoors/exercise-and-fitness/yoga-16328/?page={page}"

    return products

# Function to analyze the data
def analyze_data(products):
    df = pd.DataFrame(products)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    # Most expensive product
    most_expensive = df.loc[df['Price'].idxmax()]

    # Cheapest product
    cheapest = df.loc[df['Price'].idxmin()]

    # Number of products from each brand
    brand_counts = df['Brand'].value_counts()

    # Number of products by each seller
    seller_counts = df['Seller'].value_counts()

    # Save to CSV
    df.to_csv('noon_yoga_products.csv', index=False)

    # Print analysis results
    print("Most Expensive Product:")
    print(most_expensive)
    print("\nCheapest Product:")
    print(cheapest)
    print("\nNumber of Products from Each Brand:")
    print(brand_counts)
    print("\nNumber of Products by Each Seller:")
    print(seller_counts)

    # Plotting
    plt.figure(figsize=(10, 5))
    brand_counts.plot(kind='bar', title='Number of Products by Brand')
    plt.xlabel('Brand')
    plt.ylabel('Number of Products')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('products_by_brand.png')
    plt.show()

    plt.figure(figsize=(10, 5))
    seller_counts.plot(kind='bar', title='Number of Products by Seller')
    plt.xlabel('Seller')
    plt.ylabel('Number of Products')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('products_by_seller.png')
    plt.show()

# Main execution
if __name__ == "__main__":
    url = "https://www.noon.com/uae-en/sports-and-outdoors/exercise-and-fitness/yoga-16328/"
    products = scrape_noon_yoga_products(url, num_products=200)
    analyze_data(products)