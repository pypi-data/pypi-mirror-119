"""
    test_esx
    ~~~~~~~~~~~~~~~
    unit tests for esx
"""

import time
import unittest
from unittest.mock import Mock
# import requests
# from mock import patch

from esx.javascript import Object
from esx.javascript import Math
from esx.javascript import Global
from esx.javascript import Window
from esx.javascript import Date
from esx.javascript import URL
from esx.javascript import Array
from esx.javascript import String

from esx.javascript import *


from inspect import stack


class TestCase(unittest.TestCase):

    # esx.Math

    def test_object(self):

        o = Object()
        print(o)
        print(type(o))

        myObj = Object()
        string = 'myString'
        rand = Math.random()
        obj1 = Object()
        myObj.type = 'Dot syntax'
        myObj['date created'] = 'String with space'
        myObj[string] = 'String value'
        myObj[rand] = 'Random Number'
        myObj[obj1] = 'Object'
        myObj[''] = 'Even an empty string'


        assert myObj.type == 'Dot syntax'
        assert myObj['date created'] == 'String with space'
        assert myObj[string] == 'String value'
        assert myObj[rand] == 'Random Number'
        # assert myObj[obj1] == 'Object' # TODO - does js do this?
        assert myObj[''] == 'Even an empty string'

        assert o is not myObj

        myCar = Object()
        propertyName = 'make'
        myCar[propertyName] = 'Ford'
        assert myCar[propertyName] == 'Ford'
        propertyName = 'model'
        myCar[propertyName] = 'Mustang'
        assert myCar[propertyName] == 'Mustang'

        def showProps(obj, objName):
            result = ''
            for i in obj:
                if obj.hasOwnProperty(i):
                    result += objName + "." + str(i) + "= " + str(obj[i]) + "\n"
            return result

        showProps(myCar, "myCar")
        # print(showProps(myCar, "myCar"))

        obj = {'a': 1}
        copy = Object.assign({}, obj)
        assert copy == {'a': 1}

        # print(Object().fromEntries())
        arr = [['0', 'a'], ['1', 'b'], ['2', 'c']]
        obj = Object.fromEntries(arr)
        print(obj)
        assert obj == {'0': "a", '1': "b", '2': "c"}

        obj = {'foo': 'bar', 'baz': 42}
        print(Object.entries(obj))
        assert Object.entries(obj) == [['foo', 'bar'], ['baz', 42]]

        # array like object
        obj = {'0': 'a', '1': 'b', '2': 'c'}
        assert Object.entries(obj) == [['0', 'a'], ['1', 'b'], ['2', 'c']]

        # def listAllProperties(o):
        #     result = []
        #     objectToInspect = o
        #     while objectToInspect != None:
        #         print(objectToInspect)
        #         objectToInspect = Object.getPrototypeOf(objectToInspect)
        #         result = Array(result).concat(Object.getOwnPropertyNames(objectToInspect))

        #     return result
        # print(listAllProperties(myCar))


        # array like object with random key ordering
        # anObj = {'100': 'a', '2': 'b', '7': 'c'}
        # print(anObj)
        # print(Object.entries(anObj))
        # assert Object.entries(anObj) == [['2', 'b'], ['7', 'c'], ['100', 'a']]

        # returns an empty array for any primitive type
        assert Object.entries(100) == []

        # iterate through key-value gracefully
        obj = {'a': 5, 'b': 7, 'c': 9}
        for key, value in Object.entries(obj):
            print(f'{key} {value}')  # "a 5", "b 7", "c 9"

        # class Car(Object):
        #     def __init__(self, make, model, year):
        #         super().__init__()
        #         self.make = make
        #         self.model = model
        #         self.year = year
        #         # super().__init__()

        # mycar = Car('Eagle', 'Talon TSi', 1993)
        # print(mycar)
        # print(mycar.make)
        # print(mycar.__attribs__)

    # Animal properties and method encapsulation


    # TODO - to get reference back to self. in a dict it needs to readd the method and pass self
    Animal = {
        'type': 'Invertebrates',  # Default value of properties
        # 'displayType': lambda self: print("STACK!!!!!",stack()[1].function)  # Method which will display type of Animal
        'displayType': lambda self: print(self.type)
    }
    animal1 = Object.create(Animal)
    print(animal1)
    # print(animal1['type'])
    print(animal1.__dict__)
    animal1.displayType(animal1)  # Output:Invertebrates #TODO - need to work without passing self

    fish = Object.create(Animal)
    fish.type = 'Fishes'
    fish.displayType(animal1)  # Output:Fishes



    def test_abs(self):
        self.assertEqual(Math.abs('-1'), 1)
        self.assertEqual(Math.abs(-2), 2)
        self.assertEqual(Math.abs(None), 0)
        self.assertEqual(Math.abs(''), 0)
        self.assertEqual(Math.abs([]), 0)
        self.assertEqual(Math.abs([2]), 2)
        self.assertEqual(Math.abs([1, 2]), None)
        self.assertEqual(Math.abs({}), None)
        self.assertEqual(Math.abs('string'), None)
        self.assertEqual(Math.abs(), None)

        self.assertEqual(100, Math.abs(-100.0))

    def test_LN2(self):
        print("test_LN2:::")
        print(Math.LN2)

    def test_LOG2E(self):
        print("test_LOG2E:::")
        print(Math.LOG2E)

    def test_LOG10E(self):
        print("test_LOG10E:::")
        print(Math.LOG10E)

    def test_PI(self):
        print("test_PI:::")
        print(Math.PI)

    def test_SQRT1_2(self):
        print("test_SQRT1_2:::")
        print(Math.SQRT1_2)

    def test_SQRT2(self):
        print("test_SQRT2:::")
        print(Math.SQRT2)

    def test_acos(self):
        print("test_acos:::")
        # print( Math.acos(-100) ) # TODO - fails numbers greater than 1 or lower than -1 - raise Error?
        print(Math.acos(0.5))

    def test_acosh(self):
        print("test_acosh:::")
        # print( Math.acosh(-100) ) # TODO - fails under zero - rause error?
        print(Math.acosh(100))

    def test_asin(self):
        print("test_asin:::")
        # print( Math.asin(-100) ) # TODO - fails numbers greater than 1 or lower than -1 - raise Error?
        print(Math.asin(0.5))

    def test_asinh(self):
        print("test_asinh:::")
        print(Math.asinh(-100))

    def test_atan(self):
        print("test_atan:::")
        print(Math.atan(-100))

    def test_atan2(self):
        print("test_atan2:::")
        print(Math.atan2(-100, 100))

    def test_atanh(self):
        print("test_atanh:::")
        # print( Math.atanh(-100) ) # TODO - fails numbers greater than 1 or lower than -1 - raise Error?
        print(Math.atanh(0.5))

    def test_cbrt(self):
        print("test_cbrt:::")
        # print( Math.cbrt(-100) ) # TODO - fails on negative numbers - raise Error?
        print(Math.cbrt(100))

    def test_ceil(self):
        print("test_ceil:::")
        print(Math.ceil(-100))

    def test_cos(self):
        print("test_cos:::")
        print(Math.cos(-100))

    def test_cosh(self):
        print("test_cosh:::")
        print(Math.cosh(-100))

    def test_E(self):
        self.assertEqual(2.718281828459045, Math.E)

    def test_exp(self):
        print("test_exp:::")
        print(Math.exp(-100))

    def test_floor(self):
        print("test_floor:::")
        print(Math.floor(-100))

    def test_LN10(self):
        self.assertEqual(2.302585092994046, Math.LN10)

    def test_log(self):
        print("test_log:::")
        # print( Math.log(-100,100) ) # TODO - fails on negative numbers - raise Error?
        print(Math.log(100, 10))

    def test_max(self):
        print("test_max:::")
        print(Math.max(-100, 100))

    def test_min(self):
        print("test_min:::")
        print(Math.min(-100, 100))

    def test_random(self):
        print("test_random:::")
        print(Math.random())

    def test_round(self):
        print("test_round:::")
        print(Math.round(-100))

    def test_pow(self):
        print("test_pow:::")
        print(Math.pow(100, 10))

    def test_sin(self):
        print("test_sin:::")
        print(Math.sin(-100))

    def test_sinh(self):
        print("test_sinh:::")
        print(Math.sinh(-100))

    def test_sqrt(self):
        print("test_sqrt:::")
        # print( Math.sqrt(-100) ) # TODO - fails on negative numbers - raise Error? check js behaviour
        print(Math.sqrt(100))

    def test_tan(self):
        print("test_tan:::")
        print(Math.tan(-100))

    def test_tanh(self):
        print("test_tanh:::")
        print(Math.tanh(-100))

    def test_trunc(self):
        print("test_trunc:::")
        print(Math.trunc(-100))

    # def test_math_test(self):
    #   print("test_math_test:::")
    #   print( Math.abs(-100)*Math.random()*10 )

    # esx.Global

    def test_isNaN(self):
        self.assertEqual(True, Global.isNaN("yo"))
        self.assertEqual(False, Global.isNaN(1))

    def test_Number(self):
        self.assertEqual(1, Global.Number(1))
        self.assertEqual("NaN", Global.Number("test"))
        self.assertEqual(2, Global.Number("1") + Global.Number("1.0"))

    def test_window_console_log(self):
        # window = Window()
        # Window().console.log("test this")
        # window.console.log("test this")

        # c = Console()
        # c.log()
        # Console.log('test')
        pass

    def test_window_alert(self):
        # Window().alert("test this 2")
        window = Window()
        window.alert("test this 2")

    def test_window_document_baseURI(self):
        # Window().alert("test this 2")
        # window = Window()
        # window.alert("test this 2")
        # print(window.document.baseURI)
        # window.document.baseURI = "eventual.technology"
        # print("=",window.document.baseURI)

        pass

    '''
    def test_window_location(self):
        # Window().alert("test this 2")
        window = Window()
        # window.alert("test this 2")
        print("window.location")
        print(window.location)
        window.location = "eventual.technology"
        print("window.location.uri")
        print(window.location)
        print(str(window.location))
        print(window.location.href)
    '''

    def test_global_encodeURIComponent(self):

        msg = "Test encoding this string! 123 aweseome"
        enc_msg = Global.encodeURIComponent(msg)
        print(enc_msg)
        # print( Global.decodeURIComponent(bytes(enc_msg, encoding="UTF-8")))
        print(Global.decodeURIComponent(enc_msg))

        # Window().alert("test this 2")
        # window = Window()
        # window.alert("test this 2")
        # print(window.document.baseURI)
        # window.document.baseURI = "eventual.technology"
        # print("=",window.document.baseURI)
        pass

    def test_esx_date(self):
        print("test_esx_date::::::::::::::::::")
        d = Date()
        print(d.getDate())
        print(d.getDay())
        print(d.getFullYear())
        print(d.getHours())
        print(d.getMilliseconds())
        print(d.getMinutes())
        print(d.getMonth())
        print(d.getSeconds())
        print(d.getTime())
        # print( d.getTimezoneOffset() )
        print(d.getUTCDate())
        print(d.getUTCDay())
        print(d.getUTCFullYear())
        print(d.getUTCHours())
        print(d.getUTCMilliseconds())
        print(d.getUTCMinutes())
        print(d.getUTCMonth())
        print(d.getUTCSeconds())
        print(d.getYear())
        print(d.now())
        # print( d.onstorage() )
        # print( d.ontimeupdate() )
        print(d.parse("July 1981"))
        print(d.setDate(1))
        print(d.setFullYear('1982'))
        print(d.setHours(2))
        # print( d.setItem() )
        print(d.setMilliseconds(12345))
        print(d.setMinutes(10))
        print(d.setMonth(10))
        print(d.setSeconds(10))
        print(d.setTime(1000))
        print(d.setUTCDate(1))
        print(d.setUTCFullYear(1928))
        print(d.setUTCHours(3))
        print(d.setUTCMilliseconds(54321))
        print(d.setUTCMinutes(50))
        print(d.setUTCMonth(3))
        print(d.setUTCSeconds(11))
        print(d.setYear(1987))
        print(d.toDateString())
        print(d.toGMTString())
        print(d.toJSON())
        print(d.toISOString())
        print(d.toLocaleDateString())
        print(d.toLocaleString())
        print(d.toLocaleTimeString())
        print(d.toTimeString())
        print(d.toUTCString())
        print(d.UTC())


    def test_esx_url(self):
        url = URL('https://somesite.com/blog/article-one#some-hash')
        print('TESTS:')
        print(url)
        print(url.toString())
        print(url.href)
        print(url.protocol)
        url.protocol = "http"
        print(url.protocol)
        print(url.host)
        print(url.pathname)
        print(url.hash)

        # print(url.origin)

        url = URL('https://somesite.com:8000/blog/article-one#some-hash')
        print(url.protocol)
        print(url.host)
        print(url.hostname)
        print(url.pathname)
        print(url.hash)
        print(url.port)

        url.host = 'test.com'
        print('host:', url.host)
        print('href:', url.href)
        print(url.hostname)
        print(url.pathname)
        print(url.hash)
        print(url.port)
        url.port = 8983
        print(url.toString())

    # def test_esx_window(self):
        # print('asdf')
        # print(window)
        # print(window.location)

        # window.location = "https://google.com"
        # print(window.location.href)
        # pass

    def test_esx_array(self):
        print("test_esx_array")
        myarr = Array("1", "2", 3, {"4": "four"}, 5, [6])
        print(myarr)
        print(type(myarr))
        print(myarr.length)
        print(myarr.includes("1"))
        print(myarr.includes(3))
        print(myarr.includes(10))
        print(myarr.indexOf(10))
        print(myarr.indexOf("1"))
        print(myarr.indexOf([6]))
        print(myarr[1])
        print(len(myarr))
        print(myarr.join('---'))  #  TODO - test some js ones
        print(myarr.lastIndexOf("1"))
        print(myarr.lastIndexOf(3))
        print(myarr.reverse())
        print(myarr.slice(0, 1))
        print(myarr.splice(1))
        # print(myarr.splice(2))
        # print(myarr.splice(3))
        # print(myarr.splice(4))
        print(myarr.splice(3, 3, "a", "b", "c"))
        print(myarr)
        print(myarr.pop())
        print(myarr)
        myarr.push(7)
        print(myarr)
        print(myarr.unshift('z'))
        print(myarr)
        print(myarr.shift())
        print(myarr)
        # print(myarr.concat())

        # myarr.sort()
        # myarr.fill()
        # myarr.isArray()?
        # myarr.map()
        # myarr.reduce()
        # myarr.reduceRight()
        # myarr.some()
        pass

    def test_esx_interval(self):

        def hi():
            print('hi')
            pass

        test = window.setInterval(hi, 1)
        print('im going to do some stuff in the background')

        # keep the test open to see if the intervals fire
        time.sleep(2)

        print('running')
        window.clearInterval(test)
        print('ran')

    def test_esx_Number(self):
        print(Number.MAX_VALUE)
        pass

    def test_esx_fetch(self):

        TEST_DOMAIN = 'http://eventual.technology'
        urls = ['http://google.com', 'http://linkedin.com', 'http://eventual.technology']  # use your own domains

        print('run 1')
        results = window.fetch(TEST_DOMAIN)
        results.then(lambda r: print(r.text))
        print('run 1 FINISHED')

        def somefunc(response):
            print("I'm a callback", response.ok)
            return response

        mydata = window.fetch(TEST_DOMAIN).then(somefunc)
        print(mydata)
        print(mydata.data)
        print(mydata.data.text)

        print('run 1111')
        results = window.fetch_set(urls)
        print(results)
        print(list(results))
        for r in results:
            if r is not None:
                print(r.ok)
                # print(r.text)

        print('run 2')
        results = window.fetch_threaded(urls)
        print(results)
        print(list(results))
        for r in results:
            if r is not None:
                print(r.ok)
                # print(r.text)

        print('run 3')
        results = window.fetch_pooled(urls, timeout=2)
        print(results)
        for r in results:
            if r is not None:
                print(r.ok)
                # print(r.text)

        print('run 4')
        results = window.fetch(urls[0])
        print(results)
        results.then(lambda r: print(r.text) if r is not None else None)

        print('ran ===')
        # return

        # TEST REGULAR

        global _results

        def get_things():
            global _results
            _results = window.fetch(urls[0])
            print('sup::', _results)

        print('BEFORE')
        test = window.setInterval(get_things, 2000)
        print('AFTER')
        print(_results)
        time.sleep(4)
        print('LATER')
        print(_results)

        print('MAKE SURE TO CLEAR INTERVAL AND RESET RESULTS!')
        window.clearInterval(test)
        _results = []

        # TEST - Threaded interval triggering a CPU pool
        def get_things():
            global _results
            _results = window.fetch_pooled(urls)
            print('sup::', _results)

        print('Are you ready')
        test = window.setInterval(get_things, 1000)
        print("wait, where my results?")
        print(_results)
        time.sleep(4)
        print("Ahhh nice")
        print(_results)
        for r in _results:
            print(r.ok)
            # print(r.text)

        window.clearInterval(test)

        # nice 😎

    def test_esx_promise(self):
        def do_test(resolve, reject):
            global _intID
            _intID = window.setInterval(resolve, 2000, 'amazing!')
            resolve("once!")
        myPromise = Promise(lambda resolve, reject: do_test(resolve, reject))
        myPromise.then(lambda successMessage: str(successMessage))
        time.sleep(3)
        window.clearInterval(_intID)
        myPromise.then(lambda successMessage: print("Yay! " + str(successMessage)))

    def test_esx_string(self):
        print("test_esx_string")
        mystr = String("Some String")

        assert(mystr.toLowerCase() == "some string")
        assert(mystr.toUpperCase() == "SOME STRING")

        # print(type(mystr))
        # print(mystr.length)
        assert(mystr.length == 11)

        assert(mystr.repeat(2) == "Some StringSome String")
        # print(mystr)
        # print(mystr)
        # print(mystr)
        assert(mystr.startsWith('S'))
        # assert(mystr.endsWith('g'))

        # print(">>", mystr.substr(1))
        assert(mystr.substr(1) == 'ome String')

        #substring
        # print(mystr)
        # print(mystr.substring(1, 3))
        assert(mystr.substring(1, 3) == 'om')

        # slice
        # print(mystr.slice(1, 3))
        assert(mystr.slice(1, 3) == 'om')

        # test trim
        mystr = String("   Some String   ")
        assert(mystr.trim() == "Some String")

        # charAt
        mystr = String("Some String")
        assert(mystr.charAt(1) == 'o')
        assert(mystr.charAt(5) == 'S')

        # charCodeAt
        assert(mystr.charCodeAt(1) == 111)
        assert(mystr.fromCharCode(111) == 'o')

        # test
        # assert(mystr.test('a') == True)
        # assert(mystr.test('b') == False)

        # replace
        # print(mystr.replace('S', 'X'))
        assert(mystr.replace('S', 'X') == "Xome String")
        assert(mystr.replace(' ', 'X') == "SomeXString")
        assert(mystr.replace('S', 'X') != "Xome Xtring")

        # localeCompare
        # assert(mystr.localeCompare('a', 'b') == -1)
        # assert(mystr.localeCompare('a', 'a') == 0)
        # assert(mystr.localeCompare('a', 'A') == 1)
        # assert(mystr.localeCompare('a', 'aa') == -1)
        # assert(mystr.localeCompare('a', 'Aa') == -1)

        # search
        mystr = String("Some String")
        assert(mystr.search('a') == False)
        assert(mystr.search('o') == True)

        # substr
        print(mystr.substr(1, 2))
        assert(mystr.substr(1, 2) == 'om')
        assert(mystr.substr(1, 3) == 'ome')
        assert(mystr.substr(1, 4) == 'ome ')
        assert(mystr.substr(1, 5) == 'ome S')


        # toLocaleLowerCase
        # print(mystr.toLocaleLowerCase())
        assert(mystr.toLocaleLowerCase() == 'some string')
        # print(mystr.toLocaleLowerCase())
        assert(mystr.toLocaleLowerCase() == 'some string')

        # toLocaleUpperCase
        # print(mystr.toLocaleUpperCase())
        assert(mystr.toLocaleUpperCase() == 'SOME STRING')

        # compile
        # print(mystr.compile())
        # assert(mystr.compile() == '"Some String"')

        # lastIndex
        # print(mystr.lastIndexOf('o'))
        assert(mystr.lastIndexOf('o') == 1)

        # replace
        assert mystr.codePointAt(1) == 111
        # print(mystr.padEnd(2))
        # print(f"-{mystr}-")
        print(f"---{mystr.padEnd(13)}-")
        assert mystr.padEnd(13) == "Some String  "
        assert mystr.padStart(13) == "  Some String"
        assert mystr.padStart(13, '-') == "--Some String"
        # assert mystr.localeCompare('a', 'a') == 0

        assert mystr.includes('a') == False
        assert mystr.includes('Some') == True
        # assert mystr.matchAll(['a', 'b']) == False # TODO - dont think this is supposed to take lists?
        # assert mystr.match('a', 'b') == False # TODO
        # assert mystr.trimStart(1) == "Some" # TODO
        # assert mystr.trimEnd(1) == "String" # TODO


    def test_esx_URLSearchParams(self):
        print("test_esx_URLSearchParams")

        paramsString = "q=test&topic=api"
        searchParams = URLSearchParams(paramsString)

        # Iterate the search parameters.
        for p in searchParams:
            print(p)

        assert searchParams.has("topic") == True  # True
        # print( searchParams.get("topic") )
        assert searchParams.get("topic") == "api"  # True
        # searchParams.getAll("topic"); # ["api"]
        assert searchParams.get("foo") is None  # true
        print(searchParams.toString())
        searchParams.append("topic", "webdev")
        print(searchParams.toString())
        assert searchParams.toString() == "q=test&topic=api&topic=webdev"
        searchParams.set("topic", "More webdev")
        assert searchParams.toString() == "q=test&topic=More+webdev"
        searchParams.delete("topic")
        assert searchParams.toString() == "q=test"

        # GOTCHAS

        paramsString1 = "http://example.com/search?query=%40"
        searchParams1 = URLSearchParams(paramsString1)

        assert searchParams1.has("query") == False
        assert searchParams1.has("http://example.com/search?query") == True

        assert searchParams1.get("query") == None
        searchParams1.get("http://example.com/search?query")  # "@" (equivalent to decodeURIComponent('%40'))

        paramsString2 = "?query=value"
        searchParams2 = URLSearchParams(paramsString2)
        print(searchParams2)
        assert searchParams2.has("query") == True

        url = URL("http://example.com/search?query=%40")

        searchParams3 = URLSearchParams(url.search)

        print(searchParams3)
        # print(str(searchParams3))
        # assert searchParams3.has("query") == True

        base64 = window.btoa(String.fromCharCode(19, 224, 23, 64, 31, 128))  # base64 is "E+AXQB+A"
        print(base64)
        searchParams = URLSearchParams("q=foo&bin=" + str(base64))  # q=foo&bin=E+AXQB+A
        # getBin = searchParams.get("bin")  # "E AXQB A" + char is replaced by spaces
        # print(getBin)
        # window.btoa(window.atob(getBin))  # "EAXQBA==" no error thrown
        # window.btoa(String.fromCharCode(16, 5, 208, 4))  # "EAXQBA==" decodes to wrong binary value
        # getBin.replace(r'/ /g', "+")  # "E+AXQB+A" is one solution

        # or use set to add the parameter, but this increases the query string length
        # searchParams.set("bin2", base64)  # "q=foo&bin=E+AXQB+A&bin2=E%2BAXQB%2BA" encodes + as %2B
        # searchParams.get("bin2")  # "E+AXQB+A"

    def test_esx_FormData(self):
        print("test_esx_FormData")
        # f = form(input(_type="text", _name="test", _id="test"))
        # d = FormData(f)
        # print(d)
        pass

    def test_esx_Worker(self):
        print("test_esx_Worker")
        # myWorker = Worker('/worker.py')
        # first = document.querySelector('input#number1')
        # second = document.querySelector('input#number2')
        # first.onchange = lambda evt : \
        #     myWorker.postMessage([first.value, second.value])
        #     print('Message posted to worker')
        pass

    def test_esx_at(self):
        print("test_esx_at")
        myarr = Array(['a', 'b', 'c', 'd'])
        assert myarr.at(-1) == 'd'
        myarr = ['a', 'b', 'c', 'd']
        myarr = Array(myarr)
        assert myarr.at(-1) == 'd'
        myarr = Array('a', 'b', 'c', 'd')
        assert myarr.at(-1) == 'd'


    # def test_esx_Node(self):
        # url = require('url');
        # console.log(url.domainToASCII('español.com'))
        # console.log(url.domainToASCII('??.com'))
        # console.log(url.domainToASCII('xn--iñvalid.com'))
        # console.log(url.domainToUnicode('español.com'))
        # console.log(url.domainToUnicode('??.com'))
        # console.log(url.domainToUnicode('xn--iñvalid.com'))


    # def test_esx_call(self):

    #     class Product():
    #         def __init__(self, name, price):
    #             self.name = name
    #             self.price = price

    #     class Food():
    #         def __init__(self, name, price):
    #             Function(Product).call(self, name, price)
    #             self.category = 'food'

    #     class Toy():
    #         def __init__(self, name, price):
    #             Function(Product).call(self, name, price)
    #             self.category = 'toy'

    #     cheese = Food('feta', 5)
    #     fun = Toy('robot', 40)

    #     print(cheese)
    #     print(fun)


    def test_esx_numbersandstrings(self):
        print("test_esx_numbersnstrings")

        n = Number(1)
        n2 = Number(2)
        print(n + n2)

        s = String('a')
        s2 = String('b')
        print(s + s2)
        print(s * n2)

        test = String("test")
        # print(test - 2) # considering allowing this

        print(test[0:1])

        print(test.toUpperCase())
        print(test.toLowerCase())
        print(test.toLocaleLowerCase())
        print(test.toLocaleUpperCase())


    def test_set(self):

        mySet1 = Set()

        mySet1.add(1)           # Set [ 1 ]
        assert mySet1.size == 1
        assert mySet1.contains(1) == True
        assert mySet1.contains(2) == False

        mySet1.add(5)           # Set [ 1, 5 ]
        assert mySet1.size == 2
        assert mySet1.contains(1) == True
        assert mySet1.contains(2) == False
        assert mySet1.contains(5) == True

        mySet1.add(5)           # Set [ 1, 5 ]
        assert mySet1.size == 2
        assert mySet1.contains(1) == True

        mySet1.add('some text') # Set [ 1, 5, 'some text' ]
        assert mySet1.size == 3
        assert mySet1.contains(1) == True
        assert mySet1.contains(2) == False
        assert mySet1.contains(5) == True
        assert mySet1.contains('some text') == True
        assert mySet1.contains('text') == False

        '''
        # TODO - make the following work. js sets can have dictionaries in them
        o = {'a': 1, 'b': 2}
        mySet1.add(o)  # TODO - ok. so we learned something. i nearly never use sets so this is a nice example of difference between python and esx sets.
        assert mySet1.size == 4
        assert mySet1.contains(a) == True

        mySet1.add({a: 1, b: 2})   # o is referencing a different object, so this is okay

        assert mySet1.has(1) == True
        assert mySet1.has(3) == False
        assert mySet1.has(5) == True
        assert mySet1.has(Math.sqrt(25)) == True
        assert mySet1.has('Some Text'.toLowerCase()) == True
        assert mySet1.has(o) == True

        mySet1.size == 5

        mySet1.delete(5)    # removes 5 from the set
        assert mySet1.has(5) == False

        mySet1.size == 4

        console.log(mySet1)
        # logs Set(4) [ 1, "some text", {…}, {…} ] in Firefox
        # logs Set(4) { 1, "some text", {…}, {…} } in Chrome
        '''

    def test_setTimeout(self):
        """ Test the Global.setTimeout function calls the callback. """

        callback = Mock()

        args = ("hello", "world")
        kwargs = {"foo": "bar"}

        timer_id = Global.setTimeout(callback, 1000, *args, **kwargs)
        callback.assert_not_called()

        assert timer_id in Global._Global__timers

        time.sleep(1.5)

        callback.assert_called_once()
        callback.assert_called_with(*args, **kwargs)

    def test_clearTimeout(self):
        """ Test that Global.clearTimeout function can cancel a timeout. """

        callback = Mock()

        args = ("hello", "world")
        kwargs = {"foo": "bar"}

        timer_id = Global.setTimeout(callback, 1000, *args, **kwargs)
        callback.assert_not_called()

        assert timer_id in Global._Global__timers
        Global.clearTimeout(timer_id)
        assert timer_id not in Global._Global__timers

        time.sleep(1.5)
        callback.assert_not_called()

    def test_timeouts(self):
        def somefunc():
            print("hi")
        someID = Global.setTimeout(somefunc, 2000)
        Global.clearTimeout(someID)
        time.sleep(2.5)
        # nice!

        # from esx.javascript import setTimeout, clearTimeout
        # setTimeout(somefunc, 2000)
        # time.sleep(2.5)

        # from esx.javascript import setInterval, clearInterval
        # def somefunc2():
            # print("testing interval")
        # interval_id = setInterval(somefunc2, 2000)
        # time.sleep(10)
        # clearInterval(interval_id)
        # time.sleep(4)
        # print('end')

        # from esx.javascript import window
        # intID = window.setInterval(somefunc2, 2000)
        # time.sleep(10)
        # clearInterval(intID)  # not clearing brings it back to life!





    # def test_storage(self):
    #     print("test_storage")

    #     myObj = Storage()
    #     myObj.name = 'John'
    #     myObj.age = 30
    #     myObj.address = '123 Main St'

    #     assert myObj.name == 'John'
    #     assert myObj.age == 30
    #     assert myObj.address == '123 Main St'

    #     window.localStorage.setItem('myObj', myObj)
    #     window.localStorage.getItem('myObj')
    #     myObj2 = window.localStorage.getItem('myObj')
    #     assert myObj2.name == 'John'
    #     assert myObj2.age == 30


    # def test_reflect(self):
    #     print("test_reflect")
    #     myObj = {'name': 'John', 'age': 30, 'address': '123 Main St'}

    #     myObj2 = Reflect(myObj)
    #     assert myObj2.name == 'John'
    #     assert myObj2.age == 30
    #     assert myObj2.address == '123 Main St'
    #     assert myObj2.toString() == '{"name": "John", "age": 30, "address": "123 Main St"}'


    # def test_symbol(self):
    #     print("test_symbol")
    #     symbol = Symbol('x')

    #     assert symbol.name == 'x'
    #     assert symbol.value == 0
    #     assert symbol.toString() == 'x'
    #     assert symbol.toNumber() == 0
    #     assert symbol.toString(True) == '0'




_intID = None
_results = []


if __name__ == '__main__':
    unittest.main()
