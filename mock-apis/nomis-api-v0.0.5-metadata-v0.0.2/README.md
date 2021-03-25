# Nomis API v2 work-in-progress

## Introduction
There are two API projects included with this source code:

- Dataset and variable API (`fe-api`)
- Metadata API (`fe-api-metadata`)

## Prerequisites

- Microsoft .NET Core

## Compile and run Dataset and Variable API

```
cd fe-api
dotnet build
dotnet run bin/Debug/netcoreapp3.1/fe-api.dll
```

### Documentation

- https://localhost:5001/swagger
- https://localhost:5001/graphql


## Compile and run Metadata API

```
cd fe-api-metadata
dotnet build
dotnet run bin/Debug/netcoreapp3.1/fe-api-metadata.dll
```

### Documentation

- https://localhost:5001/swagger

