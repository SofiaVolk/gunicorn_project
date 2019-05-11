import csv
import database1
import unicodecsv as s
with open('dataset_sample.csv', newline='', encoding='utf-8') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=',', dialect='excel')

    for line in spamreader:
        try:
            desc = line['descrirption']

            database1.add_youla(line['title'],desc,line['product_id'],line['category_id']
                                ,line['subcategory_id'],line['properties'],line['image_links'])
        except:
            continue

# import csv
# import database1
# import unicodecsv as s
# with open('dataset_vacancy.csv', newline='', encoding='utf-8') as csvfile:
#     spamreader = csv.DictReader(csvfile, delimiter='|', dialect='excel')
#
#     for line in spamreader:
#         z = database1.get_vacancy(line['id'])
#         if z == None:
#             database1.add_vacancy(line['id'],line['name']
#                                   , None if line['profarea_name']=='' else line['profarea_name']
#
#                                   , None if line['employer']=='' else line['employer']
#                                   , None if line['description']=='' else line['description']
#                                   , None if line['salary_from']=='' else line['salary_from']
#                                   , None if line['salary_to']=='' else line['salary_to']
#                                   , None if line['currency']=='' else line['currency']
#                                   , None if line['metro_station']=='' else line['metro_station']
#             )


