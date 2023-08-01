class Vacancy:
    def __init__(self, name, salary_from, salary_to, url, info, responsibility):
        self.name = name
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.url = url
        self.info = info
        self.responsibility = responsibility

    def __repr__(self):
        return self.name
