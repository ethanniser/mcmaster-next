import csv

def generate_categories_mutation_batch(categories):
    mutations = []
    for category in categories:
        slug, name, collection_id, image_url = category
        mutations.append(f"""
        {{
          id: "{slug}"
          collectionId: "{collection_id}"
          imageUrl: "{image_url}"
          name: "{name}"
          slug: "{slug}"
        }}
        """)
    return f"""
    mutation {{
      category_insertMany(
        data: [{','.join(mutations)}]
      )
    }}
    """

def generate_collections_mutation_batch(collections):
    mutations = []
    for collection in collections:
        collection_id, name, slug = collection
        mutations.append(f"""
        {{
          id: "{collection_id}"
          name: "{name}"
          slug: "{slug}"
        }}
        """)
    return f"""
    mutation {{
      collection_insertMany(
        data: [{','.join(mutations)}]
      )
    }}
    """

def generate_products_mutation_batch(products):
    mutations = []
    for product in products:
        slug, name, description, price, subcategory_slug, image_url = product
        mutations.append(f"""
        {{
          id: "{slug}"
          name: "{name}"
          description: "{description}"
          price: {price}
          subcategoryId: "{subcategory_slug}"
          imageUrl: "{image_url}"
          slug: "{slug}"
        }}
        """)
    return f"""
    mutation {{
      product_insertMany(
        data: [{','.join(mutations)}]
      )
    }}
    """

def generate_subcategories_mutation_batch(subcategories):
    mutations = []
    for subcategory in subcategories:
        slug, name, subcollection_id, image_url = subcategory
        mutations.append(f"""
        {{
          id: "{slug}"
          name: "{name}"
          subcollectionId: "{subcollection_id}"
          imageUrl: "{image_url}"
          slug: "{slug}"
        }}
        """)
    return f"""
    mutation {{
      subcategory_insertMany(
        data: [{','.join(mutations)}]
      )
    }}
    """

def generate_subcollections_mutation_batch(subcollections):
    mutations = []
    for subcollection in subcollections:
        subcollection_id, name, category_slug = subcollection
        mutations.append(f"""
        {{
          id: "{subcollection_id}"
          name: "{name}"
          categoryId: "{category_slug}"
        }}
        """)
    return f"""
    mutation {{
      subcollection_insertMany(
        data: [{','.join(mutations)}]
      )
    }}
    """

def read_csv_and_generate_category_mutations(file_path):
    mutations = []
    with open(file_path, mode='r', newline='') as csvfile, open('Category_insert.gql', mode='w') as gqlfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        for row in csvreader:
            slug, name, collection_id, image_url = row
            mutations.append(f"""
            {{
              id: "{slug}"
              collectionId: "{collection_id}"
              imageUrl: "{image_url}"
              name: "{name}"
              slug: "{slug}"
            }}""")
        
        single_mutation = f"""mutation {{
  category_insertMany(
    data: [{','.join(mutations)}]
  )
}}"""
        gqlfile.write(single_mutation)

def read_csv_and_generate_collection_mutations(file_path):
    mutations = []
    with open(file_path, mode='r', newline='') as csvfile, open('Collection_insert.gql', mode='w') as gqlfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        for row in csvreader:
            if len(row) != 3:
                print(f"Skipping malformed row: {row}")
                continue
            collection_id, name, slug = row
            mutations.append(f"""
            {{
              id: "{collection_id}"
              name: "{name}"
              slug: "{slug}"
            }}""")
        
        single_mutation = f"""mutation {{
  collection_insertMany(
    data: [{','.join(mutations)}]
  )
}}"""
        gqlfile.write(single_mutation)

def read_csv_and_generate_product_mutations(file_path):
    mutations = []
    file_counter = 1
    row_counter = 0
    MAX_ROWS = 50000
    existing_ids = set()
    
    with open(file_path, mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        
        for row in csvreader:
            if len(row) != 6:
                print(f"Skipping malformed row: {row}")
                continue
                
            slug, name, description, price, subcategory_slug, image_url = row
            
            # Skip row if slug contains quotes
            if '"' in slug or "'" in slug or '"' in description or "'" in description:
                print(f"Skipping row with quotes in slug: {row}")
                continue
            
            if slug in existing_ids:
                print(f"Skipping duplicate id: {slug}")
                continue
            
            existing_ids.add(slug)
            mutations.append(f"""
            {{
              id: "{slug}"
              name: "{name}"
              description: "{description}"
              price: {price}
              subcategoryId: "{subcategory_slug}"
              imageUrl: "{image_url}"
              slug: "{slug}"
            }}""")
            
            row_counter += 1
            
            if row_counter >= MAX_ROWS:
                with open(f'Product_insert_{file_counter}.gql', mode='w') as gqlfile:
                    single_mutation = f"""mutation {{
  product_insertMany(
    data: [{','.join(mutations)}]
  )
}}"""
                    gqlfile.write(single_mutation)
                mutations = []
                row_counter = 0
                file_counter += 1
        
        # Write remaining mutations if any
        if mutations:
            with open(f'Product_insert_{file_counter}.gql', mode='w') as gqlfile:
                single_mutation = f"""mutation {{
  product_insertMany(
    data: [{','.join(mutations)}]
  )
}}"""
                gqlfile.write(single_mutation)

def read_csv_and_generate_subcategory_mutations(file_path):
    mutations = []
    with open(file_path, mode='r', newline='') as csvfile, open('Subcategory_insert.gql', mode='w') as gqlfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        for row in csvreader:
            if len(row) != 4:
                print(f"Skipping malformed row: {row}")
                continue
            slug, name, subcollection_id, image_url = row
            
            mutations.append(f"""
            {{
              id: "{slug}"
              name: "{name}"
              subcollectionId: "{subcollection_id}"
              imageUrl: "{image_url}"
              slug: "{slug}"
            }}""")
        
        single_mutation = f"""mutation {{
  subcategory_insertMany(
    data: [{','.join(mutations)}]
  )
}}"""
        gqlfile.write(single_mutation)

def read_csv_and_generate_subcollection_mutations(file_path):
    mutations = []
    with open(file_path, mode='r', newline='') as csvfile, open('Subcollection_insert.gql', mode='w') as gqlfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        for row in csvreader:
            if len(row) != 3:
                print(f"Skipping malformed row: {row}")
                continue
            subcollection_id, name, category_slug = row
            mutations.append(f"""
            {{
              id: "{subcollection_id}"
              name: "{name}"
              categoryId: "{category_slug}"
            }}""")
        
        single_mutation = f"""mutation {{
  subcollection_insertMany(
    data: [{','.join(mutations)}]
  )
}}"""
        gqlfile.write(single_mutation)

# Example usage
read_csv_and_generate_category_mutations('categories.csv')
read_csv_and_generate_collection_mutations('collections.csv')
read_csv_and_generate_product_mutations('products.csv')
read_csv_and_generate_subcategory_mutations('subcategories.csv')
read_csv_and_generate_subcollection_mutations('subcollections.csv')