#!/usr/bin/env python3

from faker import Faker
import random

from app import app
from models import db, Hero , Power , HeroPower
strengths = ["Strong", "Weak", "Average"]


with app.app_context():
    fake = Faker()

    try:
        Hero.query.delete()
    except Exception as e:
        pass

    heroes = []
    for i in range(50):
        hero = Hero(
            name=fake.unique.first_name(),
            super_name=fake.last_name(),
        )
        heroes.append(hero)

    db.session.add_all(heroes)
    db.session.commit()

    try:
        Power.query.delete()
    except Exception as e:
        pass

    powers = []
    for i in range(25):
        power = Power(
            name=fake.unique.company(),
            description=fake.text(max_nb_chars=20), 
        )
        powers.append(power)

    db.session.add_all(powers)
    db.session.commit()

    try:
        HeroPower.query.delete()
    except Exception as e:
        pass

    for i in range(100):
        hero_power = HeroPower(
            strength=random.choice(strengths),  
            hero_id=fake.random_element(elements=heroes).id,
            power_id=fake.random_element(elements=powers).id
        )
        db.session.add(hero_power)

    db.session.commit()
