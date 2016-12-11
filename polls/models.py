class Buyer:
    def __init__(self, idBuyer, nameBuyer, surnameBuyer, age):
        self.idBuyer = idBuyer
        self.nameBuyer = nameBuyer
        self.surnameBuyer = surnameBuyer
        self.age = age


def buyerFromDict(dict):
    buyer = Buyer(dict['idBuyer'], dict['nameBuyer'], dict['surnameBuyer'], dict['age'])
    return buyer


class Book:
    def __init__(self, idBook, titleBook, author, publisherBook):
        self.idBook = idBook
        self.titleBook = titleBook
        self.author = author
        self.publisherBook = publisherBook


def bookFromDict(dict):
    book = Book(dict['idBook'], dict['titleBook'], dict['author'], dict['publisherBook'])
    return book


class Journal:
    def __init__(self, idJournal, titleJournal, publisher):
        self.idJournal = idJournal
        self.titleJournal = titleJournal
        self.publisher = publisher


def journalFromDict(dict):
    journal = Journal(dict['idJournal'], dict['titleJournal'], dict['publisher'])
    return journal


class Purchase:
    def __init__(self, idPurchase, buyer, book, journal, buyDate, price):
        self.idPurchase = idPurchase
        self.buyer = buyer
        self.book = book
        self.journal = journal
        self.buyDate = buyDate
        self.price = price


def purchaseFromDict(dict):
    purchase = None
    if dict != None:
        purchase = Purchase(dict['idPurchase'], buyerFromDict(dict['buyer']), bookFromDict(dict['book']),
                              journalFromDict(dict['journal']), dict['buyDate'], dict['price'])
    return purchase
