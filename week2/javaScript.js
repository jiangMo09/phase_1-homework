// task 1

console.log("--------------------task 1------------------------");
const metroMap = {
  songshan: { self: [0, 0] },
  nanjing: { sanmin: { self: [1, 0] }, fuxing: { self: [3, 0] } },
  taipei: { arena: { self: [2, 0] } },
  songjiang: { nanjing: { self: [4, 0] } },
  zhonshan: { self: [5, 0] },
  beimen: { self: [6, 0] },
  ximen: { self: [7, 0] },
  xiaonanmen: { self: [8, 0] },
  chiang: { "kai-shek": { memorial: { hall: { self: [9, 0] } } } },
  guting: { self: [10, 0] },
  taipower: { building: { self: [11, 0] } },
  gongguan: { self: [12, 0] },
  wanlong: { self: [13, 0] },
  jingmei: { self: [14, 0] },
  dapinglin: { self: [15, 0] },
  qizhang: { self: [16, 0] },
  xiaobitan: { self: [16, 1] },
  xindian: { self: [18, 0], city: { hall: { self: [17, 0] } } }
};

function findAndPrint(messages, currentStation) {
  const currentIdx = getStationIdx(
    currentStation.toLowerCase().split(" "),
    metroMap
  );
  let nearDistance;
  let closestPerson;

  for (user in messages) {
    const wordArr = messages[user].toLowerCase().split(/[ .]/);
    const stationIdx = getStationIdx(wordArr, metroMap);
    const distance =
      Math.abs(currentIdx[0] - stationIdx[0]) +
      Math.abs(currentIdx[1] - stationIdx[1]);
    if (nearDistance === undefined || distance < nearDistance) {
      nearDistance = distance;
      closestPerson = user;
    }
  }
  console.log(closestPerson);
  return;
}

function getStationIdx(wordArr, metroMap) {
  let current = metroMap;
  for (let i = 0; i < wordArr.length; i++) {
    if (wordArr[i] in current && wordArr[i + 1] in current[wordArr[i]]) {
      current = current[wordArr[i]];
    } else if (wordArr[i] in current) {
      return current[wordArr[i]].self;
    }
  }
}

const messages = {
  Bob: "I'm at Ximen MRT station.",
  Mary: "I have a drink near Jingmei MRT station.",
  Copper: "I just saw a concert at Taipei Arena.",
  Leslie: "I'm at home near Xiaobitan station.",
  Vivian: "I'm at Xindian station waiting for you."
};
findAndPrint(messages, "Wanlong"); // print Mary
findAndPrint(messages, "Songshan"); // print Copper
findAndPrint(messages, "Qizhang"); // print Leslie
findAndPrint(messages, "Ximen"); // print Bob
findAndPrint(messages, "Xindian City Hall"); // print Vivian

// task 2
console.log("--------------------task 2------------------------");
const consultantsMap = new Map();
function isFreeTime(schedule, hour, duration) {
  for (let i = hour; i < hour + duration; i++) {
    if (schedule.has(i)) {
      return false;
    }
  }

  return true;
}

function book(consultants, hour, duration, criteria) {
  consultants.sort((a, b) => {
    if (criteria === "price") {
      return a.price - b.price;
    }
    if (criteria === "rate") {
      return b.rate - a.rate;
    }
  });

  for (const consultant of consultants) {
    const schedule = consultantsMap.get(consultant.name) || new Set();

    if (isFreeTime(schedule, hour, duration)) {
      for (let i = hour; i < hour + duration; i++) {
        schedule.add(i);
      }
      consultantsMap.set(consultant.name, schedule);
      console.log(consultant.name);
      return;
    }
  }

  console.log("No Service");
}
const consultants = [
  { name: "John", rate: 4.5, price: 1000 },
  { name: "Bob", rate: 3, price: 1200 },
  { name: "Jenny", rate: 3.8, price: 800 }
];
book(consultants, 15, 1, "price"); // Jenny
book(consultants, 11, 2, "price"); // Jenny
book(consultants, 10, 2, "price"); // John
book(consultants, 20, 2, "rate"); // John
book(consultants, 11, 1, "rate"); // Bob
book(consultants, 11, 2, "rate"); // No Service
book(consultants, 14, 3, "price"); // John

// task 3
console.log("--------------------task 3------------------------");
const getMiddleLetter = (name) => {
  const middleIndex = Math.floor(name.length / 2);
  return name[middleIndex];
};

function func(...data) {
  if (data.length === 0) {
    console.log("沒有");
    return;
  }

  const namesMap = new Map();

  for (const name of data) {
    const middleLetter = getMiddleLetter(name);
    const isMiddleLetterAvailable = namesMap.get(middleLetter);
    namesMap.set(middleLetter, isMiddleLetterAvailable ? "" : name);
  }
  for (const nameSet of namesMap) {
    if (nameSet[1] != "") {
      console.log(nameSet[1]);
      return;
    }
  }

  console.log("沒有");
}
func("彭大牆", "陳王明雅", "吳明"); // print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花"); // print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花"); // print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆"); // print 夏曼藍波安

// task 4
console.log("--------------------task 4------------------------");
function getNumber(index) {
  if (index === 0) {
    console.log(0);
    return;
  }

  if (index < 0 || !Number.isInteger(index)) {
    console.log("index 不得為非正整數");
    return;
  }

  const remainder = index % 3;
  const groups = Math.floor(index / 3);

  const result = 7 * groups + remainder * 4;
  console.log(result);
}
getNumber(1); // print 4
getNumber(5); // print 15
getNumber(10); // print 25
getNumber(30); // print 70

// task5
console.log("--------------------task 5------------------------");
function find(spaces, stat, n) {
  let minSpaces = Infinity;
  let fittestIdx = -1;

  for (i in spaces) {
    if (stat[i] === 1 && spaces[i] == n) {
      console.log(i);
      return;
    }

    if (stat[i] === 1 && spaces[i] > n) {
      if (spaces[i] < minSpaces) {
        minSpaces = spaces[i];
        fittestIdx = i;
      }
    }
  }

  console.log(fittestIdx);
}
find([3, 1, 5, 4, 3, 2], [0, 1, 0, 1, 1, 1], 2); // print 5
find([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4); // print -1
find([4, 6, 5, 8], [0, 1, 1, 1], 4); // print 2
