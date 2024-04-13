# task1
print("--------------------task 1------------------------")
greenLine = [
    "songshan",
    "nanjing sanmin",
    "nanjing fuxing",
    "taipei arena",
    "songjiang nanjing",
    "zhonshan",
    "beimen",
    "ximen",
    "xiaonanmen",
    "chiang kai-shek memorial hall",
    "guting",
    "taipower building",
    "gongguan",
    "wanlong",
    "jingmei",
    "dapinglin",
    "qizhang",
    "xindian city hall",
    "xindian",
]

limeLine = [
    "qizhang",
    "xiaobitan",
]

stations_list = list(set(greenLine + limeLine))


class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = set()

    def add_edge(self, node1, node2):
        if node1 not in self.graph:
            self.add_node(node1)
        if node2 not in self.graph:
            self.add_node(node2)
        self.graph[node1].add(node2)
        self.graph[node2].add(node1)

    def bfs(self, start, end):
        visited = {start}
        queue = [(start, 0)]

        while queue:
            current_node, distance = queue.pop(0)

            if current_node == end:
                return distance

            for neighbor in self.graph[current_node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, distance + 1))

        return None


subway_map = Graph()
for i in range(len(greenLine)):
    subway_map.add_node(greenLine[i])
for i in range(len(limeLine)):
    subway_map.add_node(greenLine[i])
for i in range(len(greenLine) - 1):
    subway_map.add_edge(greenLine[i], greenLine[i + 1])
for i in range(len(limeLine) - 1):
    subway_map.add_edge(limeLine[i], limeLine[i + 1])


def find_and_print(messages, station):
    shortest_distance = float("inf")
    closest_person = None
    for person, message in messages.items():
        for station_name in stations_list:
            if station_name in message.lower():
                distance = subway_map.bfs(station.lower(), station_name)
                if distance is not None and distance < shortest_distance:
                    shortest_distance = distance
                    closest_person = person

    print(closest_person)


messages = {
    "Bob": "I'm at Ximen MRT station.",
    "Mary": "I have a drink near Jingmei MRT station.",
    "Copper": "I just saw a concert at Taipei Arena.",
    "Leslie": "I'm at home near Xiaobitan station.",
    "Vivian": "I'm at Xindian station waiting for you.",
}

find_and_print(messages, "Wanlong")  # print Mary
find_and_print(messages, "Songshan")  # print Copper
find_and_print(messages, "Qizhang")  # print Leslie
find_and_print(messages, "Ximen")  # print Bob
find_and_print(messages, "Xindian City Hall")  # print Vivian


#  task2
print("--------------------task 2------------------------")
consultants_map = {}


def is_free_time(schedule, hour, duration):
    for i in range(hour, hour + duration):
        if i in schedule:
            return False
    return True


def book(consultants, hour, duration, criteria):
    consultants.sort(
        key=lambda x: x[criteria], reverse=True if criteria == "rate" else False
    )

    for consultant in consultants:
        schedule = consultants_map.get(consultant["name"], set())

        if is_free_time(schedule, hour, duration):
            for i in range(hour, hour + duration):
                schedule.add(i)
            consultants_map[consultant["name"]] = schedule
            print(consultant["name"])
            return

    print("No Service")


consultants = [
    {"name": "John", "rate": 4.5, "price": 1000},
    {"name": "Bob", "rate": 3, "price": 1200},
    {"name": "Jenny", "rate": 3.8, "price": 800},
]

book(consultants, 15, 1, "price")  # Jenny
book(consultants, 11, 2, "price")  # Jenny
book(consultants, 10, 2, "price")  # John
book(consultants, 20, 2, "rate")  # John
book(consultants, 11, 1, "rate")  # Bob
book(consultants, 11, 2, "rate")  # No Service
book(consultants, 14, 3, "price")  # John

#  task3
print("--------------------task 3------------------------")


def getMiddleLetter(name):
    middleIndex = len(name) // 2
    return name[middleIndex]


def func(*data):
    if len(data) == 0:
        print("沒有")
        return

    hashMap = {}
    for name in data:
        middleLetter = getMiddleLetter(name)
        hashMap[middleLetter] = hashMap.get(middleLetter, 0) + 1

    for name in data:
        middleLetter = getMiddleLetter(name)
        if hashMap[middleLetter] == 1:
            print(name)
            return

    print("沒有")


func("彭大牆", "陳王明雅", "吳明")  # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花")  # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花")  # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆")  # print 夏曼藍波安

#  task4
print("--------------------task 4------------------------")


def getNumber(index):
    if index == 0:
        print(0)
        return

    if index < 0 or not isinstance(index, int):
        print("index 不得為非正整數")
        return

    remainder = index % 3
    groups = index // 3

    result = 7 * groups
    if remainder == 1:
        result += 4
    if remainder == 2:
        result += 8

    print(result)


getNumber(1)  # print 4
getNumber(5)  # print 15
getNumber(10)  # print 25
getNumber(30)  # print 70


#  task5
print("--------------------task 5------------------------")


def find(spaces, stat, n):
    hashMap = {}
    for i in range(len(spaces)):
        if stat[i] == 1:
            hashMap[i] = spaces[i]

    minusMap = {}
    closestCabinValue = n
    closestCabinIndex = -1
    for key, value in hashMap.items():
        if value == n:
            print(key)
            return

        minusMap[key] = value - n

    for key, value in minusMap.items():
        if value > 0 and value < closestCabinValue:
            closestCabinIndex = key
            closestCabinValue = value

    print(closestCabinIndex)


find([3, 1, 5, 4, 3, 2], [0, 1, 0, 1, 1, 1], 2)  # print 5
find([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4)  # print -1
find([4, 6, 5, 8], [0, 1, 1, 1], 4)  # print 2

