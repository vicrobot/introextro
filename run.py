import random
from numpy.random import choice
from termcolor import colored

universe = (-10, 10)
launch_int = (5,7)
people_rad = 3
num_persons = 10
frames_num = 10

class people:
    def __init__(self, x, y, lr, im, om, identity):
        self.x = x
        self.y = y
        self.lr = lr #launching resistance
        self.im = im #intake mag. (this'll be prob of it accepting the intent)
        self.om = om #outgive mag. (this'll be prob of it giving the intent)
        self.id = identity
        self.outgiving = False
        self.old_coords = []
        self.friends = dict([]) #ids with intensity of ids(increases by 1 on each repeated meet
                             #here a lot of stuffs can be made to happen like person granting subset of
                             #friends of friends and making them their own friend and stuffs like points
                             #being always outgiving and intaking for already friends etc etc.
    def move(self, new_x, new_y):
        self.x, self.y = new_x, new_y
    def get_coords(self):
        return (self.x, self.y) #or simply do instance.x, instance.y

"""
randrange(start, stop=None, step=1, _int=<class 'int'>) method of random.Random instance
    Choose a random item from range(start, stop[, step]).
    
    This fixes the problem with randint() which includes the
    endpoint; in Python this is usually not what you want.

"""
def generate_persons():
    return [people(random.randrange(*universe), random.randrange(*universe), random.randrange(0,5), 
            round(random.random(), 2), round(random.random(), 2), i+1) for i in range(num_persons)]

def launch_person(person_list):
    launch_mag = random.randint(*launch_int)
    for person in person_list:
        net = launch_mag - person.lr
        random_ax = random.randint(0,1) #0 for x, 1 for y axis
        random_dir = random.choice([-1,1]) #backward or forward motion
        #print(f"person_id: {person.id}")
        old_coords = person.get_coords()
        #print(f"old_coords: {old_coords}")
        #print(f"net: {net}")
        #print(f"random_ax: {random_ax}\nrandom_dir: {random_dir}")
        temp_x = person.x + random_dir*net
        temp_y = person.y + random_dir*net
        if random_ax == 0:
            if random_dir == 1: person.x = temp_x if temp_x <=  universe[1] else person.x
            else: person.x = temp_x if temp_x >= universe[0] else person.x
        else:
            if random_dir == 1: person.y = temp_y if temp_y <=  universe[1] else person.y
            else: person.y = temp_y if temp_y >= universe[0] else person.y
        new_coords = person.get_coords()
        #print(f"new_coords: {new_coords}")
        #if old_coords!= new_coords:
        person.old_coords.append(old_coords)
        #print(colored("Person moved", "green"))

def outgive(person_list):
    for person in person_list:
        person.outgiving = choice([True, False], p = [person.om, 1-person.om])

def coord_collector(point_coord, rad):
    """
    Collect squares that are fully inside a circle neighborhood(including itself) of radius "rad".
    idk if its a correct in-circle point integral coord collector, but its working method is below defined
    """
    """
    Works in integer world.
    So suppose you've a point: a,b and radius is r then ill settle on x axis, will cover
    both -ve and +ve dirs with r units and include them. Now ill decrease r by 1 and  will do same
    but on y + 1 and on y - 1 and so on.
    """
    coord_list = []
    r = rad
    x,y = point_coord
    for i in range(r+1):
        if i == 0:
            for j in range(x-r, x+r+1): coord_list.append((j,y))
        else:
            for j in range(x-(r-i), x+(r-i)+1):
                coord_list.append((j, y+i))
                coord_list.append((j,y-i))
    return coord_list

def intake(person_list):
    person_list_copy = person_list.copy()
    for person in person_list:
        for neighb in person_list:
            neighb_coords = neighb.get_coords()
            if neighb_coords != person.get_coords():
                if sum(map(abs, neighb_coords)) <= people_rad:
                    accepting_status = choice(["accepted","rejected"], p = [neighb.im, 1-neighb.im])
                    if accepting_status == "accepted":
                        already_exists = neighb.friends.get(person.id)
                        if already_exists == None:
                            neighb.friends[person.id] = 1
                            person.friends[neighb.id] = 1
                        else:
                            neighb.friends[person.id] += 1
                            person.friends[neighb.id] += 1
        

if __name__ == "__main__":
    for i in range(frames_num+1):
        if not i: person_list = generate_persons()
        else: launch_person(person_list)#generates lr and launches points to new coords
        outgive(person_list) #randomly(by om prob) generate outgiving status in "outgiving" attribute.
        intake(person_list)  #accept an in-rad announcement by scanning on outgiving=true persons
                             #in people_rad radius and change both's data of friendlist.
    if frames_num >= 1:
        import matplotlib.pyplot as plt
        for person in person_list:
            print(f"person_id: {person.id}")
            indentation = " "*4
            if person.im < person.om:
                print(indentation+"person is genetically "+ colored("extrovert", "green"))
            else: print(indentation+"person is genetically "+ colored("introvert","green"))
            print(indentation+f"coords: {person.get_coords()}")
            print(indentation+f"person_friends: {person.friends}")
            print(indentation+f"old_coords: {person.old_coords}")
            person_coords = person.get_coords()
            for k,v in person.friends.items():
                plt.plot(person_coords, (person_list[k-1]).get_coords())
        plt.show()












































