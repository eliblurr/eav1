class NotFoundError(Exception):
    def __init__(self, message):
        self.message = message

# class NotFoundError_(Exception):
#     def __init__(self, expression, message):
#         self.expression = expression
#         self.message = message
    
# class NotFoundError3(Exception):
#     def __init__(self, message):
#         self.message = message