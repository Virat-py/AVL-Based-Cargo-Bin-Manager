with open('data.txt', 'r') as file:
    lines = [line.strip() for line in file.readlines()]
    lines=lines[2:]
    newlines=[i.split(",") for i in lines]
    for message,fingers,tail,species in newlines:
        temp=message.split()
        s=set(species)
        for i in temp:
            if set(i).isdisjoint(s):
                print(i,fingers,tail,species)
