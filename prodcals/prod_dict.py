class ProdDict(dict):
    def is_value(self, day):
        if day.year in self.keys() and day.month in self[day.year].keys():
            if day.day in self[day.year][day.month]:
                return True
        return False

        '''
        path = self[day.year][day.month] if day.year in self.keys() else ''
        if path:
            if day.day in path:
                return True
            else:
                return False
        '''