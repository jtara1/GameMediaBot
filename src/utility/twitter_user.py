class TwitterUser:
    def __init__(self, screen_name, categories):
        """
        Args:
            screen_name (str):
                Username as seen on twitter
            categories (collection of ClassificationCategory): 
                List of possible categories that each tweet can be classified as
        """
        self.screen_name = screen_name
        self.categories = categories
