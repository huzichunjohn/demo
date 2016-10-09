class AzureTable(object):
    def __init__(self, url, row=None, col=None, level='table'):
        self.__url = url
        self.__row = row
        self.__col = col
        self.__level = level
        print self.__url, self.__row, self.__col, self.__level

    def _fetch(self):
        assert self.__level == 'col'
        print '*** Downloading from\n\t"{}/{}/{}"'.format(self.__url, self.__row, self.__col)
        print '*** Downloading Complete'
        return "Hello Pycon 2016: {}.{}".format(self.__row, self.__col)

    def __getattr__(self, item):
        print item
        if self.__level == "table":
            return AzureTable(self.__url, row=item, level='row')
        elif self.__level == "row":
            return AzureTable(self.__url, row=self.__row, col=item, level='col')

        if item == 'data':
            return self._fetch()

students = AzureTable('user1.storage.azure.com/table/students')
print "-" * 10, "start", "-" *10
print students.xiaoMing.Address.data
print '-' * 30
print students.Jim.brithday.data
print "-" * 10, "end", "-" *10
