from pymongo import MongoClient, database

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

def get_client() -> MongoClient:
    """Get a MongoDB client.
    
    Returns:
        The MongoDB client.
    """
    return MongoClient(
        host = MONGODB_HOST,
        port = MONGODB_PORT
    )

def get_db(name: str) -> database.Database:
    """Get the MongoDB database.

    Args:
        name: The name of the database.
    
    Returns:
        The MongoDB database.
    """
    return get_client()[name]

def get_collection(db_name: str, name: str) -> database.Collection:
    """Get the MongoDB collection.

    Args:
        db_name: The name of the database.

        name: The name of the collection.
    
    Returns:
        The MongoDB collection.
    """
    return get_db(db_name)[name]

def insert(db_name: str, name: str, data: dict | list):
    """Insert data into a MongoDB collection.

    Args:
        db_name: The name of the database.

        name: The name of the collection.

        data: The data to insert.
    """
    db = get_collection(db_name, name)

    try:
        db.insert_many(data)

    except Exception as e:
        db.insert_one(data)

def upsert(db_name: str, name: str, field: str, data: dict):
    """Upsert data into a MongoDB collection.

    Args:
        db_name: The name of the database.

        name: The name of the collection.

        field: The field to filter.

        data: The data to upsert.
    """
    db = get_collection(db_name, name)
    db.update_one(
        {field: data[field]},
        {'$set': data},
        upsert = True
    )
    
def list_items(
        db_name: str, 
        name: str, 
        field: str | None = None, 
        value: int | str | None = None
    ) -> list:
    """List items from a MongoDB collection.

    Args:
        db_name: The name of the database.

        name: The name of the collection.

        field: The field to filter. If None, return all items.

        value: The value to filter. If None, return all items.

    Returns:
        list: The items from the collection.
    """
    db = get_collection(db_name, name)

    if (field is None) or (value is None):
        result = list(db.find())
    
    else:
        result = list(db.find({field: value}))

    # Remove _id field
    for item in result:
        item.pop('_id', None)

    return result

def is_in_collection(
        db_name: str, 
        name: str, 
        field: str, 
        value: str
    ) -> bool:
    """Check if an item is in a MongoDB collection.

    Args:
        db_name: The name of the database.

        name: The name of the collection.

        field: The field to filter.

        value: The value to filter.

    Returns:
        bool: True if the item is in the collection, False otherwise.
    """
    db = get_collection(db_name, name)
    return db.find_one({field: value}) is not None