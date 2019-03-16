from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from showroom_database import Showroom, Base, Bike, User

engine = create_engine('sqlite:///bikewala.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
User1 = User(
    name="Revanth Mandava",
    email="revanth.mandava007@gmail.com",
    picture="https://lh3.googleusercontent.com/a-"
    "/AAuE7mCZfJuZMDXynsUcR-n63Utx6sW8CKJn9oMlQMxqvQ=s96"
    )
session.add(User1)
session.commit()

#

showroom1 = Showroom(name="Royal Enfield", user_id=1)
session.add(showroom1)
session.commit()

# clasic 350  info
bike1 = Bike(
              bike_name="Royal Enfield clasic 350",
              about="Classic 350 commuter mimics elder sibling"
              "Classic 500 when it comes to styling, or to put"
              "it this way, it can be referred as the smaller"
              "version of the latter. Donning the retro design,"
              "the commuter bike is reminiscent of classic"
              "machines from yesteryears.Power generation"
              "is done by a UCE engine displacing 346cc."
              "Outputting decent power and torque, the engine"
              "yields reasonable mileage. On the performance"
              "front, Classic 350 does well, offering great"
              "ride quality.",
              millage="37 Kmpl",
              engine_capacity="346.0 CC",
              max_power="19.80 bhp @ 5250 rpm",
              Transmission="5 speed",
              kerb_weight="195kg",
              price="₹ 1.45 Lakh On-Road Price ",
              bike_id=1,
              user_id=1
            )
session.add(bike1)
session.commit()

# classic 500 info
bike2 = Bike(
    bike_name="Royal Enfield clasic 500",
    about="The standard model lacks pillion seat, there is only"
    "a single seat for the rider. However the pillion seat can be availed"
    "as a part of accessories. The rounded headlamp cluster features"
    "‘Tiger eye lamps’ which lends it bullet like stance, moreover"
    "the halogen bulbs produce ample light to guide riders during"
    "RE offers the vintage look silencer on the bike as"
    "an additional accessory. In tandem with the rest of the"
    "styling, the tail lamps too feature a classic design ",
    millage="25.5 kmpl",
    engine_capacity="499.0 CC",
    max_power="27.20 bhp @ 5250 rpm",
    Transmission="5 speed",
    kerb_weight="194kg",
    price="₹ 1.9 Lakh On-Road Price ",
    bike_id=1,
    user_id=1)
session.add(bike2)
session.commit()

# thunderbird 350x info
bike3 = Bike(
    bike_name="Royal Enfield Thunderbird 350X",
    about="The Royal Enfield Thunderbird 350X offers"
    "a host of features that are first-of-its-kind"
    " on a Royal Enfield like -"
    "new matte black alloy wheels instead of wire-spoked"
    "wheels, tubeless tyres, and a matte black silencer."
    "The bikes also come with a new handlebar,"
    "black casing for the projector headlamps and LED"
    "taillamps and a new one-piece seat instead"
    "of the split seats from the standard Thunderbird. ",
    millage="35.5 kmpl",
    engine_capacity="499.0 CC",
    max_power="19.80 bhp @ 5250 rpm",
    Transmission="5 speed",
    kerb_weight="194kg",
    price="₹ ₹ 1.7 Lakh On-Road Price  ",
    bike_id=1,
    user_id=1)
session.add(bike3)
session.commit()

# Royal Enfield Interceptor 650 info
bike4 = Bike(
    bike_name="Royal Enfield Interceptor",
    about="The Royal Enfield 650 Twins are based on the brand new 649 cc,"
    "air and oil cooled, parallel-twin engine that belts out 47 bhp at 7250"
    "rpm and 52 Nm of peak torque at 5250 rpm. About 80 per cent of the torque"
    "is available from 2500 rpm and a flat torque curve results in ample power"
    "all thee way till about 6000 rpm. Sending power to the rear wheels is"
    "a 6-speed gearbox that comes with a slipper clutch, for a lighter lever"
    "operation. The bikes are capable of speeds in excess of 160 kmph.",
    millage="25.5 Kmpl",
    engine_capacity="648.0 CC",
    max_power="47.00 bhp @ 7250 rpm",
    Transmission="6 speed",
    kerb_weight="202kg",
    price="₹ 2.78 Lakh On-Road Price ",
    bike_id=1,
    user_id=1)
session.add(bike4)
session.commit()


# jawa
showroom2 = Showroom(name="jawa", user_id=1)
session.add(showroom2)
session.commit()

# jawa 300
bike1 = Bike(
     bike_name="jawa 300",
     about="Jawa has revealed little about its all-new motorcycle,"
     "but we do know that it will be powered by an"
     "all-new 293 cc single cylinder liquid cooled DOHC"
     "engine that has been tuned to offer a maximum"
     "output of 27 bhp and develop 28 Nm of torque."
     "The company claims that the engine will offer a"
     "generous mid-range and a flat torque curve for an unwavering,"
     "consistently powered ride, and it has been built on"
     "a BS6 ready platform.",
     millage="35.5 kmpl",
     engine_capacity="293.0 CC",
     max_power="27.00 bhp @ rpm",
     Transmission="6 speed",
     kerb_weight="170kg",
     price="₹ 1.78 Lakh On-Road Price ",
     bike_id=2,
     user_id=1
     )
session.add(bike1)
session.commit()

# jawa fourty two
bike2 = Bike(
    bike_name="jawa 42",
    about="Jawa has revealed little about its all-new motorcycle,"
    "but we do know that it will be powered by an all-new 293 cc single"
    "cylinder liquid cooled DOHC engine that has been tuned to offer a maximum"
    "output of 27 bhp and develop 28 Nm of torque. The company claims that the"
    "engine will offer a generous mid-range and a"
    "flat torque curve for an unwavering,"
    "consistently powered ride,and it has been"
    "built on a BS6 ready platform.",
    millage="35.5 kmpl",
    engine_capacity="293.0 CC",
    max_power="27.00 bhp @ rpm",
    Transmission="6 speed",
    kerb_weight="170kg",
    price="₹ 1.69 Lakh On-Road Price ",
    bike_id=2,
    user_id=1)
session.add(bike2)
session.commit()

# JAWA Perak
bike3 = Bike(
    bike_name="jawa  Perak",
    about="Jawa has revealed little about its all-new motorcycle,"
    " but we do know that it will be powered by an all-new 293 cc"
    "single cylinder liquid cooled DOHC engine that has been tuned to"
    "offer a maximum output of 27 bhp and develop 28 Nm of torque."
    "The company claims that the engine will offer a generous mid-range"
    "and a flat torque curve for an unwavering, consistently powered ride,"
    "and it has been built on a BS6 ready platform.",
    millage="25.5 kmpl",
    engine_capacity="348.0 CC",
    max_power="27.00 bhp @ rpm",
    Transmission="6 speed",
    kerb_weight="190kg",
    price="₹ 2.15 Lakh On-Road Price ",
    bike_id=2,
    user_id=1)
session.add(bike3)
session.commit()
# indian motorcycles
showroom3 = Showroom(name="indian motorcycles", user_id=1)
session.add(showroom3)
session.commit()

# Indian Scout Sixty
bike1 = Bike(
     bike_name="Indian Scout Sixty",
     about="The Indian Scout Sixty is the most affordable motorcycle"
     "in the manufacturer’s line up. The motorcycle has been introduced"
     "to directly take on the Harley-Davidson Sportster range."
     "This motorcycle is also targeted towards enthusiasts looking to"
     " get into the Indian brand or into cruisers motorcycles.",
     millage="15.5 kmpl",
     engine_capacity="999.0 CC",
     max_power="88.8 Nm @ 5,800 rpm",
     Transmission="5 speed",
     kerb_weight="280kg",
     price="₹ 10,99,500 Lakh On-Road Price ",
     bike_id=3,
     user_id=1
     )
session.add(bike1)
session.commit()


# Indian chief classic
bike2 = Bike(
     bike_name="Indian chief classic",
     about="The Indian chief classic the most affordable motorcycle"
     "in the manufacturer’s line up. The motorcycle has been introduced"
     "to directly take on the Harley-Davidson Sportster range."
     "This motorcycle is also targeted towards enthusiasts looking to get"
     "into the Indian brand or into cruisers motorcycles.",
     millage="15.5 kmpl",
     engine_capacity="1826.0 CC",
     max_power="88.8 Nm @ 5,800 rpm",
     Transmission="5 speed",
     kerb_weight="280kg",
     price="₹ 22,99,500 Lakh On-Road Price ",
     bike_id=3,
     user_id=1)
session.add(bike2)
session.commit()


# Indian FTR 1200
bike3 = Bike(
    bike_name="Indian FTR 1200",
    about="The Indian FTR 1200 is a flat-track motorcycle that is based"
    "on the manufacturer championship-winning FTR 750 race bike."
    "The motorcycle"
    "has being offered in two variants – FTR 1200 S and the"
    "FTR 1200 Race Replica."
    "The motorcycle was first unveiled during the 2018 Intermot in Germany.",
    millage="18.5 kmpl",
    engine_capacity="1203.0 CC",
    max_power="88.8 Nm @ 5,800 rpm",
    Transmission="5 speed",
    kerb_weight="190kg",
    price="₹ 16,99,500 Lakh On-Road Price ",
    bike_id=3, user_id=1)
session.add(bike3)
session.commit()
print("list of showrooms are added!!!")
