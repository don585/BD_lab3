from datetime import date
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.code import Code
from polls.models import purchaseFromDict, buyerFromDict, bookFromDict, journalFromDict
import redis
import random
import json
import pickle


class DB(object):
    def __init__(self):
        self.connection = MongoClient('localhost', 27017)
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.db = self.connection.new_purchase
        self.buyers = self.db.Buyer
        self.books = self.db.Book
        self.journals = self.db.Journal
        self.purchases = self.db.Purchase

    def generate(self):
        idPurchase = self.purchases.count() + 1
        for i in range (0, 50000):
            rand_buyer = random.randint(0, 4)
            rand_book = random.randint(0, 4)
            rand_journal = random.randint(0, 4)
            buyer = self.buyers.find().skip(rand_buyer).next()
            book = self.books.find().skip(rand_book).next()
            journal = self.journals.find().skip(rand_journal).next()
            purchase = {'idPurchase': str(idPurchase),'buyer': buyer, 'book': book, 'journal': journal, 'buyDate': date.today().strftime(
                '%Y/%m/%d'), 'price': str(random.randint(100, 1000))}
            self.purchases.insert(purchase)
            idPurchase += 1

    def initialization(self):
        self.books.drop()
        self.journals.drop()
        self.buyers.drop()
        self.purchases.drop()

        data = json.load(open('test.json'))

        idBuyer = 1
        idBook = 1
        idJournal = 1
        idPurchase = 1
        buyer_list = data['buyer']
        for buyer in buyer_list:
            try:
                name = str(buyer['nameUser'])
                surname = str(buyer['surnameUser'])
                age = str(buyer['age'])
                self.buyers.insert({"idBuyer": str(idBuyer), "nameBuyer": name, "surnameBuyer": surname, "age": age})
                idBuyer += 1
            except IndexError:
                pass
            continue

        journal_list = data['journal']
        for journal in journal_list:
            try:
                titleJournal = str(journal['titleJournal'])
                publisher = str(journal['publisher'])
                self.journals.insert({"idJournal": str(idJournal), "titleJournal": titleJournal, "publisher":
                    publisher})
                print(titleJournal, publisher)
                idJournal += 1
            except IndexError:
                pass
            continue

        book_list = data['book']
        for book in book_list:
            try:
                titleBook = str(book['titleBook'])
                author = str(book['author'])
                publisherBook = str(book['publisher'])
                self.books.insert({"idBook": str(idBook), "titleBook": titleBook, "author": author, "publisherBook":
                    publisherBook})
                print(titleBook, author)
                idBook += 1
            except IndexError:
                pass
            continue

        purchase_list = data['purchase']

        for purchase in purchase_list:
            try:
                buyer = self.buyers.find({"idBuyer": str(purchase['buyer'])})
                book = self.books.find({"idBook": str(purchase['book'])})
                journal = self.journals.find({"idJournal": str(purchase['titleJournal'])})
                price = int(purchase['price'])
                saleDate = str(purchase['saleDate'])
                self.purchases.insert_one({"idPurchase": str(idPurchase),"buyDate": saleDate, "price": price,
                                        "journal": journal[0], "book": book[0], "buyer": buyer[0]})
                idPurchase += 1
            except IndexError:
                pass
            continue
        self.generate()

    def getBuyer(self):
        buyers = []
        res = self.buyers.find()
        for x in res:
            buyers.append(buyerFromDict(x))
        return buyers

    def getJournal(self):
        journal = []
        res = self.journals.find()
        for x in res:
            journal.append(journalFromDict(x))
        return journal

    def getBooks(self):
        books = []
        res = self.books.find()
        for x in res:
            books.append(bookFromDict(x))
        return books

    def getPurchaseList(self):
        res = []
        result = self.purchases.find()
        for x in result:
            res.append(purchaseFromDict(x))
        return res

    def getPurchase(self, id):
        return purchaseFromDict(self.purchases.find_one({"idPurchase": str(id)}))

    def savePurchase(self, buyDate, price, idBook, idJournal, idBuyer):
        idPurchase = self.purchases.count()
        journal = self.journals.find({"idJournal": idJournal})
        book = self.books.find({"idBook": idBook})
        buyer = self.buyers.find({"idBuyer": idBuyer})
        res = self.purchases.insert_one({"idPurchase": str(idPurchase+1), "buyDate": buyDate, "price": price,
                                        "journal": journal[0], "book": book[0], "buyer": buyer[0]})

    def updatePurchase(self, idPurchase, buyDate, price, book, journal, buyer):
        print(idPurchase, buyDate, book, journal, buyer)
        new_buyer = self.buyers.find({"idBuyer": buyer})
        new_book = self.books.find({"idBook": book})
        new_journal = self.journals.find({"idJournal": journal})
        pur = self.purchases.find_one({"idPurchase": str(idPurchase)})
        self.r.delete(pur["buyer"]["idBuyer"])
        self.r.delete(buyer)
        res = self.purchases.update_one({"idPurchase": str(idPurchase)}, {'$set': {"buyer": new_buyer[0],
            "book": new_book[0], "journal": new_journal[0], "buyDate": buyDate, "price": price}})
        return res

    def removePurchase(self, id):
        print (id)
        pur = self.purchases.find_one({"idPurchace": str(id)})
        self.r.delete(pur["buyer"]["idBuyer"])
        self.purchases.remove({"idPurchase": str(id)}, 1)

    def search(self, idBuyer):
        if self.r.exists(idBuyer) != 0:
            purchase = pickle.loads(self.r.get(idBuyer))
        else:
            query = {}
            if idBuyer != '0':
                query["buyer.idBuyer"] = idBuyer # ObjectId(request.GET['client_id'])
                purchase = list(self.purchases.find(query))
            self.r.set(idBuyer,  pickle.dumps(purchase))
        new_purchases = []
        for x in purchase:
            new_purchases.append(purchaseFromDict(x))
        return new_purchases
        # return list(competitions)

    def status(self, idBuyer):
        if self.r.exists(idBuyer) != 0:
            return 0
        else: return 1


