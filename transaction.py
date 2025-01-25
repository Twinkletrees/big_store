from datetime import datetime

class Transaction:
    def __init__(self, ID, Date, Customer_ID, Transaction_ID, SKU_Category, SKU, Quantity, Sales_Amount):
        """
        Initialize a Transaction object with the provided attributes.

        Args:
            ID (int): Unique identifier of the transaction.
            Date (str): Transaction date in MM/DD/YYYY format.
            Customer_ID (int): Unique identifier of the customer.
            Transaction_ID (int): Unique identifier of the transaction.
            SKU_Category (str): Category of the SKU.
            SKU (str): Stock Keeping Unit identifier.
            Quantity (int): Quantity of items sold.
            Sales_Amount (float): Total sales amount for the transaction.
        """
        self._ID = None
        self._Date = None
        self._Customer_ID = None
        self._Transaction_ID = None
        self._SKU_Category = None
        self._SKU = None
        self._Quantity = None
        self._Sales_Amount = None

        # Use setters to ensure validation during initialization
        self.ID = ID
        self.Date = Date
        self.Customer_ID = Customer_ID
        self.Transaction_ID = Transaction_ID
        self.SKU_Category = SKU_Category
        self.SKU = SKU
        self.Quantity = Quantity
        self.Sales_Amount = Sales_Amount

    # ID Property
    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value):
        if not isinstance(value, int):
            raise TypeError("ID must be an integer.")
        if value <= 0:
            raise ValueError("ID must be a positive integer.")
        self._ID = value

    # Date Property
    @property
    def Date(self):
        return self._Date

    @Date.setter
    def Date(self, value):
        if isinstance(value, datetime):
            self._Date = value
        elif isinstance(value, str):
            try:
                self._Date = datetime.strptime(value, "%d/%m/%Y")
            except ValueError:
                raise ValueError("Date must be in DD/MM/YYYY format." + value)
        else:
            raise TypeError("Date must be a string inD/MM/YYYY format or a datetime object.")

    # Customer_ID Property
    @property
    def Customer_ID(self):
        return self._Customer_ID

    @Customer_ID.setter
    def Customer_ID(self, value):
        if not isinstance(value, int):
            raise TypeError("Customer_ID must be an integer.")
        if value <= 0:
            raise ValueError("Customer_ID must be a positive integer.")
        self._Customer_ID = value

    # Transaction_ID Property
    @property
    def Transaction_ID(self):
        return self._Transaction_ID

    @Transaction_ID.setter
    def Transaction_ID(self, value):
        if not isinstance(value, int):
            raise TypeError("Transaction_ID must be an integer.")
        if value <= 0:
            raise ValueError("Transaction_ID must be a positive integer.")
        self._Transaction_ID = value

    # SKU_Category Property
    @property
    def SKU_Category(self):
        return self._SKU_Category

    @SKU_Category.setter
    def SKU_Category(self, value):
        if not isinstance(value, str):
            raise TypeError("SKU_Category must be a string.")
        if not value:
            raise ValueError("SKU_Category cannot be empty.")
        self._SKU_Category = value
    # SKU Property
    @property
    def SKU(self):
        return self._SKU

    @SKU.setter
    def SKU(self, value):
        if not isinstance(value, str):
            raise TypeError("SKU must be a string.")
        if not value:
            raise ValueError("SKU cannot be empty.")
        self._SKU = value

    @property
    def product(self)->str:
        assert self._SKU_Category is not None , "No empty catagory "
        assert  self._SKU is not None , "No empty products "
        return self._SKU_Category + "_"  +  self._SKU

    # Quantity Property
    @property
    def Quantity(self)->float:
        return self._Quantity

    @Quantity.setter
    def Quantity(self, value:float):
        if not isinstance(value, float):
            raise TypeError("Quantity must be an float.")
        if value < 0:
            raise ValueError("Quantity cannot be negative.")
        self._Quantity = value

    # Sales_Amount Property
    @property
    def Sales_Amount(self):
        return self._Sales_Amount

    @Sales_Amount.setter
    def Sales_Amount(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Sales_Amount must be a number.")
        if value < 0:
            raise ValueError("Sales_Amount cannot be negative.")
        self._Sales_Amount = float(value)

    @classmethod
    def from_csv_row(cls, row):
        """
        Create a Transaction instance from a CSV row string.

        Args:
            row (str): A string representing a CSV row.

        Returns:
            Transaction: An instance of Transaction.

        Raises:
            ValueError: If the row does not contain exactly 8 fields or if type conversion fails.
        """
        fields = row.strip().split(',')
        if len(fields) != 8:
            raise ValueError(f"Expected 8 fields, got {len(fields)}: {row}")

        try:
            ID = int(fields[0])
            Date = fields[1]
            Customer_ID = int(fields[2])
            Transaction_ID = int(fields[3])
            SKU_Category = fields[4]
            SKU = fields[5]
            Quantity = float (fields[6])
            Sales_Amount = float(fields[7])
        except ValueError as ve:
            raise ValueError(f"Error parsing fields: {ve}. Row: {row}")

        return cls(ID, Date, Customer_ID, Transaction_ID, SKU_Category, SKU, Quantity, Sales_Amount)

    def __repr__(self):
        """
        Return an unambiguous string representation of the Transaction object.

        Returns:
            str: String representation of the Transaction.
        """
        return (f"Transaction(ID={self.ID}, Date={self.Date.strftime('%m/%d/%Y')}, "
                f"Customer_ID={self.Customer_ID}, Transaction_ID={self.Transaction_ID}, "
                f"SKU_Category='{self.SKU_Category}', SKU='{self.SKU}', "
                f"Quantity={self.Quantity}, Sales_Amount={self.Sales_Amount})")

    # Example usage:
if __name__ == "__main__":
    sample_data = [
        "1,02/01/2016,2547,1,X52,0EM7L,1,3.13",
        "2,02/01/2016,822,2,2ML,68BRQ,1,5.46",
        "3,02/01/2016,3686,3,0H2,CZUZX,1,6.35",
        "4,02/01/2016,3719,4,0H2,549KK,1,5.59",
        "5,02/01/2016,9200,5,0H2,K8EHH,1,6.88",
        "6,02/01/2016,5010,6,JPI,GVBRC,1,10.77"
    ]

    transactions = []
    for row in sample_data:
        try:
            transaction = Transaction.from_csv_row(row)
            transactions.append(transaction)
        except ValueError as e:
            print(f"Error processing row: {e}")

    for transaction in transactions:
        print(transaction)


