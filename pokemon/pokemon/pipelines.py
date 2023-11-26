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
        categorie_liste = adapter.get('categories', [])
        categories_filtre = [category.strip() for category in ",".join(categorie_liste).split(',') if category.strip()]
        adapter['categories'] = categories_filtre

        return item
