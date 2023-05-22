from django import dispatch

bookingNotification = dispatch.Signal(providing_args=["booking", 'user'])
