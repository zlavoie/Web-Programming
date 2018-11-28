class Email:
    def __init__(self,subject,Num,recepient,message,sender):
        self.subject=subject
        self.Num=Num
        self.recepient=recepient
        self.message=message
        self.sender=sender

    def toString(self):
        return self.subject+" "+self.Num+" "+self.recepient+" "+self.message+" "+self.sender
