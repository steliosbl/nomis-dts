from configManager import ConfigManager, create_api_connection_info

# todo

c = ConfigManager()

print("\n")
print("Configuration")
config = c.decode_into_configuration()
print(config.validate())

print("\n")
print("Cantabular Credentials")
cant_creds = c.decode_into_cantabular_credentials()
print(cant_creds.validate())

print("\n")
print("Cantabular Connecton Information")
cant_conn = c.decode_into_cantabular_connection_info()
print(cant_conn.validate())

print("\n")
print("Nomis Credentials")
nom_creds = c.decode_into_nomis_credentials()
print(nom_creds.validate())

print("\n")
print("Nomis Connecton Information")
nom_conn = c.decode_into_nomis_connection_info()
print(nom_conn.validate())

print("\n")
print("Cantabular Complete API Connecton Information")
cant = create_api_connection_info(cant_creds, cant_conn)
print(cant.address)

print("\n")
print("Nomis Complete API Connecton Information")
nom = create_api_connection_info(nom_creds, nom_conn)
print(nom.address)
