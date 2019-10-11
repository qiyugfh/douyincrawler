# coding: utf-8


import pymongo



client = pymongo.MongoClient('mongodb://root:123456@localhost:27017/')
contents = client['crawler']['contents']

ws = contents.find({'website': {'$regex': 'douyin'}})
for w in ws:
    print(w['_id'])
    if 'videos' not in w or len(w['videos']) == 0:
        contents.delete_one({'_id': w['_id']})
        continue
    videos = w['videos']
    if 'path' in videos[0]:
        path = videos[0]['path']
        if not path.endswith('.mp4'):
            contents.delete_one({'_id': w['_id']})
    else:
        contents.delete_one({'_id': w['_id']})
