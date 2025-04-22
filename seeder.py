from sqlmodel import SQLModel, Session
from db.database import engine, create_db_and_tables, drop_db_and_tables
from models.author import Author
from models.entry import Entry
from models.category import Category

def seed_data():
    # Borrar la base de datos y las tablas existentes
    drop_db_and_tables() 
    # Crear la base de datos y las tablas
    create_db_and_tables()

    with Session(engine) as session:
        # Crear autores
        try:
            author1 = Author(name="Emma Johnson", email="emma.johnson@example.com")
            author2 = Author(name="Liam Smith", email="liam.smith@example.com")
            author3 = Author(name="Olivia Davis", email="olivia.davis@example.com")
            session.add_all([author1, author2, author3])
            session.commit()
        except Exception as e:
            print(f"Error creating authors: {e}")

        try:
            category1 = Category(name="Technology", description="The application of scientific knowledge for practical purposes, especially in industry.")
            category2 = Category(name="Movies", description="A recording of moving images that tells a story and that people watch on a screen.")
            category3 = Category(name="Science", description="The systematic study of the structure and behaviour of the physical and natural world through observation, experimentation, and the testing of theories against the evidence obtained.")
            session.add_all([category1, category2, category3])
            session.commit()
        except Exception as e:
            print(f"Error creating categories: {e}")

        # Create entradas linkadas a autores
        try:
            entry1 = Entry(title="How Intel Can Help Carmakers Compete With China", content="""
                           Western automotive giants face an existential challenge as China’s carmakers surge ahead. Much of China’s edge comes from how its automotive sector is structured: streamlined, fast, and incredibly tech-forward.
                           R&D cycles for Chinese electric vehicles (EVs) typically span just nine to 18 months. In contrast, many Western automakers require five to seven years to bring a new vehicle from concept to production. If this gap isn’t 
                           closed — and fast — the Western auto industry could become irrelevant by 2030.
                           Let’s talk about how Intel and others could save the auto industry. Then, we’ll close with my Product of the Week: the HP EliteBook Ultra G1i 14-inch AI PC.
                           """, author_id=author1.id, category_id=1)
            entry2 = Entry(title="Tron: Ares Official Trailer", content="""
                           Worlds are about to collide as Walt Disney Pictures releases the official trailer for the upcoming sequel film Tron: Ares. View trailer below.
                           Tron: Ares follows a highly sophisticated program, Ares, who is sent from the digital world into the real world on a dangerous mission, marking humankind’s first encounter with A.I. beings.
                           Oh wow…. a trailer…finally. I remember hearing about this movie for quite some time…. ever since 2010’s Tron: Legacy. While I did like Tron: Legacy, I don’t think a sequel was necessary. And yet, I would welcome such an idea.
                           After years of waiting and rumors of trying to get the project off the ground, the long-awaited follow-up sequel to Tron: Legacy has arrived, with the official teaser trailer showcasing the first real 
                           look at the upcoming film. To its credit, the preview does certainly a grab the attention, viewing that people from “The Grid” are now in the real world and how the two worlds will collide in this 
                           latest installment. It still remains to be seeing how good the movie will actually be as the Tron franchise isn’t quite strong and I am aware that actor Jared Leto may not be the most ideal choice 
                           to lead a project like this. In the end, Tron: Ares definitely looks interesting, and I intrigued by it, yet I still have some reservations if this movie will be good or not. Only time will tell….
                           """, author_id=author2.id, category_id=2)
            entry3 = Entry(title="Space Clock Redefines Time Measurement Itself", content="""
                           Time moves differently in space – and a revolutionary European timepiece launched this week will prove it with unprecedented precision.
                           The Atomic Clock Ensemble in Space (ACES) successfully reached orbit on April 21, launching aboard a SpaceX Falcon 9 rocket from NASA’s Kennedy Space Center. The mission puts the most accurate timekeeping system 
                           ever sent to space on the International Space Station, where it will test fundamental physics theories while losing just one second every 300 million years.
                           “The launch of ACES marks a major milestone for European science and international cooperation in space,” said Daniel Neuenschwander, Director of Human & Robotic Exploration at ESA. “With this mission, we are placing 
                           the most precise timepiece ever sent to orbit aboard the International Space Station — opening new frontiers in fundamental physics, time transfer, and global synchronization.”
                           """, author_id=author1.id, category_id=3)
            session.add_all([entry1, entry2, entry3])
            session.commit()
        except Exception as e:
            print(f"Error creating entries: {e}")

if __name__ == "__main__":
    seed_data()