import requests
import json
import math


class RMPScraper:

    def __init__(self, school_id, department, num_of_prof):
        self.school_id = school_id
        self.department = department
        self.professors = self.create_professor_list(num_of_prof)
        self.check = False

    def format_department(self):
        if " " in self.department:
            temp_department = self.department.split(" ")
            return "%20".join(temp_department)
        return "%20" + self.department

    def create_professor_list(self, num_of_prof):
        professor_list = []
        pages = math.ceil(num_of_prof / 20)

        for i in range(1, pages + 1):
            page = requests.get("https://www.ratemyprofessors.com/find/professor/?department=" + str(
                self.format_department()) + "&institution=University+of+California+Irvine&page=" + str(
                i) + "&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(self.school_id) + "&sortBy=")
            temp_jsonpage = json.loads(page.content)
            temp_list = temp_jsonpage['professors']
            for x in temp_list:
                if x['tDept'] == self.department and x['overall_rating'] != 'N/A':
                    professor_list.append(x)
        return professor_list

    def check_professor(self, name):
        name = name.split(" ")
        for i in range(len(self.professors)):
            if name[0].lower() == self.professors[i]['tFname'].lower():
                if name[-1].lower() == self.professors[i]['tLname'].lower():
                    return i
                elif name[-1].lower() in self.professors[i]['tLname'].lower():
                    return i
            elif name[0][0].lower() == self.professors[i]['tFname'][0].lower():
                if name[-1].lower() == self.professors[i]['tLname'].lower():
                    return i
                elif name[-1].lower() in self.professors[i]['tLname'].lower():
                    return i
            elif name[0].lower() == self.professors[i]['tLname'].lower() and name[-1].lower() == self.professors[i]['tFname'].lower():
                return i
        return False

    def output(self, name):
        self.check = self.check_professor(name)
        if self.check is False:
            return 'N/A'
        return f"{name}'s Rating: {self.professors[self.check]['overall_rating']} - Number of Ratings: {self.professors[self.check]['tNumRatings']}"


# number of Computer Science professors: w N/A = 95 | w/o N/A = 82
# number of Informatics professors: w N/A = 31 | w/o N/A = 29
# number of Statistics professors: w N/A = 25 | w/o N/A = 21
# number of Education professors: w N/A = 84 | w/o N/A = 77
# number of Information Science professors: w N/A = 8-10 | w/o N/A = 5

if __name__ == '__main__':
    cs = RMPScraper(1074, 'Computer Science', 95)
    inf = RMPScraper(1074, 'Informatics', 31)
    stats = RMPScraper(1074, 'Statistics', 25)
    educ = RMPScraper(1074, 'Education', 84)
    information = RMPScraper(1074, 'Information Science', 10)

    # Length of Professor Lists by Department
    print(len(cs.professors))
    print(len(inf.professors))
    print(len(stats.professors))
    print(len(educ.professors))
    print(len(information.professors))

    # Computer Science/ICS Professors
    print(cs.output('Michael Carey'))
    print(cs.output('Sharad Mehrotra'))
    print(cs.output('Jennifer Lee Wong-ma'))
    print(cs.output('Sergio Gago Masague'))
    print(cs.output('Raymond O. Klefstad'))
    print(cs.output('Stephan M Mandt'))
    print(cs.output('Gopi Meenakshisundaram'))
    print(cs.output('Adriaan Van Der Hoek'))
    print(cs.output('Steven Franklin'))
    print(cs.output('Zhao Shuang'))
    print(cs.output('Michael Shindler'))
    print(cs.output('Elaheh Bozorgzadeh'))

