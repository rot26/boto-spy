class BotoSessionSpySingleton:
    """
    A Singleton class that spies on a boto session.

    This class is designed to track all request ids made via a boto session.
    For each session, there is only one instance of this class.

    Attributes:
        _instances (dict): A dictionary to store instances of this class.
        session (str): The session associated with the instance.
        request_ids (list): A list to store all request ids made via the session.

    Usage:
        # Create a new instance or get the existing one for the session 'session1'
        s1 = BotoSessionSpySingleton('session1')

        # Add a request id to the instance's list of request ids
        s1.add_request_id('request1')

        # Print all request ids for the instance
        print(s1.get_request_ids())  # ['request1']

        # Create a new instance or get the existing one for the session 'session2'
        s2 = BotoSessionSpySingleton('session2')

        # Add a request id to the instance's list of request ids
        s2.add_request_id('request2')

        # Print all request ids for the instance
        print(s2.get_request_ids())  # ['request2']

        # Get the existing instance for the session 'session1'
        s1_again = BotoSessionSpySingleton('session1')

        # Print all request ids for the instance
        # It should print ['request1'] because it's the same instance as s1
        print(s1_again.get_request_ids())  # ['request1']
    """

    _instances = {}

    def __new__(cls, session):
        """
        Create a new instance of the class for the given session if it doesn't exist,
        or return the existing one.

        Args:
            session (str): The session to get the instance for.

        Returns:
            BotoSessionSpySingleton: The instance of the class for the given session.
        """
        session_id = id(session)
        if session_id not in cls._instances:
            cls._instances[session_id] = super(BotoSessionSpySingleton, cls).__new__(cls)
            cls._instances[session_id].session = session
            cls._instances[session_id].request_ids = []
        return cls._instances[session_id]

    def add_request_id(self, request_id):
        """
        Add a request id to the instance's list of request ids.

        Args:
            request_id (str): The request id to add.
        """
        self.request_ids.append(request_id)

    def get_request_ids(self):
        """
        Return all request ids for the instance.

        Returns:
            list: The list of request ids.
        """
        return self.request_ids
