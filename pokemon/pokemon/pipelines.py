# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class PokemonPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # field_names = adapter.field_names()
        # for field_name in field_names:
            # if field_name != 'description':
                # value = adapter.get(field_name)
                # adapter[field_name] = value.strip()

        # Iterate over all fields in the item
        for field_name, field_value in item.items():
            # Check if the field value is a list
            if isinstance(field_value, list):
                # Convert numeric strings to integers and strip other strings
                formatted_value = [int(val) if val.isdigit() else val.strip() for val in field_value]
                # Join the list elements into a string
                formatted_value = ', '.join(map(str, formatted_value))
            else:
                # Convert the single value to a string
                formatted_value = str(field_value)

            # Set the formatted value to the adapter
            adapter[field_name] = formatted_value.strip()


        lowercase_keys = ['tags', 'categories']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        #garder nombre dans stock, et éliminer texte
        stock_string = adapter.get('stock')
        split_string_array = stock_string.split()
        adapter['stock']= int(split_string_array[0])
        

        #elimine pokemon de categories
        categorie_liste = adapter.get('categories')
        #transforme categories en liste pour supprimer "pokemon"
        categorie_liste = [element.strip() for element in categorie_liste.split(',')] 
        categorie_liste = [cat for cat in categorie_liste if cat.lower() != "pokemon"] 
        adapter['categories'] = ', '.join(categorie_liste)      


        return item
    

import mysql.connector

class SaveToMySQLPipeLine:

    def __init__(self):
    self.conn = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'Plasma2020@',
        database = 'pokemon'
    )

    #create cursor, to execute commands
    self.cur = self.conn.cursor()

    #create pokemon table
    self.cur.execute("""
    CREATE TABLE IF NOT EXISTS pokemon(
        id INT NOT NULL AUTO_INCREMENT,
        name VARCHAR(255),
        price DECIMAL,
        description VARCHAR(255),
        stock INTEGER,
        sku INTEGER,
        categories VARCHAR(255),
        tags VARCHAR(255),
        weight DECIMAL,
        height DECIMAL,
        width DECIMAL, 
        depth DECIMAL, 
        PRIMARY KEY (id)
)
""")

