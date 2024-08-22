from flask import Flask, render_template, request
import sqlite3
import pandas as pd

app = Flask(__name__)

# SQLite database file
db_file = 'products.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_file)

# Load the data into a DataFrame
df = pd.read_sql_query("SELECT * FROM products", conn)

# Close the connection
conn.close()

# Calculate statistics
total_listings = df.shape[0]
avg_price = df['Price'].mean()
avg_ratings = df['Rating'].mean()
# Assuming you want to calculate average review count and total questions from your data
avg_review_count = df['Total Rating'].mean()  # Replace with your actual logic
total_questions = df['Questions'].sum()   # Replace with your actual logic

# Function to get top 5 products based on defined criteria
def get_top_products(df):
    sorted_df = df.sort_values(by=['Rating', 'Price'], ascending=[False, True])
    top_products = sorted_df.head(5)
    
    # Add a new column 'ImageLink' with image links
    image_links = [
        "https://static-01.daraz.pk/p/5d378773aefb501f1c15e5dd03063796.jpg_300x0q75.webp",
        "https://static-01.daraz.pk/p/4ea7260fa09eacba42e5f7ef3c2a4c6e.jpg_300x0q75.webp",
        "https://static-01.daraz.pk/p/bd6712dd72bec6bb303cde04ce798361.jpg_300x0q75.webp",
        "https://static-01.daraz.pk/p/4ec97ac3de5fd8b84f73402d48a3a164.jpg_300x0q75.webp",
        "https://static-01.daraz.pk/p/c032380d580be6d3d12c2791010a30b6.png_300x0q75.webp"
    ]

    top_products['ImageLink'] = image_links

    return top_products

def get_product_data(product_id):
    # Sample logic to fetch product details for the given product_id
    product_data = df[df['Id'] == product_id].iloc[0].to_dict()
    return product_data

# Route for the main dashboard
@app.route('/')
def dashboard():
    top_products = get_top_products(df)
    return render_template(
        'main.html',
        top_products=top_products,
        total_listings=total_listings,
        avg_price=avg_price,
        avg_ratings=avg_ratings,
        avg_review_count=avg_review_count,
        total_questions=total_questions
    )

# Sample route for product details
@app.route('/product_details/<int:product_id>')
def product_details(product_id):
    # Sample logic to fetch and display details for the given product_id
    product_data = get_product_data(product_id)
    return render_template('product_details.html', product_data=product_data)

# Route to handle user queries
@app.route('/query', methods=['POST'])
def query():
    user_input = request.form['user_input']
    # results = filter_data(user_input)
    # Process the results and provide necessary data for the frontend
    pass

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)