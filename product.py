class Product:
    def __init__(self, SKU_Category, SKU: str):
        """
        Initialize a Product object with the provided SKU_Category and SKU.

        Args:
            SKU_Category (str): The category of the SKU.
            SKU (str): The Stock Keeping Unit identifier.
        """
        self._SKU_Category = None
        self._SKU = None

        # Use setters to ensure validation during initialization
        self.SKU_Category = SKU_Category
        self.SKU = SKU

    # SKU_Category Property
    @property
    def SKU_Category(self):
        """Get the SKU_Category of the Product."""
        return self._SKU_Category

    @SKU_Category.setter
    def SKU_Category(self, value):
        """
        Set the SKU_Category of the Product with validation.

        Args:
            value (str): The new SKU_Category value.

        Raises:
            TypeError: If the value is not a string.
            ValueError: If the value is an empty string.
        """
        if not isinstance(value, str):
            raise TypeError("SKU_Category must be a string.")
        if not value.strip():
            raise ValueError("SKU_Category cannot be empty.")
        self._SKU_Category = value.strip()

    # SKU Property
    @property
    def SKU(self):
        """Get the SKU of the Product."""
        return self._SKU

    @SKU.setter
    def SKU(self, value):
        """
        Set the SKU of the Product with validation.

        Args:
            value (str): The new SKU value.

        Raises:
            TypeError: If the value is not a string.
            ValueError: If the value is an empty string.
        """
        if not isinstance(value, str):
            raise TypeError("SKU must be a string.")
        if not value.strip():
            raise ValueError("SKU cannot be empty.")
        self._SKU = value.strip()

    def __eq__(self, other):
        """
        Check equality between two Product instances.

        Two products are considered equal if both their SKU_Category and SKU are identical.

        Args:
            other (Product): The other Product instance to compare against.

        Returns:
            bool: True if both products are equal, False otherwise.
        """
        if not isinstance(other, Product):
            return NotImplemented
        return (self.SKU_Category, self.SKU) == (other.SKU_Category, other.SKU)

    def __hash__(self):
        """
        Return the hash of the Product instance.

        The hash is based on the SKU_Category and SKU, making the object usable in sets and as dictionary keys.

        Returns:
            int: The hash value of the Product.
        """
        return hash((self.SKU_Category, self.SKU))

    def __gt__(self, other):
        """
        Define the greater-than comparison between two Product instances.

        Products are compared first by SKU_Category and then by SKU in lexicographical order.

        Args:
            other (Product): The other Product instance to compare against.

        Returns:
            bool: True if self is greater than other, False otherwise.

        Raises:
            TypeError: If 'other' is not an instance of Product.
        """
        if not isinstance(other, Product):
            raise TypeError("Comparisons should be between Product instances.")
        return (self.SKU_Category, self.SKU) > (other.SKU_Category, other.SKU)

    def __repr__(self):
        """
        Return an unambiguous string representation of the Product object.

        Returns:
            str: String representation of the Product.
        """
        return f"Product(SKU_Category='{self.SKU_Category}', SKU='{self.SKU}')"

