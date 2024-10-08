#!/usr/bin/env python3

from app import app
from models import db, Plant

# Ensure you are working within the app context to access the database properly
with app.app_context():

    # Delete all existing records in the Plant table
    Plant.query.delete()

    # Define new plants to seed the database
    aloe = Plant(
        name="Aloe",  # The id will auto-increment
        image="./images/aloe.jpg",
        price=11.50,
    )

    zz_plant = Plant(
        name="ZZ Plant",
        image="./images/zz-plant.jpg",
        price=25.98,
    )

    # Add the plants to the session
    db.session.add_all([aloe, zz_plant])

    # Commit the session to save the changes in the database
    db.session.commit()

    # Optional: Print a success message
    print("Database seeded successfully!")
