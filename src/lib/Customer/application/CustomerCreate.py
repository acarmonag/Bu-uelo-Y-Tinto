from src.lib.Customer.domain.Customer import Customer
from src.lib.Customer.domain.CustomerSpecification import CustomerCommandCreate
from src.lib.Customer.domain.CustomerRepository import CustomerRepository
from src.lib.Shared.domain.errors.DomainError import ValidationError


class CustomerCreator:
    """Application service responsible for creating new customers.
    
    This class implements the use case for customer creation, following the
    Command pattern. It orchestrates the validation and persistence of new customers.
    
    Attributes:
        repository: CustomerRepository instance for data persistence
    """
    
    def __init__(self, repository: CustomerRepository):
        """Initialize the CustomerCreator with a repository.
        
        Args:
            repository: CustomerRepository instance for data persistence
        """
        self.repository = repository
    
    def execute(self, command: CustomerCommandCreate) -> Customer:
        """Executes the customer creation use case.
        
        This method follows a two-step process:
        1. Validates the input command
        2. Persists the command through the repository
        
        Args:
            command: CustomerCommandCreate DTO containing the customer data
            
        Returns:
            Customer: The newly created and persisted customer entity
            
        Raises:
            ValidationError: If the command data is invalid
            RepositoryError: If there's an error during persistence
        """
        # 1. Validate command
        errors = command.validate()
        if errors:
            raise ValidationError(', '.join(errors))
        
        # 2. Save to repository
        saved_customer = self.repository.create(command)
        
        return saved_customer