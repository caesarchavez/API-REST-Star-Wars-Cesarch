from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Float, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    favorite = relationship("Favorite", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }



class Vehicle(db.Model): 
    id: Mapped[int] = mapped_column(primary_key =True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    model: Mapped[str] = mapped_column(String(120), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(120), nullable=False)
    favorite = relationship("Favorite", back_populates="vehicle")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "price": self.price,
            "manufacturer": self.manufacturer
        }
    
class People(db.Model): 
        id: Mapped[int] = mapped_column(primary_key =True)
        name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
        origin: Mapped[str] = mapped_column(String(120), nullable=False)
        eye_color: Mapped[str] = mapped_column(String(120), nullable=False)
        gender: Mapped[str] = mapped_column(String(120), nullable=False)
        favorite = relationship("Favorite", back_populates="people")
        
        def serialize(self):
            return {
            "id": self.id,
            "name": self.name,
            "origin": self.origin,
            "eye_color": self.eye_color,
            "gender": self.gender
        }

class Planet(db.Model): 
      id: Mapped[int] = mapped_column(primary_key =True)
      name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
      climate: Mapped[str] = mapped_column(String(120), nullable=False)
      diameter: Mapped[float] = mapped_column(Float, nullable=False)
      population: Mapped[int] = mapped_column(Integer, nullable=False)
      favorite = relationship("Favorite", back_populates="planet")

      def serialize(self):
            return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "population": self.population
        }


class Favorite(db.Model): 
      id: Mapped[int] = mapped_column(primary_key =True)

      people_id: Mapped[int] = mapped_column(db.ForeignKey("people.id"), nullable=True)
      people = relationship("People", back_populates="favorite")

      planet_id: Mapped[int] = mapped_column(db.ForeignKey("planet.id"), nullable=True)
      planet = relationship("Planet", back_populates="favorite")

      vehicles_id: Mapped[int] = mapped_column(db.ForeignKey("vehicle.id"), nullable=True)
      vehicle = relationship("Vehicle", back_populates="favorite")

      user_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"), nullable=True)
      user = relationship("User", back_populates="favorite")