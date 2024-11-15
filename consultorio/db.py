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

def get_db() -> database.Database:
    """Get the MongoDB database.
    
    Returns:
        The MongoDB database.
    """
    return get_client().reserva

def get_collection() -> database.Collection:
    """Get the MongoDB collection.
    
    Returns:
        The MongoDB collection.
    """
    return get_db().reservas

def insert_reserva(data: dict):
    """Insert a reservation into the database.
    
    Args:
        data: The reservation data.
    """
    db = get_collection()
    db.reservas.insert_one(data)
    
def list_reservas(rut: str) -> list:
    """List all reservations.
    
    Returns:
        A list of reservations.
    """
    db = get_collection()
    return list(db.reservas.find({"rut": rut}))