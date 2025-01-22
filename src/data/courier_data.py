class CourierData:
    COURIER_DATA_1 = {"login": "namo2201-17", "password": "1234", "firstName": "namo"}
    COURIER_DATA_2 = {"login": "namo2201-18", "password": "4321", "firstName": "namonamo"}

    COURIER_INVALID_DATA = [{"login": "namo123", "password": "", "firstName": "namoname"},
                        {"login": "", "password": "123", "firstName": "namoname"},
                        {"login": "", "password": "", "firstName": "namoname"},
                        {"login": "", "password": "", "firstName": ""},
                        {},
                        {"password": "123", "firstName": "namoname"},
                        {"login": "123", "firstName": "namoname"}]

    COURIER_INVALID_LOGIN_DATA = [{"login": "namo123", "password": ""},
                              {"login": "", "password": "123"}]

    COURIER_UNKNOWN_ID = [{"id": 12345}]
    COURIER_INVALID_ID = [{"id": ""}]

