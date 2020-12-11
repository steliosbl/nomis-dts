from configManager import ConfigManager

# todo

c = ConfigManager()

print("")
print("Configuration")
config = c.decode_into_configuration()
print(config.validate())

print("")
print("Cantabular Credentials")
cant_creds = c.decode_into_cantabular_credentials()
print(cant_creds.validate())

print("")
print("Cantabular Connecton Information")
cant_conn = c.decode_into_cantabular_connection_info()
print(cant_conn.validate())

print("")
print("Nomis Credentials")
nom_creds = c.decode_into_nomis_credentials()
print(nom_creds.validate())

print("")
print("Nomis Connecton Information")
nom_conn = c.decode_into_nomis_connection_info()
print(nom_conn.validate())

print("")
print("Cantabular Complete API Connecton Information")
cant = c.create_api_connection_info(cant_creds, cant_conn)
print(cant.key)

print("")
print("Nomis Complete API Connecton Information")
nom = c.create_api_connection_info(nom_creds, nom_conn)
print(nom.port)
