


from transaction import Transaction

class Purchase:
    def __init__(self):
        self.transactions = list[  Transaction ]

    def get_total_cost_of_purchases(self):
        total = 0.0
        it: Transaction = None
        for it  in self.transactions :
            total += it.Sales_Amount

        return total

    def addTransaction(self, transaction: Transaction)-> bool :
        if transaction in self.transactions:
            return True

        if len( self.transactions) > 0 :
            aTransaction:Transaction  = self.transactions[ 0  ]
            custID = aTransaction.Customer_ID
            puchaseID = aTransaction.Transaction_ID
            if custID == transaction.Transaction_ID and puchaseID == transaction.Transaction_ID:
                self.transactions.append( transaction )
                return True

        return False



class Customer:
    def __init__(self, Customer_ID):
        self.Customer_ID = Customer_ID
        self.transactions =  dict[ str, Purchase]( )

    def addTransaction(self , trans : Transaction):
        assert  isinstance( trans , Transaction )==True , "Only add transactions"
        assert  self.Customer_ID == trans.Customer_ID , " do not add transactions which do not belong"
        product = trans.product

        if product not in self.transactions :
            self.transactions[ product ]  =  trans

    def get_total_cost_of_purchases(self)->float:
        total = 0.0
        for purch  in self.transactions:
            total += self.transactions[ purch].Sales_Amount

        return total

    def getID(self):
        return self.Customer_ID

if __name__ == "__main__":
    sample_data = [
            '1,02/01/2016,2547,1,X52,0EM7L,1,3.13',
            '2,02/01/2016,822,2,2ML,68BRQ,1,5.46',
            '3,02/01/2016,3686,3,0H2,CZUZX,1,6.35',
            '4,02/01/2016,3719,4,0H2,549KK,1,5.59',
            '5,02/01/2016,9200,5,0H2,K8EHH,1,6.88',
            '6,02/01/2016,5010,6,JPI,GVBRC,1,10.77',
            '7,02/01/2016,1666,7,XG4,AHAE7,1,3.65',
            '8,02/01/2016,1666,7,FEW,AHZNS,1,8.21',
            '9,02/01/2016,1253,8,0H2,9STQJ,1,8.25',
            '10,02/01/2016,5541,9,N5F,7IE9S,1,8.18',
            '11,02/01/2016,5541,9,H8O,M15RG,1,6.35',
            '12,02/01/2016,7548,10,N8U,UNJKW,1,2.11'
        ]

    transactions = list()
    customers = dict[str, Customer]( )

    for row in sample_data:
        try:
            transaction = Transaction.from_csv_row(row)
            transactions.append(transaction)
        except ValueError as e:
            print(f"Error processing row: {e}")

    for tran in transactions:
        if tran.Customer_ID not in customers:
            newCustomer = Customer( tran.Customer_ID )
            customers[  tran.Customer_ID ] = newCustomer

        theCustomer = customers[ tran.Customer_ID ]
        assert  theCustomer is not None , "should always be in dictionary "
        theCustomer.addTransaction( tran )

    for cust in customers.keys():
        print(f" {cust}, {customers[cust ]}")

    #part 2 - do recogmender



