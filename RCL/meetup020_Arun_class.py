class Employee:
    emp_count = 0 # class variable

    def __init__(self, fname, lname, age):
        Employee.emp_count += 1
        self.fname = fname
        self.lname = lname
        self.age = int(age)
        #self.email = self.fname + "." + self.lname +"@gmail.com"
    def __repr__(self):
        return self.fname
    @classmethod
    def from_str(cls, emp_str):
        fname,lname,age = emp_str.split("_")
        return cls(fname,lname,age)
    @property
    def email(self):
        return self.fname + "." + self.lname +"@gmail.com"
    @property
    def fullname(self):
        return self.fname + " " +self.lname
    
    @fullname.setter
    def fullname(self,val):
        self.fname, self.lname = val.split(" ")
    @fullname.deleter
    def fullname(self):
        self.fname, self.lname = None, None
    
    def age_days(self):
        return self.age *365

    def odd_even(self,num):
        return num%2 ==0

e1 = Employee("arun","prakash",22)
e2 = Employee.from_str("arun_prakash_29")

print(e2.odd_even(e2.age))
print(e2.fname)
print(e2)




