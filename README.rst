------------
Pivot Table
------------

------------
Introduction
------------

Given a list of arbitrary objects this module will help you transpose certain selected attributes in order to show them as columns in a table.

Some features:

- support for Python 2.4 up to 2.7
- support for Unicode
- you don't need to add boilerplate code to fill up missing values
- both columns and rows will be ordered out of the box

**Note**: Certain parts of this module (Aggregation and Y-Axis definition) are *heavily* based on `Collective.Pivottable`_ written by Luciano Pacheco

----------
An example
----------

Let's dive into an example so you can see right now if this module may help you or not. Later on, we have full details of every part of it:

Let's say you have a web service that connects every day to DistroWatch and retrieves a list with the five more popular distros in the Page Hit Ranking. This service gives you the name of the distro, the H.P.D., the tendency and the number of releases each distro has.

An object that can hold such structure might look like this ::

    >>> class Distros(object):                                                                                                                                                       
    ...    def __init__(self, name, h_p_d, tendency, releases):
    ...        self.name = name
    ...        self.h_p_d = h_p_d
    ...        self.tendency = tendency 
    ...        self.releases = releases                            
    ...    def __repr__(self):
    ...        return "<Distro: %s, %d, %s, %d>" % (self.name, self.h_p_d, self.tendency, self.releases)

You retrieve this week's data and you get ::

    >>> distros = [
    ...            Distros(u'Ubuntu', 2075, u'+', 13),
    ...            Distros(u'Mint', 1547, u'=', 12),
    ...            Distros(u'Fedora', 1460, u'+', 14),
    ...            Distros(u'Debian', 1143, u'+', 10),
    ...            Distros(u'OpenSuse', 1135, u'+', 26)
    ...           ]

With this information you would like to get a table like this (notice that the distros are alphabetically ordered and the name of the object attributes are different):

+-------------------+--------+--------+--------+----------+--------+
|  Distro           | Debian | Fedora |  Mint  | OpenSuse | Ubuntu |
+===================+========+========+========+==========+========+
| Hits per distro   |  1143  |  1460  |  1547  |   1135   |  2075  |
+-------------------+--------+--------+--------+----------+--------+
| Tendency          |   \+   |   \+   |   =    |    \+    |   \+   | 
+-------------------+--------+--------+--------+----------+--------+
| Releases          |   10   |   14   |   12   |    26    |   13   |
+-------------------+--------+--------+--------+----------+--------+

You can use this module in this way to get the transposed data (don't worry, we'll explain each attribute later) ::

    >>> from pivottable import PivotTable, Sum, GroupBy
    >>> pt = PivotTable()
    >>> pt.rows = distros
    >>> pt.xaxis = "name"
    >>> pt.yaxis = [
    ...         {'attr':u'h_p_d', 'label':u'Hits per distro', 'aggr':Sum},
    ...         {'attr':u'tendency', 'label':u'Tendency', 'aggr':Sum},
    ...         {'attr':u'releases', 'label':u'Releases', 'aggr':Sum}]

And finally here's the result ::

    >>> [a for a in pt.result] 
    [[u'metric', u'Debian', u'Fedora', u'Mint', u'OpenSuse', u'Ubuntu'], [u'Hits per distro', u'1143', u'1460', u'1547', u'1135', u'2075'], [u'Tendency', u'+', u'+', u'=', u'+', u'+'], [u'Releases', u'10', u'14', u'12', u'26', u'13']]

Or using .next() to get a more clean detail ::

    >>> a = pt.result 
    >>> a.next()
    [u'metric', u'Debian', u'Fedora', u'Mint', u'OpenSuse', u'Ubuntu']
    >>> a.next() 
    [u'Hits per distro', u'1143', u'1460', u'1547', u'1135', u'2075']
    >>> a.next() 
    [u'Tendency', u'+', u'+', u'=', u'+', u'+']
    >>> a.next() 
    [u'Releases', u'10', u'14', u'12', u'26', u'13']

As you might have noticed, the column that brings the name for the measured attribute it's called *metric*. In the current release of this library, this name is hardcoded and cannot be changed (although it's trivial to fix, it might be ready in the next release of this library). 

---------------------------
Complete module's reference
---------------------------

**class PivotTable**:

This is the module's main class where you can store the rows you want to pivot and the one that holds the pivotted data. By default it has no __init__ method so it can be initialized by simply calling PivotTable().

*Attributes*:

- **rows**: An attribute where you set the list of objects you want to transpose.

- **result**: this is a read only attribute that will return the properly transposed data. In case some required attribute is missing or wrong, calling result will raise a PivotTableError.

- **xaxis**: The name of the object attribute that will be use to pivot values.  This attr must exist in every object of the list assigned to rows. E.g. if you want a table that, as columns, has all the months for a given year and your object provides such date in a 'period' attribute, you should assign 'period' as the xaxis.

- **xaxis_format**: Callable that will be applied to the pivotted headers. Useful for localization: if your columns will be datetime objects, instead of returning the datetime repr, return a string: e.g: "jan-10", "ene-10", etc.

- **xaxis_sort**: Boolean flag. Set it to True if you want the pivotted columns to be ordered when building the table. *Warning*: setting this value as False will not return the columns in the order you append the objects to the list assigned to rows but rather a semi random one (before transposing, a set() operation is applied and afterwards a sorted() operation, in case you set this attribute to True). Default: True

- **yaxis**: A list of dictionaries that provides the information required to proper understand your object and what kind of pivot table you need. Provide a dictionary for each attribute in your object you want in the table minus the xaxis attr (that you have already defined in xaxis). Each attribute you define will be a row in the new table except the ones you define as GroupBy attributes (these are going to be use as the pivot keys). The supported keys in each dictionary are:
    * Mandatory:
        * *attr*: the name of the attr in your object that will provide a value to use in the table
        * *label*: the name you want to show in the table that represents the attr. Useful for translation purposes
        * *aggr*: the kind of operation that will be acted upon the submitted attr. See pivottable.Aggregation for more on this. 
    * Optional:
        * *format*: a callable that will be use in 'attr' before presenting the information. Useful for localizing number formats (e.g. an attr value is 0.234 but you want to display '23.4%' to american audiences and '23,4%' to german ones). This callable must only accept a "value" parameter.

- **yaxis_order**: In case you're providing more than one attribute as the key to group the data (denoted in yaxis by using 'aggr':GroupBy as value:key for the given attributes), you can tell the module in this attribute in what order you want these columns to appear in the final table.

- **headers**: This is a read only attribute. After you completed all the required attributes, you can use this attribute to see which are the values for the header row. This same attribute will be the first value in the result attribute (but it will be properly formatted then).
 

**class PivotTableError**:

The main error class for this module: will report any errors encountered while pivotting the rows

**class Aggregation**:

This class works as template for you to define new forms of aggregation you might find useful. At the current release, other than GroupBy and Sum are not defined and has no meaning other than to allow PivotTable to differenciate between keys to transpose and keys as Y-Axis. This is because subtotals and totals are not yet implemented. In a next version of this module these two features will be developed and you will be able to subclass Aggregation and create new forms of Aggregations.

----------------------
A more complex example
----------------------

We are ready to work on a more complex example, trying to showcase all PivotTable features.

Imagine you work as a reporting analyst at `Capsule Corp`_. Capsule Corp. has at least two commercial offices in some of the major cities of the world. Your boss requests a report with the results for some key drivers (Customer Base, Churn Rate, Sales and Net Income) for every month in 2010.

To make the scenario a little more complex (and the example shorter) we won't report every city, every office, every month. Let's see how PivotTable takes care of filling in the blanks:

Let's start by creating an object that can hold our data and some formatting functions ::

    >>> from babel import numbers, dates
    >>> import datetime
    >>> from decimal import Decimal
    >>> locale = "en"
    >>> class Office(object): 
    ...    def __init__(self, city, office, month, initial_customer_base, sales, cancellations, income): 
    ...        self.city = city
    ...        self.office = office
    ...        self.month = month
    ...        self.initial_customer_base = initial_customer_base
    ...        self.sales = sales
    ...        self.cancellations = cancellations
    ...        self.income = Decimal(income)
    ...    @property
    ...    def net_income(self):
    ...        return self.income-(self.income*Decimal('0.21'))
    ...    @property
    ...    def churn(self):
    ...        try:
    ...            return float(self.cancellations)/(float(self.initial_customer_base)+float(self.sales))
    ...        except TypeError:
    ...            if self.cancellations is None: return 0
    ...            elif self.sales is None:
    ...                return float(self.cancellations)/float(self.initial_customer_base)
    ...
    >>> def percent(value):
    ...     try:
    ...         return numbers.format_percent(value, '#.##%', locale)
    ...     except TypeError:
    ...         return u''
    ...
    >>> def currency(value):
    ...     try:
    ...         return numbers.format_currency(value or 0, 'USD', locale=locale)
    ...     except TypeError:
    ...         return u''
    ...
    >>> def numerical(value):
    ...     try:
    ...         return numbers.format_number(value, locale=locale)
    ...     except TypeError:
    ...         return None
    ...
    >>> def format_month(value):
    ...     try:
    ...         return dates.format_date(value, 'MMM-yy', locale)
    ...     except AssertionError:
    ...         return value
    ...

And now a list of Office objects ::

    >>> data = [
    ...     Office(u'West City', u'2nd Office', datetime.date(2010, 1, 1), 12309, 245, 14, 15687697),
    ...     Office(u'West City', u'3nd Office', datetime.date(2010, 1, 1), 4562, 11, 5, 567332),
    ...     Office(u'West City', u'1nd Office', datetime.date(2010, 1, 1), 896466, 2344, 156, 16677999),
    ...     Office(u'West City', u'4nd Office', datetime.date(2010, 1, 1), 976, None, 1, 44780),
    ...     Office(u'North City', u'1nd Office', datetime.date(2010, 1, 1), 3678, 34, 5, 333241),
    ...     Office(u'North City', u'1nd Office', datetime.date(2010, 9, 1), 4016, 84, 20, 338930),
    ...     Office(u'North City', u'1nd Office', datetime.date(2010, 8, 1), 3999, 18, 1, 336808),
    ...     Office(u'North City', u'1nd Office', datetime.date(2010, 7, 1), 3854, 167, 22, 335697),
    ...     Office(u'North City', u'1nd Office', datetime.date(2010, 6, 1), 3766, 99, 11, 334243),
    ...     Office(u'North City', u'1nd Office', datetime.date(2010, 5, 1), 3771, 12, 17, 333796),
    ...     Office(u'North City', u'1nd Office', datetime.date(2010, 4, 1), 3754, 34, 5, 333574),
    ...     Office(u'North City', u'1nd Office', datetime.date(2010, 3, 1), 3722, 45, 13, 333370),
    ...     Office(u'North City', u'1nd Office', datetime.date(2010, 2, 1), 3707, 20, 2, 333466),
    ...     Office(u'North City', u'1nd Office', datetime.date(2010, 10, 1), 4080, 135, 28, 338257),
    ...     Office(u'North City', u'1nd Office', datetime.date(2010, 11, 1), 4187, 259, 33, 340268),
    ...     Office(u'North City', u'1nd Office', datetime.date(2010, 12, 1), 4413, 367, 17, 343352),
    ...     Office(u'West City', u'2nd Office', datetime.date(2010, 2, 1), 12540, 245, 14, 15688736),
    ...     Office(u'West City', u'3nd Office', datetime.date(2010, 2, 1), 4568, 11, 5, 567575),
    ...     Office(u'West City', u'1nd Office', datetime.date(2010, 2, 1), 898654, 2344, 156, 16687999),
    ...     Office(u'West City', u'4nd Office', datetime.date(2010, 2, 1), 975, None, 1, 44788),
    ...     Office(u'West City', u'2nd Office', datetime.date(2010, 3, 1), 12771, 245, 14, 15689723),
    ...     Office(u'West City', u'3nd Office', datetime.date(2010, 3, 1), 4574, 11, 5, 567441),
    ...     Office(u'West City', u'1nd Office', datetime.date(2010, 3, 1), 900842, 2344, 156, 16689588),
    ...     Office(u'South City', u'1nd Office', datetime.date(2010, 1, 1), 1238754, 9011, 794, 1177405748),
    ...     Office(u'South City', u'1nd Office', datetime.date(2010, 3, 1), 1256852, 4028, 893, 1177869032),
    ...     Office(u'South City', u'1nd Office', datetime.date(2010, 5, 1), 1261837, 7988, 1705, 1179026096),
    ...     Office(u'South City', u'1nd Office', datetime.date(2010, 7, 1), 1262820, 5555, 1094, 1182109042),
    ...     Office(u'South City', u'1nd Office', datetime.date(2010, 9, 1), 1266728, 8234, 693, 1184648971),
    ...     Office(u'South City', u'1nd Office', datetime.date(2010, 11, 1), 1272283, 8887, 917, 1185449009),
    ...     Office(u'South City', u'1nd Office', datetime.date(2010, 12, 1), 1280253, 8845, 820, 1277349020),
    ...     Office(u'West City', u'4nd Office', datetime.date(2010, 5, 1), 974, None, 1, 44233),
    ...     Office(u'West City', u'4nd Office', datetime.date(2010, 6, 1), 973, None, 2, 44356),
    ...     Office(u'West City', u'4nd Office', datetime.date(2010, 7, 1), 971, None, 1, 44441),
    ...     Office(u'North City', u'2nd Office', datetime.date(2010, 6, 1), 0, 555, 2, 50001),
    ...     Office(u'North City', u'2nd Office', datetime.date(2010, 7, 1), 553, 10, None, 52345),
    ...     Office(u'North City', u'2nd Office', datetime.date(2010, 8, 1), 563, 20, 11, 53400),
    ...     Office(u'North City', u'2nd Office', datetime.date(2010, 9, 1), 572, 34, 5, 55890),
    ...     Office(u'North City', u'2nd Office', datetime.date(2010, 10, 1), 601, 256, 25, 77860),
    ...     Office(u'North City', u'2nd Office', datetime.date(2010, 11, 1), 832, 322, 11, 100543),
    ...     Office(u'North City', u'2nd Office', datetime.date(2010, 12, 1), 1143, 477, 77, 135789)
    ...     ]
    ...

Now, we'll try to pivot this information. Let's see step by step.

First, we build a PivotTable instance ::

    >>> pt = PivotTable()

In our object Office, the attribute *month* is the one we want to transpose into columns ::

   >>> pt.xaxis = "month"

Since it's a date instance and we want to show a localized string instead of datetime default repr, we apply a formatter function (we defined *format_month* at the beginning of this exercise) ::

   >>> pt.xaxis_format = format_month

We want the months to be ordered ::

   >>> pt.xaxis_sort = True

Enough about the X-axis, let's start working with the Y-axis. First we need to tell PivotTable what Office's attributes should be presented as rows and which ones should be use as Y-axis keys to separate the data. Plus we want to label each metric with a special name and apply some formatter options.
Here we have the Y-axis keys ::

   >>> pt.yaxis = [
   ...         {'attr':'city', 'label':u'City', 'aggr':GroupBy},
   ...         {'attr':'office', 'label':u'Office', 'aggr':GroupBy}]
   ...


Now the metrics that will be transformed into rows. As explained before, at the moment, the Aggregate functions (other than GroupBy) bear no meaning and not specific action will be apply when they're invoked. Nevertheless, we need to defined an Aggregation function that's not GroupBy in order PivotTable can tell which ones are keys and which ones, metrics ::

   >>> pt.yaxis += [
   ...         {'attr':'initial_customer_base', 'label':u'Customer Base', 'aggr':Sum, 'format':numerical},
   ...         {'attr':'churn', 'label':u'Churn Rate', 'aggr':Sum, 'format':percent},
   ...         {'attr':'sales', 'label':u'Sales', 'aggr':Sum, 'format':numerical},
   ...         {'attr':'net_income', 'label':u'Net Income', 'aggr':Sum, 'format':currency}]
   ...

And finally in which order we want the Y-axis keys be presented: first city and then office ::

   >>> pt.yaxis_order = [u'city', u'office']

Now that everything's configured, let's add our objects ::

   >>> pt.rows = data

Just to get a preview, we can see which are going to be our headers (previous to formatting) ::

   >>> pt.headers
   ['city', 'office', u'metric', datetime.date(2010, 1, 1), datetime.date(2010, 2, 1), datetime.date(2010, 3, 1), datetime.date(2010, 4, 1), datetime.date(2010, 5, 1), datetime.date(2010, 6, 1), datetime.date(2010, 7, 1), datetime.date(2010, 8, 1), datetime.date(2010, 9, 1), datetime.date(2010, 10, 1), datetime.date(2010, 11, 1), datetime.date(2010, 12, 1)]

And here's the final output. We have all the information ordered out of the box both in the Y-axis and the X-axis and with the proper formatting, ready to be incorporated in wherever we need it (for example a template language to build html pages) ::

   >>> for a in pt.result: print(a)
   ['city', 'office', u'metric', u'Jan-10', u'Feb-10', u'Mar-10', u'Apr-10', u'May-10', u'Jun-10', u'Jul-10', u'Aug-10', u'Sep-10', u'Oct-10', u'Nov-10', u'Dec-10']
   [u'North City', u'1nd Office', u'Customer Base', u'3,678', u'3,707', u'3,722', u'3,754', u'3,771', u'3,766', u'3,854', u'3,999', u'4,016', u'4,080', u'4,187', u'4,413']
   [u'North City', u'1nd Office', u'Churn Rate', u'0.13%', u'0.05%', u'0.34%', u'0.13%', u'0.45%', u'0.28%', u'0.55%', u'0.02%', u'0.49%', u'0.66%', u'0.74%', u'0.36%']
   [u'North City', u'1nd Office', u'Sales', u'34', u'20', u'45', u'34', u'12', u'99', u'167', u'18', u'84', u'135', u'259', u'367']
   [u'North City', u'1nd Office', u'Net Income', u'$263,260.39', u'$263,438.14', u'$263,362.30', u'$263,523.46', u'$263,698.84', u'$264,051.97', u'$265,200.63', u'$266,078.32', u'$267,754.70', u'$267,223.03', u'$268,811.72', u'$271,248.08']
   [u'North City', u'2nd Office', u'Customer Base', None, None, None, None, None, u'0', u'553', u'563', u'572', u'601', u'832', u'1,143']
   [u'North City', u'2nd Office', u'Churn Rate', None, None, None, None, None, u'0.36%', u'0%', u'1.89%', u'0.82%', u'2.92%', u'0.95%', u'4.75%']
   [u'North City', u'2nd Office', u'Sales', None, None, None, None, None, u'555', u'10', u'20', u'34', u'256', u'322', u'477']
   [u'North City', u'2nd Office', u'Net Income', None, None, None, None, None, u'$39,500.79', u'$41,352.55', u'$42,186.00', u'$44,153.10', u'$61,509.40', u'$79,428.97', u'$107,273.31']
   [u'South City', u'1nd Office', u'Customer Base', u'1,238,754', None, u'1,256,852', None, u'1,261,837', None, u'1,262,820', None, u'1,266,728', None, u'1,272,283', u'1,280,253']
   [u'South City', u'1nd Office', u'Churn Rate', u'0.06%', None, u'0.07%', None, u'0.13%', None, u'0.09%', None, u'0.05%', None, u'0.07%', u'0.06%']
   [u'South City', u'1nd Office', u'Sales', u'9,011', None, u'4,028', None, u'7,988', None, u'5,555', None, u'8,234', None, u'8,887', u'8,845']
   [u'South City', u'1nd Office', u'Net Income', u'$930,150,540.92', None, u'$930,516,535.28', None, u'$931,430,615.84', None, u'$933,866,143.18', None, u'$935,872,687.09', None, u'$936,504,717.11', u'$1,009,105,725.80']
   [u'West City', u'1nd Office', u'Customer Base', u'896,466', u'898,654', u'900,842', None, None, None, None, None, None, None, None, None]
   [u'West City', u'1nd Office', u'Churn Rate', u'0.02%', u'0.02%', u'0.02%', None, None, None, None, None, None, None, None, None]
   [u'West City', u'1nd Office', u'Sales', u'2,344', u'2,344', u'2,344', None, None, None, None, None, None, None, None, None]
   [u'West City', u'1nd Office', u'Net Income', u'$13,175,619.21', u'$13,183,519.21', u'$13,184,774.52', None, None, None, None, None, None, None, None, None]
   [u'West City', u'2nd Office', u'Customer Base', u'12,309', u'12,540', u'12,771', None, None, None, None, None, None, None, None, None]
   [u'West City', u'2nd Office', u'Churn Rate', u'0.11%', u'0.11%', u'0.11%', None, None, None, None, None, None, None, None, None]
   [u'West City', u'2nd Office', u'Sales', u'245', u'245', u'245', None, None, None, None, None, None, None, None, None]
   [u'West City', u'2nd Office', u'Net Income', u'$12,393,280.63', u'$12,394,101.44', u'$12,394,881.17', None, None, None, None, None, None, None, None, None]
   [u'West City', u'3nd Office', u'Customer Base', u'4,562', u'4,568', u'4,574', None, None, None, None, None, None, None, None, None]
   [u'West City', u'3nd Office', u'Churn Rate', u'0.11%', u'0.11%', u'0.11%', None, None, None, None, None, None, None, None, None]
   [u'West City', u'3nd Office', u'Sales', u'11', u'11', u'11', None, None, None, None, None, None, None, None, None]
   [u'West City', u'3nd Office', u'Net Income', u'$448,192.28', u'$448,384.25', u'$448,278.39', None, None, None, None, None, None, None, None, None]
   [u'West City', u'4nd Office', u'Customer Base', u'976', u'975', None, None, u'974', u'973', u'971', None, None, None, None, None]
   [u'West City', u'4nd Office', u'Churn Rate', u'0.1%', u'0.1%', None, None, u'0.1%', u'0.2%', u'0.1%', None, None, None, None, None]
   [u'West City', u'4nd Office', u'Sales', None, None, None, None, None, None, None, None, None, None, None, None]
   [u'West City', u'4nd Office', u'Net Income', u'$35,376.20', u'$35,382.52', None, None, u'$34,944.07', u'$35,041.24', u'$35,108.39', None, None, None, None, None]

If we change the locale, we will get the information localized for a different culture (of course, PivotTable has nothing to do with it, that's Babel work) ::

   >>> locale = "es"
   >>> a = pt.result
   >>> a.next()
   ['city', 'office', u'metric', u'ene-10', u'feb-10', u'mar-10', u'abr-10', u'may-10', u'jun-10', u'jul-10', u'ago-10', u'sep-10', u'oct-10', u'nov-10', u'dic-10']
   >>> a.next()
   [u'North City', u'1nd Office', u'Customer Base', u'3.678', u'3.707', u'3.722', u'3.754', u'3.771', u'3.766', u'3.854', u'3.999', u'4.016', u'4.080', u'4.187', u'4.413']
   >>> a.next()
   [u'North City', u'1nd Office', u'Churn Rate', u'0,13%', u'0,05%', u'0,34%', u'0,13%', u'0,45%', u'0,28%', u'0,55%', u'0,02%', u'0,49%', u'0,66%', u'0,74%', u'0,36%']
   >>> a.next()
   [u'North City', u'1nd Office', u'Sales', u'34', u'20', u'45', u'34', u'12', u'99', u'167', u'18', u'84', u'135', u'259', u'367']
   >>> a.next()
   [u'North City', u'1nd Office', u'Net Income', u'US$\xa0263.260,39', u'US$\xa0263.438,14', u'US$\xa0263.362,30', u'US$\xa0263.523,46', u'US$\xa0263.698,84', u'US$\xa0264.051,97', u'US$\xa0265.200,63', u'US$\xa0266.078,32', u'US$\xa0267.754,70', u'US$\xa0267.223,03', u'US$\xa0268.811,72', u'US$\xa0271.248,08']

We can change the Y-axis order too ::

   >>> locale = "en"
   >>> pt.yaxis_order = [u'office', u'city']
   >>> a = pt.result
   >>> a.next()
   ['office', 'city', u'metric', u'Jan-10', u'Feb-10', u'Mar-10', u'Apr-10', u'May-10', u'Jun-10', u'Jul-10', u'Aug-10', u'Sep-10', u'Oct-10', u'Nov-10', u'Dec-10']
   >>> a.next()
   [u'1nd Office', u'North City', u'Customer Base', u'3,678', u'3,707', u'3,722', u'3,754', u'3,771', u'3,766', u'3,854', u'3,999', u'4,016', u'4,080', u'4,187', u'4,413']
   >>> a.next()
   [u'1nd Office', u'North City', u'Churn Rate', u'0.13%', u'0.05%', u'0.34%', u'0.13%', u'0.45%', u'0.28%', u'0.55%', u'0.02%', u'0.49%', u'0.66%', u'0.74%', u'0.36%']
   >>> a.next()
   [u'1nd Office', u'North City', u'Sales', u'34', u'20', u'45', u'34', u'12', u'99', u'167', u'18', u'84', u'135', u'259', u'367']
   >>> a.next()
   [u'1nd Office', u'North City', u'Net Income', u'$263,260.39', u'$263,438.14', u'$263,362.30', u'$263,523.46', u'$263,698.84', u'$264,051.97', u'$265,200.63', u'$266,078.32', u'$267,754.70', u'$267,223.03', u'$268,811.72', u'$271,248.08']
   >>> a.next()
   [u'1nd Office', u'South City', u'Customer Base', u'1,238,754', None, u'1,256,852', None, u'1,261,837', None, u'1,262,820', None, u'1,266,728', None, u'1,272,283', u'1,280,253']

I guess that's all. Thanks for your patience. If you are interested in more examples you can check the `test suite`_ for PivotTable.

.. _Collective.Pivottable: http://pypi.python.org/pypi/collective.pivottable/1.1.1dev-r97462
.. _Capsule Corp: http://www.dragonballencyclopedia.com/index.php?title=Capsule_Corporation&variant=qdb
.. _test suite: https://bitbucket.org/marplatense/python-pivottable/
