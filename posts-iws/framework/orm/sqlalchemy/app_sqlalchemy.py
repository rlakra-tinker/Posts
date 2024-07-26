#
# Author: Rohtash Lakra
#
from sqlalchemy import create_engine
from entity import AbstractEntity, Role, User, Address
from sqlalchemy.orm import Session


class SqlAlchemy:

    def __init__(self):
        # The echo=True parameter indicates that SQL emitted by connections will be logged to standard out.
        self.engine = create_engine("sqlite://", echo=True)

    def create_database(self):
        print(f"create_database\n")
        # Using our table metadata and our engine, we can generate our schema at once in our target SQLite database,
        # using a method called 'MetaData.create_all()':
        AbstractEntity.metadata.create_all(self.engine)
        print()

    def populate_database(self):
        print(f"populate_database\n")
        with Session(self.engine) as session:
            # create roles
            admin_role = Role(name="ADMIN")
            user_role = Role(name="USER")
            guest_role = Role(name="GUEST")
            # add all roles
            session.add_all([admin_role, user_role, guest_role])

            # create users
            roh = User(
                user_name="roh@lakra.com",
                password="Roh",
                email="roh@lakra.com",
                first_name="Rohtash",
                last_name="Lakra",
                admin=True,
                addresses=[Address(
                    street1="Tennison Rd",
                    city="Hayward",
                    state="California",
                    country="US",
                    zip="94544"
                )],
            )

            san = User(
                user_name="san@lakra.com",
                password="San",
                email="roh@lakra.com",
                first_name="Sangita",
                last_name="Lakra",
                admin=True,
                addresses=[Address(
                    street1="Mission Blvd",
                    city="Hayward",
                    state="California",
                    country="US",
                    zip="94544"
                ),
                    Address(
                        street1="Mission Rd",
                        city="Fremont",
                        state="California",
                        country="US",
                        zip="94534"
                    )
                ]
            )

            # add users
            session.add_all([roh, san])
            session.commit()
        print()

    def fetch_records(self):
        print(f"fetch_records\n")
        # Simple SELECT
        from sqlalchemy import select
        session = Session(self.engine)
        stmt = select(User).where(User.first_name.in_(["Rohtash", "Sangita"]))
        for user in session.scalars(stmt):
            print(user)
        print()

    def fetch_with_joins(self):
        print(f"fetch_with_joins\n")
        from sqlalchemy import select
        session = Session(self.engine)
        stmt = (
            select(Address)
            .join(Address.user)
            .where(Address.state == "California")
            .where(User.first_name == "Rohtash")
        )
        roh_address = session.scalars(stmt).one()
        print(roh_address)
        print()

    def update_records(self):
        print(f"update_records\n")
        from sqlalchemy import select
        session = Session(self.engine)
        stmt = (
            select(Address)
            .join(Address.user)
            .where(Address.state == "California")
            .where(User.first_name == "Rohtash")
        )
        roh_address = session.scalars(stmt).one()
        print(f"roh_address\n{roh_address}")
        roh_address.street2 = "roh@sqlalchemy.org"
        print(f"After update roh_address\n{roh_address}")

        # add new address
        stmt = select(User).where(User.first_name == "Sangita")
        san = session.scalars(stmt).one()
        print(f"san\n{san}")
        san.addresses.append(
            Address(
                street1="Mission Creek",
                city="Fremont",
                state="California",
                country="US",
                zip="94536"
            )
        )

        # stmt = select(User).where(User.first_name == "Sangita")
        print(f"san.addresses\n{san.addresses}")
        session.commit()
        print()

    def delete_record(self):
        print(f"delete_record\n")
        from sqlalchemy import select
        session = Session(self.engine)

        stmt = select(Address).where(Address.zip == "94536")
        san_address = session.scalars(stmt).one()
        print(f"san_address\n{san_address}")
        print()

        san = session.get(User, 2)
        print(f"san\n{san}")
        print()

        print(f"deleting address: {san_address.id}")
        san.addresses.remove(san_address)
        session.flush()

        print(f"Deleting User:\n{san}")
        session.delete(san)
        session.commit()
        print()


if __name__ == '__main__':
    # sqlalchemy.__version__
    sqlAlchemy = SqlAlchemy()
    sqlAlchemy.create_database()
    sqlAlchemy.populate_database()
    sqlAlchemy.fetch_records()
    sqlAlchemy.fetch_with_joins()
    sqlAlchemy.update_records()
    sqlAlchemy.delete_record()
