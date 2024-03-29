from selenium_scraping import neighbour_construction, spokeo_construction,propertyShark
from ownerly import ownerlyConstruction
from xome import xomeConstruction


def init():
    print("\n\tYEAR BUILT BOT")
    print("-----------------------------------------------------------------------\n")
    input_address = input('Enter the address :').upper().replace(",", "")
    addressList = input_address.split()

    if (addressList[-1] == "STATES" and addressList[-2] == "UNITED"):
        addressList.remove("STATES")
        addressList.remove("UNITED")

    if addressList[-1] == "USA":
        addressList.remove("USA")
    original_list = input_address[:]
    direction = ["", ""]
    cityInput = input('Enter city name:').upper().split(" ")

    if "CO" in cityInput:
        cityInput.remove("CO")
        addressList.remove("CO")
    cityCount = len(cityInput)
    ignore_list = ["N", "S", "W", "E", "NE", "NW", "SE", "SW"]
    dir_status = 0
    count = 0
    for component in addressList:
        if component in ignore_list:
            direction[0] = component
            direction[1] = count
            dir_status = 1
            addressList.remove(component)
        count = count+1

    street = addressList[1:-3-(cityCount-1)]

    zip = addressList[-1]
    buildingNum = addressList[0]
    state = addressList[-2]

    city = addressList[-3-(cityCount-1):-2]

    print("-----------------------------------------------------------------------\n")

    try:
        ownerlyConstruction(state, city, street, buildingNum,
                            direction, dir_status)
    except:
        print("OWNERLY: ERROR")
    try:
        neighbour_construction(state, street, city,
                               buildingNum, direction, dir_status)
    except:
        print("NEIGHBOUR WHO: ERROR")

    try:
        spokeo_construction(state, street, city, buildingNum,
                            direction, dir_status)
    except:
        print("SPOKEO: ERROR")
    try:
        propertyShark(input_address)
    except:
        print("PROPERTY SHARK: ERROR")

    # try:
    #     been_verified(state, street, city, buildingNum,
    #                   direction, dir_status)
    # except:
    #     print("BEEN VERIFIED: ERROR")

    try:
        xomeConstruction(state, city, street, buildingNum,
                         zip, original_list, dir_status, direction)
    except:
        print("XOME: ERROR")

    print("\n-----------------------------------------------------------------------\n")


while True:
    init()

    print("-----------------------------------------------------------------------\n")
    # choice = input("Enter Y to check another address, N to exit: ")
    # if (choice == 'N'):
    #     break
    # print("-----------------------------------------------------------------------\n")
