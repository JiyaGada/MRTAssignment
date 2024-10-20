vehicleList=[]
Report=[]
Customers=[]
class Vehicle:
    vehicle_type="Car"

    def __init__(self, vehicle_id, make, model, year, rental_rate, availability):
        self.vehicle_id=vehicle_id
        self.make=make
        self.model=model
        self.year=year
        self.rental_rate=rental_rate
        self.availability=availability
    
    def Rent(vehicle, customer_id, rental_duration): #rental duration in days
        
        if vehicle.availability==True:
            y=False
            for i in Customers:
                if i.customer_id==customer_id:
                    y=True
                    if type(i)==PremiumCustomer:
                        PremiumCustomer.ApplyDiscount(vehicle, rental_duration)
                    elif type(i)==RegularCustomer:
                        c=input("You have "+ str(i.loyalty_points)+ " loyalty points. Do you want to redeem? (Y/N): ")
                        if c=="y" or c=="Y":
                            RegularCustomer.RedeemLoyaltyPoints(i,vehicle,rental_duration)
                        i.loyalty_points+=1 #adding loyalty points for rented vehicle
                    vehicle.availability=False
                    Report.append([vehicle.__dict__,i.__dict__])
                    i.rental_history.append(vehicle.__dict__)
                    break
            if (not y):
                print("No such customer exists. Add customer first.")   
            print(vehicle.vehicle_id + " rented to " + customer_id +" - "+i.name+ " for " + str(rental_duration) + " days.") 
        else :
            print("Vehicle not available" )  
    
    def Return(): #customer_id may be added
        id=input("Enter vehicle id:")
        for vehicle in vehicleList:
            if vehicle.vehicle_id==id:
                if vehicle.availability==False:
                    vehicle.availability=True
                    print("Vehicle returned")
                else: 
                    print("Vehicle was not rented")
                
    
    def DisplayVehicleDetails(id):
        for vehicle in vehicleList:
            if vehicle.vehicle_id==id:
                print(vehicle.__dict__)

class Luxury_Vehicle(Vehicle):
    rental_rate=1.20 # ?

    def __init__(self, vehicle_id, make, model, year, rental_rate, availability, extra_features):
        super().__init__(vehicle_id, make, model, year, rental_rate, availability)
        Luxury_Vehicle.extra_features=extra_features
    
    def DisplayExtraFeatures(self):
        print(self.extra_features)

class Customer:
    def __init__(self, customer_id, name, contact_info, rental_history):
        self.customer_id=customer_id
        self.name=name
        self.contact_info=contact_info
        self.rental_history=rental_history
    
    def DisplayCustomerDetails(customer_id):
        for i in Customers:
            if i.customer_id==customer_id:
                print(i.__dict__)
                break

    def DisplayCustomerRentalDetails(customer_id):
        for i in Customers:
            if i.customer_id==customer_id:
                print(i.rental_history)
                break

    def AddCustomerDetails():
        customer_id=input("Enter customer id:")
        name=input("Enter customer name:")
        contact_info=input("Enter contanct info:")
        rental_history=[]
        type=input("Is he/she a premium customer?(Y/N):")
        if type=="Y" or type=="y":
            customer=PremiumCustomer(customer_id, name, contact_info,rental_history)
        else:
            loyalty_points=0
            customer=RegularCustomer(customer_id, name, contact_info,rental_history,loyalty_points)
        Customers.append(customer)

class RegularCustomer(Customer):
    def __init__(self,customer_id, name, contact_info, rental_history, loyalty_points):
        super().__init__(customer_id, name, contact_info, rental_history)
        RegularCustomer.loyalty_points=loyalty_points

    def RedeemLoyaltyPoints(customer,vehicle, rental_duration):
        if customer.loyalty_points>0:
            price=vehicle.rental_rate*rental_duration*0.99*customer.loyalty_points 
            customer.loyalty_points=0 #reset points after redeeming
            print("Customer has to pay" + str(price))
        else:
            print("Insufficient loyalty points to redeem")


class PremiumCustomer(Customer):
    def ApplyDiscount(vehicle, rental_duration):
        price=vehicle.rental_rate*rental_duration*0.9
        print("Customer has to pay " + str(price) + " after premium customer discount")

class RentalManager:
    def AddVehicle():
        vehicle_id=input("Enter vehicle id:")
        make=input("Enter make:")
        model=input("Enter model:")
        year=input("Enter year:")
        rental_rate=int(input("Enter rental rate:"))
        availability=True
        luxury=input("Is it a luxury vehicle?(Y/N):")
        if luxury=="Y" or luxury=="y":
            extra=input("Enter extra faetures:")
            vehicle=Luxury_Vehicle(vehicle_id,make,model,year,rental_rate,availability, extra)
            vehicleList.append(vehicle)
        else:
            vehicle=Vehicle(vehicle_id,make,model,year,rental_rate,availability)
            vehicleList.append(vehicle)

    def ShowAvailableVehicles():
        for i in vehicleList:
            if i.availability==True:
                print(i.__dict__)

    def RemoveUnavailableVehicles():
        for i in vehicleList:
            if i.availability==False:
                vehicleList.remove(i)

    def ShowReport():
        for i in Report:
            print(i)
    

print('''
      1:Add Vehicle
      2:Add Customer
      3:Rent Vehicle
      4:Return Vehicle
      5:Show Available Vehicles
      6:Show Report of Hired Veihcles
      7:Show Customer Rental History
      8:Show Customer Details
      9:Show Vehicle Details
      10:Exit''')

while True:
    c=int(input("Enter your choice:"))
    if c==1:
        RentalManager.AddVehicle()
    elif c==2:
        Customer.AddCustomerDetails()
    elif c==3:
        id=input("Enter vehicle id:")
        customer_id=input("Enter customer id:")
        rental_duration=int(input("Enter rental duration:"))
        x=False
        for vehicle in vehicleList:
            if vehicle.vehicle_id==id:
                x=True
                Vehicle.Rent(vehicle, customer_id, rental_duration)
                break
        if (not x):
            print("No such vehicle exists. Add a vehicle first")
    elif c==4:
        Vehicle.Return()
    elif c==5:
        RentalManager.ShowAvailableVehicles()
    elif c==6:
        RentalManager.ShowReport()
    elif c==7:
        id=input("Enter customer id:")
        Customer.DisplayCustomerRentalDetails(id)
    elif c==8:
        id=input("Enter customer id:")
        Customer.DisplayCustomerDetails(id)
    elif c==9:
        id=input("Enter vehicle id:")
        Vehicle.DisplayVehicleDetails(id)
    elif c==10:
        break
    else:
        print("Invalid Input")