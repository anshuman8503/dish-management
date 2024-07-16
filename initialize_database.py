import sqlite3

def create_database():
    conn = sqlite3.connect('dishes.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dishes (
            dishId TEXT PRIMARY KEY,
            dishName TEXT NOT NULL,
            imageUrl TEXT NOT NULL,
            isPublished BOOLEAN NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def populate_database():
    dishes = [
        {
            "dishName": "Jeera Rice",
            "dishId": "1",
            "imageUrl": "https://nosh-assignment.s3.ap-south-1.amazonaws.com/jeera-rice.jpg",
            "isPublished": True
        },
        {
            "dishName": "Paneer Tikka",
            "dishId": "2",
            "imageUrl": "https://nosh-assignment.s3.ap-south-1.amazonaws.com/paneer-tikka.jpg",
            "isPublished": True
        },
        {
            "dishName": "Rabdi",
            "dishId": "3",
            "imageUrl": "https://nosh-assignment.s3.ap-south-1.amazonaws.com/rabdi.jpg",
            "isPublished": True
        },
        {
            "dishName": "Chicken Biryani",
            "dishId": "4",
            "imageUrl": "https://nosh-assignment.s3.ap-south-1.amazonaws.com/chicken-biryani.jpg",
            "isPublished": True
        },
        {
            "dishName": "Alfredo Pasta",
            "dishId": "5",
            "imageUrl": "https://nosh-assignment.s3.ap-south-1.amazonaws.com/alfredo-pasta.jpg",
            "isPublished": True
        }
    ]

    conn = sqlite3.connect('dishes.db')
    cursor = conn.cursor()

    for dish in dishes:
        cursor.execute('''
            INSERT OR REPLACE INTO dishes (dishId, dishName, imageUrl, isPublished)
            VALUES (?, ?, ?, ?)
        ''', (dish["dishId"], dish["dishName"], dish["imageUrl"], dish["isPublished"]))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    populate_database()