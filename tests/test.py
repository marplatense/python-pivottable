# -*- coding: UTF-8 -*-
import datetime
from random import shuffle
from nose.tools import eq_, raises, assert_raises

from pivottable import (
PivotTable, GroupBy, Sum
)
from pivottable.pivottable import PivotTableError

class TestError(Exception):
    pass

class DummyData(object):

    def __init__(self, team, city, period, won, drawn, lost):
        self.team = team
        self.city = city
        self.period = period
        self.won = won
        self.drawn = drawn
        self.lost = lost

    @property
    def played(self):
        return self.won+self.drawn+self.lost

    @property
    def points(self):
        return self.won*3+self.drawn*1

    @property
    def effectivity(self):
        try:
            return float(self.won)/float(self.played)
        except ZeroDivisionError:
            return float(0)

    def __repr__(self):
        return "<DummyData: %s, %s, %s>" % (self.team.encode('utf-8'), 
                                            self.city.encode('utf-8'), 
                                            self.period)

class GenericObject(object):

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)

    def __repr__(self):
        return "Values: <%s>" % (", ".join([str(getattr(self, a)) for a in \
                                            dir(self) if not a.startswith('_')]))

def percent(value):
    return u'%.2f%%' % (value*100)

def year_month(value):
    return value.strftime("%b-%y")

class TestPivot_A(object):

    pt = PivotTable()
    pt.rows = [
        GenericObject(**{'name':u'Asia', 'population':3879000000,
                         'area':44579000}),
        GenericObject(**{'name':u'North America', 'population':528720588,
                         'area':24709000}),
        GenericObject(**{'name':u'Africa', 'population':1000010000,
                         'area':30221532}),
        GenericObject(**{'name':u'Antarctica', 'population':1000,
                         'area':1400000}),
        GenericObject(**{'name':u'Europe', 'population':731000000,
                         'area':10180000}),
        GenericObject(**{'name':u'South America', 'population':385742554,
                         'area':17840000})
    ]
    pt.xaxis = "name"
    pt.xaxis_sort = True
    pt.yaxis = [
        {'attr':u'population', 'label':u'Population', 'aggr':Sum},
        {'attr':u'area', 'label':u'Area', 'aggr':Sum}]

    def test_AA_data(self):
        eq_(self.pt.headers, ["metric", "Africa", "Antarctica", "Asia",
                              "Europe", "North America", "South America"])

    def test_AB_results(self):
        eq_([a for a in self.pt.result], [
            [u"metric", u"Africa", u"Antarctica", u"Asia", u"Europe", 
             u"North America", u"South America"],
            [u"Population", u'1000010000', u'1000', u'3879000000', u'731000000',
             u'528720588', u'385742554'],
            [u"Area", u'30221532', u'1400000', u'44579000', u'10180000', 
             u'24709000', u'17840000']
        ])

class TestPivot_B(object):

    pt = PivotTable()
    pt.rows = [
        GenericObject(**{'country':u'Uruguay', 'year':1930, 'champion':u'x',
                         'runnerup':None}),
        GenericObject(**{'country':u'Argentina', 'year':1930,
                         'champion':None, 'runnerup':u'x'}),
        GenericObject(**{'country':u'Italy', 'year':1934, 'champion':u'x',
                         'runnerup':None}),
        GenericObject(**{'country':u'Czechoslovakia', 'year':1934, 
                         'champion':None, 'runnerup':u'x'}),
        GenericObject(**{'country':u'Italy', 'year':1938, 'champion':u'x',
                         'runnerup':None}),
        GenericObject(**{'country':u'Hungary', 'year':1938, 'champion':None,
                         'runnerup':u'x'}),
        GenericObject(**{'country':u'Uruguay', 'year':1950, 'champion':u'x',
                         'runnerup':None}),
        GenericObject(**{'country':u'Brazil', 'year':1950, 'champion':None,
                         'runnerup':u'x'}),
        GenericObject(**{'country':u'Germany', 'year':1954, 'champion':u'x',
                         'runnerup':None}),
        GenericObject(**{'country':u'Hungary', 'year':1954, 'champion':None,
                         'runnerup':u'x'}),
        GenericObject(**{'country':u'Brazil', 'year':1958, 'champion':u'x',
                         'runnerup':None}),
        GenericObject(**{'country':u'Sweden', 'year':1958, 'champion':None,
                         'runnerup':u'x'}),
        GenericObject(**{'country':u'Brazil', 'year':1962, 'champion':u'x',
                         'runnerup':None}),
        GenericObject(**{'country':u'Czechoslovakia', 'year':1962, 
                         'champion':None, 'runnerup':u'x'}),
        GenericObject(**{'country':u'England', 'year':1966, 'champion':u'x',
                         'runnerup':None}),
        GenericObject(**{'country':u'Germany', 'year':1966, 'champion':None,
                         'runnerup':u'x'}),
        GenericObject(**{'country':u'Brazil', 'year':1970, 'champion':u'x',
                         'runnerup':None}),
        GenericObject(**{'country':u'Italy', 'year':1970, 'champion':None,
                         'runnerup':u'x'}),
        GenericObject(**{'country':u'Germany', 'year':1974, 'champion':u'x',
                         'runnerup':None}),
        GenericObject(**{'country':u'Netherlands', 'year':1974, 
                         'champion':None, 'runnerup':u'x'}),
        GenericObject(**{'country':u'Argentina', 'year':1978,
                         'champion':u'x', 'runnerup':None}),
        GenericObject(**{'country':u'Netherlands', 'year':1978, 
                         'champion':None, 'runnerup':u'x'}),
        GenericObject(**{'country':u'Italy', 'year':1982, 'champion':u'x',
                         'runnerup':None}),
        GenericObject(**{'country':u'Germany', 'year':1982, 'champion':None,
                         'runnerup':u'x'}),
        GenericObject(**{'country':u'Argentina', 'year':1986,
                         'champion':u'x', 'runnerup':None}),
        GenericObject(**{'country':u'Germany', 'year':1986, 'champion':None,
                         'runnerup':u'x'}),
        GenericObject(**{'country':u'Germany', 'year':1990, 'champion':u'x',
                         'runnerup':None}),
        GenericObject(**{'country':u'Argentina', 'year':1990,
                         'champion':None, 'runnerup':u'x'}),
        GenericObject(**{'country':u'Brazil', 'year':1994, 'champion':u'x',
                         'runnerup':None}),
        GenericObject(**{'country':u'Italy', 'year':1994, 'champion':None,
                         'runnerup':u'x'}),
        GenericObject(**{'country':u'France', 'year':1998, 'champion':u'x',
                         'runnerup':None}),
        GenericObject(**{'country':u'Brazil', 'year':1998, 'champion':None,
                         'runnerup':u'x'}),
        GenericObject(**{'country':u'Brazil', 'year':2002, 'champion':u'x',
                         'runnerup':None}),
        GenericObject(**{'country':u'Germany', 'year':2002, 'champion':None,
                         'runnerup':u'x'}),
        GenericObject(**{'country':u'Italy', 'year':2006, 'champion':u'x',
                         'runnerup':None}),
        GenericObject(**{'country':u'France', 'year':2006, 'champion':None,
                         'runnerup':u'x'}),
        GenericObject(**{'country':u'Spain', 'year':2010, 'champion':u'x',
                         'runnerup':None}),
        GenericObject(**{'country':u'Netherlands', 'year':2010, 
                         'champion':None, 'runnerup':u'x'})
        ]
    pt.xaxis = "year"
    pt.xaxis_sort = True
    pt.yaxis = [
        {'attr':u'country', 'label':u'Country', 'aggr':GroupBy},
        {'attr':u'champion', 'label':u'Champion', 'aggr':Sum},
        {'attr':u'runnerup', 'label':u'Runner Up', 'aggr':Sum}
    ]
    pt.yaxis_order = ["country"]

    def test_BA_result(self):
        shuffle(self.pt.rows)
        all1 = self.pt.result
        all2 = [
            [u"country", u"metric", u"1930", u"1934", u"1938", u"1950", u"1954",
             u"1958", u"1962", u"1966", u"1970", u"1974", u"1978", u"1982",
             u"1986", u"1990", u"1994", u"1998", u"2002", u"2006", u"2010"],
            [u"Argentina", u"Champion", None, None, None, None, None, 
             None, None, None, None, None, u'x', None, 
             u'x', None, None, None, None, None, None], 
            [u"Argentina", u"Runner Up", u'x', None, None, None, None, 
             None, None, None, None, None, None, None, 
             None, u'x', None, None, None, None, None], 
            [u"Brazil", u"Champion", None, None, None, None, None, 
             u'x', u'x', None, u'x', None, None, None, 
             None, None, u'x', None, u'x', None, None], 
            [u"Brazil", u"Runner Up", None, None, None, u'x', None, 
             None, None, None, None, None, None, None, 
             None, None, None, u'x', None, None, None], 
            [u"Czechoslovakia", u"Champion", None, None, None, None, None, 
             None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None], 
            [u"Czechoslovakia", u"Runner Up", None, u'x', None, None, None, 
             None, u'x', None, None, None, None, None, 
             None, None, None, None, None, None, None], 
            [u"England", u"Champion", None, None, None, None, None, 
             None, None, u'x', None, None, None, None, 
             None, None, None, None, None, None, None], 
            [u"England", u"Runner Up", None, None, None, None, None, 
             None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None], 
            [u"France", u"Champion", None, None, None, None, None, 
             None, None, None, None, None, None, None, 
             None, None, None, u'x', None, None, None], 
            [u"France", u"Runner Up", None, None, None, None, None, 
             None, None, None, None, None, None, None, 
             None, None, None, None, None, u'x', None], 
            [u"Germany", u"Champion", None, None, None, None, u'x', 
             None, None, None, None, u'x', None, None, 
             None, u'x', None, None, None, None, None], 
            [u"Germany", u"Runner Up", None, None, None, None, None, 
             None, None, u'x', None, None, None, u'x', 
             u'x', None, None, None, u'x', None, None], 
            [u"Hungary", u"Champion", None, None, None, None, None, 
             None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None], 
            [u"Hungary", u"Runner Up", None, None, u'x', None, u'x', 
             None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None], 
            [u"Italy", u"Champion", None, u'x', u'x', None, None, 
             None, None, None, None, None, None, u'x', 
             None, None, None, None, None, u'x', None], 
            [u"Italy", u"Runner Up", None, None, None, None, None, 
             None, None, None, u'x', None, None, None, 
             None, None, u'x', None, None, None, None], 
            [u"Netherlands", u"Champion", None, None, None, None, None, 
             None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None], 
            [u"Netherlands", u"Runner Up", None, None, None, None, None, 
             None, None, None, None, u'x', u'x', None, 
             None, None, None, None, None, None, u'x'], 
            [u"Spain", u"Champion", None, None, None, None, None, 
             None, None, None, None, None, None, None, 
             None, None, None, None, None, None, u'x'], 
            [u"Spain", u"Runner Up", None, None, None, None, None, 
             None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None], 
            [u"Sweden", u"Champion", None, None, None, None, None, 
             None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None], 
            [u"Sweden", u"Runner Up", None, None, None, None, None, 
             u'x', None, None, None, None, None, None, 
             None, None, None, None, None, None, None], 
            [u"Uruguay", u"Champion", u'x', None, None, u'x', None, 
             None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None], 
            [u"Uruguay", u"Runner Up", None, None, None, None, None, 
             None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None]] 
        for i in enumerate(all1): 
            eq_(i[1], all2[i[0]])

class TestPivot_C(object):

    pt = PivotTable()
    pt.rows = [
    DummyData(u'Estudiantes', u'La Plata', datetime.date(2011,2,1), 14, 3,
              2),
    DummyData(u'Vélez Sársfield', u'Buenos Aires', datetime.date(2011,2,1),
              13, 4, 2),
    DummyData(u'Arsenal', u'Sarandí', datetime.date(2011,2,1), 9, 5, 5),
    DummyData(u'River Plate', u'Buenos Aires', datetime.date(2011,2,1), 8, 
              7, 4),
    DummyData(u'Godoy Cruz', u'Mendoza', datetime.date(2011,2,1), 7, 8, 4),
    DummyData(u'Banfield', u'Banfield', datetime.date(2009,12,13), 12, 5, 
              2),
    DummyData(u"Newell's Old Boys", u'Rosario', datetime.date(2009,12,13), 
              12, 3, 4),
    DummyData(u'Colón', u'Santa Fé', datetime.date(2009,12,13), 10, 4, 5),
    DummyData(u'Independiente', u'Avellaneda', datetime.date(2009,12,13), 
              10, 4, 5),
    DummyData(u'Vélez Sársfield', u'Buenos Aires', datetime.date(2009,12,13),
              10, 4, 5),
    DummyData(u'Argentinos Juniors', u'Buenos Aires',
              datetime.date(2010,5,23), 12, 5, 2),
    DummyData(u'Estudiantes', u'La Plata', datetime.date(2010,5,23), 12, 4,
              3),
    DummyData(u'Godoy Cruz', u'Mendoza', datetime.date(2010,5,23), 11, 4,
              3),
    DummyData(u'Independiente', u'Avellaneda', datetime.date(2010,5,23),
              10, 4, 5),
    DummyData(u'Banfield', u'Banfield', datetime.date(2010,5,23), 9, 5, 5),
    DummyData(u'San Lorenzo', u'Buenos Aires', datetime.date(2008, 12, 14),
              12, 3, 4),
    DummyData(u'Boca Juniors', u'Buenos Aires', datetime.date(2008,12,14), 
              12,3,4),
    DummyData(u'Tigre', u'Tigre', datetime.date(2008,12,14),12,3,4),
    DummyData(u'Lanús', u'Lanús', datetime.date(2008,12,14),11,4,4),
    DummyData(u"Newell's Old Boys", u'Rosario', datetime.date(2008,12,14),
              8,7,4),
    DummyData(u'Vélez Sársfield', u'Buenos Aires', 
              datetime.date(2009, 7,5), 11, 7, 1),
    DummyData(u'Huracán', u'Buenos Aires', datetime.date(2009,7,5),
              12,2,5),
    DummyData(u'Lanús', u'Lanús', datetime.date(2009,7,5), 12,2,5),
    DummyData(u'Colón', u'Santa Fé', datetime.date(2009,7,5), 10,4,5),
    DummyData(u'Racing', u'Avellaneda', datetime.date(2009,7,5), 8,6,5)
    ]

    def test_CA_xaxis_property(self):
        self.pt.xaxis = "period"
        self.pt.xaxis_sort = True
        try:
            self.pt.xaxis_format = u"hello world"
        except PivotTableError:
            pass
        else:
            raises(TestError("Assigning a non callable to xaxis_format should "
                             "raise an error"))
        self.pt.xaxis_format = year_month
        eq_(self.pt.xaxis_format(datetime.date(2010,1,1)), u"Jan-10")

    def test_CC_wrong_attr_xaxis(self):
        assert_raises(PivotTableError, setattr, self.pt, 'xaxis', u"johnny")
        eq_(self.pt.xaxis, "period")

    @raises(PivotTableError)
    def test_CD_yaxis_property(self):
        self.pt.yaxis = [
                {'hello':u'world', 'label':u'Team', 'aggr':GroupBy}]

    def test_CE_yaxis_property(self):
        self.pt.yaxis = [
                    {'attr':u'team', 'label':u'Team', 'aggr':GroupBy},
                    {'attr':u'city', 'label':u'City', 'aggr':GroupBy},
                    {'attr':u'won', 'label':u'Won', 'aggr':Sum},
                    {'attr':u'lost', 'label':u'Lost', 'aggr':Sum},
                    {'attr':u'drawn', 'label':u'Drawn', 'aggr':Sum},
                    {'attr':u'effectivity', 'label':u'Efectivity', 
                     'aggr':Sum, 'format':percent}]

    def test_CF_yaxis_order(self):
        self.pt.yaxis_order = [u'city', u'team']
        # let's check the headers: they must obey yaxis_order and, if declared, 
        # the sort order for xaxis 
        eq_(self.pt.headers, 
            [u'city', u'team', u'metric', datetime.date(2008, 12, 14),
             datetime.date(2009, 7, 5), datetime.date(2009, 12, 13),
             datetime.date(2010, 5, 23), datetime.date(2011, 2, 1)])

    @raises(PivotTableError)
    def test_CG_wrong_xaxis_attr(self):
        self.pt.xaxis = "hello_world"

    def test_CH_wrong_xaxis_attr(self):
        eq_(self.pt.xaxis, "period")

    @raises(AttributeError)
    def test_CI_headers_ro(self):
        self.pt.headers = ["These", "are", "my", "headers"]

    @raises(AttributeError)
    def test_CJ_result_ro(self):
        self.pt.result = ["This", "is", "my", "result"]

    def test_CK_result(self):
        all1 = self.pt.result
        all2 = [
         [u'city', u'team', u'metric', "Dec-08", "Jul-09", "Dec-09",
          "May-10", "Feb-11"], 
         [u'Avellaneda', u'Independiente', u'Won', None, None, u'10', u'10',
          None],
         [u'Avellaneda', u'Independiente', u'Lost', None, None, u'5', u'5',
          None],
         [u'Avellaneda', u'Independiente', u'Drawn', None, None, u'4', u'4',
          None],
         [u'Avellaneda', u'Independiente', u'Efectivity', None, None,
          u'52.63%', u'52.63%', None],
         [u'Avellaneda', u'Racing', u'Won', None, u'8', None, None, None],
         [u'Avellaneda', u'Racing', u'Lost', None, u'5', None, None, None],
         [u'Avellaneda', u'Racing', u'Drawn', None, u'6', None, None, None],
         [u'Avellaneda', u'Racing', u'Efectivity', None, u'42.11%', None, None,
          None],
         [u'Banfield', u'Banfield', u'Won', None, None, u'12', u'9', None],
         [u'Banfield', u'Banfield', u'Lost', None, None, u'2', u'5', None],
         [u'Banfield', u'Banfield', u'Drawn', None, None, u'5', u'5', None],
         [u'Banfield', u'Banfield', u'Efectivity', None, None, u'63.16%',
          u'47.37%', None],
         [u'Buenos Aires', u'Argentinos Juniors', u'Won', None, None, None,
          u'12', None],
         [u'Buenos Aires', u'Argentinos Juniors', u'Lost', None, None, None,
          u'2', None],
         [u'Buenos Aires', u'Argentinos Juniors', u'Drawn', None, None, None,
          u'5', None],
         [u'Buenos Aires', u'Argentinos Juniors', u'Efectivity', None, None,
          None, u'63.16%', None],
         [u'Buenos Aires', u'Boca Juniors', u'Won', u'12', None, None, None,
          None],
         [u'Buenos Aires', u'Boca Juniors', u'Lost', u'4', None, None, None,
          None],
         [u'Buenos Aires', u'Boca Juniors', u'Drawn', u'3', None, None, None,
          None],
         [u'Buenos Aires', u'Boca Juniors', u'Efectivity', u'63.16%', None,
          None, None, None],
         [u'Buenos Aires', u'Huracán', u'Won', None, u'12', None, None, None],
         [u'Buenos Aires', u'Huracán', u'Lost', None, u'5', None, None, None],
         [u'Buenos Aires', u'Huracán', u'Drawn', None, u'2', None, None, None],
         [u'Buenos Aires', u'Huracán', u'Efectivity', None, u'63.16%', None,
          None, None],
         [u'Buenos Aires', u'River Plate', u'Won', None, None, None, None,
          u'8'],
         [u'Buenos Aires', u'River Plate', u'Lost', None, None, None, None,
          u'4'],
         [u'Buenos Aires', u'River Plate', u'Drawn', None, None, None, None,
          u'7'],
         [u'Buenos Aires', u'River Plate', u'Efectivity', None, None, None,
          None, u'42.11%'],
         [u'Buenos Aires', u'San Lorenzo', u'Won', u'12', None, None, None,
          None],
         [u'Buenos Aires', u'San Lorenzo', u'Lost', u'4', None, None, None,
          None],
        [u'Buenos Aires', u'San Lorenzo', u'Drawn', u'3', None, None, None,
         None],
        [u'Buenos Aires', u'San Lorenzo', u'Efectivity', u'63.16%', None, None,
         None, None],
        [u'Buenos Aires', u'Vélez Sársfield', u'Won', None, u'11', u'10', None,
         u'13'],
        [u'Buenos Aires', u'Vélez Sársfield', u'Lost', None, u'1', u'5', None,
         u'2'],
        [u'Buenos Aires', u'Vélez Sársfield', u'Drawn', None, u'7', u'4', None,
         u'4'],
        [u'Buenos Aires', u'Vélez Sársfield', u'Efectivity', None, u'57.89%',
         u'52.63%', None, u'68.42%'],
        [u'La Plata', u'Estudiantes', u'Won', None, None, None, u'12', u'14'],
        [u'La Plata', u'Estudiantes', u'Lost', None, None, None, u'3', u'2'],
        [u'La Plata', u'Estudiantes', u'Drawn', None, None, None, u'4', u'3'],
        [u'La Plata', u'Estudiantes', u'Efectivity', None, None, None,
         u'63.16%', u'73.68%'],
        [u'Lanús', u'Lanús', u'Won', u'11', u'12', None, None, None],
        [u'Lanús', u'Lanús', u'Lost', u'4', u'5', None, None, None],
        [u'Lanús', u'Lanús', u'Drawn', u'4', u'2', None, None, None],
        [u'Lanús', u'Lanús', u'Efectivity', u'57.89%', u'63.16%', None, None,
         None],
        [u'Mendoza', u'Godoy Cruz', u'Won', None, None, None, u'11', u'7'],
        [u'Mendoza', u'Godoy Cruz', u'Lost', None, None, None, u'3', u'4'],
        [u'Mendoza', u'Godoy Cruz', u'Drawn', None, None, None, u'4', u'8'],
        [u'Mendoza', u'Godoy Cruz', u'Efectivity', None, None, None, u'61.11%',
         u'36.84%'],
        [u'Rosario', u"Newell's Old Boys", u'Won', u'8', None, u'12', None,
         None],
        [u'Rosario', u"Newell's Old Boys", u'Lost', u'4', None, u'4', None,
         None],
        [u'Rosario', u"Newell's Old Boys", u'Drawn', u'7', None, u'3', None,
         None],
        [u'Rosario', u"Newell's Old Boys", u'Efectivity', u'42.11%', None,
         u'63.16%', None, None],
        [u'Santa Fé', u'Colón', u'Won', None, u'10', u'10', None, None],
        [u'Santa Fé', u'Colón', u'Lost', None, u'5', u'5', None, None],
        [u'Santa Fé', u'Colón', u'Drawn', None, u'4', u'4', None, None],
         [u'Santa Fé', u'Colón', u'Efectivity', None, u'52.63%', u'52.63%',
          None, None],
         [u'Sarandí', u'Arsenal', u'Won', None, None, None, None, u'9'],
         [u'Sarandí', u'Arsenal', u'Lost', None, None, None, None, u'5'],
         [u'Sarandí', u'Arsenal', u'Drawn', None, None, None, None, u'5'],
         [u'Sarandí', u'Arsenal', u'Efectivity', None, None, None, None,
          u'47.37%'],
         [u'Tigre', u'Tigre', u'Won', u'12', None, None, None, None],
         [u'Tigre', u'Tigre', u'Lost', u'4', None, None, None, None],
         [u'Tigre', u'Tigre', u'Drawn', u'3', None, None, None, None],
         [u'Tigre', u'Tigre', u'Efectivity', u'63.16%', None, None, None,
          None]]
        for i in enumerate(all1): 
            eq_(i[1], all2[i[0]])

class TestPivot_D(object):

    pt = PivotTable()
    pt.rows = [
        GenericObject(**{'distro':u'Ubuntu', 'page_hits':2075, 'releases':13}),
        GenericObject(**{'distro':u'Mint', 'page_hits':1547, 'releases':12}),
        GenericObject(**{'distro':u'Fedora', 'page_hits':1460, 'releases':14}),
        GenericObject(**{'distro':u'Debian', 'page_hits':1143, 'releases':10}),
        GenericObject(**{'distro':u'OpenSuse', 'page_hits':1135, 'releases':26})
    ]

    def test_DA_data(self):
        assert_raises(PivotTableError, getattr, self.pt, 'headers')
        self.pt.xaxis = "distro"
        assert_raises(PivotTableError, getattr, self.pt, 'headers')
        self.pt.yaxis = [
            {'attr':u'page_hits', 'label':u'Page Hits', 'aggr':Sum},
            {'attr':u'releases', 'label':u'Releases', 'aggr':Sum}]
        self.pt.xaxis_sort = False
        self.pt.yaxis_order = None
        assert_raises(TypeError, getattr, self.pt, 'result')
        del self.pt.yaxis_order
        self.pt.yaxis.append(
            {'attr':u'distro', 'label':u'Distro', 'aggr':GroupBy})
        self.pt.headers
        all_ = [a for a in self.pt.result]
